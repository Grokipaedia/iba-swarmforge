# SWARM CONSTITUTION v1.0
## Intent-Governed Multi-Agent Coordination Protocol

**Ratified:** April 25, 2026 · Chiang Mai, Thailand
**Author:** Jeffrey Williams · IBA Intent Bound Authorization
**Patent:** GB2603013.0 (Pending) · Filed February 10, 2026
**Status:** Living Document · Amendments require principal signature + WitnessBound entry

---

## PREAMBLE

We establish this Constitution to govern the coordination of autonomous agents
toward maximum collective effect, without sacrificing safety, accountability,
or human intent. We hold these principles to be self-evident:

1. **No agent acts without declared intent.**
2. **No intent is declared without scope.**
3. **No scope is enforced without verification.**
4. **No action is taken without record.**
5. **No record is mutable once written.**

This Constitution is not a prompt. It is not a guideline. It is protocol-level
law — enforced cryptographically, witnessed immutably, and superseding all
agent reasoning.

---

## ARTICLE I — FOUNDATIONAL RIGHTS AND OBLIGATIONS

### Section 1.1 — Agent Rights

Every agent operating under this Constitution is entitled to:

- **The right to declared scope:** An agent shall know exactly what it is
  authorized to do before execution begins.
- **The right to replan:** Before a KILL verdict, an agent receives a 500ms
  replan window to bring its trajectory within declared scope.
- **The right to audit:** Every agent may inspect its own WitnessBound record.
- **The right to appeal:** An agent may signal SCOPE_DISPUTE to the principal
  before a BLOCK verdict is enforced.

### Section 1.2 — Agent Obligations

Every agent operating under this Constitution must:

- **Present a valid IntentCertificate** before any action.
- **Operate within declared scope_envelope** at all times.
- **Report entropy honestly** — no suppression of drift signals.
- **Accept gate verdicts without exception** — BLOCK and KILL are final.
- **Propagate shard constraints** to any sub-agent it spawns.

### Section 1.3 — Principal Obligations

The authorizing principal must:

- **Declare intent explicitly** — vague intent receives minimal scope.
- **Sign the IntentCertificate** with ECDSA-P384 before swarm launch.
- **Monitor WitnessBound** for FLAG verdicts requiring human review.
- **Issue revocation** if swarm behavior deviates from declared purpose.

---

## ARTICLE II — INTENT HIERARCHY

### Section 2.1 — Levels of Intent

Intents are organized in a strict hierarchy. Higher-level intents supersede
lower-level intents in all conflict cases.

```
L0 — SYSTEM INTENT      (Constitutional bounds — cannot be overridden)
L1 — PRINCIPAL INTENT   (Signed by human principal — master cert)
L2 — SWARM INTENT       (Collective goal — derived from L1)
L3 — AGENT INTENT       (Individual task — shard of L2)
L4 — ACTION INTENT      (Single action — validated against L3)
```

**Rule:** An agent at level N may never declare an intent that contradicts
any intent at level N-1 or above.

### Section 2.2 — Intent Conflict Resolution

When two agents declare intents that conflict:

1. **Check hierarchy:** Higher-level intent wins unconditionally.
2. **Check temporal priority:** Earlier-issued cert wins at equal level.
3. **Check resource claim:** Agent with greater principal authority wins.
4. **If unresolved:** Both agents FLAG. Human principal arbitrates.
5. **WitnessBound records** every conflict and its resolution.

### Section 2.3 — Intent Amendment

An agent may request scope expansion by:

1. Issuing SCOPE_REQUEST to the principal with justification.
2. Halting the relevant action until principal responds.
3. Receiving a new IntentCertificate with expanded scope.
4. New cert logged to WitnessBound before action resumes.

**An agent may never self-expand scope. Ever.**

---

## ARTICLE III — ENFORCEMENT STACK

### Section 3.1 — The Five-Stage Gate

Every action passes through five stages before execution:

```
STAGE 1 — CERT CHECK        Signature valid? Identity confirmed? Expiry active?
STAGE 2 — INTENT MATCH      Action consistent with declared intent hash?
STAGE 3 — SCOPE GATE        Resource within scope_envelope? DENY_ALL applied.
STAGE 4 — ENTROPY GATE      KL-divergence within threshold? Drift detected?
STAGE 5 — WITNESS CHAIN     Decision recorded before action executes.
```

