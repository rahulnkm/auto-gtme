---
name: gtme-score
description: Use after signals are detected, when you need to rank and route accounts for outreach — decide who to reach first and how. Triggers include "score the accounts", "rank the prospects", "prioritize", or the scoring step of an auto-gtme run.
---

# gtme-score

## Overview

Rank accounts by **value × fit × decayed-signal**, then route them. This is the single owner of the decay math (`gtme-signals` emits raw strength + dates; you apply the curve — do not expect it pre-decayed). Output: `scored.jsonl`, ranked, with a routing decision and a coverage state per account.

**Signal is a multiplier on the map, never a filter on it.** An account with no signal still scores — on how much it is worth and how well it fits. This is the difference between a priority order and a qualification gate, and getting it wrong collapses the whole TAM to zero except the slice you happened to research. ([Vercel's Roniesha Copeland](https://atlas.attio.com/build-the-system-before-the-message): intent is an effort multiplier on the TAM, never a filter. [@codyschneider](https://x.com/codyschneider/status/2077891033023631681): the output is a coverage map, "every account tagged covered / thin / whitespace, sorted by value.")

The formula is **fixed** — scores must be comparable across runs and re-runs, so don't reinvent constants each time.

## When to Use

- After `gtme-signals` (+ `gtme-enrich` for contacts), before `gtme-write`/`gtme-sequence`
- Input: `06-list/tam.jsonl` (fit_tier) + `07-signals/signals.jsonl` (raw signals) + `07-enrich/prospects.jsonl` (contacts) + `03-icp/icp.json`'s `icp.scoring` (formerly score_hint). Output: `runs/<slug>/08-score/scored.jsonl` + `runs/<slug>/08-score/scored_contacts.jsonl` (+ the standard folder companions `provenance.md` and `decisions.md`). Reference implementation: `score.py` in this skill — the constants there ARE the formula.

## The formula (fixed constants)

```
SIGNAL (timing) — unchanged, still the only cross-cycle tunable
  raw points:    strong=10  medium=5  weak=2  counter=-8   unknown=0
  signal prior:  prior[type] — from measure.json signal_priors; DEFAULT 1.0 if absent
  decay:         decayed = raw × prior[type] × 0.5^(age_days / 90)   # age from event_date
  signal_score:  Σ decayed  (across an account's events)
  signal_mult:   max(0.1, 1 + signal_score / 10)      # 1.0 when no signal — never 0

VALUE (how big the deal is) — log-scaled, shrunk when the size is guessed
  raw:           clamp(0.6 + 0.5 × log10(seats / 3), 0.6, 1.4)
                 seats = the ICP's sub_team metric (the team that would use the product),
                 NOT headcount. Missing → 1.0.
  shrinkage:     value_mult = raw          # k = 1.0 for BOTH researched and imputed
                 NO manual shrink. Imputation ALREADY pulls an estimate toward the mean
                 conditioned on what was actually observed (Manski, Gmeiner & Tamburc,
                 arXiv 2102.11334) — halving it again double-shrinks a value that is
                 already conservative. The shrink TARGET also matters: toward 1.0 (the
                 mean) is statistically correct; toward 0 would encode "unknown = bad",
                 which is a business judgment, not a statistical one. If a seller wants
                 an unknown-data penalty it must be a SEPARATE, visible term so it can
                 be audited — never smuggled into the estimate.
                 Default (set 2026-07-28): no penalty. Rationale: imputed rows here are
                 accounts nobody has researched yet, not accounts that resisted research.

FIT (how well they match) — continuous, not just a tier label
  fit_mult:      tier_base × geo × stage × incumbent
                 tier_base  {1:1.0, 2:0.75, 3:0.5}
                 geo        1.0 in an ICP geo · 0.9 outside
                 stage      1.0 in the tier's allowed stages · 0.9 outside
                 incumbent  1.1 if incumbent_tech non-empty (pays a vendor today = proven
                            budget, per icp.budget_evidence_any_of) · 1.0 otherwise

need_mult:       fit_mult × signal_mult                # propensity: has the problem, now
final_score:     10 × value_mult × need_mult            # expected value: size × propensity
```

Range in practice: ~3 (small, off-ICP, no signal) to ~30 (large tier-1 with a fresh strong signal). A zero-signal account tops out around 15, so **signal still decides the top of the queue — it just no longer decides whether you are on the list at all.**

`prior[type]` is the only tunable that changes between cycles — `gtme-measure` retunes it from book-rate. Everything else (points, half-life, the value curve, the fit multipliers, the ×10) is **frozen** so scores stay comparable across runs; all cross-cycle learning flows through `signal_priors` and the ICP's `icp.scoring.boosts[].signal` membership. First cycle / no measurement → every prior is 1.0.

- Trust the signal's emitted `strength` and `counter` label — **do not re-interpret what a signal means.** If `tech_stack_change` fired as `counter`, score it negative; its sign was decided at detection. (A "ripped out the incumbent" event should have been emitted `strong/acquire`, a "adopted a competitor" event `counter` — that call belongs to `gtme-signals`.)
- Counter-signals are **negative, not zero.** They pull `signal_mult` below 1.0 and, once `signal_score` goes net negative, the suppress gate fires regardless of how big or well-fitting the account is. Zero lets a stale positive drag a bad-timing account back into the queue — the classic mis-fire.
- **A guessed number still gets no free pass — but the fix is disclosure, not a haircut.** `size_source` rides on every row so a reader can see which accounts are sorted on a real count and which on `headcount × 0.03` (headcount wearing a costume). Emit it; don't silently discount it.

## Capacity: rank by value per scarce hour, then guard the ratio

Ranking by score alone answers "who is most valuable" and ignores that the seller is a three-person team with **2–3 in-VPC pilot slots a quarter** (`offer.json economics`). Two accounts scoring 25 are not equal if one takes four founder-weeks and the other takes three days.

```
serve_hours:  desk audit ~20h · in-VPC audit ~80h · heavy-procurement accounts ×1.5
density:      final_score / serve_hours        # value per scarce hour
```

Rank the batch by `density`. **Then apply the guard, which is not optional:**

Dividing by cost ranks by value density, which is provably optimal **only for fractional knapsack** — where you can take part of an item. A pilot is indivisible, so this is 0/1 knapsack, where pure ratio-greedy is *arbitrarily bad*. Chekuri's counterexample: an item of size 1 / profit 2 beats an item of size B / profit B on density, and earns 2 instead of B. Brealey & Myers put it in business terms — a $100 project returning $200 beats a $1M project returning $1.5M on ratio, but "the second makes you richer."

**The guard (Chekuri, ½-approximation):** compute both the density-ranked batch *and* the single highest-`final_score` account that fits the capacity, and take whichever has more total value. Emit `capacity_guard_triggered: true` when the single account wins, because that is a fact a human should see, not a silent reordering.

**State the limit honestly in decisions.md:** ratio ranking has **no guarantee once two resources are rationed**, and this pipeline rations at least two — founder hours *and* send/LinkedIn capacity. Brealey & Myers: the profitability index "breaks down whenever more than one resource is rationed… the only general solution is linear programming." Treat density ranking as a heuristic with a known failure mode, not an optimality result.

## Validation: top-decile lift, or admit it is noise

Once `gtme-measure` has real replies, report **top-decile lift** — reply rate of the top-scoring 10% divided by the overall average.

| Lift | Read |
|---|---|
| ≥3x | The model discriminates. Keep the weights. |
| 1.5–3x | Weak but real. Retune `signal_priors`, leave structure alone. |
| ≤1.5x | Noise wearing precision. **Flatten the weights toward equal** rather than defending them. |

Every constant in this skill is a prior chosen before any data existed. The first measured cycle's job is to replace them, and a scoring model that cannot report its own lift is not a model — it is a sorting opinion.

## Routing — four independent axes

Don't collapse these into one label. Each account gets all four:

| Axis | Set by | Values |
|---|---|---|
| `effort_mode` | **fit_tier** | tier 1 → `human_assisted` (bespoke, human approves send) · tier 2 → `semi_auto` · tier 3 → `fully_auto` |
| `priority` | **final_score** | `high` ≥18 · `medium` 11 ≤ x < 18 · `low` < 11 · suppressed accounts → `n/a` |
| `route` | **suppress gate** | `signal_score < 0` (net counter) → `hold_human_review`; else `send` |
| `coverage_state` | **contacts on hand** | `covered` (≥1 contact at 1st/2nd degree) · `thin` (contacts, but all cold) · `whitespace` (none) |

`coverage_state` is the axis that tells `gtme-enrich` where to go next. It answers a question `priority` cannot: *do we have a way in?* A high-priority whitespace account is not a send — it is an enrichment target. Sorting the map by `final_score` **within** `whitespace` gives you the enrichment queue, which is the only way enrichment stops being aimed at wherever signals happened to fire. ([@codyschneider](https://x.com/codyschneider/status/2077830639890382973): lead score the people, *then* waterfall enrich — score gates the spend, not the other way round.)

- `has_active_counter` — `true` when the account has any `counter` event whose decayed value still contributes materially negative (i.e. it's pulling `signal_score` down). This is what trips the suppress gate.
- `top_signal` — the **highest positive `acquire`** decayed signal; this is the hook `gtme-write` opens with. Never a `counter` (a counter is a reason to hold, not a hook). If an account has no positive signal, `top_signal` is `null` — and it's suppressed anyway, so `gtme-write` won't run on it.

Why separate: a high-fit tier-1 account still deserves a *human-assisted* touch (codyschneider: spend human effort where fit is best), but an active counter-signal must be able to **suppress it regardless of tier** — the trap a firmographics-led model falls into (blasting a tier-1 that just tooled up). `effort_mode` says *how much craft*, `route` says *whether to send at all*.

## scored.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "company": "Mercury", "fit_tier": 1,
 "value_mult": 1.21, "fit_mult": 1.0, "signal_score": 15.31, "signal_mult": 2.53,
 "final_score": 30.60, "coverage_state": "thin", "has_active_counter": false,
 "effort_mode": "human_assisted", "priority": "high", "route": "send",
 "top_signal": {"type": "job_posting_intent", "decayed": 9.40, "direction": "acquire"},
 "message_angle": "fresh hiring intent on top of a recent raise — team scaling, CRM pain imminent",
 "sub_team_est": 42, "size_source": "researched", "scored_at": "<iso8601>"}
```

Emit the three multipliers separately, not just the product. A score you cannot decompose cannot be argued with — and `gtme-measure` needs to know *which* term was carrying an account before it can tell you the term was wrong.

`top_signal` (+ its `direction`) is what `gtme-write` leads the message with. `message_angle` is a one-line hook, not the message.

## Two layers: accounts set the ceiling, contacts set the order

**Scoring an account is not scoring a person, and only one of them receives a message.** An account score answers *is this company worth spending on* — it is where fit, signals, and revenue potential live, because those are properties of a company. But every account holds several humans of unequal reachability, and ranking sends purely by account rank throws that away: a second-degree champion at a medium-signal account is a better first touch than a cold third-degree contact at a strong one, and account-only scoring cannot express that.

So score twice:

**Layer 1 — account score:** value × fit × decayed-signal → tier and routing. Sets a **ceiling**: no contact outranks what its account justifies spending. A net counter-signal (e.g. the fraud team was just laid off) trips the suppress gate on the account and every contact in it, regardless of how warm the person is.

**Layer 2 — contact score: a PRODUCT, never a sum.**

```
reach_mult:     max(1.0, 1 + warmth_pts / 10)        # 1.0 when cold — never 0
contact_score:  account_ev × reach_mult
```

**Why a product.** An additive contact layer (`account/2 + orbit + degree + …`) lets its constants decide the account-vs-person trade-off row by row: measured on a real run, the account's share of the total swung 41%–94% across the top 8 contacts. Nobody chose that; it fell out of the arithmetic. A product fixes the ratio by construction, and matches what the score is trying to estimate — likelihood of acceptance is *does this company need it* × *can this person be reached*, not a pile of bonus points.

**Why `reach_mult` floors at 1.0.** A cold 3rd-degree contact is the **baseline, not an impossibility** — typically ~80% of a file has no warmth at all. An unfloored product zeroes every one of them and leaves a queue containing only the warm tail, which is how a scoring change silently becomes a coverage cut.

`warmth_pts` — and *only* these, because only these describe reachability:

| Input | Why it moves the number |
|---|---|
| Shared employer with the seller's founders (`founder_orbit`, +6) | The warmest cold open there is — "I was at $BIGCO too" opens a door a cold line never does. Read it from **employment history**, never the headline: a headline says where someone works now, and the whole signal is where they worked *before*. The employer set comes from `company.json` `warm_universe.founder_orbit.employers`, never hardcoded. |
| Shared school (+3) | Weaker but real — shared-alumni intros are how a lot of first hires and first customers actually happen. Read from the profile's education section; the school set comes from `warm_universe.founder_orbit.schools`. |
| `network_degree` (1st +5 / 2nd +3 / 3rd+ 0 / unknown +0.5) | A real intro path — but **only for whoever's account measured it**. See the warmth-ownership rule below. |

**Role and seniority are routing, not score.** The champion is likelier to *reply*; the economic buyer is likelier to *decide*. Those pull opposite ways, so averaging them into one number destroys the distinction the sequencer needs. Emit `is_champion`, `is_senior`, `touch_order` as fields and let `gtme-sequence` use them. Same for contact-level timing (new-in-seat) and public problem posts: they belong to `gtme-signals` and `gtme-research` as *hooks*, not to the ranking.

**Ties are then normal, so break them explicitly.** With role out of the score, two contacts at one account with equal warmth tie exactly, and their order becomes sort-stability — i.e. arbitrary. Order by `(-contact_score, champion first, senior next, name)`. Routing orders *within* a score; it never moves the score.

### Warmth belongs to a person — record which one

**Connection degree is not a property of the contact. It is a property of the edge between the contact and whoever was logged in.** An operator running enrichment from their own LinkedIn account measures *their* distance to the target. If the message will be sent by the founder, that number is describing a path the sender does not have.

This fails silently, which is why it needs a rule rather than care:

- Always emit `network_owner` on every contact row — the account the degree was measured from. Never emit a bare `connection_degree`.
- If `network_owner != sender_identity.sender_name`, the degree is a **tiebreak**, not the dominant term. It is evidence that an intro is *brokerable*, not that the sender is warm.
- The sender's own warm surface is then carried entirely by `founder_orbit`, which is computable from any account because shared-employer and shared-school history are on the target's public profile. **This is the term to invest lookups in when you cannot see the sender's graph.**
- Diagnostic before you trust a degree column: name the seller's single warmest known relationship and check whether it shows up. If a founder spent four years at some company and not one contact there is 1st or 2nd degree, the column is not measuring the founder's network. Cheap test, catches the whole class of error.
- **`founder_orbit` holds employers, not backers.** Only places a founder actually worked. "We took an angel check from Stripe" is not a relationship with everyone who ever worked at Stripe, and an investor list quietly seeded into the orbit set manufactures warmth at the top of the queue — the same failure as the degree column, one layer down. Build the set from the founders' CVs; if a name got in from a funding claim, cut it.
- Record the match in `orbit_evidence` with its kind — `employer_past` (an ex-colleague, the real thing), `employer_current` (works where a founder used to; warm but a different claim), or `school` with the school named. Same-university-different-program is a thinner tie than the points suggest, and only a named row lets the writer see that before leaning on it.

Record the constraint in the run rather than papering over it — a scored list whose warmth belongs to the wrong person is worse than one with no warmth column at all, because it looks finished.

**`confidence` neither ranks nor gates.** It never enters `contact_score` — record quality is not prospect quality, and mixing them makes a well-sourced junior analyst outrank a thinly-sourced Head of Fraud. It is no longer read by `send_gate` either. No skill ever defined what earns a 0.6 over an 0.85, so it was a feel assigned per record, and it read **0.85 on the one record known to resolve to the wrong human** — it never discriminated. Both jobs it might have held now have real answers: identity by `record_status` plus the evidence `prospects.schema.json` demands, deliverability by `email_status`, which carries a provider's verdict. Keep emitting it as description; do not gate on it. `email_status` gates **per channel** in `gtme-sequence` — a dead address closes email, it does not demote the human.

**`send_gate` is an allowlist, and it lives in `gate.py`.** It is the one part of the formula not in `score.py`, because it needs unit tests and `score.py` runs its whole pipeline at import. `ready` requires BOTH: `record_status` exactly `verified`, and an `identity.pulled` date inside `icp.scoring.identity_max_age_days` (default 30). `not_found` / `wrong_person` / `stale` are `do_not_send`. Everything else — `ambiguous`, `unchecked`, an absent status, a status nobody recognises — is `verify_first`.

Enumerating the bad values and letting the rest through is how this went wrong the first time: `record_status` was optional, an absent one matched no branch and fell through to `ready`, and 111 of 178 send-ready contacts in a live run had never had their identity checked at all. Age downgrades `ready` to `verify_first` and never to `do_not_send` — a stale check is weaker evidence, not counter-evidence. The gate assumes nothing about its input being schema-valid: it is the second of two defenses, and a record written by something that skipped `validate.py` is exactly what it exists to catch.

**Keep the three multipliers separate on the row.** `value_mult`, `need_mult` (and its `fit_mult` / `signal_mult` parts), and `reach_mult` are emitted individually, not just their product. Every constant in them is invented; the point is not accuracy but **attributable error** — when replies land, `gtme-measure` can say *which term* was wrong rather than "the ranking was wrong." A single opaque score is unfalsifiable, and an unfalsifiable score never improves.

**`dominant_reason` must clear a bar to count.** Only a warmth component worth ≥3 points can be the reason (connection ≥2nd degree, founder-orbit). Anything smaller is a tiebreak, not an opening line. If nothing clears the bar the reason is `account_fit`, which is honest: you are reaching out because of the company, not the person, and `gtme-write` should open on the account signal rather than fake a personal hook.

Emit `08-score/scored_contacts.jsonl` alongside `08-score/scored.jsonl` — same account keys plus `contact_score`, `reach_mult`, `warmth_pts`, `send_rank`, `send_gate`, `dominant_reason`, and the routing fields (`is_champion`, `is_senior`, `touch_order`). `gtme-sequence` consumes contact order; `gtme-write` reads `dominant_reason` to choose the opening line.

**The trap this avoids:** an account-only pipeline sends to whoever happened to get resolved first, then reports "our ICP is wrong" when replies don't come. Contact ordering is often the difference, and it is invisible until it is scored separately.

## Common Mistakes

| Mistake | Fix |
|---|---|
| No signal → score 0 | Signal is a **multiplier** (`1 + s/10`), never the whole score. Zero-signal accounts still rank on value × fit, or the map collapses to whatever you happened to research. |
| Re-inventing decay/points per run | Constants are fixed; scores must compare across runs. |
| Expecting pre-decayed signals | You own decay; signals arrive raw + dated. |
| Counter-signal scored as 0 | Negative (−8). Zero re-admits bad-timing accounts. |
| Re-interpreting a signal's meaning | Trust emitted `strength`/`counter`; the sign was set at detection. |
| Collapsing routing to one flag | Four axes: `effort_mode` (tier), `priority` (score), `route` (counter gate), `coverage_state` (do we have a way in). |
| Auto-sending a tier-1 with a live counter | Suppress gate fires regardless of tier or size → `hold_human_review`. |
| `confidence` used as a ranking term, or as a gate | It does neither. Nothing defines what a given value means, so it measures nothing. Identity is gated on `record_status` + evidence; email on `email_status`. |
| Connection degree with no owner recorded | Emit `network_owner`. A degree measured from the operator's account is not the sender's warmth, and nothing about the number says so. |
| `founder_orbit` read off the job headline | Read employment **history**. A headline says where they work now; the signal is where they worked before. Grepping headlines returns zero hits and looks like "no warm paths exist." |
| Investors/backers in the orbit employer set | Founders' CVs only. An angel check is not a relationship with that company's alumni. |
| A gated contact still holding a `send_rank` | `do_not_send` → `send_rank: null`. A dead record sitting at #3 in the queue is an invitation to step over the gate. |
| Value term built on an imputed size | Shrink by half when `firmographic_source != "researched"`. Check before trusting it. |
| Scoring only what you enriched | Score the **whole** TAM on value × fit first; `coverage_state` + rank is then the enrichment queue. |

## Next

`gtme-write` reads `08-score/scored.jsonl` (order + `top_signal` + `effort_mode`) and `08-score/scored_contacts.jsonl` (`dominant_reason` → opening line) → drafts the message; tier-1 `human_assisted` accounts get a bespoke draft for approval, tier-3 `fully_auto` flow straight to `gtme-sequence`.
