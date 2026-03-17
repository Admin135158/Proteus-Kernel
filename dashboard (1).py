#!/usr/bin/env python3
import json
import os
from pathlib import Path
import http.server
import socketserver
import threading
import time
import webbrowser

DNA_PATH = Path.home() / "proteus/dna_store/genes"
PORT = 8080

class ProteusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Get all genes
            genes = []
            for gene_file in sorted(DNA_PATH.glob("*.json"), key=os.path.getmtime, reverse=True):
                try:
                    with open(gene_file) as f:
                        gene = json.load(f)
                        genes.append(gene)
                except Exception as e:
                    print(f"Error reading {gene_file}: {e}")
                    continue
            
            # Calculate stats
            olce_count = sum(1 for g in genes if "OLCE" in g.get("tags", []))
            ggse_count = sum(1 for g in genes if "GGSE" in g.get("tags", []))
            watchdog_count = sum(1 for g in genes if "WATCHDOG" in g.get("tags", []))
            
            # Generate HTML
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>🧬 Proteus DNA Store</title>
    <meta http-equiv="refresh" content="5">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{ 
            font-family: 'Courier New', monospace; 
            background: #0f0f0f; 
            color: #00ff00;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ 
            color: #00ff00; 
            border-bottom: 2px solid #00ff00; 
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 2.5em;
            text-shadow: 0 0 10px #00ff00;
        }}
        h2 {{ color: #00cc00; margin: 20px 0 10px; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{ 
            background: #1a1a1a; 
            padding: 20px; 
            border-radius: 10px;
            border: 1px solid #00ff00;
            text-align: center;
        }}
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            color: #00ff00;
        }}
        .stat-label {{
            color: #888;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .genes-grid {{ 
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .gene-card {{ 
            background: #1a1a1a;
            border: 1px solid #00ff00;
            border-radius: 8px;
            padding: 15px;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}
        .gene-card:hover {{ 
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0, 255, 0, 0.3);
        }}
        .gene-id {{ 
            color: #00ffff; 
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 5px;
        }}
        .gene-tags {{ margin: 10px 0; }}
        .tag {{ 
            display: inline-block;
            background: #00ff00;
            color: #000;
            padding: 2px 10px;
            border-radius: 15px;
            margin: 2px;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .tag.olce {{ background: #ff9900; }}
        .tag.ggse {{ background: #9933ff; color: white; }}
        .tag.watchdog {{ background: #ff3333; color: white; }}
        .timestamp {{ 
            color: #666; 
            font-size: 11px;
            border-top: 1px solid #333;
            padding-top: 8px;
            margin-top: 8px;
        }}
        .error {{ 
            color: #ff9900;
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 5px;
        }}
        .footer {{ 
            margin-top: 40px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #333;
            padding-top: 20px;
        }}
        .status {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }}
        .status.running {{ background: #00ff00; box-shadow: 0 0 10px #00ff00; }}
        .refresh-note {{
            text-align: right;
            color: #666;
            font-size: 11px;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Proteus DNA Store</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(genes)}</div>
                <div class="stat-label">Total Genes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{olce_count}</div>
                <div class="stat-label">OLCE Cycles</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{ggse_count}</div>
                <div class="stat-label">GGSE Insights</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{watchdog_count}</div>
                <div class="stat-label">Watchdog Events</div>
            </div>
        </div>
        
        <h2>📋 Recent Genes</h2>
        <div class="genes-grid">
"""

            # Add genes
            for gene in genes[:8]:  # Show all 8 genes
                tags = gene.get('tags', [])
                tags_html = ''
                for tag in tags:
                    tag_class = tag.lower()
                    if 'olce' in tag_class:
                        tags_html += f'<span class="tag olce">{tag}</span>'
                    elif 'ggse' in tag_class:
                        tags_html += f'<span class="tag ggse">{tag}</span>'
                    elif 'watchdog' in tag_class:
                        tags_html += f'<span class="tag watchdog">{tag}</span>'
                    else:
                        tags_html += f'<span class="tag">{tag}</span>'
                
                error_html = ""
                if 'error' in gene.get('payload', {}):
                    error_val = gene['payload']['error']
                    error_html = f'<div class="error">⚠️ Error: {error_val:.4f}</div>'
                
                html += f"""
            <div class="gene-card">
                <div class="gene-id">🔬 {gene['id']}</div>
                <div class="gene-tags">{tags_html}</div>
                {error_html}
                <div class="timestamp">📅 {gene['created_at']}</div>
            </div>
"""
            
            html += f"""
        </div>
        
        <div class="refresh-note">
            🔄 Auto-refreshes every 5 seconds • Last update: {time.strftime('%H:%M:%S')}
        </div>
        
        <div class="footer">
            🧬 Proteus Cognitive OS • Running on Termux<br>
            <span class="status running"></span> System Active • {len(genes)} genes in DNA store
        </div>
    </div>
</body>
</html>
"""
            
            self.wfile.write(html.encode())
            print(f"[{time.strftime('%H:%M:%S')}] Served dashboard - {len(genes)} genes")
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Not Found")

def start_server():
    """Start the HTTP server"""
    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), ProteusHandler) as httpd:
            print("\n" + "="*50)
            print("🧬 PROTEUS DASHBOARD")
            print("="*50)
            print(f"📁 Gene store: {DNA_PATH}")
            print(f"📊 Total genes: {len(list(DNA_PATH.glob('*.json')))}")
            print("\n🌐 Access dashboard at:")
            print(f"   ➜ http://localhost:{PORT}")
            print(f"   ➜ http://127.0.0.1:{PORT}")
            print("\n📱 On Android, open in browser:")
            print(f"   ➜ http://localhost:{PORT}")
            print("\n⚠️  Make sure you're connected to the internet")
            print("="*50)
            print("\nPress Ctrl+C to stop the server\n")
            
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port {PORT} is already in use!")
            print(f"   Try: pkill -f dashboard.py")
        else:
            print(f"\n❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Proteus DNA Store Dashboard...")
    print(f"📁 Checking for genes in: {DNA_PATH}")
    
    # Check if directory exists
    if not DNA_PATH.exists():
        print(f"⚠️  Gene directory not found! Creating...")
        DNA_PATH.mkdir(parents=True, exist_ok=True)
    
    # Count genes
    gene_count = len(list(DNA_PATH.glob("*.json")))
    print(f"📊 Found {gene_count} genes")
    
    if gene_count == 0:
        print("⚠️  No genes found! Creating genesis gene...")
        try:
            from dna_vfs.store import save_gene
            gid = save_gene({"type": "genesis", "message": "Dashboard genesis"}, 
                          tags=["genesis", "dashboard"])
            print(f"✅ Created genesis gene: {gid}")
        except Exception as e:
            print(f"❌ Could not create genesis gene: {e}")
    
    start_server()
