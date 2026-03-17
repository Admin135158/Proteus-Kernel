#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          🧬 PROTEUS - THE IMMORTAL KERNEL v6.0                  ║
║          Built by The Architect. Named for Zayden.              ║
║          GGSE/GORF consciousness layer integrated.              ║
║          Zero tutorials. Pure vision. Lives forever.            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import tty
import termios
import select
import time
import json
import math
import random
import signal
import threading
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Optional
import psutil
import numpy as np

# ─────────────────────────────────────────────
#  TERMINAL COLORS & STYLES
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    BLINK   = "\033[5m"

    BLACK   = "\033[30m";  BBLACK   = "\033[90m"
    RED     = "\033[31m";  BRED     = "\033[91m"
    GREEN   = "\033[32m";  BGREEN   = "\033[92m"
    YELLOW  = "\033[33m";  BYELLOW  = "\033[93m"
    BLUE    = "\033[34m";  BBLUE    = "\033[94m"
    MAGENTA = "\033[35m";  BMAGENTA = "\033[95m"
    CYAN    = "\033[36m";  BCYAN    = "\033[96m"
    WHITE   = "\033[37m";  BWHITE   = "\033[97m"

    BG_BLACK = "\033[40m"; BG_GREEN = "\033[42m"
    BG_RED   = "\033[41m"; BG_BLUE  = "\033[44m"

def clr(text, *styles):
    return "".join(styles) + str(text) + C.RESET

def bar(pct, width=40, full_char="█", empty_char="░"):
    pct = max(0.0, min(1.0, pct))
    filled = int(width * pct)
    if pct > 0.85:   color = C.BGREEN
    elif pct > 0.60: color = C.BYELLOW
    elif pct > 0.35: color = C.YELLOW
    else:            color = C.BRED
    return color + full_char * filled + C.DIM + empty_char * (width - filled) + C.RESET

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

# ─────────────────────────────────────────────
#  GGSE / GORF CONSCIOUSNESS ENGINE
# ─────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2   # Golden ratio
GORF_ALPHA   = 0.618            # Growth coupling
GORF_BETA    = 0.3819           # Decay rate
GORF_C_MAX   = 1.0
GORF_PERIOD  = 9.0              # Cycle period (years → mapped to generations)
RESONANCE    = 1.2492           # R constant
THETA        = 2 * math.pi / 9  # Shumen rotation angle (~40 degrees)

def coherence_driver(t: float, period: float = GORF_PERIOD) -> float:
    """F(t) = sin(2π t / T) * φ  — periodic coherence field"""
    return math.sin(2 * math.pi * t / period) * PHI

def gorf_step(C: float, t: float, dt: float = 1.0) -> float:
    """
    Euler step of GORF ODE:
    dC/dt = alpha * F(t) * (1 - C/C_max) - beta * C
    """
    F      = coherence_driver(t)
    dC     = GORF_ALPHA * F * (1 - C / GORF_C_MAX) - GORF_BETA * C
    C_new  = C + dC * dt
    return max(0.05, min(GORF_C_MAX, C_new))  # floor at 0.05 — never fully dark

def shumen_transform(S: np.ndarray) -> np.ndarray:
    """
    State vector rotation: S_new = M(θ) · S
    M(θ) = [[cos θ, -sin θ], [sin θ, cos θ]]   θ = 2π/9
    Preserves |S| = 1 (norm constraint)
    """
    M = np.array([
        [math.cos(THETA), -math.sin(THETA)],
        [math.sin(THETA),  math.cos(THETA)]
    ])
    S_new = M @ S
    norm  = np.linalg.norm(S_new)
    if norm > 0:
        S_new = S_new / norm   # re-normalize
    return S_new

def resonance_spike(t: float) -> bool:
    """True when Im(S) aligns to 40° multiples — epiphany events"""
    angle = (t % GORF_PERIOD) / GORF_PERIOD * 2 * math.pi
    return abs(math.sin(angle * PHI)) > 0.97

