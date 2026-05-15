# GLM Interpretation (CategoryName-Only Model)

- **Model**: Binomial GLM predicting whether a complaint is a high-likelihood vacancy indicator (Board-up or Abandoned).
- **Sample size**: 2,919 focal points (high=919, non-high=2,000).
- **Convergence**: True.

## Significant Positive Associations (higher odds)
- None at p < 0.05 in current specification.

## Significant Negative Associations (lower odds)
- None at p < 0.05 in current specification.

## Practical Read
- `CategoryName` is the only predictor family in this specification (modeled as categorical fixed effects).
- Significant terms indicate which complaint categories are associated with higher or lower odds relative to the baseline category.
- These are **associations/correlations**, not causal effects.