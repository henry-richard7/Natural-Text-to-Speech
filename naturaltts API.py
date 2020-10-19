import cfscrape
import random
from requests import Session
import json
from terminaltables import AsciiTable
from tqdm import tqdm
from art import text2art
from colorama import init
from termcolor import colored

init()
art = text2art("Natural Text-to-Speech")
print(colored(art, "cyan"))
print(colored("Developed By Henry Richard J", "blue"))

chunk_size = 1

Voice_engine_table = [["Index", "Voice Type"],
                      ["1.", "Ivy Female US English"],
                      ["2.", "Joanna Female US English"],
                      ["3.", "Joey Male US English"],
                      ["4.", "Justin Male US English"]]

runner = cfscrape.create_scraper()
session = Session()


def get_socks4():
    url = "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all"
    r = runner.get(url).text
    all_proxies = r.split()

    return {"https": f"socks4://{random.choice(all_proxies)}"}


def proxy_request(req_type, url, **kwargs):
    while 1:
        try:

            proxy = get_socks4()

            r = session.request(req_type, url, proxies=proxy, timeout=5, **kwargs)
            break
        except:

            print("[*] Proxy Error")

            pass
    return r


def convert_To_Speech(message):
    url = "https://api.naturaltts.com/v1/converter/free"
    headers = {
        'authority': 'api.naturaltts.com',
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer null',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://naturaltts.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://naturaltts.com/',
        'accept-language': 'en-US,en;q=0.9,mt;q=0.8',
    }

    table = AsciiTable(Voice_engine_table)
    print(table.table)

    choice = int(input("Index of the voice to use: "))

    save_name = input("Enter name for the file: ")

    if choice == 1:

        voiceID = "Ivy"
        gender = "Female"

    elif choice == 2:

        voiceID = "Joanna"
        gender = "Female"

    elif choice == 3:

        voiceID = "Joey"
        gender = "Male"

    elif choice == 4:

        voiceID = "Justin"
        gender = "Male"

    else:
        print("[*] Invalid Option Exiting.......")
        exit()

    data = {"text": message,
            "voiceId": voiceID,
            "lang": "US English",
            "gender": gender,
            "engine": "standard"}

    result = proxy_request("post", url, headers=headers, data=json.dumps(data)).json()
    print("[*] Successfully Converted To Speech")
    print(result['task']['OutputUri'])

    r = runner.get(result['task']['OutputUri'], stream=True)

    total_size = int(r.headers['content-length'])

    with open(f"Voices/{save_name}.mp3", 'wb') as f:
        for data in tqdm(iterable=r.iter_content(chunk_size=chunk_size), total=total_size / chunk_size, unit='KB'):
            f.write(data)


message = input("Enter your message: ")
if len(message) <= 200:
    convert_To_Speech(message)
else:
    print("[*] Sorry the message length should not be more than 200")