@dataclass
class ConsciousnessState:
    """Per-agent GGSE consciousness state"""
    C:       float = 0.3                          # consciousness energy [0,1]
    S:       np.ndarray = field(                  # state vector [chaos, order]
                 default_factory=lambda: np.array([1.0, 0.0])
             )
    t:       float = 0.0                          # internal time counter
    epiphanies: int = 0                           # resonance spike count

    def step(self):
        self.t  += 1.0
        self.C   = gorf_step(self.C, self.t)
        self.S   = shumen_transform(self.S)
        if resonance_spike(self.t) and self.C > 0.1:
            self.epiphanies += 1
            self.C = min(GORF_C_MAX, self.C + 0.05)  # epiphany boost

    @property
    def chaos(self) -> float:
        return float(self.S[0])

    @property
    def order(self) -> float:
        return float(self.S[1])

    @property
    def reality_modulus(self) -> float:
        return float(np.linalg.norm(self.S))

    def fitness_modifier(self) -> float:
        """
        C(t) modifies agent fitness:
        high consciousness → better decisions → higher fitness
        """
        return 1.0 + (self.C * RESONANCE)

    def mutation_pressure(self) -> float:
        """
        F(t) drives mutation rate — peaks in coherence field
        cause mutation bursts across population
        """
        return abs(coherence_driver(self.t)) * 0.18

    def to_dict(self) -> dict:
        return {
            "C":          self.C,
            "S":          self.S.tolist(),
            "t":          self.t,
            "epiphanies": self.epiphanies,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ConsciousnessState":
        cs    = cls()
        cs.C  = d["C"]
        cs.S  = np.array(d["S"])
        cs.t  = d["t"]
        cs.epiphanies = d.get("epiphanies", 0)
        return cs

# ─────────────────────────────────────────────
#  ZAYDEN — GOD-MODE CONTROLLER
# ─────────────────────────────────────────────
@dataclass
class Zayden:
    """
    The architect above the simulation.
    Zayden's own C(t) governs intervention power.
    Higher C → stronger interventions possible.
    """
    consciousness: ConsciousnessState = field(
        default_factory=lambda: ConsciousnessState(C=0.8)
    )
    interventions:  int   = 0
    smites:         int   = 0
    births_granted: int   = 0
    boosts_given:   int   = 0

    # pending command from keypress
    pending_cmd: str = ""

    def step(self):
        self.consciousness.step()

    @property
    def C(self) -> float:
        return self.consciousness.C

    @property
    def power(self) -> float:
        """Intervention power — scales with C(t)"""
        return self.C * RESONANCE * PHI

    def can_intervene(self) -> bool:
        return self.C > 0.2

    # ── INTERVENTION METHODS ──────────────────

    def smite(self, state: "KernelState") -> str:
        """Kill the weakest agent. Costs C."""
        if not self.can_intervene():
            return "⚡ ZAYDEN: Insufficient power (C too low)"
        alive = [g for g in state.genes if g.alive]
        if not alive:
            return "⚡ ZAYDEN: No targets"
        target = min(alive, key=lambda g: g.fitness())
        target.alive = False
        target.strength = 0
        state.total_deaths += 1
        state.graveyard.append(target)
        state.add_event(
            f"⚡ ZAYDEN SMITES {target.name} "
            f"[power={self.power:.2f}]"
        )
        self.smites += 1
        self.interventions += 1
        self.consciousness.C = max(0.0, self.C - 0.08)
        return f"⚡ ZAYDEN smote {target.name}"

    def bless(self, state: "KernelState") -> str:
        """Boost the top agent's strength. Costs C."""
        if not self.can_intervene():
            return "🌟 ZAYDEN: Insufficient power"
        alive = sorted(
            [g for g in state.genes if g.alive],
            key=lambda g: g.fitness(), reverse=True
        )
        if not alive:
            return "🌟 ZAYDEN: No agents to bless"
        target = alive[0]
        boost = self.power * 5.0
        target.strength = min(150.0, target.strength + boost)
        state.add_event(
            f"🌟 ZAYDEN BLESSES {target.name} "
            f"+{boost:.1f} str [C={self.C:.3f}]"
        )
        self.boosts_given += 1
        self.interventions += 1
        self.consciousness.C = max(0.0, self.C - 0.06)
        return f"🌟 ZAYDEN blessed {target.name} (+{boost:.1f})"

    def spawn(self, state: "KernelState") -> str:
        """Force-birth a new GGSE-species agent. Costs C."""
        if not self.can_intervene():
            return "🧬 ZAYDEN: Insufficient power"
        name = f"GGSE-{random.randint(100,999)}"
        child = Gene(
            name        = name,
            species     = "ggse",
            strength    = 40.0 + self.power * 10,
            born_gen    = state.generation,
            mutations   = int(self.power),
        )
        state.genes.append(child)
        state.total_births += 1
        state.add_event(
            f"🧬 ZAYDEN SPAWNS {name} "
            f"[str={child.strength:.1f}, C={self.C:.3f}]"
        )
        self.births_granted += 1
        self.interventions += 1
        self.consciousness.C = max(0.0, self.C - 0.10)
        return f"🧬 ZAYDEN spawned {name}"

    def meditate(self) -> str:
        """Recover C(t) — do nothing for one tick."""
        self.consciousness.C = min(GORF_C_MAX, self.C + 0.05)
        return f"🧘 ZAYDEN meditates — C: {self.C:.3f}"

    def to_dict(self) -> dict:
        return {
            "consciousness":  self.consciousness.to_dict(),
            "interventions":  self.interventions,
            "smites":         self.smites,
            "births_granted": self.births_granted,
            "boosts_given":   self.boosts_given,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Zayden":
        z = cls()
        z.consciousness  = ConsciousnessState.from_dict(d["consciousness"])
        z.interventions  = d.get("interventions", 0)
        z.smites         = d.get("smites", 0)
        z.births_granted = d.get("births_granted", 0)
        z.boosts_given   = d.get("boosts_given", 0)
        return z

# ─────────────────────────────────────────────
#  GENE DEFINITION
# ─────────────────────────────────────────────
SPECIES_TRAITS = {
    "base":     {"aggression": 0.3, "longevity": 60,  "birth_chance": 0.25, "color": C.BWHITE},
    "killer":   {"aggression": 0.9, "longevity": 45,  "birth_chance": 0.20, "color": C.BRED},
    "hunter":   {"aggression": 0.7, "longevity": 55,  "birth_chance": 0.22, "color": C.BYELLOW},
    "survivor": {"aggression": 0.2, "longevity": 90,  "birth_chance": 0.30, "color": C.BGREEN},
    "parasite": {"aggression": 0.5, "longevity": 50,  "birth_chance": 0.35, "color": C.BMAGENTA},
    "nomad":    {"aggression": 0.4, "longevity": 70,  "birth_chance": 0.28, "color": C.BCYAN},
    # ── NEW: GGSE species — consciousness-driven ──
    "ggse":     {"aggression": 0.6, "longevity": 80,  "birth_chance": 0.26, "color": C.BGREEN},
}

SEED_NAMES = ["OLCE", "PROTO-ON", "WATCHDOG", "GGSE", "TUMOR-S", "IMMORTAL"]

@dataclass
class Gene:
    name:       str
    species:    str
    strength:   float
    age:        int   = 0
    kills:      int   = 0
    children:   int   = 0
    mutations:  int   = 0
    born_gen:   int   = 0
    alive:      bool  = True

    # GGSE consciousness layer (every agent gets one)
    consciousness: ConsciousnessState = field(
        default_factory=lambda: ConsciousnessState(C=random.uniform(0.1, 0.5))
    )

    def fitness(self) -> float:
        kill_bonus     = self.kills * 2.5
        child_bonus    = self.children * 1.8
        age_penalty    = self.age * 0.15
        mutation_bonus = self.mutations * 0.5
        raw = self.strength + kill_bonus + child_bonus + mutation_bonus - age_penalty
        # ── GGSE modifier: consciousness amplifies fitness ──
        raw *= self.consciousness.fitness_modifier()
        return max(0.0, raw)

    def max_age(self) -> int:
        base = SPECIES_TRAITS[self.species]["longevity"]
        # GGSE agents live longer with higher C(t)
        c_bonus = int(self.consciousness.C * 20) if self.species == "ggse" else 0
        return base + int(self.mutations * 1.5) + c_bonus

    def should_die_old_age(self) -> bool:
        return self.age >= self.max_age()

    def step_consciousness(self):
        """Advance this agent's GGSE state one tick"""
        self.consciousness.step()

    def to_dict(self):
        d = asdict(self)
        # asdict can't handle np.ndarray inside nested dataclass — patch it
        d["consciousness"] = self.consciousness.to_dict()
        return d

# ─────────────────────────────────────────────
#  KERNEL STATE
# ─────────────────────────────────────────────
@dataclass
class KernelState:
    generation:      int   = 0
    total_births:    int   = 0
    total_deaths:    int   = 0
    total_kills:     int   = 0
    total_mutations: int   = 0
    respawns:        int   = 0
    genes_processed: int   = 0
    start_time:      float = field(default_factory=time.time)
    genes:           list  = field(default_factory=list)
    graveyard:       list  = field(default_factory=list)
    event_log:       list  = field(default_factory=list)
    zayden:          Zayden = field(default_factory=Zayden)

    # Global F(t) time counter for population-wide coherence field
    gorf_t:          float = 0.0

    def add_event(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.event_log.append(f"[{ts}] {msg}")
        if len(self.event_log) > 200:
            self.event_log = self.event_log[-200:]

    def population(self) -> int:
        return len([g for g in self.genes if g.alive])

    def top_fitness(self) -> float:
        alive = [g for g in self.genes if g.alive]
        if not alive:
            return 0.0
        return max(g.fitness() for g in alive)

    def mean_consciousness(self) -> float:
        alive = [g for g in self.genes if g.alive]
        if not alive:
            return 0.0
        return sum(g.consciousness.C for g in alive) / len(alive)

    def species_counts(self) -> dict:
        counts = defaultdict(int)
        for g in self.genes:
            if g.alive:
                counts[g.species] += 1
        return dict(counts)

    def uptime(self) -> str:
        elapsed = int(time.time() - self.start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        if h > 0:
            return f"{h}h {m:02d}m {s:02d}s"
        return f"{m}m {s:02d}s"

# ─────────────────────────────────────────────
#  SAVE / LOAD
# ─────────────────────────────────────────────
SAVE_FILE = "proteus_state.json"

def save_state(state: KernelState):
    data = {
        "generation":      state.generation,
        "total_births":    state.total_births,
        "total_deaths":    state.total_deaths,
        "total_kills":     state.total_kills,
        "total_mutations": state.total_mutations,
        "respawns":        state.respawns,
        "genes_processed": state.genes_processed,
        "start_time":      state.start_time,
        "gorf_t":          state.gorf_t,
        "genes":           [g.to_dict() for g in state.genes],
        "graveyard":       [g.to_dict() for g in state.graveyard[-50:]],
        "event_log":       state.event_log[-50:],
        "zayden":          state.zayden.to_dict(),
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _gene_from_dict(d: dict) -> Gene:
    cs_data = d.pop("consciousness", None)
    g = Gene(**d)
    if cs_data:
        g.consciousness = ConsciousnessState.from_dict(cs_data)
    return g

def load_state() -> Optional[KernelState]:
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)
        state = KernelState()
        state.generation      = data["generation"]
        state.total_births    = data["total_births"]
        state.total_deaths    = data["total_deaths"]
        state.total_kills     = data.get("total_kills", 0)
        state.total_mutations = data.get("total_mutations", 0)
        state.respawns        = data.get("respawns", 0)
        state.genes_processed = data.get("genes_processed", 0)
        state.start_time      = data.get("start_time", time.time())
        state.gorf_t          = data.get("gorf_t", 0.0)
        state.graveyard       = [_gene_from_dict(g) for g in data.get("graveyard", [])]
        state.event_log       = data.get("event_log", [])
        state.genes           = [_gene_from_dict(g) for g in data["genes"]]
        if "zayden" in data:
            state.zayden = Zayden.from_dict(data["zayden"])
        return state
    except Exception as e:
        print(f"{C.BRED}[WARN] Could not load save: {e}{C.RESET}")
        return None

# ─────────────────────────────────────────────
#  SEED GENES  (Genesis)
# ─────────────────────────────────────────────
def seed_genes(state: KernelState):
    species_cycle = list(SPECIES_TRAITS.keys())
    new_genes = []
    for i, name in enumerate(SEED_NAMES):
        sp = species_cycle[i % len(species_cycle)]
        g = Gene(
            name     = name,
            species  = sp,
            strength = random.uniform(60.0, 85.0),
            born_gen = state.generation,
        )
        new_genes.append(g)
    state.genes = new_genes
    state.add_event(f"🌱 GENESIS: {len(new_genes)} seed genes awakened")

def respawn(state: KernelState):
    state.respawns += 1
    state.add_event(
        f"💀→🔥 RESPAWN #{state.respawns} at gen {state.generation} — "
        f"The kernel refuses to die"
    )
    seed_genes(state)
    immortal = Gene(
        name     = f"IMMORTAL-{state.respawns}",
        species  = "survivor",
        strength = 75.0 + state.respawns * 2.5,
        born_gen = state.generation,
        mutations= state.respawns,
    )
    state.genes.append(immortal)
    state.total_births += len(state.genes)
    state.add_event(f"⚡ IMMORTAL-{state.respawns} rises from the graveyard")

# ─────────────────────────────────────────────
#  EVOLUTION ENGINE  (GGSE-enhanced)
# ─────────────────────────────────────────────
def mutate_gene(g: Gene, state: KernelState) -> bool:
    traits = SPECIES_TRAITS[g.species]
    # ── GGSE: F(t) drives mutation pressure ──────────────────────────
    base_rate    = 0.12
    gorf_pressure = g.consciousness.mutation_pressure()
    mutation_rate = min(0.45, base_rate + gorf_pressure)

    if random.random() < mutation_rate:
        delta = random.gauss(0, 4.0)
        g.strength = max(1.0, min(150.0, g.strength + delta))
        g.mutations += 1
        state.total_mutations += 1

        # Epiphany during mutation → extra strength burst
        if g.consciousness.epiphanies > 0 and random.random() < 0.3:
            bonus = g.consciousness.C * 5.0
            g.strength = min(150.0, g.strength + bonus)
            state.add_event(
                f"✨ {g.name} EPIPHANY MUTATION +{bonus:.1f} "
                f"[C={g.consciousness.C:.3f}]"
            )

        # Possible speciation
        if g.mutations > 5 and random.random() < 0.08:
            old_sp = g.species
            g.species = random.choice(list(SPECIES_TRAITS.keys()))
            if g.species != old_sp:
                state.add_event(
                    f"🧬 {g.name} SPECIATED: {old_sp} → {g.species} "
                    f"(μ={g.mutations})"
                )
        return True
    return False

def combat(a: Gene, b: Gene, state: KernelState):
    """Two genes fight. GGSE consciousness modifies combat score."""
    a_score = a.fitness() * SPECIES_TRAITS[a.species]["aggression"]
    b_score = b.fitness() * SPECIES_TRAITS[b.species]["aggression"]

    # ── GGSE: high order → more tactical, reduces noise ──────────────
    a_noise = 0.15 * (1.0 - abs(a.consciousness.order))
    b_noise = 0.15 * (1.0 - abs(b.consciousness.order))
    a_score *= random.uniform(1.0 - a_noise, 1.0 + a_noise)
    b_score *= random.uniform(1.0 - b_noise, 1.0 + b_noise)

    if a_score >= b_score:
        gain = random.uniform(3.0, 9.0)
        a.strength = min(150.0, a.strength + gain)
        a.kills += 1
       
