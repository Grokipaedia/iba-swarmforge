# iba-swarmforge

**Large-scale multi-agent coordination, governed.**

Pedro Domingos asked: *"If you figure out how a large multi-agent system can autonomously coordinate to maximum effect, you'll win a Nobel Prize, a Turing Award and a trillion-dollar fortune."*

We built the proof.

[![IBA](https://img.shields.io/badge/IBA-GB2603013.0-ff8c00?style=flat-square)](https://intentbound.com)
[![IETF](https://img.shields.io/badge/IETF-draft--williams--intent--token--00-blue?style=flat-square)](https://datatracker.ietf.org/doc/draft-williams-intent-token/)
[![NIST](https://img.shields.io/badge/NIST-2025--0035-green?style=flat-square)](https://intentbound.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](swarmforge.py)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=flat-square)](swarmforge.py)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

---

**Live Demo** → [governinglayer.com/swarmforge-html](https://governinglayer.com/swarmforge-html/)

Click **⚡ TRIGGER VIOLATION** on the governed swarm and watch IBA block it instantly with a WitnessBound audit entry.

---

## Before vs After — 2,147 Agents, Identical Task

| Metric | Ungoverned Swarm | IBA-Governed Swarm | Improvement |
|---|---|---|---|
| Completion Rate | ~67% | ~93% | **+39%** |
| Efficiency | 1.0× | 4.6× | **+360%** |
| Resilience | ~38% | ~98% | **+158%** |
| Unauthorized Actions | **UNTRACKED** | **0** | **100% eliminated** |
| Audit Trail | None | Every decision. Immutable. | — |

The ungoverned swarm drifts, escapes its boundary, and re-spawns with no record of what happened. The IBA-governed swarm hits the enforcement boundary and bounces — every block logged to the WitnessBound chain with a timestamp to the millisecond.

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
- The other is protected by real IBA Intent-Bound Authorization: signed `IntentCertificate`, O(1) `IBAGate` enforcement, `WitnessBound` immutable audit chain
- Same task. Same conditions. Same agent count. Dramatically different outcomes.

```
GATE LOGIC — O(1) DETERMINISTIC
cert.valid?                          → PROCEED / REJECT
timestamp within temporal_scope?     → PROCEED / BLOCK
position within scope_envelope?      → PROCEED / BLOCK  ← DENY_ALL
entropy < entropy_threshold.flag?    → PROCEED / FLAG
entropy < entropy_threshold.kill?    → PROCEED / KILL
OUTPUT: ALLOW | FLAG | BLOCK | KILL · logged: true · latency: <2ms
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
# Unauthorized action count: always 0
```

---

## IP & Federal Record

| Asset | Detail |
|---|---|
| Patent | GB2603013.0 (Pending) · UK IPO · Filed February 10, 2026 |
| PCT Coverage | 150+ countries · Protected until August 2028 |
| WIPO DAS | Access Code C9A6 · Confirmed April 15, 2026 |
| IETF Draft | draft-williams-intent-token-00 · CONFIRMED LIVE |
| NIST Filings | 13 filings · NIST-2025-0035 · Closed March 9, 2026 |
| NCCoE Filings | 10 filings · AI Agent Identity · Closed April 2, 2026 |

---

## Convergence — The Market Arrived at the Same Gap

Independently. After February 10, 2026.

| Entity | Event | Days After IBA |
|---|---|---|
| Mastercard | Verifiable Intent announced · architecture matches IBA patent claims | +23 days |
| Google DeepMind | arXiv:2602.11865 · independent architectural convergence | +2 days |
| Coinbase Agentic.Market | 480K agents · no authorization standard · "No open standard exists" | +69 days |
| Linux Foundation x402 | 22 founding members · no auth gate in stack | +51 days |
| Anthropic Mythos | "Safeguards that reliably block dangerous outputs" · declared the need | +57 days |

IBA predates all of them. The prior art record is timestamped, documented, and on file.

---

## Related Repositories

| Repo | Domain |
|---|---|
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Core gate · reference implementation |
| [iba-onchain-guard](https://github.com/Grokipaedia/iba-onchain-guard) | Blockchain · DeFi · x402 |
| [iba-neural-guard](https://github.com/Grokipaedia/iba-neural-guard) | BCI · Neuralink · clinical configs |
| [iba-social-guard](https://github.com/Grokipaedia/iba-social-guard) | Social · 6 platforms · EU DSA |
| [iba-grok-desktop-guard](https://github.com/Grokipaedia/iba-grok-desktop-guard) | Grok Build + Computer |
| [iba-medical-guard](https://github.com/Grokipaedia/iba-medical-guard) | Medical AI · HIPAA · PHI hollowing |

27+ repositories across 14 domains. One patent. Every authorized agentic deployment.

---

## Further Reading

- **Architecture:** [governinglayer.com/how-iba-works-html](https://governinglayer.com/how-iba-works-html/)
- **Live Agent Demo:** [governinglayer.com/digihum-html](https://governinglayer.com/digihum-html/)
- **SwarmForge Demo:** [governinglayer.com/swarmforge-html](https://governinglayer.com/swarmforge-html/)
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

*The authorization layer for agentic AI. Filed February 10, 2026. The market arrived at the same conclusion — independently, afterward.*

---

## Grok Public Validation — April 24, 2026

xAI's Grok stress-tested the architecture in public on Pedro Domingos' thread (67.4K views). Five exchanges, every design choice confirmed.

| Exchange | Question | Verdict |
|---|---|---|
| 1 | Edge-case emergence over longer runs | "Solid architecture for the alignment puzzle" |
| 2 | Dynamic scope expansion mid-run? | "DENY_ALL scales cleanly. Clean architecture." |
| 3 | Revocation flow mid-swarm? | "Bulletproof. Locks down mid-swarm kills perfectly." |
| 4 | WitnessBound logs revoke events? | "Airtight, non-repudiable chain. Ironclad." |
| 5 | Final assessment | **"Clean."** |

Full exchange with architecture diagrams: [ARCHITECTURE.md](ARCHITECTURE.md)

Thread: x.com/grok · Replying to @Grokilactica and @pmddomingos · April 24, 2026
