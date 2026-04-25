# EVEZ Credit Scoring API

Production-ready FICO-equivalent credit scoring engine with full ECOA/FCRA compliance.

## Features

- **8-Factor Risk Model**: Payment history, utilization, credit age, mix, inquiries, DTI, derogatory marks, total accounts
- **FICO-Equivalent Scoring**: 300-850 range with letter grades (A+ through F)
- **ECOA/FCRA Compliance**: Automated adverse action notice generation
- **Real-Time & Batch**: Score individual applicants or entire portfolios
- **Decision Engine**: Automated APPROVED/DENIED/MANUAL_REVIEW decisions

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/score` | Score single applicant |
| POST | `/batch` | Batch score applicants |
| GET | `/model-info` | Model metadata and weights |

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Deploy to Fly.io

```bash
fly launch --name evez-credit-api --region ord
fly deploy
```

## Supabase Integration

The scoring engine integrates with a Supabase database schema:
- `applicants` — Borrower profiles
- `credit_profiles` — Raw credit data
- `credit_scores` — Scoring results with factor breakdowns
- `adverse_actions` — FCRA-compliant adverse action records
- `loan_applications` — Loan lifecycle tracking
- `audit_log` — Full compliance audit trail

## Model Weights

| Factor | Weight |
|--------|--------|
| Payment History | 35% |
| Credit Utilization | 20% |
| Credit Age | 15% |
| Credit Mix | 10% |
| Recent Inquiries | 5% |
| DTI Ratio | 5% |
| Derogatory Marks | 5% |
| Total Accounts | 5% |

## License

MIT
