import discord
from discord.ext import commands
from discord import app_commands

import typing
import logging

# Setup logging
logs = logging.getLogger("discord").getChild("Colors")
logs.name = "BunnyBot.commands.Colors"
logs.setLevel(logging.INFO)
logs.name = "BunnyBot.commands.Colors"

class Colors(commands.Cog, name="Colors"):
    
    def __init__(self, bot: commands.Bot) -> None:
        logs.info("Initializing Colors")
        self.bot = bot
        
        # self.color_role_prefix = "color-"
        self.color_role_postfix = "color"  # eg. "user-color"
        logs.info("Colors initialized...")
    
    # Define group command 'color'
    group = app_commands.Group(name="color", description="Color role commands")
    
      
    # color set - rgb values
    @group.command(name='set-rgb', description='Set a display color for yourself using rgb values')
    async def set_rgb(self, interaction: discord.Interaction, r: app_commands.Range[int, 0, 255], g: app_commands.Range[int, 0, 255], b: app_commands.Range[int, 0, 255]):
        
        color = discord.Color.from_rgb(r, g, b)
        
        await interaction.response.defer(ephemeral=True)
        
        await self.set_color(color=color, user=interaction.user, guild=interaction.guild)
        
        await interaction.followup.send("Color set!")
        
    # color set - hex values
    @group.command(name='set-hex', description='Set a display color for yourself using a hex value')
    async def set_hex(self, interaction: discord.Interaction, hex_code:str):
        
        try:
            color = discord.Color.from_str(hex_code)
            
            await interaction.response.defer(ephemeral=True)
            
            await self.set_color(color=color, user=interaction.user, guild=interaction.guild)

            await interaction.followup.send("Color set!")
            
        except ValueError:
            await interaction.response.send_message("Unable to convert given hex to color", ephemeral=True)
    
    
    # color get
    @group.command(name='get', description='Get the display color for yourself or someone else')
    async def get(self, interaction: discord.Interaction, target: typing.Optional[discord.Member]):
        
        if target:
            role = await self.get_role(target)
            username = target.name
        else:
            role = await self.get_role(interaction.user)
            username = interaction.user.name
            
        if role is not None:
            await interaction.response.send_message(
                f"Colors for {username}\n"
                f"R: {role.color.r}\n"
                f"G: {role.color.g}\n"
                f"B: {role.color.b}\n"
                f"\nHex: {hex(role.color.value)}\n")
        else:
            await interaction.response.send_message(f"Did not find a color role on {username}", ephemeral=True)
    
    
    # color steal
    @group.command(name='steal', description='Steal the display color of someone else')
    async def get(self, interaction: discord.Interaction, target: discord.Member):
        
        role = await self.get_role(target)
        
        if role is None:
            await interaction.response.send_message(f"Could not find a role on {target.name}", ephemeral=True)
            return
        
        color = role.color
        
        await interaction.response.defer(ephemeral=True)
        
        await self.set_color(color, interaction.user, interaction.guild)
        
        await interaction.followup.send(f"Successfully stole colors from {target.name}", ephemeral=False)
    
    # Tries to set the role color, makes it if role does not exist
    async def set_color(self, color: discord.Color, user: discord.Member, guild: discord.Guild):
        # Check if role exists for user
        role_name = f"{user.name}-{self.color_role_postfix}"
        color_role = await self.get_role(user, role_name)
        
        if color_role:
            logs.info(f"set_color - Got color role for {user.name} - setting color to [R: {color.r}, G: {color.g}, B: {color.b}]")

            await color_role.edit(color=color)
            
            return
        else:
            logs.info(f"Unable to get color role, attempting to make new color role")
            
            color_role = await guild.create_role(name=role_name, color=color)
            
            logs.info(f"Getting bot's highest role position - bot_id: {self.bot.user.id}")
            top_pos = guild.get_member(self.bot.user.id)
            
            # Make the top position 1 position under the highest role the bot has
            top_pos = top_pos.top_role.position - 1 
            
            logs.info(f"Top position for bot is {top_pos + 1} - placing color roles at position {top_pos}")
            
            # Fix color role position
            await color_role.edit(position=top_pos)
            
            # Add role to user
            await user.add_roles(color_role)
            
    
    # Searches user roles for role:str and returns it as a discord.Role object
    # Returns None if role is not found
    async def get_role(self, user: discord.Member, user_role: str = None) -> discord.Role:
        if user_role is None:
            user_role = f"{user.name}-{self.color_role_postfix}"
        
        for role in user.roles:
            if role.name == user_role:
                return role
            
        return None
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Colors(bot))