"""
Intent Ledger v1.0
IBA Intent Bound Authorization · SwarmForge IGCP Layer

Patent GB2603013.0 (Pending) · Filed February 10, 2026
© 2026 Jeffrey Williams · IntentBound.com

ChatGPT (OpenAI) · April 25, 2026:
"Intents must become first-class system objects. Every action resolves
through an intent. Stored in an append-only intent log. This is what
separates a coordination substrate from an execution engine."

The Intent Ledger is the state layer of the IGCP stack:
  IBA Gate          → permission layer
  Intent Ledger     → state layer       ← THIS FILE
  Conflict Engine   → arbitration layer
  Market Layer      → optimization layer
  WitnessBound      → audit layer

Every intent is:
  - Cryptographically signed by a principal
  - Staked with a confidence value
  - Prioritized in the hierarchy (L0–L4)
  - Append-only once committed
  - Immutable once witnessed

Usage:
    from intent_ledger import IntentLedger, IntentObject, StakedIntent
"""

import hashlib
import json
import time
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from enum import IntEnum


# ── Intent Priority Levels (Constitution Article II) ──────────────────────────

class Priority(IntEnum):
    """
    Intent hierarchy — Constitution Article II, Section 2.1.
    Higher priority supersedes lower in all conflict cases.
    """
    SYSTEM      = 0   # L0 — Constitutional bounds, cannot be overridden
    PRINCIPAL   = 1   # L1 — Human principal, signed mandate
    SWARM       = 2   # L2 — Collective swarm goal
    AGENT       = 3   # L3 — Individual agent task
    ACTION      = 4   # L4 — Single atomic action


# ── Intent Resolution Status ──────────────────────────────────────────────────

class IntentStatus:
    PENDING    = "PENDING"     # Submitted, awaiting conflict check
    ACTIVE     = "ACTIVE"      # Executing
    SATISFIED  = "SATISFIED"   # Goal achieved
    BLOCKED    = "BLOCKED"     # Blocked by higher-priority intent
    EXPIRED    = "EXPIRED"     # Hard expiry reached
    WITHDRAWN  = "WITHDRAWN"   # Principal revoked
    SLASHED    = "SLASHED"     # Failed delivery — stake penalized


# ── Core Intent Object ────────────────────────────────────────────────────────

@dataclass
class IntentObject:
    """
    First-class intent object — every action resolves through this.

    ChatGPT architecture:
    intent = {
        actor, goal, constraints, stake, priority, signature
    }

    Extended with IBA fields:
    scope_envelope, entropy_threshold, hard_expiry, witness_chain
    """
    # Identity
    intent_id:    str
    actor:        str                    # agent_id or principal
    principal:    str                    # authorizing human identity

    # Declared goal
    goal:         str                    # natural language + machine-readable
    goal_hash:    str = ""               # SHA3-256 of tokenized goal embedding

    # Constraints (IBA scope_envelope)
    constraints:  Dict[str, Any] = field(default_factory=dict)
    permissions:  List[str] = field(default_factory=list)
    denied:       List[str] = field(default_factory=list)
    default_posture: str = "DENY_ALL"

    # Economics
    stake:        float = 1.0           # confidence stake — slashed on failure
    priority:     Priority = Priority.AGENT
    budget:       float = 100.0

    # Temporal
    issued_at:    float = field(default_factory=time.time)
    hard_expiry:  float = field(default_factory=lambda: time.time() + 3600)
    hw_enforced:  bool = True

    # Cryptographic
    signature:    str = ""              # ECDSA-P384 (simulated as SHA-256)
    witness_chain: str = ""             # witnessbound://intent-{id}

    # State
    status:       str = IntentStatus.PENDING
    parent_intent: Optional[str] = None  # for sub-intents
    children:     List[str] = field(default_factory=list)

    # Outcomes
    satisfaction_score: float = 0.0
    stake_remaining:    float = 0.0     # updated on slash

    def __post_init__(self):
        if not self.goal_hash:
            self.goal_hash = hashlib.sha3_256(
                self.goal.encode()
            ).hexdigest()[:32]
        if not self.signature:
            self.signature = self._sign()
        if not self.witness_chain:
            self.witness_chain = f"witnessbound://intent-{self.intent_id}"
        self.stake_remaining = self.stake

    def _sign(self) -> str:
        """Simulate ECDSA-P384 signature over full payload."""
        payload = (f"{self.intent_id}:{self.actor}:{self.principal}:"
                   f"{self.goal_hash}:{self.stake}:{self.priority}:"
                   f"{self.issued_at}")
        return hashlib.sha256(payload.encode()).hexdigest()[:24]

    def is_valid(self) -> bool:
        return (time.time() < self.hard_expiry and
                self.status not in (IntentStatus.EXPIRED,
                                    IntentStatus.WITHDRAWN,
                                    IntentStatus.SLASHED))

    def is_expired(self) -> bool:
        return time.time() >= self.hard_expiry

    def authorize(self, action: str, value: float = 0.0) -> bool:
        """
        IBA authorization check against this intent.
        action must be in permissions AND within constraints.
        """
        if not self.is_valid():
            return False
        if action in self.denied:
            return False
        if self.permissions and action not in self.permissions:
            return False
        if value > self.budget:
            return False
        return True

    def to_dict(self) -> Dict:
        return {
            "intent_id":    self.intent_id,
            "actor":        self.actor,
            "principal":    self.principal,
            "goal":         self.goal,
            "goal_hash":    self.goal_hash,
            "constraints":  self.constraints,
            "permissions":  self.permissions,
            "stake":        self.stake,
            "priority":     int(self.priority),
            "budget":       self.budget,
            "issued_at":    self.issued_at,
            "hard_expiry":  self.hard_expiry,
            "signature":    self.signature,
            "status":       self.status,
            "stake_remaining": self.stake_remaining,
        }


