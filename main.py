import asyncio
import aiohttp
import aiohttp.web # Handling http exceptions
import base64
import os
import colorama
from colorama import Fore
import json

os.system('cls' if os.name == 'nt' else 'clear')
colorama.init()

class Skin:
    def __init__(self, name:str,url:str,uuid:str) -> None:
        self.name = name
        self.url = url
        self.hash = url.split("/")[4]
        self.uuid = uuid

class Cape:
    def __init__(self, name:str,url:str,uuid:str) -> None:
        self.name = name
        self.url = url
        self.hash = url.split("/")[4]
        self.uuid = uuid

class OptifineCape:
    def __init__(self, name:str,url:str) -> None:
        self.name = name
        self.url = url


class MojangAPI:
    @staticmethod
    async def GetPlayerUUID(name:str) -> str:

        async with aiohttp.ClientSession() as s:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
                'Accept':"*/*"
            }
            try:
             async with s.get(url=f'https://api.mojang.com/users/profiles/minecraft/{name}',headers=headers) as response:
                id = await response.json()
                return id["id"]
                
            except aiohttp.web.HTTPClientError as e:
                return e.reason
            
    @staticmethod
    async def GetPlayerInfo(uuid:str) -> str:
        async with aiohttp.ClientSession() as s:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
                'Accept':"*/*"
            }
            try:
             async with s.get(url=f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}',headers=headers) as response:
                json = await response.json()
                return ConvertFromBase64toString(json["properties"][0]["value"])
                
            except aiohttp.web.HTTPClientError as e:
                return e.reason
    @staticmethod
    async def GetOptifineCape(username:str) -> str: # Optifine cape

        async with aiohttp.ClientSession() as s:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
                'Accept':"*/*"
            }
            try:
             async with s.get(url=f'http://s.optifine.net/capes/{username}.png',headers=headers) as response:
                if response.status == 200:
                    return f'http://s.optifine.net/capes/{username}.png'
                else:
                    return "400 response"
                
            except aiohttp.web.HTTPClientError as e:
                return e.reason
            except Exception as e:
                return str(e)


# A Function to read user inputs

async def GetChoice():
    try:
     target = input(Fore.GREEN + "[+] " + Fore.LIGHTMAGENTA_EX + "Target IGN: " + Fore.RESET)
     if not target:
        print("[+] Error Null String.")
        os.system('cls' if os.name == 'nt' else 'clear')
        await GetChoice()
     os.system('cls' if os.name == 'nt' else 'clear')
     choice = int(input(Fore.MAGENTA + '[+] Choose:\n[1] Skin\n[2] Minecon Cape\n[3] Optifine Cape\n' + Fore.RESET))
     if choice == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        skin = await GetPlayerSkin(target)
        print(f'{Fore.MAGENTA}[Username] {Fore.LIGHTBLUE_EX}{skin.name}\n{Fore.MAGENTA}[URL] {Fore.LIGHTBLUE_EX}{skin.url}\n{Fore.MAGENTA}[Hash] {Fore.LIGHTBLUE_EX}{skin.hash}\n{Fore.MAGENTA}[UUID] {Fore.LIGHTBLUE_EX}{skin.uuid}')
        print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Press Any key to continue..." + Fore.RESET)
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        await GetChoice()
     elif choice == 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        cape = await GetPlayerCape(target)
        if cape == None:
            print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Error: Maybe the player dosent has a cape?" + Fore.RESET)
            print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Press Any key to continue..." + Fore.RESET)
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
            await GetChoice()
        print(f'{Fore.MAGENTA}[Username] {Fore.LIGHTBLUE_EX}{cape.name}\n{Fore.MAGENTA}[URL] {Fore.LIGHTBLUE_EX}{cape.url}\n{Fore.MAGENTA}[Hash] {Fore.LIGHTBLUE_EX}{cape.hash}\n{Fore.MAGENTA}[UUID] {Fore.LIGHTBLUE_EX}{cape.uuid}')
        print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Press Any key to continue..." + Fore.RESET)
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        await GetChoice()
     elif choice == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        cape = await MojangAPI.GetOptifineCape(target)
        if target in cape:
            print("[+] Cape URL : " + cape)
        elif '400' in cape:
            print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Player dosent has a cape." + Fore.RESET)
        else:
            print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Error: Maybe the player dosent has a cape?" + Fore.RESET)
        print(Fore.MAGENTA + "[+] " + Fore.LIGHTBLUE_EX + "Press Any key to continue" + Fore.RESET)
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        await GetChoice()
     
    except Exception as e:
     if 'Attempt to decode JSON with unexpected mimetype' in str(e):
        print("[+] Error: Player Not Found\n[+] Press any key to try again..")
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        await GetChoice()
    else:
        print("[+] Error: Player dosent exist or dont have skin or cape.\n[+] Press Any Key to Continue..")
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        await GetChoice()
    
def ConvertFromBase64toString(text:str) -> str: # he player information are bas64 encoded so we need that method to decode the base64 string
    return base64.b64decode(text).decode('utf-8')

    
async def GetPlayerSkin(username:str) -> Skin: # Get The Player Skin
    uuid = await MojangAPI.GetPlayerUUID(username)
    Info = json.loads(await MojangAPI.GetPlayerInfo(uuid))
    return Skin(Info['profileName'],Info['textures']['SKIN']['url'],uuid)

async def GetPlayerCape(username:str) -> Cape: # Minecon Cape
    try:
     uuid = await MojangAPI.GetPlayerUUID(username)
     Info = json.loads(await MojangAPI.GetPlayerInfo(uuid))
     return Cape(Info['profileName'],Info['textures']['CAPE']['url'],uuid)
    except:
        return None


if __name__ == '__main__':
    print(Fore.LIGHTMAGENTA_EX + '''\t\t\t      |\      _,,,---,,_
\t\t\tZZZzz /,`.-'`'    -.  ;-;;,_
\t\t\t     |,4-  ) )-,_. ,\ (  `'-'
\t\t\t    '---''(_/--'  `-'\_)\n\n\t\t\t[+] Made by Raz\n\n\n''' + Fore.RESET)
    try:
     asyncio.run(GetChoice())
    except RuntimeError:
        pass
    except KeyboardInterrupt:
        print(Fore.RED + "[+] Program Closed."+ Fore.RESET)
        
        