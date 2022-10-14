import logging
import configparser
import os

import discord
from discord.ext import commands


# Setup logging
logs = logging.getLogger("discord").getChild("BunnyBot")
logs.setLevel(logging.INFO)
logs.name = "BunnyBot"
logs.info("Logger ready.")

# Load config
config = configparser.ConfigParser()
config.read('config.ini')
secret = config['BOT']['TOKEN2']
cid = config['BOT']['CLIENT_ID2']
logs.info("Config loaded")

class BunnyBot(commands.Bot):
    
    def __init__(self, client_id=None):
        logs.info("Initializing BunnyBot...")
        super().__init__(
            command_prefix = '?',
            intents = discord.Intents.default(),
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
        logs.info(f"Syncing commands...")

        await bot.tree.sync()
        
        logs.info(f"Syncing done..")
        
    async def on_ready(self):
        logs.info("BunnyBot is ready")


bot = BunnyBot(client_id=cid)
bot.run(secret)