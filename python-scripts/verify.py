#!/usr/bin/env python3.9

import socket
import sys
import json
from utils import MCUtils
import asyncio
import random
import string
import subprocess


try:
    player = sys.argv[1]
except IndexError:
    exit("No argument was supplied for player name")


async def main():
    try:
        code = await random_str(16)
        uuid = await MCUtils.ign_to_uuid(player)
        base_color = "#85A5DF"
        link_color = "#6864DF"
        await socket_client(code, uuid)
        tellraw_json = ["",
            {
                "text":"> ",
                "bold":True,
                "color":"#3E71FF"
            },
            {
                "text": "Verify your account on the ",
                "color": f"{base_color}"
            },
            {
                "text": "Discord",
                "color": f"{link_color}",
                "clickEvent": {
                    "action": "open_url",
                    "value": "https://discord.gg/8tFZa7VWvy"
                }
            },
            {
                "text": " server\\n",
                "color": f"{base_color}"
            },
            {
                "text":"> ",
                "bold":True,
                "color":"#3E71FF"
            },
            {
                "text": "Click on the code: ",
                "color": f"{base_color}"
            },
            {
                "text": f"{code}", "color": f"{link_color}",
                "clickEvent": {
                    "action": "copy_to_clipboard",
                    "value": f"{code}"
                },
                "hoverEvent":{
                    "action": "show_text",
                    "contents":["Copy to clipboard"]
                }
            }
        ]
        tellraw_json_2 = ["",
            {
                "text":"> ",
                "bold":True,
                "color":"#3E71FF"
            },
            {
                "text":"Paste the code in the Verify Account box in the discord-rules channel",
                "color": f"{base_color}"
            }
        ]
        await send_to_screen("tellraw", player, json.dumps(tellraw_json))
        await send_to_screen("tellraw", player, json.dumps(tellraw_json_2))
    except socket.error:
        await send_to_screen("tell", player, "Error, please contact a staff member for help.")


async def send_to_screen(command, player, message):
    subprocess.run(f"screen -S screen_name -X stuff '{command} {player} {message}'\015", shell=True)


async def socket_client(code, uuid):

    host = "insert host"
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    json_payload = {
        "command": "verify",
        "uuid": str(uuid),
        "code": str(code)
    }
    s.sendall(bytes(json.dumps(json_payload), "utf8"))
    s.close()


async def random_str(size):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=size))


if __name__ == '__main__':
    asyncio.run(main()