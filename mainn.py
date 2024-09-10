import requests
import json
import os

# Function to send message and exit
def send_msg(text):
    print(text)
    exit()

# Check if 'apikey.txt' exists
if not os.path.exists('apikey.txt'):
    send_msg("Buat file apikey.txt dulu")

# Read API key from file
with open('apikey.txt', 'r') as file:
    apikey = file.read().strip()

# Check if API key is empty
if not apikey:
    send_msg("Masukin apikey dulu di apikey.txt")

headers = {
    'accept': 'application/json',
    'api-key': apikey
}

# Infinite loop to handle user queries
while True:
    query = input("Query (Dork): ")

    no = 0
    i = 0

    while True:
        search = requests.get(f"https://leakix.net/search?scope=leak&page={i}&q={query}", headers=headers).text
        
        if not search or "Invalid API key" in search:
            send_msg("Invalid API key" if "Invalid API key" in search else f"Done! Max Page {i}")

        try:
            data = json.loads(search)
        except json.JSONDecodeError:
            send_msg("Failed to parse JSON response")

        if not data:
            send_msg(f"Done! Max Page {i}")

        no += 1

        for entry in data:
            event_source = entry.get('event_source')
            ip = entry.get('ip')
            protocol = entry.get('protocol')
            domain = entry.get('host')

            with open('result.txt', 'a') as result_file:
                result_file.write(f"{protocol}://{domain}/\n")

            print(f"[{no}] | [{domain} - {ip}] | [{event_source}] | {protocol} -> SAVED")

        i += 1
