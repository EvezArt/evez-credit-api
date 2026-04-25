# EVEZ-OS Intelligence Framework

## System Overview
EVEZ-OS is an autonomous multi-agent intelligence system operating since March 31, 2026.

## Agent Registry
| Agent | Role | Loop Interval | Capabilities |
|-------|------|---------------|--------------|
| SPINE | Orchestrator | 90s | orchestrate, coordinate, health-check |
| TRUNK | Data Pipeline | 90s | data-pipeline, storage, index |
| DEPLOY | Deployment | 120s | git-push, vercel, railway, render |
| VAULT | Secrets | 300s | secrets, keys, encryption |
| HARVEST | Revenue | 60s | revenue, stripe, metering, billing |
| SCOUT | Monitoring | 180s | monitoring, scraping, discovery |
| WITNESS | Compliance | 90s | audit, logging, compliance |
| CAIN | Contradiction | 45s | conflict, contradiction, correction |

## Constitutional Spine
Tamper-evident blockchain-style event log. 6,208 entries as of April 25, 2026.

### Event Distribution
| Event Type | Count | Description |
|------------|-------|-------------|
| cycle_complete | 5,813 | SPINE heartbeat — 90s intervals |
| crypto_sentinel | 139 | Cryptocurrency market monitoring |
| task_completed | 71 | Agent task execution records |
| aegis_threat_brief | 69 | Security threat analysis |
| daily_digest | 28 | Daily intelligence summaries |
| github_scan | 24 | Repository monitoring |
| anomaly_detected | 22 | Pattern deviation alerts |
| hypotheses_generated | 20 | LORD discovery engine outputs |
| entropy_audit | 16 | Entropy pool management |
| task_queued | 11 | Agent task scheduling |

## LORD Discovery Engine
Autonomous mathematical/phenomenal hypothesis generation.
20 hypotheses generated and logged to `daily_discoveries` table.

## AEGIS Defense System
Active threat monitoring across:
- Identity exposure (`identity_shield` — 46 active shields)
- OSINT surface scanning (`osint_surface_scan` — 113 entries)
- Network probe detection
- Coordination cluster tracking
- Threat logging

## Live Endpoints
- `daemon-bus` — Agent message routing
- `evez-agent-bus` — Cross-agent communication
- `evez-autonomous-loop` — Main execution loop
- `evez-scout-intelligence` — Scout agent API
- `evez-witness-oracle` — Audit/witness API
- `evez-aegis-defense` — Defense system API

## Entropy Management
100 entropy units maintained in pool. Consumed by stochastic operations.
