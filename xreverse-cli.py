import requests
requests.packages.urllib3.disable_warnings()
import os
import socket
import re
from bs4 import BeautifulSoup
import concurrent.futures
import httpx
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, Style, init

init(autoreset=True)

ips = []

def free(ip):
    global ips
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.107 Mobile Safari/537.36'
        }
        ips2 = ip.replace('http://', '').replace('https://', '').replace('/', '')
        url = socket.gethostbyname(ips2)
        if url in ips:
            print(f"{Fore.RED}IP already resolved: {url}")
            return
        ips.append(url)
        with httpx.Client() as client:
            response = client.get("https://apiv2.xreverselabs.my.id/?apiKey=ralph&ip="+url, headers=headers)
        get_r = response.json()
        if "domains" in get_r:
         result = get_r["domains"]
         for results in result:
            print("[>] {} >> {} Domains".format(Fore.LIGHTCYAN_EX + ips2 + Fore.RESET, Fore.LIGHTYELLOW_EX + str(len(results))))
            all_domains = []
            all_domains.extend(results)
            unique_domains = list(set(all_domains))  # Remove duplicates
            open('xrevip.txt', 'a').write(unique_domains+"\n")
        else:
            print("BAD IP " + ips2)
            
    except Exception as er:
        print(f"{Fore.RED}Error occurred while parsing JSON: {e} -> {ip}")
        #pass

def revip(url):
    try:
        free(url)
        
    except Exception as e:
        print("Error in revip:", e)

def Main():
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        response = requests.get('https://google.com/')
        if response.status_code == 200:
            print("{}   xReverse | {}#No_Identity - @xxyz4".format(Fore.CYAN, Fore.GREEN))
            print("\t{} IP Reverse {}Private API !\n".format(Fore.GREEN, Fore.YELLOW))
            print("{} Copyright : #No_Identity - {}t.me/xxyz4 !".format(Fore.WHITE, Fore.YELLOW))
            print("{} Telegram Channel : {}t.me/exploi7 !".format(Fore.WHITE, Fore.YELLOW))
            print("{} Site : https://xreverselabs.my.id{} - the best all in one hacking tools !\n".format(Fore.WHITE, Fore.YELLOW))
            try:
                list = input(" root@youez[ip list]:~# ")
                url = open(list, 'r').read().splitlines()
                with concurrent.futures.ThreadPoolExecutor(max_workers=int(20)) as executor:
                        executor.map(revip, url)
            except Exception as e:
                print("Error in Main:", e)
        else:
            print(f"\n{y}[-] {r}CHECK YOUR NETWORK CONNECTION{o}")
    except requests.exceptions.SSLError:
        print("Opps, fuck you.")

if __name__ == '__main__':
    Main()