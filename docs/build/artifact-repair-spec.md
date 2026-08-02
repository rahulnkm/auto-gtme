# Artifact repair spec

An audit of the four judgment artifacts (`company.json`, `market-pain.json`, `icp.json`, `offer.json`) found 24 defects. This spec says what changes, in what order, and how each phase proves itself done.

> **Shipped 2026-08-02.** All six phases are implemented; `validate.py runs/mousecat` and 157 tests pass. Three things changed during implementation and are corrected in place below: the capacity contradiction turned out to be two real quantities the prose had collapsed, the `unread_fields` check needed to respect pipeline order or it laundered the drift it was built to catch, and `Lead Bank` was removed rather than annotated. What each phase actually did is recorded in its **Shipped** note.

## What the audit actually found

`artifact-design.md` states the admission test. Rule 2:

> **A named downstream stage reads it.** Every field holds its seat by a consumer. No consumer, no seat.

Eight fields violate it today:

| field | produced by | read by |
|---|---|---|
| `predicted_objections` | market-pain | nobody |
| `market_pain_stats` | market-pain | nobody |
| `pain_keywords` | market-pain | nobody |
| `likelihood_levers` | offer | nobody |
| `proof_inventory` | offer | nobody |
| `seed_targets` | icp | nobody |
| `channel-plan.json` | (run root) | nobody |
| `sample-messages.json` | (run root) | nobody |

The rule was written and never enforced. Nothing checks it, so drift is silent and free.

That is the same failure class as the two checks already in `validate.py`. `distillation_gaps` exists because validation catches invented fields and is blind to dropped ones. `orphaned_citations` exists because a third of one stage's evidence was researched and silently unused. Both make an unexplained drop impossible to do quietly. Neither can see a field that has no reader.

Almost nothing found by this audit is missing research. The TAM existed. The beta attribution existed. The sender identity existed. Each was sitting in a file nothing opens.

## Ordering

**Phase 0 first, because it is the only change that prevents recurrence.** Every other phase fixes instances; Phase 0 fixes the class. Shipping it first also means Phases 1 to 5 are verified by a check rather than by review.

**Phase 1 second, because `offer.json` is the only artifact with no schema.** Three of four stages validate. The offer does not, and it holds nine of the 24 defects. That is causal, not coincidental.

Phases 2 to 5 are independent of each other and may ship in any order.

---

## Phase 0: make "no consumer, no seat" checkable

### 0.1 Declare readers in the registry

`skills/validate.py` already maps stage to artifact and schema. Extend it with the read side: for each artifact, which stage reads which top-level field.

```python
READERS = {
    "market": {
        "pains":                ["gtme-icp", "gtme-offer", "gtme-write"],
        "predicted_objections": ["gtme-write"],
        "market_pain_stats":    ["gtme-write"],
        ...
    },
    ...
}
```

### 0.2 Add `unread_fields(artifact, stage)`

Returns top-level fields present in the artifact with no declared reader. Mirrors `distillation_gaps` in shape and intent: it does not verify a reader is truthful, it makes an unread field impossible to add silently.

Escape hatch, matching the `UNUSED:` convention in `orphaned_citations`: a field may declare `"readers": []` with a stated reason in the stage's `decisions.md`. A decision on the record beats silence.

### 0.3 Add `seeds_pass_disqualifiers(icp)`

`icp.seed_targets` contains `Lead Bank`. `icp.disqualifiers.depository_charter` excludes any entity licensed to take deposits. A hand-picked seed violates the filter it was picked under, and nothing catches it because seeds are bare strings.

This check depends on Phase 5.2 (seeds carry structure). Ship the check with that change.

### 0.4 Add `numbers_agree(run)`

Cross-file quantities that must match, asserted once:

- `offer.scarcity_facts` in-VPC capacity == `offer.economics.vpc_audit_capacity_per_quarter` (today: 2 vs 3)
- `icp.niche_slap_guard` account bar <= `05-list/tam.jsonl` line count (today: 500 vs 774, never checked)

