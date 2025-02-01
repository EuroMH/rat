import requests
import time
import threading
import discord
from discord.ext import commands

class Controller:
    def __init__(self, webhook_url, bot_token):
        self.webhook_url = webhook_url
        self.bot_token = bot_token
        self.running = False
        intents = discord.Intents.default()
        intents.messages = True  # This enables receiving messages

        self.bot = commands.Bot(command_prefix="!", intents=intents)

    def send_webhook_message(self, message):
        payload = {'content': message}
        try:
            requests.post(self.webhook_url, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook message: {e}")

    def control_loop(self):
        @self.bot.event
        async def on_ready():
            print(f"Logged in as {self.bot.user.name}")

        @self.bot.command(name="start")
        async def start(ctx):
            if not self.running:
                self.running = True
                self.send_webhook_message("Worker started.")
                threading.Thread(target=self.main_loop).start()
                await ctx.send("Worker started.")
            else:
                await ctx.send("Worker is already running.")

        @self.bot.command(name="stop")
        async def stop(ctx):
            if self.running:
                self.running = False
                self.send_webhook_message("Worker stopped.")
                await ctx.send("Worker stopped.")
            else:
                await ctx.send("Worker is already stopped.")

        @self.bot.command(name="status")
        async def status(ctx):
            if self.running:
                await ctx.send("Worker is running.")
            else:
                await ctx.send("Worker is stopped.")

        self.bot.run(self.bot_token)

    def main_loop(self):
        while self.running:
            time.sleep(10)

if __name__ == "__main__":
    WEBHOOK_URL = "https://discord.com/api/webhooks/1335341177234264217/KfbTw7q3sBrWYPDwacLgF7Sl-M686NB7o59ZEoyegAzqgg3wKqB-tIID9tePm2pewpfR"
    BOT_TOKEN = "MTMzNTM0MzYxNDg4NDA1NzEzOQ.GxR_6p.aTY4VKRO9Qc6f6EDaMOJ7hLX5U18AqZllPg70s"
    controller = Controller(WEBHOOK_URL, BOT_TOKEN)
    controller.control_loop()
