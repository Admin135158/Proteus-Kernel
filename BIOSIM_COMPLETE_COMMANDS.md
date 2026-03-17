# 🧬 BIOSIM BRANCH — COMPLETE DEPLOYMENT COMMANDS

**Execute these AFTER you've created the biosim branch. These commands deploy the full research infrastructure.**

---

## PHASE 0: SWITCH TO BIOSIM BRANCH

```bash
# Navigate to repo
cd /path/to/Proteus-Kernel

# Switch to biosim branch
git checkout biosim

# Verify you're on biosim
git branch
# Should show: * biosim

# Pull latest biosim code
git pull origin biosim

# Verify biosim files exist
ls -la biosim_engine.py biosim_api.py dashboard.py
# Should show all 3 files
```

---

## PHASE 1: SETUP BIOSIM PYTHON ENVIRONMENT

```bash
# Create virtual environment
python3 -m venv venv_biosim

# Activate environment
source venv_biosim/bin/activate  # macOS/Linux
# OR
venv_biosim\Scripts\activate     # Windows

# Verify activation (should show (venv_biosim) prompt)

# Install core dependencies
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installations
pip list | grep -E "flask|numpy|psutil|recharts"

# Additional BioSim-specific packages
pip install flask-cors
pip install flask-restx
pip install python-dotenv

# Verify all installed
python -c "import flask; import numpy; import psutil; print('✅ All dependencies installed')"
```

---

## PHASE 2: SETUP BIOSIM DATABASE (Optional but Recommended)

```bash
# Create data directory
mkdir -p data/simulations
mkdir -p data/exports

# Create initial state file
cat > data/simulations/default.json << 'EOF'
{
  "generation": 0,
  "total_births": 0,
  "total_degradations": 0,
  "total_replication_events": 0,
  "total_mutations": 0,
  "respawns": 0,
  "genes_processed": 0,
  "start_time": 0,
  "gorf_t": 0.0,
  "mode": "biology",
  "genes": [],
  "graveyard": [],
  "event_log": [],
  "zayden": {
    "consciousness": {
      "C": 0.8,
      "S": [1.0, 0.0],
      "t": 0.0,
      "epiphanies": 0
    },
    "interventions": 0,
    "purges": 0,
    "births_granted": 0,
    "boosts_given": 0
  }
}
EOF

# Create .env file for configuration
cat > .env << 'EOF'
# BioSim Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=0.0.0.0

# Database
DATA_DIR=./data/simulations
EXPORT_DIR=./data/exports

# API
API_TIMEOUT=300
MAX_RESULTS=1000

# Simulation
AUTO_SAVE_INTERVAL=50
TICK_INTERVAL=0.35
RENDER_EVERY=3
EOF

# Load environment variables (optional)
export $(cat .env | xargs)
```

---

## PHASE 3: START BIOSIM API SERVER

### Step 3A: Run API in Development Mode

```bash
# Make sure venv is activated
source venv_biosim/bin/activate

# Start the API server
python biosim_api.py

# Should output:
# 🧬 BioSim Engine API Server
# ==================================================
# Starting REST API on http://localhost:5000
# Simulation loaded from generation XXX
# Or: No save found - starting Genesis...

# Server is now running. Leave this terminal open.
```

### Step 3B: Test API Endpoints (In Another Terminal)