**Shipped.** `unread_fields`, `numbers_agree`, `seeds_pass_disqualifiers` in `validate.py`; tests in `skills/tests/test_unread_fields.py`. Verified non-vacuous by injecting three regressions into `icp.json` and confirming each check fires independently.

Two corrections from implementation:

**Readers are discovered by scanning SKILL.md, not declared in a table.** A hand-kept registry drifts from the skills it describes, and that drift is exactly what the check exists to catch.

**A reader must run after the producer.** `gtme-company` mentions `pain_keywords` and runs two stages before the pain map exists, which made a dead field look consumed. Without the `PIPELINE` order check, `unread_fields` launders the drift it was built to find.

**Done when:** `validate.py` fails on the current `runs/mousecat` with the eight unread fields named.

---

## Phase 1: give the offer a contract

Write `skills/gtme-offer/offer.schema.json` **from `gtme-offer/SKILL.md`, not from the live artifact.** Building the market-pain schema from its artifact reproduced the exact drift it was meant to catch; that lesson applies here.

Register it in `validate.py` `REGISTRY`. Add `skills/tests/test_offer_schema.py` following the shape of `test_icp_schema.py`, including `test_live_artifact_validates` as the migration signal.

### Shape changes the schema encodes

**1.1 `likelihood_levers`: string -> object.** Today it is bare strings carrying `81% precision`, `77% recall`, `$1.5M/month prevented`. These are founder-claimed figures from two unnamed betas, published to fraud teams whose job is catching unsupported claims. It is the least disciplined field on the most dangerous path.

```json
{"claim": "...", "evidence_class": "primary|vendor_consensus|founder_claimed|assumption", "cites": ["[O1]"]}
```

`company.warm_universe.beta_users` already records the attribution (`"crypto exchange (unnamed - the $1.5M/month account)"`). The evidence exists; only the link is missing.

**1.2 `problems[].persona` -> `personas[]`.** Upstream `pains[].who_feels` is plural; the offer narrowed it to one. Measured effect:

```
p1 (pain:unworked_backlog) serves champion; UNREACHABLE: ['economic_buyer']
p3 (pain:false_positives)  serves economic_buyer; UNREACHABLE: ['champion']
```

Two of five problems cannot be sold to half the people who have them.

**1.3 Add a `problems[]` row for `pain:evidence_assembly`.** The strongest pain in the map has no problem row, so it cannot be sold at all.

**1.4 `front_end_offers[].acceptance_path` required.** `f1` (Desk Audit, $5-10k) has one. `f2` (Shadow Audit, $10-25k, in-VPC, requires security review) does not. The higher-friction offer is missing the route through the friction, and the cut list names it as the touch-1 ask.

**1.5 Capacity stated once.** Remove the in-VPC number from `scarcity_facts` prose; have it reference `economics.vpc_audit_capacity_per_quarter`. Resolve 2 vs 3 first: this number gates the delivery plan and no reader can currently tell which governs.

**1.6 De-duplicate `signals`.** `problems[].signals` and `front_end_offers[].signals` hold the same six values. One side references the other's id.

**1.7 Add `urgency_facts` and `bonuses`.** Named in the skill spec, absent from the artifact.

**1.8 The gate is 12 questions, not 11.** The skill listed 11; the artifact answered 12. The extra one, acceptance obstacles, comes from the belief-weak doctrine already in the skill prose but was never added to the numbered list. The artifact was right and the spec was behind it.

**Shipped.** `offer.schema.json` + `test_offer_schema.py` (23 tests). Two things the schema learned from the artifact rather than the other way round: `acceptance_path` is an escalation ladder, not one sentence, and `warm_first_plan.named_paths` already existed, so `count` was deleted instead (it read 5 beside four paths).

