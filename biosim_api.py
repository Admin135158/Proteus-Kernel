#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║           BioSim Engine REST API Wrapper                         ║
║           Exposes simulation as HTTP endpoints                   ║
║           Used by web dashboards & research tools               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import threading
import time
from dataclasses import asdict
from typing import Optional, Dict, List
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import csv
import io
from datetime import datetime

# Import BioSim Engine
from biosim_engine import (
    KernelState, Zayden, Sequence, ConsciousnessState,
    save_state, load_state, seed_genes, evolve_tick,
    coherence_driver, SPECIES_TRAITS
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from web dashboard

# ─────────────────────────────────────────────
#  GLOBAL SIMULATION STATE
# ─────────────────────────────────────────────
simulation_state: Optional[KernelState] = None
simulation_thread: Optional[threading.Thread] = None
is_running = False
simulation_speed = 1.0  # Multiplier for tick interval

# ─────────────────────────────────────────────
#  SIMULATION LOOP (Background Thread)
# ─────────────────────────────────────────────
def simulation_loop():
    """Run the simulation in background thread"""
    global simulation_state, is_running
    
    TICK_INTERVAL = 0.35 / simulation_speed
    
    while is_running:
        if simulation_state:
            evolve_tick(simulation_state)
            
            # Auto-save every 50 generations
            if simulation_state.generation % 50 == 0:
                save_state(simulation_state)
        
        time.sleep(TICK_INTERVAL)

# ─────────────────────────────────────────────
#  API ENDPOINTS
# ─────────────────────────────────────────────

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current simulation status"""
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    alive = [g for g in simulation_state.genes if g.alive]
    species_counts = {}
    for g in alive:
        species_counts[g.species] = species_counts.get(g.species, 0) + 1
    
    return jsonify({
        "generation": simulation_state.generation,
        "population": len(alive),
        "total_births": simulation_state.total_births,
        "total_degradations": simulation_state.total_degradations,
        "total_replication_events": simulation_state.total_replication_events,
        "total_mutations": simulation_state.total_mutations,
        "respawns": simulation_state.respawns,
        "uptime": simulation_state.uptime(),
        "is_running": is_running,
        "gorf_t": simulation_state.gorf_t,
        "gorf_f": coherence_driver(simulation_state.gorf_t),
        "mean_consciousness": simulation_state.mean_consciousness(),
        "mean_fidelity": simulation_state.mean_replication_fidelity(),
        "top_fitness": simulation_state.top_fitness(),
        "species_counts": species_counts,
        "architect_c": simulation_state.zayden.C,
        "architect_power": simulation_state.zayden.power,
    })

@app.route('/api/sequences', methods=['GET'])
def get_sequences():
    """Get all active sequences with full details"""
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    alive = sorted(
        [g for g in simulation_state.genes if g.alive],
        key=lambda g: g.fitness(),
        reverse=True
    )
    
    sequences = []
    for seq in alive:
        sequences.append({
            "name": seq.name,
            "species": seq.species,
            "stability": seq.stability,
            "fitness": seq.fitness(),
            "age": seq.age,
            "replication_events": seq.replication_events,
            "offspring": seq.offspring,
            "mutations": seq.mutations,
            "consciousness_c": seq.consciousness.C,
            "consciousness_epiphanies": seq.consciousness.epiphanies,
            "replication_fidelity": seq.replication_fidelity,
        })
    
    return jsonify({
        "count": len(sequences),
        "sequences": sequences,
    })

@app.route('/api/top-sequences', methods=['GET'])
def get_top_sequences():
    """Get top N sequences by fitness"""
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    limit = request.args.get('limit', 10, type=int)
    alive = sorted(
        [g for g in simulation_state.genes if g.alive],
        key=lambda g: g.fitness(),
        reverse=True
    )[:limit]
    
    sequences = []
    for seq in alive:
        sequences.append({
            "name": seq.name,
            "species": seq.species,
            "fitness": seq.fitness(),
            "stability": seq.stability,
            "replication_events": seq.replication_events,
            "offspring": seq.offspring,
            "mutations": seq.mutations,
            "replication_fidelity": seq.replication_fidelity,
            "consciousness_c": seq.consciousness.C,
        })
    
    return jsonify(sequences)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get recent events from log"""
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    limit = request.args.get('limit', 50, type=int)
    events = simulation_state.event_log[-limit:]
    
    return jsonify({
        "total": len(simulation_state.event_log),
        "events": events,
    })

@app.route('/api/metrics/history', methods=['GET'])
def get_metrics_history():
    """Get aggregated metrics (for graphing)"""
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    # This is a simplified version — in production, you'd store snapshots
    return jsonify({
        "generation": simulation_state.generation,
        "population": len([g for g in simulation_state.genes if g.alive]),
        "births": simulation_state.total_births,
        "degradations": simulation_state.total_degradations,
        "mutations": simulation_state.total_mutations,
        "mean_consciousness": simulation_state.mean_consciousness(),
        "mean_fidelity": simulation_state.mean_replication_fidelity(),
    })

# ─────────────────────────────────────────────
#  CONTROL ENDPOINTS
# ─────────────────────────────────────────────

@app.route('/api/control/start', methods=['POST'])
def start_simulation():
    """Start/resume simulation"""
    global is_running, simulation_state, simulation_thread
    
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    if is_running:
        return jsonify({"status": "already running"}), 200
    
    is_running = True
    simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
    simulation_thread.start()
    
    return jsonify({"status": "started", "generation": simulation_state.generation})

@app.route('/api/control/pause', methods=['POST'])
def pause_simulation():
    """Pause simulation"""
    global is_running
    is_running = False
    return jsonify({"status": "paused", "generation": simulation_state.generation if simulation_state else 0})

@app.route('/api/control/step', methods=['POST'])
def step_simulation():
    """Execute one generation"""
    global is_running, simulation_state
    
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    if is_running:
        return jsonify({"error": "Pause simulation to step"}), 400
    
    evolve_tick(simulation_state)
    
    return jsonify({
        "status": "stepped",
        "generation": simulation_state.generation,
        "population": len([g for g in simulation_state.genes if g.alive]),
    })

@app.route('/api/control/architect/<action>', methods=['POST'])
def architect_action(action: str):
    """Execute Architect intervention"""
    global simulation_state
    
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    action = action.lower()
    result = None
    
    if action == "purge":
        result = simulation_state.zayden.purge(simulation_state)
    elif action == "elevate":
        result = simulation_state.zayden.elevate(simulation_state)
    elif action == "synthesize":
        result = simulation_state.zayden.synthesize(simulation_state)
    elif action == "meditate":
        result = simulation_state.zayden.meditate()
    else:
        return jsonify({"error": f"Unknown action: {action}"}), 400
    
    return jsonify({
        "action": action,
        "result": result,
        "architect_c": simulation_state.zayden.C,
        "architect_power": simulation_state.zayden.power,
    })

@app.route('/api/control/speed', methods=['POST'])
def set_speed():
    """Set simulation speed multiplier"""
    global simulation_speed
    data = request.json
    speed = data.get('speed', 1.0)
    
    if speed <= 0:
        return jsonify({"error": "Speed must be > 0"}), 400
    
    simulation_speed = speed
    return jsonify({"speed": simulation_speed})

# ─────────────────────────────────────────────
#  FILE OPERATIONS
# ─────────────────────────────────────────────

@app.route('/api/load', methods=['POST'])
def load_simulation():
    """Load saved simulation"""
    global simulation_state, is_running
    
    is_running = False
    state = load_state()
    
    if not state:
        return jsonify({"error": "No save file found"}), 404
    
    simulation_state = state
    return jsonify({
        "status": "loaded",
        "generation": state.generation,
        "population": len([g for g in state.genes if g.alive]),
        "total_births": state.total_births,
    })

@app.route('/api/new', methods=['POST'])
def new_simulation():
    """Start fresh simulation"""
    global simulation_state, is_running
    
    is_running = False
    simulation_state = KernelState(mode="biology")
    seed_genes(simulation_state)
    
    return jsonify({
        "status": "created",
        "generation": 0,
        "population": len(simulation_state.genes),
    })

@app.route('/api/save', methods=['POST'])
def save_simulation():
    """Manually save simulation"""
    global simulation_state
    
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    save_state(simulation_state)
    
    return jsonify({
        "status": "saved",
        "generation": simulation_state.generation,
        "filename": "biosim_state.json",
    })

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export current sequences as CSV"""
    global simulation_state
    
    if not simulation_state:
        return jsonify({"error": "No simulation loaded"}), 404
    
    alive = sorted(
        [g for g in simulation_state.genes if g.alive],
        key=lambda g: g.fitness(),
        reverse=True
    )
    
    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "name", "species", "fitness", "stability", "age",
            "replication_events", "offspring", "mutations",
            "consciousness_c", "consciousness_epiphanies",
            "replication_fidelity"
        ]
    )
    writer.writeheader()
    
    for seq in alive:
        writer.writerow({
            "name": seq.name,
            "species": seq.species,
            "fitness": f"{seq.fitness():.2f}",
            "stability": f"{seq.stability:.2f}",
            "age": seq.age,
            "replication_events": seq.replication_events,
            "offspring": seq.offspring,
            "mutations": seq.mutations,
            "consciousness_c": f"{seq.consciousness.C:.4f}",
            "consciousness_epiphanies": seq.consciousness.epiphanies,
            "replication_fidelity": f"{seq.replication_fidelity:.4f}",
        })
    
    bytes_io = io.BytesIO(output.getvalue().encode())
    return send_file(
        bytes_io,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"biosim_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

# ─────────────────────────────────────────────
#  HEALTH CHECK
# ─────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "ok",
        "simulation_loaded": simulation_state is not None,
        "is_running": is_running,
    })

# ─────────────────────────────────────────────
#  STARTUP
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🧬 BioSim Engine API Server")
    print("=" * 50)
    print("Starting REST API on http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /api/status              — Current simulation state")
    print("  GET  /api/sequences           — All active sequences")
    print("  GET  /api/top-sequences       — Top N sequences by fitness")
    print("  GET  /api/events              — Recent events")
    print("  POST /api/control/start       — Start simulation")
    print("  POST /api/control/pause       — Pause simulation")
    print("  POST /api/control/step        — Step one generation")
    print("  POST /api/control/architect/* — Purge, Elevate, Synthesize, Meditate")
    print("  POST /api/load                — Load saved simulation")
    print("  POST /api/new                 — Create new simulation")
    print("  POST /api/save                — Save simulation")
    print("  GET  /api/export/csv          — Export sequences as CSV")
    print("\nDocs: http://localhost:5000/api/status")
    print("=" * 50)
    print()
    
    # Load or create initial state
    simulation_state = load_state()
    if not simulation_state:
        simulation_state = KernelState(mode="biology")
        seed_genes(simulation_state)
    
    app.run(debug=False, host='0.0.0.0', port=5000)