@dataclass
class StakedIntent:
    """
    Intent with economic stake — used in market bidding.
    Stake is slashed on failed delivery.
    Stake grows via reputation on success.
    """
    intent:       IntentObject
    staker:       str                   # agent_id placing stake
    stake_amount: float = 1.0
    confidence:   float = 0.5          # 0.0–1.0
    bid_price:    float = 0.0
    committed_at: float = field(default_factory=time.time)
    settled:      bool = False
    outcome:      Optional[bool] = None # True=success, False=failure

    def effective_stake(self) -> float:
        """Stake weighted by confidence and priority."""
        priority_multiplier = {
            Priority.SYSTEM:    5.0,
            Priority.PRINCIPAL: 3.0,
            Priority.SWARM:     2.0,
            Priority.AGENT:     1.0,
            Priority.ACTION:    0.5,
        }.get(self.intent.priority, 1.0)
        return self.stake_amount * self.confidence * priority_multiplier

    def slash(self, fraction: float = 0.5) -> float:
        """Slash stake on failure — return amount slashed."""
        slashed = self.stake_amount * fraction
        self.stake_amount = max(0, self.stake_amount - slashed)
        self.intent.stake_remaining = max(
            0, self.intent.stake_remaining - slashed)
        self.intent.status = IntentStatus.SLASHED
        return slashed

    def reward(self, multiplier: float = 1.2) -> float:
        """Reward stake on success."""
        gain = self.stake_amount * (multiplier - 1.0)
        self.stake_amount += gain
        self.intent.stake_remaining = self.stake_amount
        self.intent.status = IntentStatus.SATISFIED
        return gain


# ── Append-Only Intent Ledger ─────────────────────────────────────────────────