**Correction to 1.5: the capacity numbers were never in conflict.** `04-offer/provenance.md` [O4] states both plainly: *"2 concurrent in-VPC slots, ~3/quarter"*. Concurrency and throughput are different quantities, and the prose "2 concurrent slots per quarter" collapsed them into what looked like one number stated twice. `economics` now names both; `numbers_agree` asserts the prose against them. The evidence had been sitting in provenance the whole time, unread, which is the pattern this whole audit is about.

**Done when:** the offer schema is registered, tests pass, `runs/mousecat/04-offer/offer.json` validates green.

---

## Phase 2: build the read side

For each unread field, one of two outcomes. No third option: an unread field is either a missing feature or dead weight, and the spec forces the call.

| field | resolution |
|---|---|
| `predicted_objections` | `gtme-write` reads it. Add `id` to each entry; add `answered_by` linking to the offer element that handles it. Today the first-touch persona's top objection ("if this works I am automating my own job") has no answer anywhere. |
| `market_pain_stats` | `gtme-write` may quote. Needs a selection rule and a staleness bound; one stat carries 2017 data. |
| `likelihood_levers` | `gtme-write` reads it as proof, after Phase 1.1 gives it an evidence class. Write must refuse anything below a stated class. |
| `pain_keywords` | `gtme-signals` and `gtme-list` search with it. Currently the practitioner vocabulary ("TMAs", "disposition alerts", "SAR narrative") is researched and never used to find anyone. |
| `seed_targets` | `gtme-list` seeds the TAM from it. See Phase 5.2. |
| `proof_inventory` | `gtme-offer` reads it to gate guarantee strength. It reports `case_studies: 0, testimonials: 0` while `likelihood_levers` asserts hard numbers; the file contradicts itself. |
| `channel-plan.json` | `gtme-write` reads `sender_identity`. This is the missing `config.sender`: the file already contains the name, role line, and the rule *"gtme-write must refuse to send with nulls here."* The enforcement instruction lives inside the file the enforcer never opens. Delete the `config.sender` reference from `gtme-write/SKILL.md`. |
| `sample-messages.json` | Delete, or move under `write/` as a named fixture. |

**Shipped.** Readers named in `gtme-write` (levers with a class-binding rule, objections, statistics with a scope rule, acceptance components, `channel-plan.json sender_identity`), `gtme-list` (warm-first gate, seed accounts, `geo_exception`), `gtme-signals` (`pain_keywords` as the query set, company `socials` as the referent for `_ours` signals), `gtme-measure` (`niche_slap_guard`, including the reachability check), and `gtme-market-pain` (`company.platform` as a `feature_ref` target).

Two extra fields surfaced once ordering was enforced, and both were real: `company.one_liner` and `company.socials`. `sample-messages.json` moved to `write/`. The phantom `config.sender` reference is deleted.

**Done when:** `unread_fields` returns empty for all four artifacts, and each newly-declared reader names the field in its SKILL.md.

---

## Phase 3: make evidence class travel the whole way

**3.1 `company.achievements[]` gets `verification`.** `credibility[]` carries it; `achievements[]` does not. Credibility holds the soft institutional material (batch, press, awards). Achievements holds the hard performance numbers that reach published copy. The safer list is disciplined and the dangerous one is not.

**3.2 `market.pains[].gap_math.observables[]`: string -> object.** `constants[]` carries `{name, value, unit, source, evidence_class}`. `observables[]` is three bare words in the same field.

Add `findable`, valued `public` or `must_ask`. Of the three on `pain:unworked_backlog`, only `analyst_count` is obtainable before contact; `alert_volume_monthly` and `backlog_age_days` are internal. Write is handed a formula with unobtainable inputs and no marking, so it will invent them or drop the math. Inventing a number in an email to a fraud team is this seller's worst failure mode.

