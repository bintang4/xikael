import os
import sys
import requests
import json

def send_msg(text):
    print(text)
    sys.exit()

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

def get2(url, headers):
    response = requests.get(url, headers=headers)
    return response.text

query = input("Query (Dork) : ")

no = 0
i = 0
while True:
    search = get2(f"https://leakix.net/search?scope=leak&page={i}&q={requests.utils.quote(query)}", headers)
    if not search:
        send_msg(f"Done! Max Page {i}")
    if "Invalid API key" in search:
        send_msg("Invalid API key")
    json_data = json.loads(search)
    no += 1

    for i2 in range(len(json_data)):
        event_source = json_data[i2]['event_source']
        ip = json_data[i2]['ip']
        protocol = json_data[i2]['protocol']
        domain = json_data[i2]['host']

        with open("result.txt", "a") as result_file:
            result_file.write(f"{protocol}://{domain}/\n")
        print(f"[{no}] | [{domain} - {ip}] | [{event_source}] | {protocol} -> SAVED")
    
    i += 1
