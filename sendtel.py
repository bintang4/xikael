import re,os
import requests

def send_telegram_file(file_path, caption):
    url = f"https://api.telegram.org/bot6258586547:AAFhXNBPJDCRQJ-1Mmj0OkSG3mHvmAbmk-0/sendDocument"
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': 5981225273, 'caption': caption}
        response = requests.post(url, data=data, files=files)
    return response

print(" TOOLS SEND FILE TO TELEGRAM ")
filees = input("Files -> ")
send_telegram_file(filees, "FILES")
