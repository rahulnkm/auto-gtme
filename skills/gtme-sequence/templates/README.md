# Sequence templates

The shape of an outbound sequence, independent of any seller. A run selects one
in `gtme-sequence` and binds it to that campaign's offer, pains and objections;
`gtme-write` then personalizes each bound touch per contact.

Three layers, and keeping them apart is the point:

```
template        the shape          reusable across clients, versioned here
sequence.json   the shape bound    which pain touch 2 leans on, which front-end
                to this campaign   offer is the ask, resolved send windows
messages.jsonl  the bound shape    one row per contact per touch
                filled per person
```

**Templates carry no seller specifics.** No prices, no company names, no product
claims. A template that only works for one seller is not a template.

**Every timing and structural claim cites `research/`.** These are not invented
cadences. When `gtme-measure` produces evidence that a template underperforms,
the fix is a new version here, not a per-run edit - that is what makes the
library compound instead of drifting.

## Two spec versions

`spec: dag/1` templates are a **graph** - `nodes` and `edges` - executed by `gtme-send` as a
state machine. Timing is event-driven: every edge fires on an event or on a timeout measured
from when the contact entered the current node, so "24 hours after the connection was
accepted" is expressible. They carry a second stage past the reply.

Templates without a `spec` field are the original v1 shape: an ordered `touches` list with
`day_offset` counted from sequence start, plus a global `branches` list. Calendar-driven, and
they end at the reply.

Prefer `dag/1` for new campaigns. See `docs/build/sequence-architecture.md` for why, and for
the engine contract. Invariants for each shape live in `skills/tests/test_sequence_schema.py`
(v1) and `skills/tests/test_sequence_dag.py` (dag/1).

## Choosing

| template | spec | use when |
|---|---|---|
| `email-4touch-dag` | dag/1 | **default.** Email is the only wired channel, or deliverability is fragile (new domain, low warmup) |
| `multichannel-4touch-dag` | dag/1 | email + LinkedIn both wired, ICP reachable on both, LinkedIn connects are the binding cap |
| `signal-4touch-dag` | dag/1 | signal coverage is dense enough that most contacts carry a recent, dated trigger |
| `email-3touch` | v1 | legacy |
| `multichannel-7touch` | v1 | legacy |
| `signal-triggered` | v1 | legacy |
| `nurture-10touch` | v1 | legacy warm track |

All three `dag/1` templates share one topology: four cold touches, the fourth marked
`is_final_cold`; any human reply exits to a `human_gate` where a person classifies it; an
interested classification reaches the product-page share. The engine enforces the final touch
being final - no cold node is reachable after it.

`gtme-sequence` records which was chosen and why, against `channel-plan.json`
(which channels are actually wired, what the daily caps are) and the ICP.

`gtme-sequence` records which was chosen and why, against `channel-plan.json`
(which channels are actually wired, what the daily caps are) and the ICP.
