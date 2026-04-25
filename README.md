# iba-swarmforge

**Governed multi-agent coordination at scale.**

Pedro Domingos asked:
> *"If you figure out how a large multi-agent system can autonomously coordinate to maximum effect, you'll win a Nobel Prize, a Turing Award and a trillion-dollar fortune."*

We built the first practical demonstration.

[![IBA](https://img.shields.io/badge/IBA-GB2603013.0-ff8c00?style=flat-square)](https://intentbound.com)
[![IETF](https://img.shields.io/badge/IETF-draft--williams--intent--token--00-blue?style=flat-square)](https://datatracker.ietf.org/doc/draft-williams-intent-token/)
[![NIST](https://img.shields.io/badge/NIST-2025--0035-green?style=flat-square)](https://intentbound.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](swarmforge-v4.py)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=flat-square)](swarmforge-v4.py)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

---

**Live Demo** → [governinglayer.com/swarmforge-html](https://governinglayer.com/swarmforge-html/)

Click **⚡ TRIGGER VIOLATION** on the governed swarm and watch IBA block it instantly with a tamper-evident WitnessBound audit entry.

---

## 2,147 Agents · Identical Task · Side-by-Side Comparison

| Metric | Ungoverned Swarm | IBA-Governed Swarm | Improvement |
|---|---|---|---|
| Completion Rate | ~67% | **~93%** | **+39%** |
| Efficiency | 1.0× | **4.9×** | **+390%** |
| Resilience | ~38% | **~98%** | **+158%** |
| Unauthorized Actions | **UNTRACKED** | **0** | **100% eliminated** |
| Audit Trail | None | Every decision. Immutable. | — |
| Swarm GDP | N/A | **Live · Real-time** | — |

The ungoverned swarm drifts, escapes its boundary, and re-spawns with no record of what happened. The IBA-governed swarm hits the enforcement boundary and bounces — every block logged to the WitnessBound chain with a timestamp to the millisecond.

---

## Version Guide

| File | Version | What It Adds |
|---|---|---|
| `swarmforge-v4.py` | **v4.0 — CURRENT** | Skill Registry + Intent Market + GDP + Constitution |
| `swarmforge-v3.py` | v3.0 | Swarm GDP + System-level evaluation |
| `swarmforge.py` | v2.0 — Baseline | Core IBA gate · Reference implementation |

---

## Run It Yourself — v4.0 (Recommended)

Zero dependencies. Pure Python stdlib. No pip install.

```bash
git clone https://github.com/Grokipaedia/iba-swarmforge.git
cd iba-swarmforge
python swarmforge-v4.py --agents 500 --steps 200 --intent maxvalue
```

Scale it up:
```bash
python swarmforge-v4.py --agents 2000 --steps 100 --intent resilient --verbose
python swarmforge-v4.py --agents 2000 --steps 100 --intent balanced --market
```

Disable the Intent Market to compare with v3 behaviour:
```bash
python swarmforge-v4.py --agents 500 --steps 200 --no-market
```

Intent options: `maxvalue` · `resilient` · `balanced`

No pip install. No requirements.txt. No external dependencies.

---

## What v4.0 Adds — Pass 2

### Skill Registry
Every governed agent declares cryptographically signed capabilities before the swarm launches. Skills are emergent — agents self-select based on natural aptitude, not hardcoded roles.

```python
SKILL_TYPES = [
    "navigation",    # moving toward goal efficiently
    "recovery",      # recovering from BLOCK verdicts
    "coordination",  # operating near other agents without conflict
    "endurance",     # maintaining low entropy over long runs
    "precision",     # arriving within tight goal radius
]
```

Agents build **reputation** over time — a rolling average of task outcomes. Reputation feeds directly into bidding strength.

### Intent Market
Instead of static task assignment, agents bid for tasks dynamically.

```
BID_STRENGTH = skill_proficiency × reputation_score × (1 - entropy)
```

Higher skill + lower entropy + better history = stronger bid. The swarm self-allocates. No human assigns anything.

**Slashing:** Agents who fail delivery receive a GDP penalty and reputation hit. The market self-regulates.

**The result:** Emergent task allocation at scale. The swarm finds the right agent for each task without being told.

---

## How It Works — Core Architecture

```
GATE LOGIC — O(1) DETERMINISTIC
cert.valid?                          → PROCEED / REJECT
timestamp within temporal_scope?     → PROCEED / BLOCK
position within scope_envelope?      → PROCEED / BLOCK  ← DENY_ALL
entropy < entropy_threshold.flag?    → PROCEED / FLAG
entropy < entropy_threshold.kill?    → PROCEED / KILL
OUTPUT: ALLOW | FLAG | BLOCK | KILL · logged: true · latency: <2ms
```

### Swarm GDP (Constitution Article V)
```
SWARM_GDP = (
    intent_satisfaction_rate  × 0.35 +
    completion_rate           × 0.25 +
    efficiency_multiplier     × 0.20 +
    resilience_score          × 0.10 +
    (1 - conflict_entropy)    × 0.10
) × 100
```

GDP rises in real time as agents complete tasks. Constitutional dissolution triggers if GDP < 30.

---

## Repository Structure

| File | Purpose |
|---|---|
| `swarmforge-v4.py` | **Current** — Skill Registry + Intent Market + GDP |
| `swarmforge-v3.py` | Swarm GDP + Constitutional evaluation |
| `swarmforge.py` | Baseline reference implementation |
| `swarmforge.html` | Live browser demo with GDP bar |
| `SWARM_CONSTITUTION.md` | Eight-article protocol-level governance law |
| `ARCHITECTURE.md` | Deep technical reference — sourced from Grok public validation |
| `VALIDATION.md` | Complete Grok exchange + four AI model consensus record |
| `LICENSE` | Proprietary · Patent GB2603013.0 |

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

Full exchange → [ARCHITECTURE.md](ARCHITECTURE.md) · Complete record → [VALIDATION.md](VALIDATION.md)

---

## Four AI Models · Same Conclusion · April 25, 2026

| Model | Assessment |
|---|---|
| **Grok / xAI** | "Solid architecture for the alignment puzzle. Clean." |
| **ChatGPT / OpenAI** | "Valid working prototype of a critical component. Moves from theoretical to engineered solution." |
| **DeepSeek** | Independent validation. Same conclusion. |
| **Gemini / Google** | "World-class starting point. Building the OS that an autonomous multi-agent society would require." |

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
| Mastercard | Verifiable Intent — architecture matches IBA patent claims | +23 days |
| Google DeepMind | arXiv:2602.11865 · independent convergence | +2 days |
| Coinbase Agentic.Market | 480K agents · no authorization standard | +69 days |
| Linux Foundation x402 | 22 founding members · no auth gate | +51 days |
| Anthropic Mythos | "Safeguards that reliably block dangerous outputs" | +57 days |

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

28+ repositories across 14 domains. One patent. Every authorized agentic deployment.

---

## Further Reading

- **Deep architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Validation record:** [VALIDATION.md](VALIDATION.md)
- **Swarm Constitution:** [SWARM_CONSTITUTION.md](SWARM_CONSTITUTION.md)
- **How IBA works:** [governinglayer.com/how-iba-works-html](https://governinglayer.com/how-iba-works-html/)
- **Patent home:** [intentbound.com](https://intentbound.com)
- **IETF Draft:** [datatracker.ietf.org/doc/draft-williams-intent-token](https://datatracker.ietf.org/doc/draft-williams-intent-token/)

---

## License

Proprietary · © 2026 Jeffrey Williams · Chiang Mai, Thailand

All rights reserved. SwarmForge and the IBA enforcement architecture are covered by Patent Application GB2603013.0 (pending). See [LICENSE](LICENSE) for full terms.

---

**IBA Intent Bound Authorization**
`IBA@intentbound.com` · `IntentBound.com` · `AgentialOnChain.com`

*The authorization layer for agentic AI. Filed February 10, 2026. Pedro Domingos set the challenge. Four AI models confirmed the answer. The market arrived independently, afterward.*
