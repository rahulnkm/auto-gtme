# The sequence DAG: architecture

How an outbound sequence is specified, bound, filled and executed — and why the execution
engine contains no model call.

Status: proposed. The current `sequence.schema.json` is calendar-driven; this replaces that
with an event-driven graph. Everything the current schema gets right (the three-layer split,
id-based binding, the volume ceiling, recorded adaptations) is preserved.

---

## 1. What was wrong

The existing spec is a **list**, not a graph:

```json
"touches": [ {"n": 1, "day_offset": 0}, {"n": 2, "day_offset": 3} ],
"branches": [ {"on": "reply_any", "action": "stop_cold"} ]
```

Four problems, in order of severity.

**`branches` is global, not per-node.** It says what the sequence does on a reply. It cannot
say what happens on a reply *to touch 3 specifically*, and it cannot express a second stage
at all. `route_to` points at another template id, so the only expressible "next" is a whole
different sequence.

**Time is absolute.** `day_offset` counts from sequence start. After any branch there is no
clock — nothing can express "if no reply within 24 hours of the connection being accepted",
because that duration is relative to an *event*, not to day zero.

**No terminal states.** The engine cannot say why a contact stopped, so `gtme-measure` cannot
distinguish "completed the sequence unanswered" from "bounced on touch 1" — which are
opposite facts about the same contact.

**Nothing marks the last touch as last.** `leans_on: breakup` is a content hint. It does not
stop the engine.

The repo's own research already called this: *"Adaptive sequences that don't follow fixed
day-timings but react to behavior… The sequence logic is event-driven, not calendar-driven."*
(`research/01-discipline-and-pipeline.md`, Frontier pattern 2026.)

---

## 2. Four layers, and the boundary that matters

```
templates/*.json      SHAPE       the graph. Reusable, versioned, no client content.
05-sequence/          BOUND       which pain node 1 opens on, which offer is the ask,
  sequence.json                   verified channels, volume ceiling.
10-write/             FILLED      one rendered message per (contact × message node).
  messages.jsonl                  Every message the engine could ever send, pre-written.
11-send/              RUN         per-contact state: current node, entered_at, history.
  state.jsonl                     A state machine. No model call.
```

The load-bearing boundary is **FILLED → RUN**. Because `gtme-write` renders every message
node for every contact ahead of time, the engine at send time only ever has to answer *which
pre-written message goes now*. That is a graph traversal, not a generation problem.

This is why there is no LLM in the engine. It is not an optimization — it is what makes the
run reproducible, auditable before a single send, and cheap to dry-run.

---

## 3. The graph

### Nodes

Every node has an `id` (unique within the template) and a `kind`:

| kind | what it does | engine behavior |
|---|---|---|
| `message` | sends one pre-written message on one channel | look up `(contact_id, node_id)` in messages.jsonl, send, record |
| `wait` | holds the contact | no action; only its outgoing edges matter |
| `human_gate` | queues for a person | engine stops touching this contact until a human resolves it |
| `terminal` | ends the run for this contact | records `outcome`, never re-enters |

`message` nodes carry the writing brief, unchanged from today: `intent`, `leans_on`, `ask`,
`word_max`, `constraints`, `binds`. That part of the current schema was right and is kept
verbatim.

Two new flags on `message`:

- **`is_final_cold: true`** — the breakup. The engine refuses to traverse to any further
  `stage: cold` node after sending it. The copy says "this is the last time I'll write";
  this flag makes that true rather than a claim.
- **`stage`** — `cold` | `warm` | `nurture`. Lets the engine enforce stage-level rules
  (cold caps, cold stop-on-reply) without hardcoding node ids.

### Edges

```json
{"from": "t1", "to": "t2", "when": "timeout", "after": "P3D", "priority": 10}
{"from": "t1", "to": "triage", "when": "reply_human", "priority": 1}
```

- **`when`** is an event name or the literal `timeout`.
- **`after`** is an ISO-8601 duration, measured from **when the contact entered `from`** —
  not from sequence start. This is what makes "24 hours after no reply" expressible.
- **`priority`** breaks ties. Lower wins. An event edge must always outrank the timeout edge
  on the same node, or a reply arriving at the same tick as a scheduled send loses.

### Events

Split by who can determine them, because that split decides what may be automated.

