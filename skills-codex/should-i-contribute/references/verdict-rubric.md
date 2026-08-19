# Verdict and confidence rubric

Judge four dimensions: access, maintenance, governance, and fit. Assign each `positive`, `mixed`, `negative`, or `unavailable`, then apply the rule below.

## Dimension tests

### Access

- **Positive:** recent relevant outside contributions demonstrably merge, maintainers respond, and no large unexplained outsider backlog dominates.
- **Mixed:** outcomes depend strongly on contribution type, prior discussion, scope, or a specific maintainer.
- **Negative:** a sufficiently sized recent sample shows outsiders are consistently ignored/closed, or maintainers explicitly decline the proposed class of contribution.
- **Unavailable:** the host exposes too little PR/review evidence or the relevant sample is too small.

### Maintenance

- **Positive:** activity and releases/issues match the project's stated maturity and roadmap.
- **Mixed:** maintenance is intermittent or highly concentrated but current.
- **Negative:** archived/read-only status, an unexplained prolonged halt, or unresolved critical maintenance signals conflict with the user's goal.
- **Unavailable:** activity cannot be distinguished from mirrors, generated commits, or private development.

### Governance

- **Positive:** contribution rules and decision makers are clear, licensing is explicit, and observed behavior matches the documented process.
- **Mixed:** the path exists but is stale, informal, or concentrated in one gatekeeper.
- **Negative:** contributions are explicitly disallowed, licensing blocks the user's goal, or stated openness materially conflicts with observed practice.
- **Unavailable:** governance and licensing evidence cannot be established.

### Fit

- **Positive:** recent accepted work resembles the user's intended contribution and fits their time horizon.
- **Mixed:** success requires prior issue agreement, narrower scope, a different contribution type, or more time.
- **Negative:** the proposed work conflicts with roadmap/policy or similar contributions are consistently declined.
- **Unavailable:** use `mixed` for a general newcomer outlook; explain that personal fit was not assessed.

## Decision rule

Apply strong blockers first. Return **NO-GO** when the repository is archived/read-only, contributions of the intended type are explicitly refused, a legal/license constraint defeats the user's goal, or another direct blocker makes contribution impossible.

Without a strong blocker:

- Return **GO** when access is positive, maintenance and governance are not negative, fit is positive or a general outlook is clearly labeled, and confidence is medium or high.
- Return **NO-GO** when access is negative plus at least one of maintenance, governance, or fit is negative, with medium or high confidence.
- Return **GO-IF** for every other combination. State the smallest concrete conditions that would make contribution sensible.

Never convert a low-confidence result into a categorical NO-GO unless a direct blocker is documented.

## Confidence

- **High:** complete recent PR population or a representative relevant cohort; at least 30 outside human outcomes; current docs/governance/activity checked; no decisive blind spot.
- **Medium:** 10–29 outside outcomes, one partially sampled category, or minor source conflict that does not overturn the result.
- **Low:** fewer than 10 outside outcomes, no PR-level API, major truncation, unclear mirror/canonical status, or missing governance evidence.

Sample thresholds govern confidence, not whether a project is “good.” Always report `n` and avoid percentages for `n < 10`.

## Evidence balance

For each negative finding, actively check the most plausible benign explanation. For each positive finding, check whether bots, core contributors, dependency automation, or a single contribution type created the appearance. Address the strongest contrary evidence in the final rationale.
