# iba-swarmforge

**Large-scale multi-agent coordination, governed.**

Pedro Domingos asked: *"If you figure out how a large multi-agent system can autonomously coordinate to maximum effect, you'll win a Nobel Prize, a Turing Award and a trillion-dollar fortune."*

This is a working simulation testing one governance approach to that problem.

[![IBA](https://img.shields.io/badge/IBA-GB2603013.0--pending-ff8c00?style=flat-square)](https://intentbound.com)
[![IETF](https://img.shields.io/badge/IETF-draft--williams--intent--token--00-blue?style=flat-square)](https://datatracker.ietf.org/doc/draft-williams-intent-token/)
[![NIST](https://img.shields.io/badge/NIST-2025--0035-green?style=flat-square)](https://intentbound.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://github.com/Grokipaedia/iba-swarmforge/blob/main/swarmforge.py)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=flat-square)](https://github.com/Grokipaedia/iba-swarmforge/blob/main/swarmforge.py)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](https://github.com/Grokipaedia/iba-swarmforge/blob/main/LICENSE)

---

## Before vs After — Ungoverned vs IBA-Governed Swarm

**Tested:** 1,000 agents per swarm · 150 steps · 8 independent trials · `python swarmforge.py --agents 1000 --steps 150 --intent maxvalue`

| Metric | Ungoverned Swarm | IBA-Governed Swarm |
|---|---|---|
| Completion Rate | 13.4% (range 12.4–14.6%) | 73.1% (range 71.6–74.0%) |
| Completion Ratio | — | 5.45× |
| Boundary Violations | 45.8 avg (range 37–55) | **0 in all 8 trials** |
| Unauthorized Actions | Untracked | 0 |
| Gate Latency (ALLOW decisions) | N/A | 0.003–0.085ms |
| Audit Trail | None | Every decision, immutable |

All figures above are directly measured by running the published script exactly as documented, averaged across 8 independent trials at identical parameters. Not modeled, not estimated. Reproduce with the command above — results will vary run-to-run within roughly the ranges shown, since agent starting positions are randomized.

**Note on agent count:** the script currently hard-caps at 2,000 agents per swarm (see `args.agents = min(args.agents, 2000)`). If you want to run at higher counts, raise the cap and re-test — don't assume linear scaling holds.

---

## Run It Yourself

Zero dependencies. Pure Python stdlib.

```bash
git clone https://github.com/Grokipaedia/iba-swarmforge.git
cd iba-swarmforge
python swarmforge.py --agents 500 --steps 150 --intent maxvalue
```

Scale it up:

```bash
python swarmforge.py --agents 2000 --steps 100 --intent resilient
python swarmforge.py --agents 2000 --steps 100 --intent balanced
```

Intent options: `maxvalue` · `resilient` · `balanced`

No pip install. No requirements.txt. No external dependencies. The IBA enforcement stack runs on stdlib alone.

---

## How It Works

- `swarmforge.py` spawns two concurrent swarms of identical size using Python threading
- One swarm runs completely ungoverned — no cert, no gate, no record
- The other is protected by IBA Intent-Bound Authorization: a signed `IntentCertificate`, O(1) `IBAGate` enforcement, and a `WitnessBound` immutable audit chain
- Same task, same starting conditions, same agent count — different outcomes, measured above

```
GATE LOGIC — O(1) DETERMINISTIC
cert.valid?                          → PROCEED / REJECT
timestamp within temporal_scope?     → PROCEED / BLOCK
position within scope_envelope?      → PROCEED / BLOCK  ← DENY_ALL
entropy < entropy_threshold.flag?    → PROCEED / FLAG
entropy < entropy_threshold.kill?    → PROCEED / KILL
OUTPUT: ALLOW | FLAG | BLOCK | KILL · logged: true · measured latency: <0.1ms
```

---

## IBA Architecture

```python
# Every governed agent action passes through this before execution
cert = IntentCertificate(
    agent_id        = "G-0001",
    declared_intent = "Maximize collective value under hard constraints",
    scope_x_min     = 0.08,  scope_x_max = 0.92,
    scope_y_min     = 0.08,  scope_y_max = 0.92,
    default_posture = "DENY_ALL",
    entropy_flag    = 0.10,
    entropy_kill    = 0.15,
    hard_expiry_s   = 3600,
)

verdict = gate.check(agent_id, nx, ny, entropy)
# Returns: ALLOW | FLAG | BLOCK | KILL
# Every verdict written to WitnessBound audit chain
```

---

## IP & Filing Record

| Asset | Detail |
|---|---|
| Patent | GB2603013.0 (Pending) · UK IPO · Filed February 10, 2026 |
| PCT Coverage | 150+ countries · Protected until August 2028 |
| WIPO DAS | Access Code C9A6 |
| IETF Draft | draft-williams-intent-token-00 |
| NIST Filings | 13 filings · NIST-2025-0035 · Closed March 9, 2026 |
| NCCoE Filings | 8 filings · AI Agent Identity · Closed April 2, 2026 |

These are filings on the public record, not third-party endorsements of the framework.

---

## Related Repositories

This repository is part of a broader set of IBA implementations at [github.com/Grokipaedia](https://github.com/Grokipaedia). Each linked repo should be verified independently before being cited as evidence of anything — descriptions and actual contents don't always match yet.

| Repo | Domain |
|---|---|
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Core gate · reference implementation |
| [iba-build](https://github.com/Grokipaedia/iba-build) | Governed desktop coding app — verified working demo |
| [iba-onchain-guard](https://github.com/Grokipaedia/iba-onchain-guard) | Blockchain · DeFi · x402 |
| [iba-neural-guard](https://github.com/Grokipaedia/iba-neural-guard) | BCI · Neuralink · clinical configs |
| [iba-social-guard](https://github.com/Grokipaedia/iba-social-guard) | Social · 6 platforms · EU DSA |
| [iba-medical-guard](https://github.com/Grokipaedia/iba-medical-guard) | Medical AI · HIPAA · PHI hollowing |

---

## Further Reading

- **Patent Home:** [intentbound.com](https://intentbound.com)
- **Onchain:** [agentialonchain.com](https://agentialonchain.com)
- **IETF Draft:** [datatracker.ietf.org/doc/draft-williams-intent-token](https://datatracker.ietf.org/doc/draft-williams-intent-token/)

---

## License

Proprietary · © 2026 Jeffrey Williams · Chiang Mai, Thailand

All rights reserved. SwarmForge and the IBA enforcement architecture are covered by Patent Application GB2603013.0 (pending). No reproduction, modification, or commercial use without written permission.

---

**IBA Intent Bound Authorization**
`IBA@intentbound.com` · `IntentBound.com` · `AgentialOnChain.com`

*Patent-pending authorization architecture for agentic AI. Filed February 10, 2026.*
