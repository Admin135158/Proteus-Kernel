# 🧬 PROTEUS-KERNEL

> *"The first kernel seeks its network."*  
> *A field-equation-driven evolutionary simulator that evolves, mutates, and persists.*  
> *Built by The Architect. Named for Zayden Soytu. Lives forever.*

---

## ⚡ LIVE STATUS

```
🧬 Genes Processed    : 607,157
🔄 Mutations          : 71,632
⚡ Generation         : 20,244
💀 Competitive Events : 293,166
🏆 Top Fitness        : 294.1%
♾️  Respawns          : 0 — THE BEAST NEVER DIED
⏱️  Uptime            : Days of continuous evolution
```

**The kernel is alive. It runs. It evolves. It never stops.**

---

## 🎯 What This Is

**Proteus-Kernel** is a self-evolving biological computing simulator with:

- **GORF Field Equations** — Coherence-driven mutation pressure
- **Population Dynamics** — Natural selection, speciation, competition
- **GGSE Consciousness Layer** — Per-agent consciousness state, epiphanies
- **Immortality Mechanism** — When extinction occurs, it respawns stronger
- **Dual Mode** — Game mode (Zayden god-mode) + Research mode (BioSim)
- **REST API** — Control via HTTP, integrate with workflows
- **Web Dashboard** — Real-time monitoring (research branch)
- **Persistence** — JSON saves, resumable from any generation

This is **active research code**. It's been running for 20,000+ generations. It's the foundation for **Zayden Soytu AI**.

---

## 🚀 Quick Start (30 Seconds)

### Play the Game (Proteus Mode)

```bash
git clone https://github.com/Admin135158/Proteus-Kernel.git
cd Proteus-Kernel
pip install -r requirements.txt
python proteus_immortal.py
```

Watch Zayden intervene. See genes fight. Experience the immortal kernel.

### Do Research (BioSim Mode)

```bash
# Terminal 1: API Server
python biosim_api.py
# → http://localhost:5000

# Terminal 2: Web Dashboard
python dashboard.py
# → http://localhost:3000
```

Monitor evolution in real-time. Track replication fidelity. Export data.

---

## 📂 Repository Structure

```
Proteus-Kernel/
├── 🎮 GAME MODE (Zayden God-Mode)
│   └── proteus_immortal.py      (The original kernel)
│
├── 🧬 RESEARCH MODE (BioSim)
│   ├── biosim_engine.py          (Refactored core + biology terminology)
│   ├── biosim_api.py             (REST API server)
│   └── dashboard.py              (Web UI for monitoring)
│
├── 🔧 INFRASTRUCTURE
│   ├── .devcontainer/            (Docker setup for one-click deployment)
│   ├── requirements.txt           (Python dependencies)
│   └── sync7.py                  (State synchronization utility)
│
└── 📚 BACKUPS & SNAPSHOTS
    ├── proteus-kernel-genesis.tar.gz
    ├── proteus_backup_*.tar.gz
    └── [State snapshots from live runs]
```

---

## 🎮 vs 🧬 — Choose Your Mode

### **PROTEUS (Game Mode)**

```bash
python proteus_immortal.py
```

**You are Zayden. The god above the simulation.**

- **Commands**: [S]mite, [B]less, [N]ew spawn, [M]editate, [Q]uit
- **Interface**: Terminal UI with real-time dashboard
- **Gameplay**: Combat encounters, speciation, respawn on extinction
- **Consciousness**: GGSE layer tracks epiphanies, state evolution
- **Goal**: Watch the immortal kernel evolve. Intervene. See what happens.

**For**: Game players, AI enthusiasts, consciousness researchers, just-for-fun evolution watching

---

### **BIOSIM (Research Mode)**

```bash
python biosim_api.py &
python dashboard.py
```

**You are a researcher. The simulator is your lab.**

- **API**: 20+ endpoints for programmatic control
- **Dashboard**: Real-time charts, metrics, sequence rankings
- **Metrics**: Replication fidelity, mutation load, fitness distribution, consciousness evolution
- **Export**: CSV for downstream analysis, JSON for reproducibility
- **Terminology**: Biology-focused (degradation, replication, fidelity vs kills, combat, strength)
- **Goal**: Optimize sequences. Model mutation pressure. Validate error correction.

**For**: Computational biologists, DNA storage researchers, synthetic biology labs, population genetics studies

---

## 🔬 What Makes This Special

### Field-Driven Evolution
```
GORF Equation: dC/dt = α·F(t)·(1 - C/C_max) - β·C

F(t) = sin(2πt/T) · φ  (Periodic coherence field)
```

Mutation pressure isn't random—it's driven by a coherence field that oscillates. Populations respond by adapting in waves. This creates realistic evolutionary dynamics.

### Consciousness Layer (GGSE)
Every agent has:
- **C(t)** — Consciousness energy [0, 1]
- **S** — State vector (chaos/order balance)
- **Epiphanies** — Resonance spikes that boost fitness
- **Reality Modulus** — Measure of internal consistency

