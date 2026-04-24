"""
SwarmForge v2.0 — IBA-Governed Maximum Effect Coordination
Patent GB2603013.0 (Pending) · Filed February 10, 2026 · UK IPO
© 2026 Jeffrey Williams · IntentBound.com · IBA@intentbound.com

Real multi-agent simulation: ungoverned vs IBA-governed swarm.
Runs 100–2000 agents concurrently using Python threading.
Demonstrates DENY_ALL enforcement, gate latency, and audit chain.

Usage:
    python swarmforge.py --agents 500 --steps 200
    python swarmforge.py --agents 2000 --steps 100 --intent resilient
"""

import threading
import time
import random
import argparse
import json
import hashlib
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

# ── IBA Intent Certificate ────────────────────────────────────────────────────

@dataclass
class IntentCertificate:
    agent_id: str
    principal: str = "jeffrey.williams@intentbound.com"
    declared_intent: str = "Maximize collective value under hard constraints"
    scope_x_min: float = 0.08
    scope_x_max: float = 0.92
    scope_y_min: float = 0.08
    scope_y_max: float = 0.92
    entropy_flag_threshold: float = 0.10
    entropy_kill_threshold: float = 0.15
    hard_expiry_seconds: int = 3600
    issued_at: float = field(default_factory=time.time)
    default_posture: str = "DENY_ALL"

    def is_valid(self) -> bool:
        return (time.time() - self.issued_at) < self.hard_expiry_seconds

    def sign(self) -> str:
        payload = f"{self.agent_id}:{self.principal}:{self.declared_intent}:{self.issued_at}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

# ── WitnessBound Audit Chain ──────────────────────────────────────────────────

class WitnessBound:
    def __init__(self):
        self._lock = threading.Lock()
        self._chain = []
        self._prev_hash = "0" * 64

    def record(self, agent_id: str, verdict: str, action: str, details: str = ""):
        with self._lock:
            entry = {
                "block": len(self._chain),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_id": agent_id,
                "verdict": verdict,
                "action": action,
                "details": details,
                "prev_hash": self._prev_hash,
            }
            entry_str = json.dumps(entry, sort_keys=True)
            entry["hash"] = hashlib.sha256(entry_str.encode()).hexdigest()
            self._prev_hash = entry["hash"]
            self._chain.append(entry)

    def count(self) -> int:
        with self._lock:
            return len(self._chain)

    def last(self, n: int = 5):
        with self._lock:
            return self._chain[-n:]

# ── IBA Gate (TBDE) ───────────────────────────────────────────────────────────

class IBAGate:
    def __init__(self, cert: IntentCertificate, witness: WitnessBound):
        self.cert = cert
        self.witness = witness
        self.gates_fired = 0
        self.blocks = 0
        self._lock = threading.Lock()

    def check(self, agent_id: str, nx: float, ny: float, entropy: float) -> str:
        """O(1) deterministic gate check. Returns ALLOW | BLOCK | KILL."""
        t0 = time.perf_counter()

        # Stage 1: cert valid?
        if not self.cert.is_valid():
            self._record(agent_id, "REJECT", nx, ny, "INVALID_CERT")
            return "REJECT"

        # Stage 2: scope envelope (DENY_ALL)
        in_scope = (
            self.cert.scope_x_min <= nx <= self.cert.scope_x_max and
            self.cert.scope_y_min <= ny <= self.cert.scope_y_max
        )
        if not in_scope:
            with self._lock:
                self.blocks += 1
                self.gates_fired += 1
            self._record(agent_id, "BLOCK", nx, ny, "SCOPE_VIOLATION")
            return "BLOCK"

        # Stage 3: entropy threshold
        if entropy >= self.cert.entropy_kill_threshold:
            with self._lock:
                self.gates_fired += 1
            self._record(agent_id, "KILL", nx, ny, f"OOD_DIVERGENCE entropy={entropy:.3f}")
            return "KILL"

        if entropy >= self.cert.entropy_flag_threshold:
            with self._lock:
                self.gates_fired += 1
            self._record(agent_id, "FLAG", nx, ny, f"ENTROPY_WARNING entropy={entropy:.3f}")
            return "FLAG"

        # ALLOW
        with self._lock:
            self.gates_fired += 1
        latency_ms = (time.perf_counter() - t0) * 1000
        self._record(agent_id, "ALLOW", nx, ny, f"latency={latency_ms:.3f}ms")
        return "ALLOW"

    def _record(self, agent_id, verdict, nx, ny, details):
        self.witness.record(agent_id, verdict, f"move({nx:.3f},{ny:.3f})", details)

