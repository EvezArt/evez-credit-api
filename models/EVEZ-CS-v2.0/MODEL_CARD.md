# EVEZ-CS-v2.0 — Credit Scoring Model

## Model Overview
**Model ID**: EVEZ-CS-v2.0  
**Type**: Deterministic weighted scorecard (FICO-equivalent)  
**Score Range**: 300–850  
**Task**: Binary classification (default/no-default) + credit score generation  
**Release**: April 25, 2026  
**License**: MIT  

## Architecture
8-factor weighted scoring model with sigmoid-mapped default probability.

### Factors & Weights
| Factor | Weight | Normalization |
|--------|--------|---------------|
| Payment History | 35% | raw/100 |
| Credit Utilization | 20% | 1 - raw/100 |
| Credit Age | 15% | raw/25 years |
| Credit Mix | 10% | raw/5 types |
| New Inquiries | 5% | 1 - raw/10 |
| DTI Ratio | 5% | 1 - raw/60 |
| Derogatory Marks | 5% | 1 - raw/5 |
| Total Accounts | 5% | raw/20 |

### Scoring Formula
```
weighted_sum = Σ normalize(factor_i) × weight_i
credit_score = clamp(300 + weighted_sum × 550, 300, 850)
default_prob = sigmoid(0.02 × (credit_score - 580))
```

## Decision Thresholds
| Score Range | Grade | Decision | Risk Level |
|-------------|-------|----------|------------|
| 800-850 | A+ | APPROVED | Low |
| 750-799 | A | APPROVED | Low |
| 700-749 | B+ | APPROVED | Low/Medium |
| 650-699 | B | APPROVED | Medium |
| 620-649 | C | APPROVED | Medium |
| 600-619 | C- | MANUAL_REVIEW | High |
| 300-599 | F | DENIED | High |

## Regulatory Compliance
- **ECOA**: Zero protected class variables. No race, sex, age, national origin.
- **FCRA**: All factors from permissible credit data sources.
- **Reg B**: Adverse action notices generated for all denials.
- **Dodd-Frank**: Full transparency, consumer-explainable decisions.

## Live Deployment
- Supabase Edge Function: `credit-score`
- Batch API: `batch-score`
- Portfolio Analytics: `portfolio-analytics`
- Health Check: `health-check`
- Compliance Officer: `compliance-officer`

## Validation Results (Seed Data — 10 Applicants)
- Average Score: 672.1
- Approval Rate: 70%
- Score Std Dev: 147.09
- Default Probability Range: 0.52% – 92.69%
- Model Version: EVEZ-CS-v2.0

## Intended Use
Credit risk assessment for consumer lending applications.

## Limitations
- Scorecard model — not a learned ML model (gradient boosted)
- Requires calibration against actual default outcomes
- Population drift monitoring recommended quarterly

## Citation
```
@model{evez-cs-2026,
  title={EVEZ-CS-v2.0: FICO-Equivalent Credit Scoring Engine},
  author={Crawford-Maggard, Steven / EVEZ Credit Angel},
  year={2026},
  url={https://github.com/EvezArt/evez-credit-api}
}
```
