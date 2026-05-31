# Decision Findings Reference

## Standard Fields

| Field | Purpose |
| --- | --- |
| `finding` | Short issue or opportunity. |
| `evidence` | Concrete source fact, count, row, or observed pattern. |
| `business_impact` | Why it matters operationally, financially, or for risk. |
| `risk` | `high`, `medium`, `low`, or `review`. |
| `recommended_action` | Next practical step. |
| `owner` | Suggested accountable role. |
| `validation_metric` | How to prove the action worked. |

## Good Finding

```text
finding: Missing target dates on open incidents
evidence: 18 open incidents have no targetDate.
business_impact: SLA risk cannot be prioritized reliably.
risk: high
recommended_action: Fix SLA mapping and update open incidents.
owner: Service desk lead
validation_metric: Open incidents without target date equals zero.
```