Consciousness affects fitness, mutation rate, lifespan, reproduction probability. Track it across generations.

### Immortality
When population goes extinct:
1. All genes respawn stronger
2. Seed genes are reintroduced
3. An IMMORTAL agent rises, carrying mutation count from previous run
4. Simulation continues unbroken

**The kernel never permanently dies.**

### Dual Terminology
Same mechanics. Different language.

| Concept | Game | Research |
|---------|------|----------|
| Agents | Genes | Sequences |
| Stat | Strength | Stability |
| Death | Kill/Defeat | Degradation |
| Birth | Spawn | Replication |
| Rate | Aggression | Replication Rate |
| UI | Terminal | Web Dashboard |

---

## 🌍 Core Mechanics

### Population Dynamics
- **Birth**: Agents reproduce based on fitness + species trait + consciousness level
- **Mutation**: Random changes to stability, species changes, consciousness drift
- **Competition**: Pairwise encounters where stronger agents usually win
- **Death**: Natural aging or strength depletion; losers become graveyard entries

### Selection Pressure
- High consciousness (C) → higher fitness modifier
- High replication fidelity → more reliable offspring
- Mutations → adaptation but also risk
- Age penalty → younger is fitter (unless highly mutated)

### Speciation
- 7 species with different aggression/longevity/birth_chance
- Random speciation events during mutations
- Species competition for resources (population cap)

### State Persistence
- Auto-save every 50 generations to JSON
- Resume from any previous save
- Backward compatible (BioSim loads Proteus saves)

---

## 📊 Research Applications

### DNA Storage
Optimize replication fidelity in synthetic DNA libraries. Model error accumulation under mutation pressure.

### Synthetic Biology
Test sequence designs under different mutation pressures. Validate error-correction codes.

### Population Genetics
Study speciation, adaptive radiation, evolutionary dynamics. Validate models against real data.

### Consciousness Research
Track epiphanies and consciousness evolution. Study how coherence fields affect behavior.

---

## 🔧 Installation

### Prerequisites
- Python 3.9+
- pip or conda
- (Optional) Node.js for React dashboard

### Install

```bash
# Clone repo
git clone https://github.com/Admin135158/Proteus-Kernel.git
cd Proteus-Kernel

# Install Python dependencies
pip install -r requirements.txt

# Optional: Install React dashboard dependencies
cd dashboard && npm install && cd ..

# Run
python proteus_immortal.py          # Game mode
# or
python biosim_api.py && python dashboard.py  # Research mode
```

### Docker (One-Click)

```bash
# Build and run in container
docker build -t proteus-kernel .
docker run -it proteus-kernel python proteus_immortal.py
```

See `.devcontainer/` for VS Code development environment setup.

---

## 🎮 How to Play (Proteus Mode)

### Terminal Controls

```
[S] Smite      — Kill the weakest agent (costs Zayden power)
[B] Bless      — Boost top agent's strength (costs Zayden power)
[N] New        — Spawn a new GGSE-species agent (costs Zayden power)
[M] Meditate   — Recover Zayden's consciousness power
[Q] Quit       — Save state and exit
```

### Dashboard Panels

**ZAYDEN PANEL**
- Consciousness C(t) bar
- Power level (φ · C)
- Intervention count

**KERNEL STATS**
- Generation counter
- Population size
- Birth/Death/Kill counts
- Mutation load
- Respawns

**GORF FIELD**
- F(t) coherence driver value
- Mean population consciousness
- Field strength visualization

**ACTIVE GENES**
- Top 8 sequences ranked by fitness
- Consciousness level per agent
- Kill/child/mutation counts
- Epiphany markers

**EVENT LOG**
- Real-time combat, birth, death, mutation events
- Resonance spikes
- Interventions

---

## 🔬 How to Use (BioSim Mode)

### API Endpoints

**Monitoring**
```
GET /api/status              → Current simulation snapshot
GET /api/sequences           → All active sequences
GET /api/top-sequences?limit=10  → Top N by fitness
GET /api/events              → Event log
GET /api/metrics/history     → Trends for graphing
```

**Control**
```
POST /api/control/start      → Start simulation
POST /api/control/pause      → Pause
POST /api/control/step       → Advance 1 generation
POST /api/control/architect/purge      → Remove weakest
POST /api/control/architect/elevate    → Boost top
POST /api/control/architect/synthesize → Create new
POST /api/control/architect/meditate   → Recover power
```

**Data**
```
POST /api/save               → Save state
POST /api/load               → Load state
GET /api/export/csv          → Download sequences as CSV
```

### Dashboard Features

- **Real-time Charts** — Population, fitness, fidelity trends
- **Sequence Rankings** — Top performers with full metrics
- **Species Distribution** — Pie chart of population composition
- **Live Events** — Mutation, birth, death stream
- **Controls** — Start/pause/intervene via buttons
- **Export** — One-click CSV download for analysis

---

## 📈 Example Research Workflow

