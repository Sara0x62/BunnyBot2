import discord
from discord import app_commands
from discord.ext import commands

import typing
import logging

# Setup logger
logs = logging.getLogger('discord').getChild("Events")
logs.name = "BunnyBot.commands.Events"
logs.setLevel(logging.INFO)

class Events(commands.Cog):
    
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        
        logs.info("Events ready.")
    
    
async def setup(bot:commands.Bot):
    await bot.add_cog(Events(bot))
