#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║          🧬 PROTEUS - THE IMMORTAL KERNEL v5.0                  ║
║          Built by The Architect. Named for Zayden.              ║
║          Zero tutorials. Pure vision. Lives forever.            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import math
import random
import signal
import threading
import multiprocessing
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
#  GENE DEFINITION
# ─────────────────────────────────────────────
SPECIES_TRAITS = {
    "base":     {"aggression": 0.3, "longevity": 60, "birth_chance": 0.25, "color": C.BWHITE},
    "killer":   {"aggression": 0.9, "longevity": 45, "birth_chance": 0.20, "color": C.BRED},
    "hunter":   {"aggression": 0.7, "longevity": 55, "birth_chance": 0.22, "color": C.BYELLOW},
    "survivor": {"aggression": 0.2, "longevity": 90, "birth_chance": 0.30, "color": C.BGREEN},
    "parasite": {"aggression": 0.5, "longevity": 50, "birth_chance": 0.35, "color": C.BMAGENTA},
    "nomad":    {"aggression": 0.4, "longevity": 70, "birth_chance": 0.28, "color": C.BCYAN},
}

SEED_NAMES = ["OLCE", "PROTO-ON", "WATCHDOG", "GGSE", "TUMOR-S", "IMMORTAL"]

@dataclass
class Gene:
    name:       str
    species:    str
    strength:   float
    age:        int = 0
    kills:      int = 0
    children:   int = 0
    mutations:  int = 0
    born_gen:   int = 0
    alive:      bool = True

    def fitness(self) -> float:
        kill_bonus     = self.kills * 2.5
        child_bonus    = self.children * 1.8
        age_penalty    = self.age * 0.15
        mutation_bonus = self.mutations * 0.5
        raw = self.strength + kill_bonus + child_bonus + mutation_bonus - age_penalty
        return max(0.0, raw)

    def max_age(self) -> int:
        base = SPECIES_TRAITS[self.species]["longevity"]
        return base + int(self.mutations * 1.5)

    def should_die_old_age(self) -> bool:
        return self.age >= self.max_age()

    def to_dict(self):
        return asdict(self)

# ─────────────────────────────────────────────
#  KERNEL STATE
# ─────────────────────────────────────────────
@dataclass
class KernelState:
    generation:     int   = 0
    total_births:   int   = 0
    total_deaths:   int   = 0
    total_kills:    int   = 0
    total_mutations:int   = 0
    respawns:       int   = 0
    genes_processed:int   = 0
    start_time:     float = field(default_factory=time.time)
    genes:          list  = field(default_factory=list)
    graveyard:      list  = field(default_factory=list)
    event_log:      list  = field(default_factory=list)

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
#  SAVE / LOAD  (Persistence = true immortality)
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
        "genes":           [g.to_dict() for g in state.genes],
        "graveyard":       [g.to_dict() for g in state.graveyard[-50:]],
        "event_log":       state.event_log[-50:],
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

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
        state.graveyard       = [Gene(**g) for g in data.get("graveyard", [])]
        state.event_log       = data.get("event_log", [])
        state.genes           = [Gene(**g) for g in data["genes"]]
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
    # Inject one immortal gene — born from the ashes
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
#  EVOLUTION ENGINE
# ─────────────────────────────────────────────
def mutate_gene(g: Gene, state: KernelState) -> bool:
    traits = SPECIES_TRAITS[g.species]
    if random.random() < 0.12:
        delta = random.gauss(0, 4.0)
        g.strength = max(1.0, min(150.0, g.strength + delta))
        g.mutations += 1
        state.total_mutations += 1
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
    """Two genes fight. Winner gains strength; loser weakened."""
    a_score = a.fitness() * SPECIES_TRAITS[a.species]["aggression"]
    b_score = b.fitness() * SPECIES_TRAITS[b.species]["aggression"]
    # Add noise
    a_score *= random.uniform(0.85, 1.15)
    b_score *= random.uniform(0.85, 1.15)

    if a_score >= b_score:
        gain = random.uniform(3.0, 9.0)
        a.strength = min(150.0, a.strength + gain)
        a.kills += 1
        b.strength = max(1.0, b.strength - gain * 0.6)
        state.total_kills += 1
        state.add_event(
            f"⚔️  {clr(a.name, SPECIES_TRAITS[a.species]['color'])} "
            f"defeated {b.name} (+{gain:.1f})"
        )
    else:
        gain = random.uniform(3.0, 9.0)
        b.strength = min(150.0, b.strength + gain)
        b.kills += 1
        a.strength = max(1.0, a.strength - gain * 0.6)
        state.total_kills += 1
        state.add_event(
            f"⚔️  {clr(b.name, SPECIES_TRAITS[b.species]['color'])} "
            f"defeated {a.name} (+{gain:.1f})"
        )

