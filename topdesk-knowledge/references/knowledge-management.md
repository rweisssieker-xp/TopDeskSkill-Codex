# TOPdesk Knowledge Management

Use this file for knowledge workflows, article lifecycle, deflection, knowledge quality, RAG sources, and article generation from incidents.

## Article Lifecycle

1. Candidate identified from repeated incidents, high-volume category, known workaround, or operator feedback.
2. Draft article created with title, symptoms, cause, resolution steps, affected services/assets, tags, visibility, and owner.
3. Technical review confirms accuracy.
4. Service owner or application manager approves visibility.
5. Article published to operator-only or SSP audience.
6. Article linked from incidents and categories.
7. Review date triggers validation or archival.

## Article Quality Checklist

- Clear title using user/search language.
- Symptoms and affected scope.
- Step-by-step resolution.
- Escalation path when steps fail.
- Required permissions or prerequisites.
- Visibility and branch/customer restrictions.
- Owner and review date.
- Linked categories, services, assets, and related articles.

## Deflection Signals

- High ticket volume with repeated solution.
- Many tickets closed with similar action text.
- Repeated SSP/search terms.
- Tickets reopened due to incomplete guidance.
- Operators repeatedly linking the same article manually.

## AI/RAG Source Quality

- Index only approved, current, visible articles.
- Keep internal-only articles out of public chatbot retrieval.
- Store language, visibility, branch, category, owner, and review status as chunk metadata.
- Cite source articles in generated answers.
- Exclude archived or expired articles by default.

## KPIs

- Article usage count.
- Article-linked incident resolution rate.
- Deflection rate.
- Articles past review date.
- Incidents without linked knowledge in top categories.
- Reopen rate after article-guided resolution.
