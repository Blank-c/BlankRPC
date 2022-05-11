#https://github.com/Blank-c/BlankRPC

import json, os, getpass, time

def clear():
    os.system('title "Blank RPC Config Generator" && cls' if os.name=='nt' else 'clear')
    print("\x1b[31;1mh\x1b[32;1mt\x1b[33;1mt\x1b[34;1mp\x1b[35;1ms\x1b[36;1m:\x1b[31;1m/\x1b[32;1m/\x1b[33;1mg\x1b[34;1mi\x1b[35;1mt\x1b[36;1mh\x1b[31;1mu\x1b[32;1mb\x1b[33;1m.\x1b[34;1mc\x1b[35;1mo\x1b[36;1mm\x1b[31;1m/\x1b[32;1mB\x1b[33;1ml\x1b[34;1ma\x1b[35;1mn\x1b[36;1mk\x1b[31;1m-\x1b[32;1mc\x1b[33;1m/\x1b[34;1mB\x1b[35;1ml\x1b[36;1ma\x1b[31;1mn\x1b[32;1mk\x1b[33;1mR\x1b[34;1mP\x1b[35;1mC\x1b[36;1m/\x1b[0m\n")
    
def iinput(msg, cumpulsory= False, clean= True):
    while True:
        q = input(f"\u001b[33;1m{msg}\u001b[35;1m{' (Leave empty if you want)' if not cumpulsory else ''}\u001b[33;1m: \u001b[36;1m").strip()
        if len(q) == 0 and cumpulsory:
            print('\n\u001b[31;1mThis is an important field, you cannot leave it empty!\u001b[0m\n')
            continue
        break
    if clean:
        clear()
    if len(q) == 0:
        return None
    return q

clear()

print("\u001b[33;1mWhich type of rich presence do you want?\n\n\u001b[36;1m1 \u001b[33;1m- Playing status\n\u001b[36;1m2 \u001b[33;1m- Streaming status\n\u001b[36;1m3 \u001b[33;1m- Listening status\n\u001b[36;1m4 \u001b[33;1m- Watching status\n\u001b[36;1m5 \u001b[33;1m- Competing status\n")

while True:
    try:
        choice = int(input("Choice: \u001b[36;1m").strip())
        if choice in (1, 2, 3, 4, 5):
            clear()
            break
    except Exception:
        pass
    print("\n\u001b[31;1mInvalid choice, choose from 1 to 5 only!\u001b[36;1m\n")
config = None
while True:
    name = iinput("Name", True)
    if len(name) <= 2:
        print(f"\u001b[31;1mName should be of 2+ characters!\u001b[0m\n")
    else:
        break

if not choice in (2, 4):
    details = iinput("Details")
else:
    details = None

if choice == 1:
    party = None
    state = None
    party_members = None
    max_party_members = None
    application_id = None

    while True:
        application_id = iinput("Application ID", clean=False)
        if not application_id or (application_id.isdigit() and len(application_id) > 17):
            break
        print("\n\u001b[31;1mInvalid Application ID\u001b[0m\n")
    clear()
    
    if application_id:
        state = iinput("State")
    if state:
        while True:
            party_members = iinput("No. of party members", clean= False)
            if not party_members is None:
                if not party_members.isdigit():
                    print("\n\u001b[31;1mEnter digits only!\u001b[0m\n")
                else:
                    break
            else:
                break
        if party_members:
            party_members = int(party_members)

    clear()
    if state and party_members is not None:
        while True:
            max_party_members = iinput("Max party size", clean= False)
            if not max_party_members is None:
                if not max_party_members.isdigit():
                    print("\n\u001b[31;1mEnter digits only!\u001b[0m\n")
                else:
                    if int(max_party_members) < party_members:
                        print("\n\u001b[31;1mMax party size can not be less than party members in it!\u001b[0m\n")
                    else:
                        max_party_members = int(max_party_members)
                        break
            else:
                max_party_members = int(int(party_members))
    
    if party_members is not None and max_party_members is not None:
        party = {'size' : [party_members, max_party_members]}
    start = int(time.time())
    
    config = {'type' : '0', 'application_id' : int(application_id) if application_id else None, 'name' : name, 'details' : details, 'state' : state, 'party' : party, 'timestamps' : {'start' : start}}

if not config:
    if choice != 5:
        choice = choice - 1
    config = {'type' : str(choice), 'name' : name, 'details' : details}

clear()
with open('config.json', 'w') as file:
    json.dump(config, file, indent= 4)
    
print(f"\u001b[32;1mFile saved as '\u001b[35;1m{os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json'))}\u001b[32;1m'\u001b[0m")
getpass.getpass('\n(press enter to exit)')