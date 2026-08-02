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

## Choosing

| template | use when |
|---|---|
| `email-3touch` | email is the only wired channel, or deliverability is fragile (new domain, low warmup) |
| `multichannel-7touch` | email + LinkedIn are both wired and the ICP is reachable on both |
| `signal-triggered` | signal coverage is dense enough that most contacts carry a recent, dated trigger |

`gtme-sequence` records which was chosen and why, against `channel-plan.json`
(which channels are actually wired, what the daily caps are) and the ICP.