```bash
# Terminal 2: Test the API

# Test health check
curl http://localhost:5000/api/health
# Should return: {"status": "ok", "simulation_loaded": true, "is_running": false}

# Get current status
curl http://localhost:5000/api/status
# Should return: JSON with current simulation metrics

# Start simulation
curl -X POST http://localhost:5000/api/control/start
# Should return: {"status": "started", "generation": XXX}

# Check status again
curl http://localhost:5000/api/status
# Should now show is_running: true

# Get top sequences
curl http://localhost:5000/api/top-sequences?limit=5
# Should return: JSON array of top 5 sequences

# Get recent events
curl http://localhost:5000/api/events?limit=10
# Should return: Last 10 events from event log

# Get metrics history
curl http://localhost:5000/api/metrics/history
# Should return: Current aggregated metrics

# Pause simulation
curl -X POST http://localhost:5000/api/control/pause
# Should return: {"status": "paused"}

# Save simulation state
curl -X POST http://localhost:5000/api/save
# Should return: {"status": "saved", "generation": XXX}

# Export to CSV
curl http://localhost:5000/api/export/csv > biosim_export.csv
# Should create CSV file with all sequences

# Test Architect interventions
curl -X POST http://localhost:5000/api/control/architect/purge
# Should remove weakest sequence

curl -X POST http://localhost:5000/api/control/architect/synthesize
# Should create new sequence

curl -X POST http://localhost:5000/api/control/architect/elevate
# Should boost top sequence

curl -X POST http://localhost:5000/api/control/architect/meditate
# Should recover Architect power
```

---

## PHASE 4: SETUP BIOSIM WEB DASHBOARD

### Step 4A: Install Dashboard Dependencies (Node.js Required)

```bash
# Check if Node.js is installed
node --version
npm --version

# If not installed:
# macOS: brew install node
# Linux: sudo apt-get install nodejs npm
# Windows: Download from nodejs.org

# Create dashboard directory
mkdir -p dashboard-app
cd dashboard-app

# Initialize npm project
npm init -y

# Install React dependencies
npm install react react-dom
npm install recharts
npm install axios
npm install react-scripts

# Create .env for dashboard
cat > .env << 'EOF'
REACT_APP_API_URL=http://localhost:5000/api
EOF

# Install dev dependencies
npm install --save-dev @types/react @types/react-dom

# Verify installations
npm list react recharts axios
```

### Step 4B: Create Dashboard Component

```bash
# Create src directory
mkdir -p src

# Create main App.js
cat > src/App.js << 'EOF'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function BioSimDashboard() {
  const [status, setStatus] = useState(null);
  const [sequences, setSequences] = useState([]);
  const [isRunning, setIsRunning] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statusRes = await axios.get(`${API_URL}/status`);
        setStatus(statusRes.data);
        setIsRunning(statusRes.data.is_running);

        const seqRes = await axios.get(`${API_URL}/top-sequences?limit=8`);
        setSequences(seqRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, [API_URL]);

  const handleStart = async () => {
    await axios.post(`${API_URL}/control/start`);
    setIsRunning(true);
  };

  const handlePause = async () => {
    await axios.post(`${API_URL}/control/pause`);
    setIsRunning(false);
  };

  const handleArchitectAction = async (action) => {
    await axios.post(`${API_URL}/control/architect/${action}`);
  };

  if (!status) return <div>Loading BioSim...</div>;

  return (
    <div style={{ padding: '2rem', background: '#0a0e27', color: '#e0e6ed' }}>
      <h1>🧬 BioSim Engine Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', margin: '2rem 0' }}>
        <div style={{ background: '#1a1f3a', padding: '1rem', borderRadius: '4px' }}>
          <div>Generation: {status.generation}</div>
          <div>Population: {status.population}</div>
        </div>
        <div style={{ background: '#1a1f3a', padding: '1rem', borderRadius: '4px' }}>
          <div>Top Fitness: {status.top_fitness.toFixed(1)}%</div>
          <div>Mean Fidelity: {(status.mean_fidelity * 100).toFixed(1)}%</div>
        </div>
        <div style={{ background: '#1a1f3a', padding: '1rem', borderRadius: '4px' }}>
          <div>Total Births: {status.total_births}</div>
          <div>Mutations: {status.total_mutations}</div>
        </div>
      </div>

      <div style={{ margin: '2rem 0' }}>
        {!isRunning ? (
          <button onClick={handleStart} style={{ padding: '0.5rem 1rem', marginRight: '1rem' }}>▶ Start</button>
        ) : (
          <button onClick={handlePause} style={{ padding: '0.5rem 1rem', marginRight: '1rem' }}>⏸ Pause</button>
        )}
        <button onClick={() => handleArchitectAction('synthesize')} style={{ padding: '0.5rem 1rem', marginRight: '1rem' }}>➕ Synthesize</button>
        <button onClick={() => handleArchitectAction('purge')} style={{ padding: '0.5rem 1rem', marginRight: '1rem' }}>✕ Purge</button>
        <button onClick={() => handleArchitectAction('elevate')} style={{ padding: '0.5rem 1rem' }}>⬆ Elevate</button>
      </div>

      <div>
        <h2>Top Sequences</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #00d9ff' }}>
              <th>Name</th>
              <th>Species</th>
              <th>Fitness</th>
              <th>Fidelity</th>
              <th>Mutations</th>
            </tr>
          </thead>
          <tbody>
            {sequences.map((seq, i) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(0,217,255,0.1)' }}>
                <td>{seq.name}</td>
                <td>{seq.species}</td>
                <td>{seq.fitness.toFixed(1)}</td>
                <td>{(seq.replication_fidelity * 100).toFixed(1)}%</td>
                <td>{seq.mutations}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default BioSimDashboard;
EOF

# Create index.js
cat > src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

# Create public/index.html
mkdir -p public
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#0a0e27" />
  <meta name="description" content="BioSim Engine - Research Dashboard" />
  <title>🧬 BioSim Engine</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      background: #0a0e27;
      color: #e0e6ed;
      font-family: 'Space Mono', monospace;
    }
  </style>
</head>
<body>
  <div id="root"></div>
</body>
</html>
EOF
```