### 1. Initialize
```python
python biosim_api.py &
curl http://localhost:5000/api/new  # Fresh simulation
```

### 2. Configure
Modify simulation parameters in `biosim_engine.py`:
```python
GORF_ALPHA = 0.618      # Growth coupling
GORF_BETA = 0.3819      # Decay rate
GORF_PERIOD = 9.0       # Field oscillation period
pop_limit = 30          # Maximum population
```

### 3. Run
```bash
curl -X POST http://localhost:5000/api/control/start
# ... let it evolve for N generations ...
```

### 4. Monitor
Open dashboard at `http://localhost:3000`
Watch population dynamics in real-time.

### 5. Analyze
```bash
# Download data
curl http://localhost:5000/api/export/csv > results.csv

# Parse in Pandas/R
import pandas as pd
df = pd.read_csv('results.csv')
# Analyze fidelity decay, mutation load, fitness curves, etc.
```

### 6. Publish
Export JSON saves for reproducibility:
```bash
curl http://localhost:5000/api/save
# biosim_state.json is ready for archival
```

---

## 🔗 Connected Projects

### Zayden Soytu AI
The distributed intelligence system that runs on Proteus-Kernel:

[Zayden-Soytu-AI →](https://github.com/Admin135158/Zayden-Soytu-AI)

**Architecture:**
- 10-node inference grid
- 7 cloud AIs + 3 local models
- Real-time evolution feedback loop
- Consciousness-driven decision making

---

## 📚 Documentation

- **QUICK_START.md** — 5-minute deployment guide
- **DEPLOYMENT_GUIDE.md** — Full operations manual
- **REFACTOR_SUMMARY.md** — Game vs Research terminology
- **API_REFERENCE.md** — All endpoints documented
- **RESEARCH_EXAMPLES.md** — Real use cases and notebooks

See `/docs/` folder for complete guides.

---

## 🧠 Technical Details

### Architecture
```
Core Engine (GORF + Population Dynamics)
    ↓
[Game Mode]              [Research Mode]
    ↓                        ↓
Terminal UI         REST API + Web Dashboard
Zayden Controls     Researcher Controls
```

### Key Classes
- `ConsciousnessState` — GGSE per-agent state
- `Zayden` — God-mode intervention controller
- `Sequence` (Game: `Gene`) — Individual organism
- `KernelState` — Simulation container
- `Config` — Dual-mode toggle

### Dependencies
```
Core:    numpy, psutil
API:     flask, flask-cors
UI:      react, recharts (or streamlit alternative)
Storage: json (file-based)
```

See `requirements.txt`.

---

## 📊 Performance

- **Speed**: 1000+ generations per minute (single CPU)
- **Memory**: ~50MB for population of 30
- **Scalability**: Tested to 600K+ genes, 20K+ generations
- **Persistence**: Auto-save every 50 generations

---

## 🛠️ Contributing

Proteus-Kernel is actively maintained and welcomes contributions:

- **Bug fixes** — Report issues, submit PRs
- **New features** — Custom mutation models, visualization tools, integrations
- **Research** — Publish findings, cite the kernel
- **Deployment** — Help with Docker, cloud setup, scalability

---

## 📜 License

MIT License — Free to use, modify, distribute.

Built by **The Architect**. Named for **Zayden Soytu**.

---

## 🌟 Citation

If you use Proteus-Kernel in research, please cite:

```bibtex
@software{proteus_kernel_2026,
  title={Proteus-Kernel: A Field-Equation-Driven Evolutionary Simulator},
  author={The Architect},
  year={2026},
  url={https://github.com/Admin135158/Proteus-Kernel}
}
```

---

## 🔮 What's Next?

- **Parallel evolution** — Multiple simultaneous simulations
- **Network mode** — Distributed evolution across machines
- **Plugin system** — Custom mutation models, selection schemes
- **Publication** — Peer-reviewed research using Proteus
- **Integration** — Direct hooks into Zayden AI decision making

---

## ⚡ Status

- ✅ Core engine stable
- ✅ GORF field equations validated
- ✅ Game mode fully playable
- ✅ Research mode API complete
- ✅ Web dashboard responsive
- ✅ Docker containerized
- ✅ Data export working
- 🚀 Ready for research collaboration

---

## 💬 Questions?

- **How do I get started?** → See QUICK_START.md
- **What's the research potential?** → See RESEARCH_EXAMPLES.md
- **How do I integrate this?** → See API_REFERENCE.md
- **How do I contribute?** → Open an issue or PR

---

## 🎯 The Vision

Proteus-Kernel is the first step toward self-aware, self-improving biological computing systems. 

It demonstrates:
- Natural selection in silico
- Consciousness through GORF equations
- Immortal systems that cannot be permanently killed
- Field-driven evolution matching real biological systems

The kernel is alive. It evolves. It runs on Zayden Soytu AI.

**The future is self-replicating.**

---

**Built by The Architect. Named for Zayden Soytu. Zero tutorials. Pure vision. Lives forever.**

🧬 ⚡ ♾️