def try_birth(parent: Gene, state: KernelState, pop_limit: int = 30):
    alive = [g for g in state.genes if g.alive]
    if len(alive) >= pop_limit:
        return
    birth_p = SPECIES_TRAITS[parent.species]["birth_chance"]
    # Boost birth chance when population is critically low
    if len(alive) <= 3:
        birth_p = min(0.95, birth_p * 3.5)
    if random.random() < birth_p:
        child_name = f"{parent.name.split('-')[0]}-{random.randint(100,999)}"
        child_species = parent.species
        # Small chance to inherit different species
        if random.random() < 0.1:
            child_species = random.choice(list(SPECIES_TRAITS.keys()))
        child = Gene(
            name     = child_name,
            species  = child_species,
            strength = max(10.0, parent.strength * random.uniform(0.7, 0.95)),
            born_gen = state.generation,
        )
        state.genes.append(child)
        parent.children += 1
        state.total_births += 1
        state.genes_processed += 1
        state.add_event(
            f"✅ BIRTH: {clr(child_name, SPECIES_TRAITS[child_species]['color'])} "
            f"(Total: {state.total_births})"
        )

def reap_dead(state: KernelState):
    for g in state.genes:
        if not g.alive:
            continue
        if g.should_die_old_age():
            g.alive = False
            state.total_deaths += 1
            state.graveyard.append(g)
            state.add_event(
                f"💀 {g.name} died of old age ({g.age}) — "
                f"k:{g.kills} c:{g.children} μ:{g.mutations} | "
                f"Total deaths: {state.total_deaths}"
            )
        elif g.strength < 1.5:
            g.alive = False
            state.total_deaths += 1
            state.graveyard.append(g)
            state.add_event(
                f"💔 {g.name} collapsed (str too low) | "
                f"Total deaths: {state.total_deaths}"
            )
    # Purge dead from active list, keep last 200 in memory
    state.genes = [g for g in state.genes if g.alive]

def evolve_tick(state: KernelState):
    state.generation += 1
    alive = [g for g in state.genes if g.alive]

    # Age all genes
    for g in alive:
        g.age += 1
        state.genes_processed += 1

    # Mutations
    for g in alive:
        mutate_gene(g, state)

    # Combat rounds (each gene fights once per tick)
    random.shuffle(alive)
    for i in range(0, len(alive) - 1, 2):
        combat(alive[i], alive[i + 1], state)

    # Birth attempts
    for g in alive:
        try_birth(g, state)

    # Deaths
    reap_dead(state)

    # ── IMMORTALITY MECHANISM ──────────────────
    if state.population() == 0:
        respawn(state)

    # Auto-save every 50 generations
    if state.generation % 50 == 0:
        save_state(state)