### Step 4C: Start Dashboard Development Server

```bash
# Make sure you're in dashboard-app directory
cd dashboard-app

# Start the development server
npm start

# Should output:
# Compiled successfully!
# You can now view dashboard-app in the browser at:
# http://localhost:3000

# Browser automatically opens. Dashboard is now live.
```

---

## PHASE 5: RUN FULL BIOSIM STACK

### All 3 Terminals Simultaneously

```bash
# TERMINAL 1: API Server
# (Already running from Phase 3A)
# python biosim_api.py
# → http://localhost:5000/api

# TERMINAL 2: Dashboard
# (Already running from Phase 4C)
# npm start
# → http://localhost:3000

# TERMINAL 3: Monitor Simulation
cd /path/to/Proteus-Kernel
source venv_biosim/bin/activate

# Watch the API in real-time
watch -n 2 'curl -s http://localhost:5000/api/status | jq .'

# Or check specific metrics
watch -n 5 'curl -s http://localhost:5000/api/status | jq ".population, .generation, .top_fitness"'
```

---

## PHASE 6: PRODUCTION DEPLOYMENT

### Step 6A: Deploy to Heroku (Free Option)

```bash
# Install Heroku CLI
# macOS: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
# Windows: Download from heroku.com/download

# Login to Heroku
heroku login

# Create Heroku app
heroku create proteus-biosim

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set PORT=5000

# Deploy
git push heroku biosim

# Monitor logs
heroku logs --tail

# View live API
heroku open /api/status

# Live URL: https://proteus-biosim.herokuapp.com/api
```

### Step 6B: Deploy Dashboard to Netlify (Free Option)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build dashboard
cd dashboard-app
npm run build

# Deploy
netlify deploy --prod --dir=build

# Follow prompts, select "Create & configure a new site"
# Live URL: https://your-site.netlify.app
```

### Step 6C: Deploy to AWS (Production)

```bash
# Setup AWS CLI
aws configure

# Create S3 bucket for API logs
aws s3 mb s3://proteus-biosim-logs

# Create EC2 instance
# Launch Ubuntu 22.04 instance
# Install Docker: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY biosim_engine.py biosim_api.py .

EXPOSE 5000

CMD ["python", "biosim_api.py"]
EOF

# Build Docker image
docker build -t proteus-biosim .

# Run container
docker run -p 5000:5000 proteus-biosim

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [account-id].dkr.ecr.us-east-1.amazonaws.com
docker tag proteus-biosim:latest [account-id].dkr.ecr.us-east-1.amazonaws.com/proteus-biosim:latest
docker push [account-id].dkr.ecr.us-east-1.amazonaws.com/proteus-biosim:latest

