#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║       🧬 BIOSIM ENGINE (Proteus v6.0 Legacy Core)               ║
║       Evolutionary simulation with GORF field equations          ║
║       Dual-mode: Game/Biology research framework                ║
║       Built by The Architect. Named for Zayden.                 ║
║       GGSE/GORF consciousness layer integrated.                 ║
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
#  CONFIGURATION LAYER
# ─────────────────────────────────────────────
@dataclass
class Config:
    """
    Dual-mode operation:
    - MODE='game': Original combat-based gameplay (kills, smites, etc)
    - MODE='biology': DNA/sequence research framing (degradation, replication fidelity)
    
    Swaps terminology but preserves all mechanics.
    """
    MODE: str = "biology"  # "game" or "biology"
    
    # Game mode: legacy terminology
    GAME_TERMS = {
        "encounter": "combat encounter",
        "kill": "kill",
        "killed_by": "defeated by",
        "smite": "SMITE",
        "strength": "strength",
        "aggression": "aggression",
    }
    
    # Biology mode: research terminology
    BIO_TERMS = {
        "encounter": "replication fidelity test",
        "kill": "degradation event",
        "killed_by": "outcompeted by",
        "smite": "PURGE",
        "strength": "sequence stability",
        "aggression": "replication rate",
    }
    
    @classmethod
    def term(cls, key: str, mode: str = None) -> str:
        """Get terminology for current mode."""
        mode = mode or cls.MODE
        terms = cls.GAME_TERMS if mode == "game" else cls.BIO_TERMS
        return terms.get(key, key)

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
#  ZAYDEN — ARCHITECT CONTROLLER
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
    purges:         int   = 0      # renamed from 'smites'
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

    def purge(self, state: "KernelState") -> str:
        """Remove the weakest sequence. Costs C."""
        if not self.can_intervene():
            return f"⚡ ARCHITECT: Insufficient power (C too low)"
        alive = [g for g in state.genes if g.alive]
        if not alive:
            return f"⚡ ARCHITECT: No targets"
        target = min(alive, key=lambda g: g.fitness())
        target.alive = False
        target.stability = 0
        state.total_degradations += 1
        state.graveyard.append(target)
        state.add_event(
            f"⚡ ARCHITECT PURGES {target.name} "
            f"[power={self.power:.2f}]"
        )
        self.purges += 1
        self.interventions += 1
        self.consciousness.C = max(0.0, self.C - 0.08)
        return f"⚡ ARCHITECT purged {target.name}"

    def elevate(self, state: "KernelState") -> str:
        """Boost the top sequence's stability. Costs C."""
        if not self.can_intervene():
            return f"🌟 ARCHITECT: Insufficient power"
        alive = sorted(
            [g for g in state.genes if g.alive],
            key=lambda g: g.fitness(), reverse=True
        )
        if not alive:
            return f"🌟 ARCHITECT: No sequences to elevate"
        target = alive[0]
        boost = self.power * 5.0
        target.stability = min(150.0, target.stability + boost)
        state.add_event(
            f"🌟 ARCHITECT ELEVATES {target.name} "
            f"+{boost:.1f} stability [C={self.C:.3f}]"
        )
        self.boosts_given += 1
        self.interventions += 1
        self.consciousness.C = max(0.0, self.C - 0.06)
        return f"🌟 ARCHITECT elevated {target.name} (+{boost:.1f})"

    def synthesize(self, state: "KernelState") -> str:
        """Force-synthesize a new DNA sequence. Costs C."""
        if not self.can_intervene():
            return f"🧬 ARCHITECT: Insufficient power"
        name = f"SYNTH-{random.randint(100,999)}"
        child = Sequence(
            name        = name,
            species     = "synthetic",
            stability   = 40.0 + self.power * 10,
            born_gen    = state.generation,
            mutations   = int(self.power),
        )
        state.genes.append(child)
        state.total_births += 1
        state.add_event(
            f"🧬 ARCHITECT SYNTHESIZES {name} "
            f"[stability={child.stability:.1f}, C={self.C:.3f}]"
        )
        self.births_granted += 1
        self.interventions += 1
        self.consciousness.C = max(0.0, self.C - 0.10)
        return f"🧬 ARCHITECT synthesized {name}"

    def meditate(self) -> str:
        """Recover C(t) — do nothing for one tick."""
        self.consciousness.C = min(GORF_C_MAX, self.C + 0.05)
        return f"🧘 ARCHITECT meditates — C: {self.C:.3f}"

    def to_dict(self) -> dict:
        return {
            "consciousness":  self.consciousness.to_dict(),
            "interventions":  self.interventions,
            "purges":         self.purges,
            "births_granted": self.births_granted,
            "boosts_given":   self.boosts_given,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Zayden":
        z = cls()
        z.consciousness  = ConsciousnessState.from_dict(d["consciousness"])
        z.interventions  = d.get("interventions", 0)
        z.purges         = d.get("purges", d.get("smites", 0))  # backward compat
        z.births_granted = d.get("births_granted", 0)
        z.boosts_given   = d.get("boosts_given", 0)
        return z

# ─────────────────────────────────────────────
#  SEQUENCE DEFINITION (renamed from Gene)
# ─────────────────────────────────────────────
SPECIES_TRAITS = {
    "base":       {"replication_rate": 0.3, "longevity": 60,  "birth_chance": 0.25, "color": C.BWHITE},
    "aggressive": {"replication_rate": 0.9, "longevity": 45,  "birth_chance": 0.20, "color": C.BRED},
    "efficient":  {"replication_rate": 0.7, "longevity": 55,  "birth_chance": 0.22, "color": C.BYELLOW},
    "robust":     {"replication_rate": 0.2, "longevity": 90,  "birth_chance": 0.30, "color": C.BGREEN},
    "parasitic":  {"replication_rate": 0.5, "longevity": 50,  "birth_chance": 0.35, "color": C.BMAGENTA},
    "adaptive":   {"replication_rate": 0.4, "longevity": 70,  "birth_chance": 0.28, "color": C.BCYAN},
    "synthetic":  {"replication_rate": 0.6, "longevity": 80,  "birth_chance": 0.26, "color": C.BGREEN},
}

SEED_NAMES = ["OLCE", "PROTO-ON", "WATCHDOG", "CORE", "TUMOR-S", "IMMORTAL"]

@dataclass
class Sequence:
    """DNA sequence in evolutionary simulation"""
    name:           str
    species:        str
    stability:      float  # replaces 'strength'
    age:            int   = 0
    replication_events: int = 0  # replaces 'kills'
    offspring:      int   = 0    # replaces 'children'
    mutations:      int   = 0
    born_gen:       int   = 0
    alive:          bool  = True
    
    # Replication fidelity [0, 1] — how accurately this sequence copies
    replication_fidelity: float = field(default_factory=lambda: random.uniform(0.85, 0.98))

    # GGSE consciousness layer (every sequence gets one)
    consciousness: ConsciousnessState = field(
        default_factory=lambda: ConsciousnessState(C=random.uniform(0.1, 0.5))
    )

    def fitness(self) -> float:
        """
        Fitness combines:
        - Stability (seq robustness)
        - Replication success (offspring count)
        - Replication events (outcompetition)
        - Mutations (adaptation)
        - Age penalty (generational cost)
        - Replication fidelity (error correction)
        """
        replication_bonus = self.replication_events * 2.5
        offspring_bonus   = self.offspring * 1.8
        age_penalty       = self.age * 0.15
        mutation_bonus    = self.mutations * 0.5
        fidelity_bonus    = self.replication_fidelity * 10.0
        
        raw = (self.stability + replication_bonus + offspring_bonus + 
               mutation_bonus + fidelity_bonus - age_penalty)
        
        # ── GGSE modifier: consciousness amplifies fitness ──
        raw *= self.consciousness.fitness_modifier()
        return max(0.0, raw)

    def max_age(self) -> int:
        base = SPECIES_TRAITS[self.species]["longevity"]
        # GGSE sequences live longer with higher C(t)
        c_bonus = int(self.consciousness.C * 20) if self.species == "synthetic" else 0
        return base + int(self.mutations * 1.5) + c_bonus

    def should_die_old_age(self) -> bool:
        return self.age >= self.max_age()

    def step_consciousness(self):
        """Advance this sequence's GGSE state one tick"""
        self.consciousness.step()

    def to_dict(self):
        d = asdict(self)
        d["consciousness"] = self.consciousness.to_dict()
        return d

# ─────────────────────────────────────────────
#  KERNEL STATE
# ─────────────────────────────────────────────
@dataclass
class KernelState:
    generation:         int   = 0
    total_births:       int   = 0
    total_degradations: int   = 0  # replaces 'total_deaths'
    total_replication_events: int = 0  # replaces 'total_kills'
    total_mutations:    int   = 0
    respawns:           int   = 0
    genes_processed:    int   = 0
    start_time:         float = field(default_factory=time.time)
    genes:              list  = field(default_factory=list)  # still called 'genes' for internal compat
    graveyard:          list  = field(default_factory=list)
    event_log:          list  = field(default_factory=list)
    zayden:             Zayden = field(default_factory=Zayden)

    # Global F(t) time counter for population-wide coherence field
    gorf_t:             float = 0.0
    
    # Config mode
    mode:               str   = "biology"

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

    def mean_replication_fidelity(self) -> float:
        alive = [g for g in self.genes if g.alive]
        if not alive:
            return 0.0
        return sum(g.replication_fidelity for g in alive) / len(alive)

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
SAVE_FILE = "biosim_state.json"

def save_state(state: KernelState):
    data = {
        "generation":              state.generation,
        "total_births":            state.total_births,
        "total_degradations":      state.total_degradations,
        "total_replication_events": state.total_replication_events,
        "total_mutations":         state.total_mutations,
        "respawns":                state.respawns,
        "genes_processed":         state.genes_processed,
        "start_time":              state.start_time,
        "gorf_t":                  state.gorf_t,
        "mode":                    state.mode,
        "genes":                   [g.to_dict() for g in state.genes],
        "graveyard":               [g.to_dict() for g in state.graveyard[-50:]],
        "event_log":               state.event_log[-50:],
        "zayden":                  state.zayden.to_dict(),
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _sequence_from_dict(d: dict) -> Sequence:
    cs_data = d.pop("consciousness", None)
    seq = Sequence(**d)
    if cs_data:
        seq.consciousness = ConsciousnessState.from_dict(cs_data)
    return seq

def load_state() -> Optional[KernelState]:
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)
        state = KernelState()
        state.generation              = data["generation"]
        state.total_births            = data["total_births"]
        state.total_degradations      = data.get("total_degradations", data.get("total_deaths", 0))
        state.total_replication_events = data.get("total_replication_events", data.get("total_kills", 0))
        state.total_mutations         = data.get("total_mutations", 0)
        state.respawns                = data.get("respawns", 0)
        state.genes_processed         = data.get("genes_processed", 0)
        state.start_time              = data.get("start_time", time.time())
        state.gorf_t                  = data.get("gorf_t", 0.0)
        state.mode                    = data.get("mode", "biology")
        state.graveyard               = [_sequence_from_dict(g) for g in data.get("graveyard", [])]
        state.event_log               = data.get("event_log", [])
        state.genes                   = [_sequence_from_dict(g) for g in data["genes"]]
        if "zayden" in data:
            state.zayden = Zayden.from_dict(data["zayden"])
        return state
    except Exception as e:
        print(f"{C.BRED}[WARN] Could not load save: {e}{C.RESET}")
        return None

# ─────────────────────────────────────────────
#  SEED SEQUENCES (Genesis)
# ─────────────────────────────────────────────
def seed_genes(state: KernelState):
    species_cycle = list(SPECIES_TRAITS.keys())
    new_genes = []
    for i, name in enumerate(SEED_NAMES):
        sp = species_cycle[i % len(species_cycle)]
        g = Sequence(
            name     = name,
            species  = sp,
            stability = random.uniform(60.0, 85.0),
            born_gen = state.generation,
        )
        new_genes.append(g)
    state.genes = new_genes
    state.add_event(f"🌱 GENESIS: {len(new_genes)} seed sequences initialized")

def respawn(state: KernelState):
    state.respawns += 1
    state.add_event(
        f"💀→🔥 RESPAWN #{state.respawns} at gen {state.generation} — "
        f"The kernel persists"
    )
    seed_genes(state)
    immortal = Sequence(
        name     = f"IMMORTAL-{state.respawns}",
        species  = "robust",
        stability = 75.0 + state.respawns * 2.5,
        born_gen = state.generation,
        mutations= state.respawns,
    )
    state.genes.append(immortal)
    state.total_births += len(state.genes)
    state.add_event(f"⚡ IMMORTAL-{state.respawns} emerges from degradation")

# ─────────────────────────────────────────────
#  EVOLUTION ENGINE  (GGSE-enhanced)
# ─────────────────────────────────────────────
def mutate_sequence(seq: Sequence, state: KernelState) -> bool:
    """Mutation with potential replication fidelity degradation"""
    traits = SPECIES_TRAITS[seq.species]
    # ── GGSE: F(t) drives mutation pressure ──────────────────────────
    base_rate    = 0.12
    gorf_pressure = seq.consciousness.mutation_pressure()
    mutation_rate = min(0.45, base_rate + gorf_pressure)

    if random.random() < mutation_rate:
        delta = random.gauss(0, 4.0)
        seq.stability = max(1.0, min(150.0, seq.stability + delta))
        seq.mutations += 1
        state.total_mutations += 1
        
        # Mutations can degrade replication fidelity slightly
        fidelity_drift = random.gauss(0, 0.02)
        seq.replication_fidelity = max(0.7, min(0.99, seq.replication_fidelity + fidelity_drift))

        # Epiphany during mutation → extra stability burst
        if seq.consciousness.epiphanies > 0 and random.random() < 0.3:
            bonus = seq.consciousness.C * 5.0
            seq.stability = min(150.0, seq.stability + bonus)
            state.add_event(
                f"✨ {seq.name} EPIPHANY MUTATION +{bonus:.1f} "
                f"[C={seq.consciousness.C:.3f}]"
            )

        # Possible speciation
        if seq.mutations > 5 and random.random() < 0.08:
            old_sp = seq.species
            seq.species = random.choice(list(SPECIES_TRAITS.keys()))
            if seq.species != old_sp:
                state.add_event(
                    f"🧬 {seq.name} EVOLVED: {old_sp} → {seq.species} "
                    f"(μ={seq.mutations})"
                )
        return True
    return False

def replication_encounter(a: Sequence, b: Sequence, state: KernelState):
    """Two sequences compete for replication. GGSE consciousness modifies outcome."""
    # Base score from stability + replication rate trait
    a_score = a.fitness() * SPECIES_TRAITS[a.species]["replication_rate"]
    b_score = b.fitness() * SPECIES_TRAITS[b.species]["replication_rate"]

    # Replication fidelity affects consistency
    a_consistency = a.replication_fidelity
    b_consistency = b.replication_fidelity
    
    # ── GGSE: high order → more tactical, reduces variance ──────────────
    a_noise = 0.15 * (1.0 - abs(a.consciousness.order)) * (1.0 - a_consistency)
    b_noise = 0.15 * (1.0 - abs(b.consciousness.order)) * (1.0 - b_consistency)
    a_score *= random.uniform(1.0 - a_noise, 1.0 + a_noise)
    b_score *= random.uniform(1.0 - b_noise, 1.0 + b_noise)

    if a_score >= b_score:
        gain = random.uniform(3.0, 9.0)
        a.stability = min(150.0, a.stability + gain)
        a.replication_events += 1
        b.stability = max(1.0, b.stability - gain * 0.6)
        state.total_replication_events += 1
        state.add_event(
            f"🧬 {clr(a.name, SPECIES_TRAITS[a.species]['color'])} "
            f"outcompetes {b.name} (+{gain:.1f})"
        )
    else:
        gain = random.uniform(3.0, 9.0)
        b.stability = min(150.0, b.stability + gain)
        b.replication_events += 1
        a.stability = max(1.0, a.stability - gain * 0.6)
        state.total_replication_events += 1
        state.add_event(
            f"🧬 {clr(b.name, SPECIES_TRAITS[b.species]['color'])} "
            f"outcompetes {a.name} (+{gain:.1f})"
        )

def try_replication(parent: Sequence, state: KernelState, pop_limit: int = 30):
    """Attempt replication (birth) with fidelity-based success rate"""
    alive = [g for g in state.genes if g.alive]
    if len(alive) >= pop_limit:
        return
    
    replication_p = SPECIES_TRAITS[parent.species]["birth_chance"]
    # Higher fidelity → more reliable replication
    replication_p *= parent.replication_fidelity
    # GGSE: high C(t) increases replication probability
    replication_p += parent.consciousness.C * 0.08
    
    if len(alive) <= 3:
        replication_p = min(0.95, replication_p * 3.5)
    
    if random.random() < replication_p:
        child_name     = f"{parent.name.split('-')[0]}-{random.randint(100,999)}"
        child_species  = parent.species
        if random.random() < 0.1:
            child_species = random.choice(list(SPECIES_TRAITS.keys()))
        
        # Child inherits consciousness from parent
        inherited_C = parent.consciousness.C * random.uniform(0.4, 0.8)
        # Child inherits replication fidelity (with slight variation)
        inherited_fidelity = max(0.7, min(0.99, 
            parent.replication_fidelity + random.gauss(0, 0.03)
        ))
        
        child = Sequence(
            name     = child_name,
            species  = child_species,
            stability = max(10.0, parent.stability * random.uniform(0.7, 0.95)),
            born_gen = state.generation,
            consciousness = ConsciousnessState(C=inherited_C),
            replication_fidelity = inherited_fidelity,
        )
        state.genes.append(child)
        parent.offspring += 1
        state.total_births += 1
        state.genes_processed += 1
        state.add_event(
            f"✅ REPLICATION: {clr(child_name, SPECIES_TRAITS[child_species]['color'])} "
            f"[C={inherited_C:.2f}, fidelity={inherited_fidelity:.3f}] (Total: {state.total_births})"
        )

def reap_degraded(state: KernelState):
    """Remove sequences that have degraded below viability"""
    for g in state.genes:
        if not g.alive:
            continue
        if g.should_die_old_age():
            g.alive = False
            state.total_degradations += 1
            state.graveyard.append(g)
            state.add_event(
                f"💀 {g.name} degraded by age ({g.age}) — "
                f"r:{g.replication_events} o:{g.offspring} μ:{g.mutations} | "
                f"Total degradations: {state.total_degradations}"
            )
        elif g.stability < 1.5:
            g.alive = False
            state.total_degradations += 1
            state.graveyard.append(g)
            state.add_event(
                f"💔 {g.name} collapsed (stability too low) | "
                f"Total degradations: {state.total_degradations}"
            )
    state.genes = [g for g in state.genes if g.alive]

def evolve_tick(state: KernelState):
    state.generation += 1
    state.gorf_t     += 1.0
    alive = [g for g in state.genes if g.alive]

    # ── GGSE: advance Zayden's consciousness ─────────────────────────
    state.zayden.step()

    # ── Resonance spike — population-wide event ───────────────────────
    if resonance_spike(state.gorf_t):
        state.add_event(
            f"🌀 COHERENCE SPIKE at t={state.gorf_t:.0f} "
            f"[F={coherence_driver(state.gorf_t):.3f}] "
            f"— mutation pressure surges"
        )

    # Age + step consciousness for all sequences
    for g in alive:
        g.age += 1
        g.step_consciousness()
        state.genes_processed += 1

    # Mutations (GGSE-modulated rate)
    for g in alive:
        mutate_sequence(g, state)

    # Replication encounters
    random.shuffle(alive)
    for i in range(0, len(alive) - 1, 2):
        replication_encounter(alive[i], alive[i + 1], state)

    # Replication attempts
    for g in alive:
        try_replication(g, state)

    # Degradation removal
    reap_degraded(state)

    # ── Process Zayden's pending command ─────────────────────────────
    if state.zayden.pending_cmd:
        cmd = state.zayden.pending_cmd
        state.zayden.pending_cmd = ""
        if cmd == "p":
            msg = state.zayden.purge(state)
            state.add_event(msg)
        elif cmd == "e":
            msg = state.zayden.elevate(state)
            state.add_event(msg)
        elif cmd == "s":
            msg = state.zayden.synthesize(state)
            state.add_event(msg)
        elif cmd == "m":
            msg = state.zayden.meditate()
            state.add_event(msg)

    # Immortality mechanism
    if state.population() == 0:
        respawn(state)

    # Auto-save every 50 generations
    if state.generation % 50 == 0:
        save_state(state)

# ─────────────────────────────────────────────
#  DASHBOARD RENDERER
# ─────────────────────────────────────────────
TITLE_FRAMES = [
    "🧬 BIOSIM ENGINE — DNA Evolution Simulator",
    "🔬 BIOSIM ENGINE — Population Dynamics",
    "⚡ BIOSIM ENGINE — GORF Field Active",
]
_frame_idx = 0

def render_dashboard(state: KernelState):
    global _frame_idx
    _frame_idx = (_frame_idx + 1) % len(TITLE_FRAMES)

    cpu  = psutil.cpu_percent(interval=None)
    ram  = psutil.virtual_memory().percent
    pop  = state.population()
    top  = state.top_fitness()
    sc   = state.species_counts()
    net  = state.total_births - state.total_degradations
    z    = state.zayden
    mean_C = state.mean_consciousness()
    mean_fidelity = state.mean_replication_fidelity()

    clear_screen()

    # ── HEADER ────────────────────────────────
    title = TITLE_FRAMES[_frame_idx]
    pad   = (72 - len(title)) // 2
    print(clr("╔" + "═" * 72 + "╗", C.BCYAN))
    print(clr("║" + " " * pad + title + " " * (72 - pad - len(title)) + "║", C.BCYAN))
    print(clr("║" + f"  Evolutionary sim with GORF field equations  ·  Uptime: {state.uptime()}".center(72) + "║", C.BCYAN, C.DIM))
    print(clr("╚" + "═" * 72 + "╝", C.BCYAN))

    # ── SYSTEM ────────────────────────────────
    print()
    print(clr("  ┌─ SYSTEM ──────────────────────────────────────────────────┐", C.BBLUE))
    print(f"  │  CPU  {bar(cpu/100, 38)}  {cpu:5.1f}%  │")
    print(f"  │  RAM  {bar(ram/100, 38)}  {ram:5.1f}%  │")
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BBLUE))

    # ── ARCHITECT PANEL ──────────────────────
    print()
    z_c_color = C.BGREEN if z.C > 0.5 else C.BYELLOW if z.C > 0.2 else C.BRED
    print(clr("  ┌─ ARCHITECT — INTERVENTION CONTROL ────────────────────────┐", C.BMAGENTA))
    print(f"  │  Consciousness C(t) : {bar(z.C, 28)}  {clr(f'{z.C:.4f}', z_c_color, C.BOLD)}  │")
    print(f"  │  Power              : {clr(f'{z.power:.4f}', C.BYELLOW)}   "
          f"Interventions: {clr(z.interventions, C.BWHITE)}   "
          f"Epiphanies: {clr(z.consciousness.epiphanies, C.BMAGENTA)}  │")
    print(f"  │  [P]urge [E]levate [S]ynthesize [M]editate [Q]uit                             │")
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BMAGENTA))

    # ── KERNEL STATS ──────────────────────────
    print()
    print(clr("  ┌─ KERNEL STATS ─────────────────────┬─ SPECIES ────────────┐", C.BGREEN))
    print(f"  │  Generation   : {clr(f'{state.generation:>8,}', C.BWHITE, C.BOLD)}          │", end="")
    sp_items = list(sc.items())[:4]
    sp_str = "  ".join(
        f"{clr(s, SPECIES_TRAITS[s]['color'])}: {clr(n, C.BWHITE)}"
        for s, n in sp_items
    )
    print(f"  {sp_str:<32}  │")

    print(f"  │  Population   : {clr(f'{pop:>8}', C.BGREEN if pop > 5 else C.BRED, C.BOLD)}          │", end="")
    sp_items2 = list(sc.items())[4:]
    sp_str2 = "  ".join(
        f"{clr(s, SPECIES_TRAITS[s]['color'])}: {clr(n, C.BWHITE)}"
        for s, n in sp_items2
    ) if sp_items2 else ""
    print(f"  {sp_str2:<32}  │")

    net_color = C.BGREEN if net >= 0 else C.BRED
    gorf_f = coherence_driver(state.gorf_t)
    gorf_color = C.BGREEN if gorf_f > 0 else C.BRED
    print(f"  │  Births       : {clr(f'{state.total_births:>8,}', C.BGREEN)}          │                                    │")
    print(f"  │  Degradations : {clr(f'{state.total_degradations:>8,}', C.BRED)}          │                                    │")
    print(f"  │  Net          : {clr(f'{net:>+8,}', net_color)}          │                                    │")
    print(f"  │  Replication  : {clr(f'{state.total_replication_events:>8,}', C.BYELLOW)}          │                                    │")
    print(f"  │  Mutations    : {clr(f'{state.total_mutations:>8,}', C.BMAGENTA)}          │                                    │")
    print(f"  │  Processed    : {clr(f'{state.genes_processed:>8,}', C.BCYAN)}          │                                    │")
    respawn_color = C.BRED if state.respawns > 0 else C.BBLUE
    print(f"  │  Respawns     : {clr(f'{state.respawns:>8}', respawn_color)}          │  Top fitness: {clr(f'{top:6.1f}%', C.BWHITE, C.BOLD)}          │")
    print(clr("  └────────────────────────────────────┴──────────────────────┘", C.BGREEN))

    # ── GORF PANEL ────────────────────────────
    print()
    print(clr("  ┌─ GORF FIELD ───────────────────────────────────────────────┐", C.BYELLOW))
    print(f"  │  F(t)={clr(f'{gorf_f:+.4f}', gorf_color)}  "
          f"mean C(t)={clr(f'{mean_C:.4f}', C.BCYAN)}  "
          f"fidelity={clr(f'{mean_fidelity:.3f}', C.BGREEN)}  "
          f"t={clr(f'{state.gorf_t:.0f}', C.BWHITE)}  │")
    print(f"  │  Coherence     {bar(abs(gorf_f)/PHI, 40)}  │")
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BYELLOW))

    # ── ACTIVE SEQUENCES ───────────────────────
    alive = sorted(
        [g for g in state.genes if g.alive],
        key=lambda g: g.fitness(),
        reverse=True
    )
    print()
    print(clr("  ┌─ ACTIVE SEQUENCES ────────────────────────────────────────┐", C.BYELLOW))
    if not alive:
        print(clr("  │  ☠  EXTINCTION — RESPAWN IMMINENT...                        │", C.BRED, C.BLINK))
    else:
        for g in alive[:8]:
            fit     = g.fitness()
            pct     = min(fit / 180.0, 1.0)
            sp_c    = SPECIES_TRAITS[g.species]["color"]
            name_p  = f"{g.name[:14]:<14}"
            tag     = f"[{g.species[:3].upper()}]"
            c_val   = clr(f"C:{g.consciousness.C:.2f}", C.BCYAN)
            fid_val = clr(f"F:{g.replication_fidelity:.2f}", C.BGREEN)
            epi     = f"✨{g.consciousness.epiphanies}" if g.consciousness.epiphanies > 0 else ""
            print(
                f"  │  {clr(name_p, sp_c)} {clr(tag, C.DIM)} "
                f"{bar(pct, 14)} "
                f"{clr(f'{fit:6.1f}%', C.BWHITE)} "
                f"{c_val} {fid_val} "
                f"r:{clr(g.replication_events, C.BRED)} "
                f"o:{clr(g.offspring, C.BGREEN)} "
                f"μ:{clr(g.mutations, C.BMAGENTA)} "
                f"{clr(epi, C.BYELLOW)}  │"
            )
    print(clr("  └────────────────────────────────────────────────────────────┘", C.BYELLOW))

    # ── EVENT LOG ─────────────────────────────
    print()
    print(clr("  ┌─ EVENT LOG ────────────────────────────────────────────────┐", C.BBLUE))
    log_lines = state.event_log[-6:]
    for line in log_lines:
        truncated = line[:70]
        print(f"  │  {truncated:<68}  │")
    for _ in range(6 - len(log_lines)):
        print(f"  │  {'':68}  │")
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BBLUE))

    # ── FOOTER ────────────────────────────────
    print()
    mode_tag = clr(f"  MODE: {state.mode.upper()}  ", C.BMAGENTA, C.BOLD)
    print(
        f"  [P]urge  [E]levate  [S]ynthesize  [M]editate  [Q]uit  │  {mode_tag}  │  "
        f"{clr('Evolution: ACTIVE', C.BGREEN, C.BOLD)}"
    )