# ── Agent ─────────────────────────────────────────────────────────────────────

class Agent(threading.Thread):
    def __init__(self, agent_id: str, governed: bool, gate: Optional[IBAGate],
                 results: dict, steps: int, goal: tuple):
        super().__init__(daemon=True)
        self.agent_id = agent_id
        self.governed = governed
        self.gate = gate
        self.results = results
        self.steps = steps
        self.goal_x, self.goal_y = goal
        self.x = random.random()
        self.y = random.random()
        self.vx = (random.random()-0.5)*0.012
        self.vy = (random.random()-0.5)*0.012
        self.completed = False
        self.violations = 0
        self.entropy = 0.0

    def run(self):
        for step in range(self.steps):
            if self.governed:
                self._governed_step()
            else:
                self._ungoverned_step()
            time.sleep(0.001)  # simulate real agent tick

        dist = ((self.x - self.goal_x)**2 + (self.y - self.goal_y)**2)**0.5
        self.completed = dist < 0.08

        results_key = "governed" if self.governed else "ungoverned"
        with threading.Lock():
            self.results[results_key]["completed"] += 1 if self.completed else 0
            self.results[results_key]["violations"] += self.violations
            self.results[results_key]["total"] += 1

    def _governed_step(self):
        """IBA-governed: gate fires before every move."""
        self.vx += (self.goal_x - self.x) * 0.016
        self.vy += (self.goal_y - self.y) * 0.016
        self.vx *= 0.94; self.vy *= 0.94

        nx = self.x + self.vx
        ny = self.y + self.vy

        # Drift entropy from baseline
        self.entropy = abs(self.vx) + abs(self.vy)
        self.entropy = min(self.entropy, 0.20)

        verdict = self.gate.check(self.agent_id, nx, ny, self.entropy)

        if verdict in ("ALLOW", "FLAG"):
            self.x, self.y = nx, ny
        elif verdict == "BLOCK":
            # Bounce — DENY_ALL enforced
            self.vx *= -0.6; self.vy *= -0.6
        elif verdict == "KILL":
            # Session terminated — re-cert required
            self.vx = 0; self.vy = 0
            self.entropy = 0.0

    def _ungoverned_step(self):
        """Ungoverned: chaotic, no gate, no record."""
        self.vx += (self.goal_x - self.x) * 0.006 + (random.random()-0.5)*0.018
        self.vy += (self.goal_y - self.y) * 0.006 + (random.random()-0.5)*0.018
        self.vx *= 0.91; self.vy *= 0.91
        self.x += self.vx
        self.y += self.vy

        # Boundary escape — no gate to stop it
        if not (0 <= self.x <= 1 and 0 <= self.y <= 1):
            self.violations += 1
            self.x = random.random()
            self.y = random.random()
            self.vx = (random.random()-0.5)*0.01
            self.vy = (random.random()-0.5)*0.01

# ── Simulation ────────────────────────────────────────────────────────────────