**3.3 Mark records too thin to use.** `company.stage.rounds[1]` is a seed with null size, valuation, equity, and instrument, two unconfirmed investors, and `verification: secondhand`. It has the same shape as a complete round, so any reader counts two rounds and concludes "raised a seed."

**Shipped.** `achievements` got its own `$defs/achievement` rather than inheriting `citedString`, which is how it had no evidence class in the first place. Observables carry `findable: public | must_ask`, and `public` must say where it is found. The thin seed round carries `completeness: thin` plus a note.

**Done when:** every claim-bearing array in the four artifacts carries an evidence or verification class, asserted by a test.

---

## Phase 4: link the numbers that must agree

**4.1 Capacity to demand.** The offer's own figures give roughly one close per quarter (3 audits x 0.33). The ICP plans for 1000 contacts across ~500 accounts. The word "audit" does not appear in `icp.json`. Either the ICP references the delivery ceiling, or `decisions.md` records the accepted tradeoff. Generating demand faster than it can be served burns the best-fit accounts first.

**4.2 Guard to TAM.** `niche_slap_guard` requires 500 accounts before the ICP may be questioned. `05-list/tam.jsonl` holds 774. Neither `icp.json` nor `gtme-icp/SKILL.md` mentions the TAM. The bar cleared by 55%, unchecked, and the margin is thinner than it reads: `contacts_per_account` ranges 1 to 3, so a low-value-weighted list closes it.

A falsification threshold nobody confirmed was reachable is not a safety catch.

**Shipped.** 4.2 is enforced by `numbers_agree` and named in `gtme-measure`. 4.1 took the second option: the ICP keeps its volume plan and `03-icp/decisions.md` records the accepted tradeoff, on the reasoning that folding fulfilment economics into a filter makes the ICP re-derive every time capacity changes. The decision states the risk being accepted and the falsifier that would reverse it.

**Done when:** `numbers_agree` passes and both linkages are named in the artifacts.

---

## Phase 5: state rules, not instances

Each item here is a table someone must keep complete forever, and none of them will be.

**5.1 `personas[].titles_by_segment` -> `identify_by`.** Titles are a search guide, not a filter. Enumerating them fails hardest at the companies with distinctive vocabulary: searching Anthropic for "Software Engineer" misses "Member of Technical Staff."

`gtme-enrich/SKILL.md:151` already tells enrich to substitute when the exact title is absent, but the substitution target is `"the closest revenue-owning exec"`, left over from a different seller. MouseCat does not sell to revenue. The function this ICP points at is written nowhere, so enrich must infer the job from the titles, which is the failure above.

```json
"identify_by": {
  "function":       "owns the fraud case queue and the analysts working it",
  "seniority":      "manager..director",
  "title_examples": ["Fraud Operations Manager", "Trust & Safety Ops Lead"],
  "title_keywords": ["fraud", "trust & safety", "fincrime", "chargeback", "AML"],
  "not_keywords":   ["credit risk", "market risk", "information security"]
}
```

`not_keywords` matters as much as the positive list: "risk" at a lending company returns credit, market, enterprise, and InfoSec risk, none of whom hold a fraud queue.

Per-segment keying is dropped. The vocabulary genuinely varies (Trust & Safety in marketplaces, FinCrime in crypto), but that is one function under different words, so it belongs in the keyword list. Update `gtme-enrich`'s substitution rule to point at `function`.

**5.2 `seed_targets`: strings -> objects.** Twenty bare names with no tier, signal, or reason. Nothing can tell whether a new company resembles them, whether one has gone stale, or that `Lead Bank` breaks the ICP's hardest disqualifier.

```json
{"name": "...", "tier": 1, "qualifying_signal": "job_posting_intent", "cites": ["[I7]"]}
```

**5.3 `market.awareness` gets a default.** Four of eight targeted company types have no awareness level and no fallback. Awareness decides the shape of the message: problem-aware means name the problem, solution-aware means differentiate from the incumbent. Opposite emails.

