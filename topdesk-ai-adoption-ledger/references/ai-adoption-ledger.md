# AI Adoption Ledger Reference

## Core Metrics

| Metric | Meaning |
| --- | --- |
| Suggestions generated | Count of AI suggestions. |
| Acceptance rate | Accepted suggestions divided by all suggestions. |
| Edit rate | Edited suggestions divided by all suggestions. |
| Rejection rate | Rejected suggestions divided by all suggestions. |
| Override rate | Edited or rejected suggestions divided by all suggestions. |
| Average confidence | Mean model confidence where available. |
| Estimated cost | Sum of provided cost estimates. |
| Estimated time saved | Sum of provided time-saved assumptions. |

## Interpretation

- High acceptance and low edit rate can justify scaling a use case.
- High rejection or override rate needs prompt, data, policy, or UX review.
- Low confidence with high acceptance needs sampling to avoid false trust.
- High cost without adoption should pause expansion.
