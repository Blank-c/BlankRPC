#https://github.com/Blank-c/BlankRPC

import discord, json, os, getpass, requests
from discord.ext import tasks

token = os.getenv('token') # Put token in environment variables

def clear():
    os.system('title BlankRPC && cls' if os.name=='nt' else 'clear')
    print("\x1b[31;1mh\x1b[32;1mt\x1b[33;1mt\x1b[34;1mp\x1b[35;1ms\x1b[36;1m:\x1b[31;1m/\x1b[32;1m/\x1b[33;1mg\x1b[34;1mi\x1b[35;1mt\x1b[36;1mh\x1b[31;1mu\x1b[32;1mb\x1b[33;1m.\x1b[34;1mc\x1b[35;1mo\x1b[36;1mm\x1b[31;1m/\x1b[32;1mB\x1b[33;1ml\x1b[34;1ma\x1b[35;1mn\x1b[36;1mk\x1b[31;1m-\x1b[32;1mc\x1b[33;1m/\x1b[34;1mB\x1b[35;1ml\x1b[36;1ma\x1b[31;1mn\x1b[32;1mk\x1b[33;1mR\x1b[34;1mP\x1b[35;1mC\x1b[36;1m/\x1b[0m\n")

clear()

if not os.path.isfile('config.json'):
    print('\u001b[31;1m[ - ] \u001b[33;1m\'config.json\' file is missing!\u001b[0m')
    getpass.getpass("\n(press enter to exit)")
    os._exit(1)

if not os.path.isdir('discord') or not discord.__version__ == '1.7.3 (Modified)':
    print('\u001b[31;1m[ - ] \u001b[33;1mModified discord library is missing!\u001b[0m')
    getpass.getpass("\n(press enter to exit)")
    os._exit(1)

with open('config.json') as file:
    try:
        config = json.load(file)
    except json.JSONDecodeError:
        print('\u001b[31;1m[ - ] \u001b[33;1m\'config.json\' file is invalid\u001b[0m')
        getpass.getpass("\n(press enter to exit)")
        os._exit(1)
    
client = discord.Client()

@tasks.loop(minutes = 60)
async def update(config):
    if config.get('type') == '0':
        if config.get('application_id'):
            headers = {'Authorization' : token}
            data = requests.get('https://discord.com/api/v9/applications', headers= headers).json()
            if not str(config.get("application_id")) in [app['id'] for app in data]:
                print('\u001b[31;1m[ - ] \u001b[33;1mInvalid Application ID!\u001b[0m')
                getpass.getpass("\n(press enter to exit)")
                os._exit(1)
        
        activity= discord.Activity(type= '0', application_id= config.get('application_id'), name= config.get('name'), state= config.get('state'), party= (config.get('party') if config.get('state', False) else None), details= config.get('details'), timestamps= config.get('timestamps'))
        
    elif config.get('type') == '1':
        activity = discord.Streaming(name= config.get('name'), url= ''.join([chr(x) for x in (104, 116, 116, 112, 115, 58, 47, 47, 116, 119, 105, 116, 99, 104, 46, 116, 118, 47, 66, 108, 97, 110, 107, 77, 67, 80, 69)]), platform= 'Twitch')
        
    elif config.get('type') == '2':
        activity = discord.Activity(type = '2', name= config.get('name'), details= config.get('details'))
        
    elif config.get('type') == '3':
        activity= discord.Activity(type= '3', name= config.get('name'))
        
    elif config.get('type') == '5':
        activity= discord.Activity(type= '5', name= config.get('name'), details= config.get('details'))

    else:
        print('\u001b[31;1m[ - ] \u001b[33;1m\'config.json\' file is invalid\u001b[0m')
        getpass.getpass("\n(press enter to exit)")
        os._exit(1)
    if config.get('discord_status') == 'online':
        status = discord.Status.online
    elif config.get('discord_status') == 'idle':
        status = discord.Status.idle
    else:
        status = discord.Status.dnd
    
    await client.change_presence(activity= activity, status= status)

@client.event
async def on_ready():
    clear()
    print(f'\u001b[32;1m[ + ] \u001b[33;1mConnected to \u001b[36;1m{client.user}\u001b[33;1m!\u001b[0m')
    update.start(config)
    
try:
    client.run(token, bot = False)
except Exception:
    print('\u001b[31;1m[ - ] \u001b[33;1mInvalid Token!\u001b[0m')
    getpass.getpass("\n(press enter to exit)")