Add `"default": {"level": "problem_aware", "rationale": "..."}`. The fix is a rule that covers segment nine, not four more rows.

**5.4 `personas[].cares_about` -> ordered pain ids.** Nine hand-typed phrases paraphrasing pains that `pains[].who_feels` already assigns. The two representations already disagree: `champion.cares_about` lists "analyst burnout," which is a symptom and not a pain id; `technical_evaluator` lists three items where the derivation yields two.

The ranking is the only information the prose adds, so keep the ordering and drop the paraphrase. Write then receives the pain's full statement, shape, and evidence instead of three words.

**5.5 Rename around collisions.** Same word, different meaning, one file:

- `company.platform` (product surface) vs `socials[].platform` (Twitter, LinkedIn)
- `company.company` (name) vs `company.socials.company` (accounts)
- `company.stage` (funding stage) vs `stage.rounds[].stage` (also funding stage)
- `icp.seed_targets` (trusted starting accounts) vs `gtme-list` "seeded" (accounts invented from model memory, which that skill calls the worst failure the pipeline can produce)

The last pair is the dangerous one: one meaning is your most trusted input, the other is the thing the pipeline forbids shipping.

**Correction to 5.2: `Lead Bank` was removed, not annotated.** Structuring the seeds made the contradiction expressible, and then the right answer was obvious: `seed_targets` means "accounts to start from", and an account we have decided not to contact is not one. `03-icp/decisions.md` carries the record and the rejected alternative (relaxing the disqualifier to fit one hand-picked name, which is the failure the disqualifier exists to prevent). `seeds_pass_disqualifiers` stays strict.

**Shipped.** 5.1 through 5.4 as specced. 5.5 partially: `socials[].platform` renamed to `network`, which was the collision that could actually mislead a reader inside one file. The `seed_targets` versus gtme-list "seeded" collision is handled by naming both in the same paragraph of `gtme-list/SKILL.md` rather than renaming, since the two words are correct in their own contexts and the danger was that nobody had ever put them side by side.

**Done when:** each field states its rule and its default; the ICP validates green after migration.

---

## What this does not cover

**The technical evaluator has nothing to say to them.** Both their pains are `latent` (no felt evidence, by design), both have empty `gap_math.constants`, their objection is unanswered, and the offer they gate has no acceptance path. Phases 1, 2, and 3 each repair one piece. Whether the persona is viable at all is a research and positioning question, not a schema one. Flagged, not solved.

**`pain:evidence_assembly`, `urgency_facts`, `bonuses`, and the guarantee strength gate need offer content**, not just shape. Phase 1 makes the slots required; filling them is `gtme-offer` work.

**Three features have no pain pointing at them:** `feat:auto_reinvestigation`, `feat:operator_console`, `prop:vpc_deploy`. The third is the differentiator the positioning rests on. That is either a missing pain (security veto, data residency) or an honest signal that it removes an objection rather than killing a pain. A judgment call for the market stage.

## Verification

Each phase ships only when `python3 skills/validate.py runs/mousecat` is green and `pytest skills/tests` passes. Phase 0 ships first and must fail loudly on the current run; a Phase 0 that passes immediately is not measuring anything.

**Final state:** validator green across all five artifacts and four provenance files; 157 tests pass. The checks were then verified non-vacuous by injecting an unread field, a disqualified seed, and an unreachable guard bar into `icp.json` and confirming three separate failures.

## The pattern worth keeping

Every fix here already exists somewhere in this repo, working:

- `gtme-write` handles `persona.md` correctly: optional input, stated default, stated reason.
- `gap_math.constants` carries evidence class correctly.
- `disqualifiers` carries rule plus reason correctly.
- `sources_swept` reports blocked sources honestly.
- `orphaned_citations` and `distillation_gaps` make silent drops impossible.

None of this is new doctrine. It is applying the repo's own patterns to the places that have not caught up.
