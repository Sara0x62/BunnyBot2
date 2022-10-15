import discord
from discord import app_commands
from discord.ext import commands

import typing
import logging

# Setup logger
logs = logging.getLogger('discord').getChild("__TEMPLATE__")
logs.name = "BunnyBot.commands.__TEMPLATE__"
logs.setLevel(logging.INFO)

class __TEMPLATE__(commands.Cog, name="__TEMPLATE__"):
    
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        
        logs.info("__TEMPLATE__ ready.")
        
    
async def setup(bot:commands.Bot):
    await bot.add_cog(__TEMPLATE__(bot))
    
# Usage;
# Search and replace all occurences of:
# __TEMPLATE__ with your group/class name