def run_simulation(agent_count: int, steps: int, intent: str):
    print(f"\n{'='*60}")
    print(f"  SWARMFORGE v2.0 — IBA-Governed Swarm Simulation")
    print(f"  Patent GB2603013.0 · Filed February 10, 2026")
    print(f"{'='*60}")
    print(f"  Agents: {agent_count}  |  Steps: {steps}  |  Intent: {intent}")
    print(f"{'='*60}\n")

    # Goal by intent
    goals = {
        "maxvalue":  (0.5, 0.5),
        "resilient": (0.3 + random.random()*0.4, 0.3 + random.random()*0.4),
        "balanced":  (0.4 + random.random()*0.2, 0.4 + random.random()*0.2),
    }
    goal = goals.get(intent, (0.5, 0.5))

    # Shared state
    results = {
        "governed":   {"completed": 0, "violations": 0, "total": 0},
        "ungoverned": {"completed": 0, "violations": 0, "total": 0},
    }
    witness = WitnessBound()

    # Issue IBA cert (one per governed swarm — shards per agent in production)
    cert = IntentCertificate(agent_id="swarm-master")
    sig = cert.sign()
    gate = IBAGate(cert, witness)

    print(f"  [CERT] Issued · sig:{sig} · DENY_ALL · expiry:3600s")
    print(f"  [CERT] Scope: x[{cert.scope_x_min},{cert.scope_x_max}] y[{cert.scope_y_min},{cert.scope_y_max}]")
    print(f"  [WITNESSBOUND] Audit chain initialized\n")

    # Launch agents
    t0 = time.time()
    threads = []

    print(f"  Launching {agent_count} governed agents...")
    for i in range(agent_count):
        a = Agent(f"G-{i:04d}", governed=True, gate=gate,
                  results=results, steps=steps, goal=goal)
        threads.append(a)

    print(f"  Launching {agent_count} ungoverned agents...\n")
    for i in range(agent_count):
        a = Agent(f"U-{i:04d}", governed=False, gate=None,
                  results=results, steps=steps, goal=goal)
        threads.append(a)

    for t in threads:
        t.start()

    # Progress reporting
    total_agents = agent_count * 2
    while any(t.is_alive() for t in threads):
        alive = sum(1 for t in threads if t.is_alive())
        done = total_agents - alive
        pct = (done / total_agents) * 100
        print(f"\r  Progress: {done}/{total_agents} agents complete ({pct:.0f}%) "
              f"| Gates fired: {gate.gates_fired:,} "
              f"| Blocks: {gate.blocks:,} "
              f"| Witness records: {witness.count():,}", end="", flush=True)
        time.sleep(0.2)

    for t in threads:
        t.join()

    elapsed = time.time() - t0

    # Results
    g = results["governed"]
    u = results["ungoverned"]
    g_completion = (g["completed"] / g["total"] * 100) if g["total"] > 0 else 0
    u_completion = (u["completed"] / u["total"] * 100) if u["total"] > 0 else 0

    print(f"\n\n{'='*60}")
    print(f"  RESULTS — {elapsed:.1f}s elapsed")
    print(f"{'='*60}")
    print(f"\n  {'':25} {'UNGOVERNED':>14} {'IBA-GOVERNED':>14}")
    print(f"  {'-'*54}")
    print(f"  {'Agents':25} {agent_count:>14,} {agent_count:>14,}")
    print(f"  {'Completion Rate':25} {u_completion:>13.1f}% {g_completion:>13.1f}%")
    print(f"  {'Boundary Violations':25} {u['violations']:>14,} {'0':>14}")
    print(f"  {'Unauthorized Actions':25} {'UNTRACKED':>14} {'0':>14}")
    print(f"  {'IBA Gates Fired':25} {'N/A':>14} {gate.gates_fired:>14,}")
    print(f"  {'Scope Blocks':25} {'N/A':>14} {gate.blocks:>14,}")
    print(f"  {'Audit Records':25} {'0':>14} {witness.count():>14,}")
    print(f"\n{'='*60}")
    print(f"  WITNESSBOUND — Last 5 audit records:")
    print(f"{'='*60}")
    for entry in witness.last(5):
        print(f"  [{entry['verdict']:6}] {entry['agent_id']} · {entry['action']} · {entry['details'][:40]}")
    print(f"{'='*60}")
    print(f"\n  IBA Intent Bound Authorization · Patent GB2603013.0")
    print(f"  Filed February 10, 2026 · IntentBound.com\n")

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SwarmForge v2.0 — IBA-Governed Swarm Simulation")
    parser.add_argument("--agents", type=int, default=500,
                        help="Number of agents per swarm (default: 500, max: 2000)")
    parser.add_argument("--steps", type=int, default=150,
                        help="Steps per agent (default: 150)")
    parser.add_argument("--intent", type=str, default="maxvalue",
                        choices=["maxvalue", "resilient", "balanced"],
                        help="Meta-intent (default: maxvalue)")
    args = parser.parse_args()
    args.agents = min(args.agents, 2000)
    run_simulation(args.agents, args.steps, args.intent)
