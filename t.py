# -*- coding: utf-8 -*-
import requests,socket
requests.packages.urllib3.disable_warnings()
from concurrent.futures import ThreadPoolExecutor
import urllib3
from urllib.parse import urlparse, urlunparse


def remove_path_from_url(url):
     """
     Remove the path from a URL and return only the domain.
    
    :param url: str, the original URL
    :return: str, the URL without the path
    """
     parsed_url = urlparse(url)
     url_without_path = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
     return url_without_path

def execute(url):
 if "://" in url:
      url = url
 else:
	  url = "http://"+url
 if url.endswith('/'):
	  url = url[:-1]
 try:
		prourls = []
		r = requests.get(url, timeout=10)
		processed_url = remove_path_from_url(r.url)
		prourls.append(processed_url)
		for url in prourls:
		 print(url)
		 simpan = open('urlnew.txt', 'a')
		 simpan.write(url+'\n')
		 simpan.close()
 except Exception as er:
		print(er)

def main():
    """
    Main function to read URLs from a file and execute concurrently.
    """
    urls = input('Urls ? ')
    opened_urls = open(urls, 'r', errors="ignore").read().splitlines()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(execute, opened_urls)

if __name__ == '__main__':
    main()