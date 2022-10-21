import discord
from discord import app_commands
from discord.ext import commands
from os import path

import typing
import logging

# Setup logger
logs = logging.getLogger('discord').getChild("ErrorHandler")
logs.name = "BunnyBot.commands.ErrorHandler"
logs.setLevel(logging.INFO)

class ErrorHandler(commands.Cog, name="ErrorHandler"):
    
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        
        logs.info("ErrorHandler ready.")


    async def owner_error(self, ctx):
        file = discord.File(path.join("gifs", "supervisor.gif"))
        await ctx.send(file=file)


    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            logs.warning(f"owner_error - {ctx.author} - error: {error}")
            await self.owner_error(ctx)
        else:
            logs.error("Unknown 'on_command_error' caught - {error}")
            raise error

    
async def setup(bot:commands.Bot):
    await bot.add_cog(ErrorHandler(bot))
