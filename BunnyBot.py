# mport tracemalloc
# tracemalloc.start()

import logging
import configparser
import os

import discord
from discord import app_commands
from discord.ext import commands

# Setup logging
logs = logging.getLogger("discord").getChild("BunnyBot")
logs.setLevel(logging.INFO)
logs.name = "BunnyBot"
logs.info("Logger ready.")

# Load config
config = configparser.ConfigParser()
config.read('config.ini')
secret = config['BOT']['TOKEN']
cid = config['BOT']['CLIENT_ID']
logs.info("Config loaded")

class BunnyBot(commands.Bot):
    
    def __init__(self, client_id = None):
        logs.info("Initializing BunnyBot...")
        
        my_intents = discord.Intents.default()
        my_intents.message_content = True
        
        super().__init__(
            command_prefix = '?',
            intents = my_intents,
            application_id = client_id,
        )
        
    async def setup_hook(self):
        logs.info("Starting setup_hook...")
        
        n = 0
        
        logs.info("=== Loading extensions ===")
        
        for file in os.listdir('commands'):
            f = os.path.join('commands', file)
            
            if os.path.isfile(f):
                filen = os.path.splitext(file)[0]
                
                if filen != "__template__":     # Dont need to load our template
                    # logs.info(f"Loading extension.. - {filen}")
                    await bot.load_extension(f"commands.{filen}")
                    n += 1
                
        
        logs.info("=== Done loading extensions ===")
        logs.info(f"Bot loaded {n} extensions...")

        
    async def on_ready(self):
        logs.info("BunnyBot is ready")
        

bot = BunnyBot(client_id=cid)
bot.activity = discord.Activity(type=discord.ActivityType.watching, name="all the cuties in this discord")

# Run bot
bot.run(secret)

"""
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ TOP 10 ]")
for stat in top_stats[:10]:
    print(f"{stat.traceback}\n\tCount: {stat.count}\n\tSize: {stat.size}\n")
"""