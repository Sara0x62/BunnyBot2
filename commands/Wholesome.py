import discord
from discord import app_commands
from discord.ext import commands

import typing
import logging

import random

# Setup logger
logs = logging.getLogger('discord').getChild("Wholesome")
logs.name = "BunnyBot.commands.Wholesome"
logs.setLevel(logging.INFO)


class Wholesome(commands.Cog, name="Wholesome"):
    
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        
        logs.info("Wholesome ready...")
    
    # Command groups
    group = app_commands.Group(name="send", description="Send a message/hug/headpat to given user")
    group_find = app_commands.Group(name="find", description="Finds someone in the discord")
    group_call = app_commands.Group(name="call", description="Tells a given user something")
    
    # find cutie
    @group_find.command(name="cutie", description="Finds a cutie in the discord")
    async def find_cutie(self, interaction:discord.Interaction):
        await interaction.response.send_message(f"Alert we found someone that is just super cute!\n"
            f"It is {interaction.user.mention} !")
    
    # call cute {user}
    @group_call.command(name="cute", description="Lets the given user know they're cute")
    async def call_cute(self, interaction:discord.Interaction, 
        user:discord.Member, option: typing.Optional[app_commands.Range[int, 0, 7]] = None):
        
        # If given user is the bot;
        if user.id == self.bot.user.id:
            logs.info(f"call_cute - User: {interaction.user.name} tried to call the bot cute... that's nice")
            await interaction.response.send_message(f"nuh-uh You're way cuter than me {interaction.user.mention}")
            return
        
        # Message list, random or 'option' will select from this
        messages = [
            f"Wow everyone look at how cute {user.mention} is!",
            f"Hello {user.mention}, a certain user would like to let you know you're a cutie",
            f"Hello there {user.mention}, are you aware that you're currently being **too cute** !?",
            f"Hey {user.mention}, just wanted to let you know that {interaction.user.mention} thinks you're cute (they're correct of course)",
            f"Such a cutieful day with you around, {user.mention}",
            f"If {user.mention} was a vegetable they'd be a cute-cumber",
            f"If {user.mention} was a fruit they'd be a fine-apple",
            f"Someone pinch me, {user.mention} is so cute i must be dreaming"
        ]
        
        # If no option is given, random.choice will be used instead
        if option is None:
            message = random.choice(messages)
        else:
            message = messages[option]
            
        # Let the command user know
        await interaction.response.send_message("I will inform them they're cute", ephemeral=True)
        
        # Send message to the channel the command was called from
        await interaction.channel.send(message)
    
    # send hug {user}
    @group.command(name="hug", description="Gives the user a hug")
    async def give_hug(self, interaction:discord.Interaction, 
        user:discord.Member, hidden:typing.Optional[bool]=True):
        
        emote = discord.utils.get(interaction.guild.emojis, name='MochaHug')
        if emote is None:
            emote = "🫂"
            
        await interaction.response.send_message(f"Sending {user.name} a hug", ephemeral=hidden)
        
        await interaction.channel.send(f"*hugs* {user.mention} {emote}")
    
    # send headpat {user}
    @group.command(name="headpat", description="Gives the user a headpat")
    async def headpat(self, interaction:discord.Interaction, 
        user:discord.Member, hidden:typing.Optional[bool] = True):
    
        emote = discord.utils.get(interaction.guild.emojis, name='headpats')
        if emote is None:
            emote = ""
            
        await interaction.response.send_message(f"Sending headpats to {user.name}", ephemeral=hidden)
        
        await interaction.channel.send(f"*headpats* {user.mention} {emote}")
    

# == SETUP ==    
async def setup(bot:commands.Bot):
    await bot.add_cog(Wholesome(bot))
