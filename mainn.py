import os
import requests
import sys
import json

def send_msg(text):
    print(text)
    sys.exit()

# Check if apikey.txt exists and read the API key
if not os.path.exists('apikey.txt'):
    send_msg("Buat file apikey.txt dulu")

with open('apikey.txt', 'r') as file:
    apikey = file.read().strip()

if not apikey:
    send_msg("Masukin apikey dulu di apikey.txt")

headers = {
    'accept': 'application/json',
    'api-key': apikey
}

# Main loop to process queries
while True:
    query = input("Query (Dork) : ").strip()
    
    no = 0
    i = 0

    while True:
        url = f"https://leakix.net/search?scope=leak&page={i}&q={requests.utils.quote(query)}"
        search = requests.get(url, headers=headers).text

        if not search:
            send_msg(f"Done! Max Page {i}")
        
        if "Invalid API key" in search:
            send_msg("Invalid API key")
        
        json_data = json.loads(search)
        no += 1

        for item in json_data:
            event_source = item['event_source']
            ip = item['ip']
            protocol = item['protocol']
            domain = item['host']

            with open("result.txt", "a") as result_file:
                result_file.write(f"{protocol}://{domain}/\n")
            
            print(f"[{no}] | [{domain} - {ip}] | [{event_source}] | {protocol} -> SAVED")
        
        i += 1

def post(url, data):
    response = requests.post(url, data=data)
    return response.text

def get(url):
    response = requests.get(url)
    return response.text

def post2(url, data, headers):
    response = requests.post(url, data=data, headers=headers)
    return response.text

def get2(url, headers):
    response = requests.get(url, headers=headers)
    return response.text

def random(jumlah):
    from random import shuffle
    digits = list('1234567890')
    shuffle(digits)
    return ''.join(digits[:jumlah])