**Machine-determinable** — an adapter observes them, no judgment required:
`bounce_hard`, `bounce_soft`, `unsubscribe`, `auto_reply_ooo`, `link_clicked`,
`connection_accepted`, `connection_withdrawn`, `meeting_booked`, `signal_expired`.

**Judgment-required** — a human or a classifier must decide:
`reply_human` (someone typed something).

The engine handles the first list with rules. **It never classifies the second.** A human
reply routes to a `human_gate`. This is the hybrid doctrine, and the research is blunt about
the cost of getting it wrong: *50–70% of AI SDR contracts cancelled within 90 days because
vendors automated volume without solving judgment* (`research/02a`). Auto-answering a warm
reply is precisely automating judgment.

---

## 4. The engine

`gtme-send` is a tick loop. Pseudocode, complete:

```
for contact in run:
    s = state[contact]
    if s.node.kind in (terminal, human_gate): continue
    if paused_by_gate or outside send_window(contact): continue

    for e in sorted(edges_from(s.node), key=priority):
        fired = (e.when == "timeout" and now - s.entered_at >= e.after) \
             or (e.when in s.events_since(s.entered_at))
        if fired:
            enter(contact, e.to); break

    if s.node.kind == message and not s.sent[s.node.id]:
        if daily_cap_remaining(s.node.channel) == 0: continue   # try next tick
        send(messages[contact][s.node.id]); s.sent[s.node.id] = True
```

Properties that fall out of this:

- **Deterministic.** Same events plus same clock produces the same path. Replayable.
- **Dry-runnable.** Feed a synthetic clock and no events; get the exact send schedule before
  anything leaves.
- **Resumable.** State is the node id and a timestamp. A crash loses nothing.
- **Cap-aware.** Hitting a daily cap defers rather than skips — a skipped touch silently
  shortens the sequence, which is the failure `gtme-sequence` already warns about.

### Guards the engine enforces, not the copy

1. Any `reply_human` cancels all remaining `stage: cold` nodes. A scheduled follow-up landing
   after a person replied is the clearest possible tell that nobody is reading.
2. `bounce_hard` and `unsubscribe` go straight to terminal. No retry, ever.
3. After `is_final_cold`, no further cold node is reachable.
4. Send only inside `send_window`, resolved per contact from their timezone.
5. Never two messages to one contact in one day, on any channel.

---

## 5. Terminal outcomes

Enumerated, because `gtme-measure` attributes against them:

`booked` · `replied_positive` · `replied_negative` · `disqualified` · `bounced` ·
`unsubscribed` · `exhausted_no_reply` · `stopped_by_human`

`exhausted_no_reply` is the honest name for what most contacts do. Distinguishing it from
`bounced` is the difference between a targeting problem and a data problem — the attribution
discipline `gtme-measure` already requires.

---

## 6. Stage 2: what happens after a reply

The shape the templates implement:

```
t1 → t2 → t3 → t4(is_final_cold) → exhausted_no_reply
 │    │    │    │
 └────┴────┴────┴──── reply_human ──→ [triage: human_gate]
                                          ├─ interested  → warm_share → warm_wait → booked
                                          ├─ not_now     → nurture_park
                                          └─ negative    → replied_negative
```

`warm_share` is the product-page touch. It is a `message` node like any other, pre-written,
and it is reached **only after a human has classified the reply as interested**. The human
does the judging; the engine does the sending.

Why not auto-send on any reply: a reply is not a yes. "Who is this?" and "send me pricing"
are both `reply_human`, and only one of them wants a product page.

---

## 7. What `gtme-write` must now produce

One row per `(contact_id, node_id)` — not per touch number — covering **every** `message`
node in the graph, including warm and nurture nodes that most contacts will never reach.

That looks wasteful and is not. Rendering warm nodes lazily would put a generation step
inside the send loop, which is the one thing this architecture exists to avoid.

---

## 8. Open questions

- **Reply classification.** Currently a human gate. A deterministic classifier for the
  obvious cases (unsubscribe phrasing, "wrong person", "not interested") would cut gate
  volume, but every rule risks mis-routing a real buyer. Needs measurement before it earns a
  place.
- **Per-contact timing personalization.** The send window is a campaign rule. Whether it
  should adapt per contact from observed open times is untested here.
- **Nurture re-entry.** `nurture_park` currently terminates. Whether a parked contact
  re-enters after N months is a policy question the human gate should own.
