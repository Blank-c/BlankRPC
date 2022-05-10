#https://github.com/Blank-c/BlankRPC

import websocket, threading, json, time, os, requests

token = os.getenv("token") #Put your user token inside environmental variables as "token" (without quotes)

with open("config.json") as f:
    config = json.load(f)

memory = {
    "ack" : [0, False],
    "resume" : False,
    "session_id" : None,
    "seq" : "null",
    "heartbeat_interval" : 0,
    "connection" : 0,
    "error" : None}

class InvalidSession(Exception): #9
    """Gateway limit exceeded, try again after some time!"""

config[0]["assets"] = {"large_text" : "BlankRPC"}
config[0]["url"] = "https://youtube.com/channel/UCKZJEX2VifHDOpuN1KU16Gw"

"""No changes are recommended in the above two values"""

def get_headers(auth = None):
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 RuxitSynthetic/1.0 v6495571190082640575 t5902745343625328559 ath1fb31b7a altpriv cvcv=2 smf=0'
    }
    if auth:
        headers['authorization'] = auth
    return headers

def receive(socket):
    resp = socket.recv()
    global memory
    if resp:
        resp = json.loads(resp)
        if resp.get("op") == 1:
            heartbeat(socket, 0, True)
        elif resp.get("op") == 0:
            memory["seq"] = resp.get('s', "null")
        elif resp.get("op") == 9:
            memory["error"] = 9
            memory["connection"] = 0
            ws.close()
        return resp
    
def send(socket, payload):
    socket.send(json.dumps(payload))

def connect(socket):
    identify_payload = {
            "op" : 2,
            "d" : {
                "token" : token,
                "properties" : {
                    "$os" : "windows",
                    "$browser" : "chrome",
                    "$device" : "pc"
                }
            }
        }
        
    send(socket, identify_payload)
    resp = receive(socket)
    global memory
    memory['session_id'] = resp.get('session_id')
    memory['connection'] = 1
    
def resume(socket):
    resume_payload = {
        "op" : 6,
        "d" : {
            "token" : token,
            "session_id" : memory.get("session_id"),
            "seq" : memory.get("seq")
        }
    }
    send(socket, resume_payload)
    resp = receive(socket)
    if resp.get('op') == 2:
        time.sleep(5)
        connect(socket)
    
def presence_update(socket):
    presence_payload = {
        "op" : 3,
        "d" : {
            "since" : "null",
            "activities" : config,
            "status" : "dnd", #Change to online or idle if you want
            "afk" : False
        }
    }
    send(socket, presence_payload)

def heartbeat_ack(socket):
    resp = receive(socket)
    if resp:
        if resp.get('op') == 11:
            global memory
            memory["ack"][1] = True
    
def heartbeat(socket, interval = None, emergency = False):
    global memory
    if not interval:
        interval = memory.get("heartbeat_interval")
    while True:
        time.sleep(interval)
        if memory["ack"][0] == 1 and not memory["ack"][1]:
            socket.close(1001)
            socket = None
            memory["error"] : 1001
            break
        payload = {
            "op" : 1,
            "d" : memory.get("seq")
        }
        send(socket, payload)
        if emergency:
            break
        memory["ack"][1] = False
        if memory["ack"][0] == 0:
            memory["ack"][0] = 1
        threading.Thread(target=heartbeat_ack, args=(socket,)).start()
        
if not token or requests.get('https://discord.com/api/v9/users/@me', headers = get_headers(token)).status_code != 200:
    print("Invalid Token")
    os._exit(1)
    
while True:
    ws = websocket.WebSocket()
    try:
        if memory.get("error") == 9:
            raise InvalidSession
        else:
            pass
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        handshake_hello = receive(ws)
        heartbeat_interval = handshake_hello['d']['heartbeat_interval'] / 1000
        memory["heartbeat_interval"] = heartbeat_interval
        threading.Thread(target=heartbeat, args=(ws, heartbeat_interval)).start()
        if memory.get('connection') == 0 or memory.get('session_id') is None:
            connect(ws)
        else:
            resume(ws)
        print("Connected!")
        while True:
            presence_update(ws)
            time.sleep(10)
    except AttributeError:
        pass
    except Exception:
        pass