class IntentLedger:
    """
    Append-only log of all intents — the state layer of IGCP.

    Properties:
    - Every intent is immutable once committed
    - Intents are indexed by actor, priority, status, and goal_hash
    - The ledger produces a cryptographic root hash (like a Merkle root)
    - Conflict detection is O(log n) via priority index
    - All mutations are thread-safe

    This is the WitnessBound for intent state — not just gate decisions,
    but the full lifecycle of every declared goal in the system.
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._ledger: List[Dict] = []           # append-only
        self._index: Dict[str, IntentObject] = {}  # intent_id → intent
        self._by_actor: Dict[str, List[str]] = {}  # actor → [intent_ids]
        self._by_priority: Dict[int, List[str]] = {
            p: [] for p in range(5)
        }
        self._by_status: Dict[str, List[str]] = {
            s: [] for s in [
                IntentStatus.PENDING, IntentStatus.ACTIVE,
                IntentStatus.SATISFIED, IntentStatus.BLOCKED,
                IntentStatus.EXPIRED, IntentStatus.WITHDRAWN,
                IntentStatus.SLASHED,
            ]
        }
        self._staked: Dict[str, StakedIntent] = {}  # intent_id → staked
        self._root_hash = "0" * 64
        self._prev_hash = "0" * 64
        self.total_committed = 0
        self.total_slashed = 0
        self.total_satisfied = 0
        self.total_stake_value = 0.0

    # ── Commit ────────────────────────────────────────────────────────────────

    def commit(self, intent: IntentObject,
               stake: Optional[StakedIntent] = None) -> str:
        """
        Commit an intent to the ledger.
        Immutable once committed — append only.
        Returns the ledger entry hash.
        """
        with self._lock:
            if intent.intent_id in self._index:
                raise ValueError(
                    f"Intent {intent.intent_id} already committed — "
                    f"ledger is append-only"
                )

            # Build ledger entry
            entry = {
                "seq":        len(self._ledger),
                "timestamp":  datetime.now(timezone.utc).isoformat(),
                "intent":     intent.to_dict(),
                "stake":      stake.stake_amount if stake else 0.0,
                "confidence": stake.confidence if stake else 0.0,
                "prev_hash":  self._prev_hash,
            }
            entry_hash = hashlib.sha256(
                json.dumps(entry, sort_keys=True).encode()
            ).hexdigest()
            entry["hash"] = entry_hash

            # Append — never modify
            self._ledger.append(entry)
            self._index[intent.intent_id] = intent
            self._prev_hash = entry_hash
            self._update_root_hash()

            # Index
            actor = intent.actor
            if actor not in self._by_actor:
                self._by_actor[actor] = []
            self._by_actor[actor].append(intent.intent_id)
            self._by_priority[int(intent.priority)].append(intent.intent_id)
            self._by_status[IntentStatus.PENDING].append(intent.intent_id)

            if stake:
                self._staked[intent.intent_id] = stake
                self.total_stake_value += stake.stake_amount

            self.total_committed += 1
            return entry_hash

    def _update_root_hash(self):
        """Merkle-style root hash over all entry hashes."""
        all_hashes = [e["hash"] for e in self._ledger]
        combined = "|".join(all_hashes)
        self._root_hash = hashlib.sha256(combined.encode()).hexdigest()

    # ── State Transitions ─────────────────────────────────────────────────────

    def activate(self, intent_id: str) -> bool:
        """Transition intent from PENDING → ACTIVE."""
        with self._lock:
            intent = self._index.get(intent_id)
            if not intent or intent.status != IntentStatus.PENDING:
                return False
            self._transition(intent, IntentStatus.ACTIVE)
            return True

    def satisfy(self, intent_id: str,
                score: float = 1.0) -> Optional[float]:
        """
        Mark intent as satisfied.
        Reward stake. Return reward amount.
        """
        with self._lock:
            intent = self._index.get(intent_id)
            if not intent:
                return None
            intent.satisfaction_score = score
            self._transition(intent, IntentStatus.SATISFIED)
            self.total_satisfied += 1

            stake = self._staked.get(intent_id)
            if stake:
                reward = stake.reward(multiplier=1.0 + score * 0.3)
                return reward
            return 0.0

    def slash(self, intent_id: str,
              fraction: float = 0.5) -> Optional[float]:
        """
        Slash stake on failed delivery.
        Return amount slashed.
        """
        with self._lock:
            intent = self._index.get(intent_id)
            if not intent:
                return None
            self._transition(intent, IntentStatus.SLASHED)
            self.total_slashed += 1

            stake = self._staked.get(intent_id)
            if stake:
                slashed = stake.slash(fraction)
                self.total_stake_value = max(
                    0, self.total_stake_value - slashed)
                return slashed
            return 0.0

    def expire_stale(self) -> int:
        """Sweep expired intents — call periodically."""
        with self._lock:
            expired = 0
            for iid, intent in list(self._index.items()):
                if (intent.status == IntentStatus.ACTIVE and
                        intent.is_expired()):
                    self._transition(intent, IntentStatus.EXPIRED)
                    expired += 1
            return expired

    def withdraw(self, intent_id: str, principal: str) -> bool:
        """Principal revokes an intent — returns True if authorized."""
        with self._lock:
            intent = self._index.get(intent_id)
            if not intent:
                return False
            if intent.principal != principal:
                return False  # only principal can withdraw
            self._transition(intent, IntentStatus.WITHDRAWN)
            return True

    def _transition(self, intent: IntentObject, new_status: str):
        """Thread-safe status transition with index update."""
        old = intent.status
        if old in self._by_status and intent.intent_id in self._by_status[old]:
            self._by_status[old].remove(intent.intent_id)
        intent.status = new_status
        if new_status not in self._by_status:
            self._by_status[new_status] = []
        self._by_status[new_status].append(intent.intent_id)

    # ── Query ─────────────────────────────────────────────────────────────────

    def get(self, intent_id: str) -> Optional[IntentObject]:
        with self._lock:
            return self._index.get(intent_id)

    def get_by_actor(self, actor: str) -> List[IntentObject]:
        with self._lock:
            ids = self._by_actor.get(actor, [])
            return [self._index[i] for i in ids if i in self._index]

    def get_active(self, priority: Optional[Priority] = None
                   ) -> List[IntentObject]:
        with self._lock:
            active_ids = self._by_status.get(IntentStatus.ACTIVE, [])
            intents = [self._index[i] for i in active_ids
                       if i in self._index]
            if priority is not None:
                intents = [i for i in intents if i.priority == priority]
            return sorted(intents, key=lambda x: int(x.priority))

    def get_pending(self) -> List[IntentObject]:
        with self._lock:
            ids = self._by_status.get(IntentStatus.PENDING, [])
            return [self._index[i] for i in ids if i in self._index]

    def get_stake(self, intent_id: str) -> Optional[StakedIntent]:
        with self._lock:
            return self._staked.get(intent_id)

    def verify(self) -> bool:
        """Verify append-only integrity — no entries modified."""
        with self._lock:
            prev = "0" * 64
            for entry in self._ledger:
                if entry["prev_hash"] != prev:
                    return False
                # Recompute hash
                check_entry = {k: v for k, v in entry.items()
                               if k != "hash"}
                expected = hashlib.sha256(
                    json.dumps(check_entry, sort_keys=True).encode()
                ).hexdigest()
                if expected != entry["hash"]:
                    return False
                prev = entry["hash"]
            return True

    # ── Analytics ─────────────────────────────────────────────────────────────

    def stats(self) -> Dict:
        with self._lock:
            return {
                "total_committed":  self.total_committed,
                "total_satisfied":  self.total_satisfied,
                "total_slashed":    self.total_slashed,
                "total_stake":      round(self.total_stake_value, 2),
                "pending":          len(self._by_status.get(
                                        IntentStatus.PENDING, [])),
                "active":           len(self._by_status.get(
                                        IntentStatus.ACTIVE, [])),
                "satisfied":        len(self._by_status.get(
                                        IntentStatus.SATISFIED, [])),
                "slashed":          len(self._by_status.get(
                                        IntentStatus.SLASHED, [])),
                "root_hash":        self._root_hash[:16] + "...",
                "ledger_size":      len(self._ledger),
                "integrity":        self.verify(),
                "satisfaction_rate": (
                    self.total_satisfied /
                    max(self.total_committed, 1) * 100
                ),
            }

    def intent_flow(self) -> Dict[str, int]:
        """Sankey-style flow counts for visualization."""
        with self._lock:
            return {s: len(ids) for s, ids in self._by_status.items()}

    def top_stakers(self, n: int = 5) -> List[Tuple[str, float]]:
        """Agents ranked by effective stake."""
        with self._lock:
            scored = [
                (si.staker, si.effective_stake())
                for si in self._staked.values()
            ]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:n]


# ── Factory helpers ───────────────────────────────────────────────────────────

def make_intent(intent_id: str, actor: str, principal: str,
                goal: str, priority: Priority = Priority.AGENT,
                stake: float = 1.0, budget: float = 100.0,
                permissions: Optional[List[str]] = None,
                constraints: Optional[Dict] = None,
                expiry_seconds: int = 3600) -> IntentObject:
    """Create a fully-formed intent object."""
    return IntentObject(
        intent_id=intent_id,
        actor=actor,
        principal=principal,
        goal=goal,
        priority=priority,
        stake=stake,
        budget=budget,
        permissions=permissions or ["move", "bid", "report"],
        constraints=constraints or {},
        hard_expiry=time.time() + expiry_seconds,
    )


def make_staked(intent: IntentObject, staker: str,
                stake_amount: float, confidence: float,
                bid_price: float = 0.0) -> StakedIntent:
    """Create a staked intent for market bidding."""
    return StakedIntent(
        intent=intent,
        staker=staker,
        stake_amount=stake_amount,
        confidence=confidence,
        bid_price=bid_price,
    )


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import random

    print("\n" + "="*60)
    print("  INTENT LEDGER v1.0 — Self Test")
    print("  IBA Intent Bound Authorization")
    print("  Patent GB2603013.0 · Filed February 10, 2026")
    print("="*60 + "\n")

    ledger = IntentLedger()

    # Commit a principal-level intent
    principal_intent = make_intent(
        intent_id="igcp-principal-001",
        actor="principal",
        principal="jeffrey.williams@intentbound.com",
        goal="Launch governed autonomous startup swarm",
        priority=Priority.PRINCIPAL,
        stake=10.0,
        budget=1000.0,
        permissions=["spawn", "bid", "coordinate", "deploy", "report"],
        constraints={"budget": 1000, "time": "1hr", "risk": "low"},
    )
    h = ledger.commit(principal_intent)
    ledger.activate("igcp-principal-001")
    print(f"  [L1 PRINCIPAL] Committed · sig:{principal_intent.signature}")

    # Commit 10 agent-level intents with stakes
    agents = []
    for i in range(10):
        intent = make_intent(
            intent_id=f"igcp-agent-{i:03d}",
            actor=f"agent-{i:03d}",
            principal="jeffrey.williams@intentbound.com",
            goal=f"Execute subtask for startup launch — agent {i}",
            priority=Priority.AGENT,
            stake=random.uniform(0.5, 3.0),
            budget=random.uniform(20, 80),
            permissions=["move", "bid", "report", "generate_content"],
        )
        staked = make_staked(
            intent=intent,
            staker=f"agent-{i:03d}",
            stake_amount=intent.stake,
            confidence=random.uniform(0.4, 0.9),
            bid_price=random.uniform(10, 50),
        )
        ledger.commit(intent, staked)
        ledger.activate(f"igcp-agent-{i:03d}")
        agents.append(intent)

    print(f"  [L3 AGENTS]    10 agents committed with stakes")

    # Simulate outcomes
    satisfied = 0
    slashed = 0
    for i, intent in enumerate(agents):
        if random.random() > 0.3:
            reward = ledger.satisfy(intent.intent_id,
                                    score=random.uniform(0.6, 1.0))
            satisfied += 1
        else:
            amount = ledger.slash(intent.intent_id, fraction=0.4)
            slashed += 1

    print(f"  [OUTCOMES]     {satisfied} satisfied · {slashed} slashed")

    # Verify integrity
    print(f"\n  [INTEGRITY]    Ledger verified: {ledger.verify()}")

    # Stats
    s = ledger.stats()
    print(f"\n  LEDGER STATS:")
    print(f"  {'Total Committed':<25} {s['total_committed']}")
    print(f"  {'Satisfied':<25} {s['satisfied']}")
    print(f"  {'Slashed':<25} {s['slashed']}")
    print(f"  {'Satisfaction Rate':<25} {s['satisfaction_rate']:.1f}%")
    print(f"  {'Total Stake Value':<25} ${s['total_stake']:.2f}")
    print(f"  {'Ledger Size':<25} {s['ledger_size']} entries")
    print(f"  {'Root Hash':<25} {s['root_hash']}")
    print(f"  {'Integrity':<25} {'✓ VERIFIED' if s['integrity'] else '✗ FAIL'}")

    print(f"\n  TOP STAKERS:")
    for staker, eff_stake in ledger.top_stakers(5):
        print(f"  {staker:<20} effective stake: {eff_stake:.3f}")

    print(f"\n  INTENT FLOW:")
    for status, count in ledger.intent_flow().items():
        if count > 0:
            bar = "█" * count
            print(f"  {status:<12} {count:>3} {bar}")

    print(f"\n  ✓ Intent Ledger v1.0 operational")
    print(f"  Patent GB2603013.0 · IntentBound.com\n")