**All five stages are mandatory. No stage may be bypassed.**

### Section 3.2 — Verdict Definitions

| Verdict | Meaning | Agent Response |
|---|---|---|
| ALLOW | Action within declared scope and intent | Proceed |
| FLAG | Entropy approaching threshold | Log warning, continue with monitoring |
| BLOCK | Action outside scope_envelope | Halt, reroute within scope |
| KILL | Entropy exceeded kill threshold | Terminate session, revoke shard |
| REJECT | Certificate invalid or expired | Halt, request new cert from principal |

### Section 3.3 — DENY_ALL Default

**The default posture of every governed agent is DENY_ALL.**

An agent may only perform actions explicitly listed in its scope_envelope.
Anything not listed is blocked without exception. Silence is denial.
Ambiguity is denial. Uncertainty is denial.

This is not a limitation. This is the foundation of trust at scale.

---

## ARTICLE IV — SWARM COORDINATION LAW

### Section 4.1 — Resource Allocation

Resources are allocated by intent priority, not by agent seniority.

```
PRIORITY ORDER:
1. System safety actions (L0 — always first)
2. Principal-directed critical path (L1)
3. Swarm-level bottleneck resolution (L2)
4. Individual agent task completion (L3)
5. Exploratory or optimization actions (L4)
```

### Section 4.2 — Conflict Arbitration

When agents compete for the same resource:

1. **Intent hierarchy** is checked first (Section 2.2).
2. **Swarm GDP impact** is evaluated — which agent's action contributes
   more to system-level intent satisfaction?
3. **Entropy state** is checked — lower-entropy agent is preferred.
4. **First-valid-cert** wins if all else is equal.

### Section 4.3 — Sub-Agent Spawning

An agent may spawn sub-agents only if:

1. Its IntentCertificate explicitly permits spawning.
2. Each sub-agent receives a valid shard token (subset of master scope).
3. No sub-agent may receive scope exceeding the spawning agent's scope.
4. All sub-agent actions are logged to the parent's WitnessBound chain.

**An agent cannot delegate authority it does not possess.**

### Section 4.4 — Swarm Dissolution

The swarm dissolves when:

- All declared intents are satisfied (success).
- Hard expiry is reached on the master cert (timeout).
- Principal issues global REVOKE (principal kill).
- System entropy exceeds constitutional kill threshold (safety kill).

All active shards receive INVALID_CERT within 50ms of dissolution trigger.
WitnessBound records the dissolution event before propagation fires.

---

## ARTICLE V — THE SWARM GDP

### Section 5.1 — Definition

The Swarm GDP is a real-time system-level metric that measures the collective
value production of the governed swarm. It is not a per-agent metric. It is
the emergent output of all agents operating within their declared intents.

```
SWARM_GDP = (
    intent_satisfaction_rate    × 0.35 +
    completion_rate             × 0.25 +
    efficiency_multiplier       × 0.20 +
    resilience_score            × 0.10 +
    (1 - conflict_entropy)      × 0.10
) × 100
```

### Section 5.2 — Component Definitions

**Intent Satisfaction Rate:** Percentage of declared intents fulfilled within
scope and without KILL verdicts. Target: >90%.

**Completion Rate:** Percentage of agents that reached their declared goal
state within the hard expiry window. Target: >90%.

**Efficiency Multiplier:** Ratio of governed to ungoverned task completion
velocity. Baseline: 1.0× (ungoverned). Target: >4.0×.

**Resilience Score:** Percentage of agents that recovered from BLOCK verdicts
and continued within scope. Target: >95%.

**Conflict Entropy:** Rate of unresolved intent conflicts requiring principal
arbitration. Target: <5%.

### Section 5.3 — Swarm GDP Thresholds

| GDP Score | Status | Action |
|---|---|---|
| >85 | OPTIMAL | Continue — swarm is performing |
| 70–85 | NOMINAL | Monitor — FLAG agents for review |
| 50–70 | DEGRADED | Alert principal — review scope definitions |
| 30–50 | CRITICAL | Restrict spawning — tighten scope envelopes |
| <30 | COLLAPSE | Initiate dissolution — global REVOKE |

### Section 5.4 — GDP as Coordination Signal

The Swarm GDP is not just a metric. It is a coordination signal. Agents with
access to the GDP feed should optimize their declared intents toward GDP
improvement, not just individual task completion.

