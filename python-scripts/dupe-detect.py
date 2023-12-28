import os
import requests
import json
from nbtlib import nbt
from webhook import DiscordWebhook

### Config ###
# Max File Size (in bytes)
maxSize = 20000
# Minumnum Book Count
minBooks = 10
# /path/to/playerdata/
dir = '/path/to/playerdata/'

#load known dupers from saved file
with open('/path/to/dupe-detector-list.json', 'r') as f:
    dupers = json.load(f)

# loop through files in playerdata directory
for i in os.listdir(dir):
    # filter only player .dat files
    if i.endswith(".dat"):
        pfile = dir + i
        psize = os.path.getsize(pfile)
        # test if player file size is larger than threshold
        # if so continue to count written_books
        if psize > maxSize:
            book_count = 0
            with nbt.load(pfile) as pdata:
                inv = pdata.root['Inventory']
                for j in inv:
                    if j['id'] == "minecraft:written_book":
                        count = str(j['Count'])
                        book_count += int(count.replace('b',''))
                # test if player has more books than threshold
                # if so continue to ban
                if book_count > minBooks:
                    # convert uuid to player name and send ban command to server
                    uuid = i.replace('.dat','')
                    nodash = uuid.replace('-','')
                    URL = 'https://api.mojang.com/user/profiles/' + nodash + '/names'
                    r = requests.get(url = URL)
                    names = json.loads(r.text)
                    name = names[-1]['name']
                    if name not in dupers:
                        url = 'discord webhook link'
                        content = "Duping action on " + name
                        webhook = DiscordWebhook(url=url, content=content)
                        webhook.execute()
                        dupers.append(name)    
                        print(name)
with open('/path/to/dupe-detector-list.json', 'w') as outfile:
    json.dump(dupers, outfile)