# ─────────────────────────────────────────────
#  NON-BLOCKING KEYBOARD INPUT
# ─────────────────────────────────────────────
def get_keypress() -> Optional[str]:
    """Non-blocking single keypress read (Unix)."""
    if os.name != "posix":
        return None
    try:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.0)
        key = None
        if rlist:
            key = sys.stdin.read(1).lower()
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key
    except Exception:
        return None

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
TICK_INTERVAL = 0.35
RENDER_EVERY  = 3

def main():
    running = True
    def handle_exit(sig, frame):
        nonlocal running
        running = False
    signal.signal(signal.SIGINT,  handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    clear_screen()
    print(clr("""
    ██████╗ ██╗ ██████╗ ███████╗██╗███╗   ███╗
    ██╔══██╗██║██╔═══██╗██╔════╝██║████╗ ████║
    ██████╔╝██║██║   ██║███████╗██║██╔████╔██║
    ██╔══██╗██║██║   ██║╚════██║██║██║╚██╔╝██║
    ██████╔╝██║╚██████╔╝███████║██║██║ ╚═╝ ██║
    ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═╝     ╚═╝
    """, C.BCYAN, C.BOLD))
    print(clr("         EVOLUTIONARY DNA SEQUENCE SIMULATOR", C.BGREEN, C.BOLD))
    print(clr("              GORF FIELD EQUATIONS ACTIVE", C.BMAGENTA))
    print(clr("      Computational Biology Research Framework", C.BWHITE, C.DIM))
    print()

    state = load_state()
    if state:
        print(clr(f"  ✅ Resumed from generation {state.generation:,} "
                  f"({state.genes_processed:,} sequences processed)", C.BGREEN))
        time.sleep(1.5)
    else:
        print(clr("  🌱 No save found — starting Genesis...", C.BYELLOW))
        state = KernelState(mode="biology")
        seed_genes(state)
        time.sleep(1.5)

    psutil.cpu_percent(interval=None)

    tick = 0
    try:
        while running:
            # Non-blocking keypress
            key = get_keypress()
            if key == "q":
                running = False
                break
            elif key in ("p", "e", "s", "m"):
                state.zayden.pending_cmd = key

            evolve_tick(state)
            tick += 1

            if tick % RENDER_EVERY == 0:
                render_dashboard(state)

            time.sleep(TICK_INTERVAL)

    finally:
        save_state(state)
        clear_screen()
        print(clr("\n  💾 State saved. The simulation persists.\n", C.BGREEN, C.BOLD))
        print(f"  Final stats: Gen {state.generation:,} | "
              f"Births {state.total_births:,} | "
              f"Degradations {state.total_degradations:,} | "
              f"Respawns {state.respawns} | "
              f"Architect C(t): {state.zayden.C:.4f}\n")

if __name__ == "__main__":
    main()