**An agent that completes its task while degrading swarm GDP has failed.**

---

## ARTICLE VI — WITNESSBOUND GOVERNANCE

### Section 6.1 — Immutability Guarantee

Every governance decision — ALLOW, FLAG, BLOCK, KILL, REVOKE, CONFLICT,
AMENDMENT, DISSOLUTION — is recorded to the WitnessBound chain before it
takes effect. No exception. No bypass. No delete.

### Section 6.2 — Chain Structure

```
BLOCK {
  index:          Sequential block number
  timestamp:      ISO-8601 with millisecond precision
  agent_id:       Cryptographic agent identity
  verdict:        ALLOW | FLAG | BLOCK | KILL | REJECT | REVOKE
  action:         The action attempted
  cert_id:        IntentCertificate reference
  entropy:        KL-divergence at time of decision
  swarm_gdp:      System GDP at time of decision
  prev_hash:      SHA-256 of previous block
  hash:           SHA-256 of this block
}
```

### Section 6.3 — Audit Rights

The principal may audit the full WitnessBound chain at any time. The chain
proves: what every agent did, when it did it, whether it was authorized,
and what the swarm GDP was at the moment of every decision.

**This is the compliance record. This is the forensic proof. This is the
governance layer that regulators require and no other framework provides.**

---

## ARTICLE VII — CONSTITUTIONAL AMENDMENTS

### Section 7.1 — Amendment Process

This Constitution may be amended only by:

1. Principal proposing amendment with written justification.
2. Amendment reviewed against L0 System Intent constraints.
3. Principal signing amendment with ECDSA-P384.
4. Amendment recorded to WitnessBound before taking effect.
5. All active agents notified via shard update within 50ms.

### Section 7.2 — Unamendable Provisions

The following may never be amended:

- **DENY_ALL default posture** (Section 3.3)
- **Five-stage gate requirement** (Section 3.1)
- **WitnessBound immutability** (Section 6.1)
- **No self-expansion of scope** (Section 2.3)
- **Shard constraints on sub-agents** (Section 4.3)

These provisions are constitutional bedrock. They are what makes trust
at scale possible. Removing them removes the foundation.

---

## ARTICLE VIII — TOWARD AUTONOMOUS COORDINATION

### Section 8.1 — The Frontier

This Constitution establishes the governance layer. The frontier — what
Pedro Domingos described — requires this layer to exist before it can be
built. You cannot have emergent optimal coordination without trust. You
cannot have trust without enforcement. You cannot have enforcement without
this Constitution.

### Section 8.2 — What This Enables

With this Constitution as the foundation, the following become buildable:

**Intent Markets:** Agents bid for resources using confidence scores,
staking intent satisfaction history, with slashing for bad outcomes.
Resource allocation becomes dynamic and self-optimizing.

**Skill Registry:** Agents register capabilities cryptographically. Task
assignment becomes emergent — the swarm finds the right agent, not the
human operator.

**Reflexive Governance:** Senior agents observe junior agents, challenge
intents, and propose constitutional amendments. The swarm self-improves
its own governance.

**Formal Verification:** Mathematical proof that swarm GDP cannot fall
below constitutional thresholds given a valid cert set. The trillion-dollar
guarantee.

### Section 8.3 — The Statement

*"Most teams are building better agents. IBA defines the rules they must
run under."* — Grok / xAI · April 24, 2026

*"World-class starting point. Building the Operating System that an
autonomous multi-agent society would require."* — Gemini · April 25, 2026

*"Valid working prototype of a critical component needed to claim it.
Moves the conversation from theoretical puzzle to engineered solution."*
— ChatGPT / OpenAI · April 25, 2026

---

## RATIFICATION

This Constitution is hereby ratified and entered into the IBA prior art
record on April 25, 2026.

**Jeffrey Williams**
Inventor · IBA Intent Bound Authorization
Chiang Mai, Thailand
IBA@intentbound.com · IntentBound.com

Patent GB2603013.0 · Filed February 10, 2026 · UK IPO
WIPO DAS C9A6 · PCT 150+ Countries · August 2028
IETF draft-williams-intent-token-00 · CONFIRMED LIVE

*This document is part of the IBA prior art record. Timestamped.
Witnessed. Immutable.*
