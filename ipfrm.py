import sys,os,socket
import urllib3
from colorama import init, Fore, Style
from urllib.parse import urlparse, urlunparse

init(autoreset=True)

def remove_path_from_url(url):
     """
     Remove the path from a URL and return only the domain.
    
    :param url: str, the original URL
    :return: str, the URL without the path
    """
     parsed_url = urlparse(url)
     url_without_path = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
     return url_without_path

def getIP(site):
		try:
				IP2 = socket.gethostbyname(sites)
				print("IP: "+IP2)
				open('ips.txt', 'a').write(IP2+'\n')
		except Exception as e:
			print("ERROR -> ", str(e) + sites)
			#pass
			
file_name = input(Style.BRIGHT + Fore.YELLOW + "File list: ")
with open(file_name) as f:
    for i in f:
        getIP(i)