# Launch ECS task (or use Lambda)
```

---

## PHASE 7: CONTINUOUS MONITORING

```bash
# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash

echo "🧬 BioSim Monitoring Started"

while true; do
  echo "=== $(date) ==="
  curl -s http://localhost:5000/api/status | jq '.generation, .population, .top_fitness, .mean_fidelity'
  sleep 10
done
EOF

# Make executable
chmod +x monitor.sh

# Run monitoring
./monitor.sh
```

---

## PHASE 8: DATA EXPORT & BACKUP

```bash
# Export current simulation as CSV
curl http://localhost:5000/api/export/csv > exports/simulation_$(date +%Y%m%d_%H%M%S).csv

# Save current state
curl -X POST http://localhost:5000/api/save

# Backup biosim_state.json
cp biosim_state.json backups/biosim_state_$(date +%Y%m%d_%H%M%S).json

# Create automated backup script
cat > backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# Backup state
cp biosim_state.json $BACKUP_DIR/biosim_state_$(date +%Y%m%d_%H%M%S).json

# Export CSV
curl -s http://localhost:5000/api/export/csv > $BACKUP_DIR/export_$(date +%Y%m%d_%H%M%S).csv

# Keep only last 10 backups
ls -t $BACKUP_DIR/biosim_state_* | tail -n +11 | xargs rm -f

echo "✅ Backup completed"
EOF

chmod +x backup.sh

# Run backup every hour (cron)
(crontab -l 2>/dev/null; echo "0 * * * * /path/to/backup.sh") | crontab -
```

---

## PHASE 9: TESTING BIOSIM

```bash
# Unit tests
python -m pytest tests/ -v

# Integration tests
python -m pytest tests/integration/ -v

# Performance tests
python -m pytest tests/performance/ --benchmark

# Load testing
# Using Apache Bench or wrk
ab -n 1000 -c 10 http://localhost:5000/api/status

# Stress testing
while true; do
  curl -s http://localhost:5000/api/status > /dev/null
done
```

---

## PHASE 10: TROUBLESHOOTING

```bash
# If API won't start
python -m flask --app biosim_api --debug run

# If port 5000 is in use
lsof -i :5000
kill -9 <PID>

# If venv issues
rm -rf venv_biosim
python3 -m venv venv_biosim
source venv_biosim/bin/activate
pip install -r requirements.txt

# If dashboard won't connect
# Check CORS is enabled in biosim_api.py
# Verify API is running on http://localhost:5000
# Check Network tab in browser DevTools

# If simulation is slow
# Increase TICK_INTERVAL in biosim_engine.py
# Reduce RENDER_EVERY value
# Lower population limit

# If data is corrupted
# Restore from backup
cp backups/biosim_state_[date].json biosim_state.json
curl -X POST http://localhost:5000/api/load
```

---

## COMPLETE COMMAND SUMMARY (Copy-Paste All at Once)

```bash
# 1. Setup BioSim
git checkout biosim
git pull origin biosim
python3 -m venv venv_biosim
source venv_biosim/bin/activate
pip install -r requirements.txt
pip install flask-cors flask-restx python-dotenv

# 2. Setup data directories
mkdir -p data/simulations data/exports backups
cat > .env << 'EOF'
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=0.0.0.0
DATA_DIR=./data/simulations
EXPORT_DIR=./data/exports
EOF

# 3. Start API (Terminal 1)
python biosim_api.py &

# 4. Setup Dashboard (Terminal 2)
cd dashboard-app
npm install
npm start &

# 5. Monitor (Terminal 3)
watch -n 2 'curl -s http://localhost:5000/api/status | jq .'

# 6. Test everything
curl http://localhost:5000/api/health
curl http://localhost:5000/api/status
curl -X POST http://localhost:5000/api/control/start

# 7. Export data
curl http://localhost:5000/api/export/csv > export.csv
curl -X POST http://localhost:5000/api/save
```

---

**BioSim is now FULLY DEPLOYED and RUNNING.** 🚀

Access:
- **API**: http://localhost:5000/api
- **Dashboard**: http://localhost:3000
- **Status**: http://localhost:5000/api/status
