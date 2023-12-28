#!/usr/bin/python3.9
import sys
import requests
import os.path
from nbtlib import nbt

# Playerdata path
pdloc = '/path/to/playerdata/'

# Test for argument
if ( len(sys.argv) < 2 ):
    exit('Please supply a player name as the first argument!')

# Test if player is online
URL = 'insert link here'
r1 = requests.get(url = URL)
plist = r1.text.split("\n")
if sys.argv[1].lower() in [x.lower() for x in plist]:
    exit('Player is online. You can process normally.')

# Convert player name to uuid with mojang api
URL = 'https://api.mojang.com/users/profiles/minecraft/' + sys.argv[1]
r2 = requests.get(url = URL)

# Test if unsuccesful response from mojang api
status = r2.status_code
if (status != 200):
    exit('Unknown player name ' + sys.argv[1] + '. Check the spelling.')

# Convert UUID to file name
uuid = r2.json()['id']
pfile = uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:] + '.dat'

if not os.path.exists(pdloc + pfile):
    exit('File for ' + sys.argv[1] +  ' was not found.')

# Test for enderclear tag and apply if needed
with nbt.load(pdloc + pfile) as pdata:
    if 'jail' not in pdata['Tags']:
        exit('Player does not have jail tag')
    if 'enderclear' in pdata['Tags']:
        exit('Player already had enderclear tag')
    if 'enderclear' not in pdata['Tags']:
        pdata['Tags'].append('enderclear')
    if 'invclear' not in pdata['Tags']:
        pdata['Tags'].append('invclear')
    if 'unjail' not in pdata['Tags']:
        pdata['Tags'].append('unjail')

    print('Added enderclear, invclear and unjail tags to ' + sys.argv[1])