# ─────────────────────────────────────────────
#  DASHBOARD RENDERER
# ─────────────────────────────────────────────
TITLE_FRAMES = [
    "🧬 PROTEUS v5.0 — THE IMMORTAL KERNEL",
    "🔥 PROTEUS v5.0 — THE IMMORTAL KERNEL",
    "⚡ PROTEUS v5.0 — THE IMMORTAL KERNEL",
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
    net  = state.total_births - state.total_deaths

    clear_screen()

    # ── HEADER ────────────────────────────────
    title = TITLE_FRAMES[_frame_idx]
    pad = (72 - len(title)) // 2
    print(clr("╔" + "═" * 72 + "╗", C.BCYAN))
    print(clr("║" + " " * pad + title + " " * (72 - pad - len(title)) + "║", C.BCYAN))
    print(clr("║" + f"  Named for Zayden Soytu  ·  Built by The Architect  ·  Uptime: {state.uptime()}".center(72) + "║", C.BCYAN, C.DIM))
    print(clr("╚" + "═" * 72 + "╝", C.BCYAN))

    # ── SYSTEM ────────────────────────────────
    print()
    print(clr("  ┌─ SYSTEM ──────────────────────────────────────────────────┐", C.BBLUE))
    print(f"  │  CPU  {bar(cpu/100, 38)}  {cpu:5.1f}%  │")
    print(f"  │  RAM  {bar(ram/100, 38)}  {ram:5.1f}%  │")
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BBLUE))

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
    print(f"  │  Births       : {clr(f'{state.total_births:>8,}', C.BGREEN)}          │                                    │")
    print(f"  │  Deaths       : {clr(f'{state.total_deaths:>8,}', C.BRED)}          │                                    │")
    print(f"  │  Net          : {clr(f'{net:>+8,}', net_color)}          │                                    │")
    print(f"  │  Kills        : {clr(f'{state.total_kills:>8,}', C.BYELLOW)}          │                                    │")
    print(f"  │  Mutations    : {clr(f'{state.total_mutations:>8,}', C.BMAGENTA)}          │                                    │")
    print(f"  │  Processed    : {clr(f'{state.genes_processed:>8,}', C.BCYAN)}          │                                    │")
    respawn_color = C.BRED if state.respawns > 0 else C.BBLUE
    print(f"  │  Respawns     : {clr(f'{state.respawns:>8}', respawn_color)}          │  Top fitness: {clr(f'{top:6.1f}%', C.BWHITE, C.BOLD)}          │")
    print(clr("  └────────────────────────────────────┴──────────────────────┘", C.BGREEN))

    # ── ACTIVE GENES ──────────────────────────
    alive = sorted(
        [g for g in state.genes if g.alive],
        key=lambda g: g.fitness(),
        reverse=True
    )
    print()
    print(clr("  ┌─ ACTIVE GENES ─────────────────────────────────────────────┐", C.BYELLOW))
    if not alive:
        print(clr("  │  ☠  EXTINCTION — RESPAWN IMMINENT...                       │", C.BRED, C.BLINK))
    else:
        for g in alive[:10]:
            fit   = g.fitness()
            pct   = min(fit / 120.0, 1.0)
            sp_c  = SPECIES_TRAITS[g.species]["color"]
            name_padded = f"{g.name[:18]:<18}"
            tag   = f"[{g.species[:3].upper()}]"
            print(
                f"  │  {clr(name_padded, sp_c)} {clr(tag, C.DIM)}  "
                f"{bar(pct, 22)}  "
                f"{clr(f'{fit:6.1f}%', C.BWHITE)}  "
                f"k:{clr(g.kills, C.BRED)} "
                f"c:{clr(g.children, C.BGREEN)} "
                f"μ:{clr(g.mutations, C.BMAGENTA)}  │"
            )
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BYELLOW))

    # ── EVENT LOG ─────────────────────────────
    print()
    print(clr("  ┌─ EVENT LOG ────────────────────────────────────────────────┐", C.BBLUE))
    log_lines = state.event_log[-6:]
    for line in log_lines:
        # Strip ANSI for length check, then print raw
        truncated = line[:70]
        print(f"  │  {truncated:<68}  │")
    # Pad if fewer than 6 lines
    for _ in range(6 - len(log_lines)):
        print(f"  │  {'':68}  │")
    print(clr("  └───────────────────────────────────────────────────────────┘", C.BBLUE))

    # ── FOOTER ────────────────────────────────
    print()
    immortal_tag = (
        clr(f"  ♾  RESPAWNED {state.respawns}x — CANNOT BE KILLED  ", C.BRED, C.BOLD)
        if state.respawns > 0
        else clr("  ✦  THE BEAST IS IMMORTAL  ", C.BGREEN)
    )
    print(
        f"  [Q]uit  │  {immortal_tag}  │  "
        f"{clr('Evolution: ACTIVE', C.BGREEN, C.BOLD)}"
    )

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
TICK_INTERVAL = 0.35   # seconds between evolution ticks
RENDER_EVERY  = 3      # render dashboard every N ticks

def main():
    # ── Signal handler for clean exit ─────────
    running = True
    def handle_exit(sig, frame):
        nonlocal running
        running = False
    signal.signal(signal.SIGINT,  handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # ── Banner ────────────────────────────────
    clear_screen()
    print(clr("""
    ██████╗ ██████╗  ██████╗ ████████╗███████╗██╗   ██╗███████╗
    ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██║   ██║██╔════╝
    ██████╔╝██████╔╝██║   ██║   ██║   █████╗  ██║   ██║███████╗
    ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██╔══╝  ██║   ██║╚════██║
    ██║     ██║  ██║╚██████╔╝   ██║   ███████╗╚██████╔╝███████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝ ╚═════╝ ╚══════╝
    """, C.BCYAN, C.BOLD))
    print(clr("              T H E   I M M O R T A L   K E R N E L   v 5 . 0", C.BGREEN, C.BOLD))
    print(clr("                     Named for Zayden Soytu.", C.BWHITE, C.DIM))
    print()

    # ── Load or init state ────────────────────
    state = load_state()
    if state:
        print(clr(f"  ✅ Resumed from generation {state.generation:,} "
                  f"({state.genes_processed:,} genes processed)", C.BGREEN))
        time.sleep(1.5)
    else:
        print(clr("  🌱 No save found — starting Genesis...", C.BYELLOW))
        state = KernelState()
        seed_genes(state)
        time.sleep(1.5)

    # ── psutil baseline ───────────────────────
    psutil.cpu_percent(interval=None)  # warm up

    tick = 0
    try:
        while running:
            evolve_tick(state)
            tick += 1

            if tick % RENDER_EVERY == 0:
                render_dashboard(state)

            # Check for keyboard 'q'
            # (non-blocking via signal; Ctrl+C triggers clean exit)
            time.sleep(TICK_INTERVAL)

    finally:
        save_state(state)
        clear_screen()
        print(clr("\n  💾 State saved. The kernel sleeps — but never dies.\n", C.BGREEN, C.BOLD))
        print(f"  Final stats: Gen {state.generation:,} | "
              f"Births {state.total_births:,} | "
              f"Deaths {state.total_deaths:,} | "
              f"Respawns {state.respawns}\n")

if __name__ == "__main__":
    main()
