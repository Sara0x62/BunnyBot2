import discord
from discord.ext import commands
from discord import app_commands

import typing
import logging

# Setup logging
logs = logging.getLogger("discord").getChild("Colors")
logs.name = "BunnyBot.commands.Colors"
logs.setLevel(logging.INFO)

class Colors(commands.Cog, name="Colors"):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        # self.color_role_prefix = "color-"
        self.color_role_postfix = "color"  # eg. "user-color"
        
        # Do we want to make sure the roles have the highest possible position?
        # This is mainly for if the discord already has other color roles we want our color rules to be above it if possible.
        self.ROLES_AT_TOP = True
        
        logs.info("Colors ready...")
    
    # Define group command 'color'
    group = app_commands.Group(name="color", description="Color role commands")
    
      
    # color set - rgb values
    @group.command(name='set-rgb', description='Set a display color for yourself using rgb values')
    async def set_rgb(self, interaction: discord.Interaction, r: app_commands.Range[int, 0, 255], g: app_commands.Range[int, 0, 255], b: app_commands.Range[int, 0, 255]):
        
        logs.info(f"set_rgb - called by {interaction.user.name} | [ r: {r}, g: {g}, b: {b} ]")
        
        color = discord.Color.from_rgb(r, g, b)
        
        await interaction.response.defer(ephemeral=True)
        
        await self.set_color(color=color, user=interaction.user, guild=interaction.guild)
        
        logs.info(f"set_rgb - color set for user: {interaction.user.name}")
        await interaction.followup.send("Color set!")
        
    # color set - hex values
    @group.command(name='set-hex', description='Set a display color for yourself using a hex value')
    async def set_hex(self, interaction: discord.Interaction, hex_code:str):
        
        try:
            logs.info(f"set_hex - called by: {interaction.user.name} hex value: {hex_code}")
            color = discord.Color.from_str(hex_code)
            
            await interaction.response.defer(ephemeral=True)
            
            await self.set_color(color=color, user=interaction.user, guild=interaction.guild)

            await interaction.followup.send("Color set!")
            
        except ValueError:
            logs.info(f"set_hex - ValueError: {interaction.user.name} hex value: {hex_code}")
            await interaction.response.send_message("Unable to convert given hex to color", ephemeral=True)
    
    
    # color show
    @group.command(name='show', description='Shows the color values of yourself or someone else')
    async def show(self, interaction: discord.Interaction, target: typing.Optional[discord.Member]):
        
        if target:
            logs.info(f"show - Got optional argument, target: {target.name}")
            role = await self.get_role(target)
            username = target.name
        else:
            logs.info(f"show - No optional argument, target: {interaction.user.name}")
            role = await self.get_role(interaction.user)
            username = interaction.user.name
            
        if role is not None:
            logs.info(f"show - got a role, colors are [R: {role.color.r}, G: {role.color.g}, B: {role.color.b}]")
            await interaction.response.send_message(
                f"Colors for {username}\n"
                f"R: {role.color.r}\n"
                f"G: {role.color.g}\n"
                f"B: {role.color.b}\n"
                f"\nHex: {hex(role.color.value)}\n")
        else:
            logs.info(f"show - No color role found for {username}")
            await interaction.response.send_message(f"Did not find a color role on {username}", ephemeral=True)
    
    
    # color steal
    @group.command(name='steal', description='Steal the display color of someone else')
    async def steal(self, interaction: discord.Interaction, target: discord.Member):
        logs.info(f"steal - User: {interaction.user.name} is trying to steal the display color of {target.name}")
        
        role = await self.get_role(target)
        
        if role is None:
            logs.info("steal - Unabled to steal color, role not found on {target.name}")
            await interaction.response.send_message(f"Could not find a role on {target.name}", ephemeral=True)
            return
        
        color = role.color
        
        file = discord.File("gifs/steal.gif")
        
        await interaction.response.defer(ephemeral=False)
        
        await self.set_color(color, interaction.user, interaction.guild)
        
        if file:
            await interaction.followup.send(f"Successfully stole colors from {target.name}", file=file, ephemeral=False)
        else:
            await interaction.followup.send(f"Successfully stole colors from {target.name}", ephemeral=False)
        
        logs.info(f"steal - Successfully stolen colors from {target.name}")
    
        """
            === ^ COLOR COMMANDS UP ^ ===
            
            ====== COLOR HANDLERS  ======
        """
    # Tries to set the role color, makes it if role does not exist
    async def set_color(self, color: discord.Color, user: discord.Member, guild: discord.Guild):
        
        logs.info(f"set_color - Setting color for user: {user.name}")
        
        # Check if role exists for user
        role_name = f"{user.name}-{self.color_role_postfix}"
        color_role = await self.get_role(user, role_name)
        
        if color_role:
            logs.info(f"set_color - Got color role for {user.name} - setting color to [R: {color.r}, G: {color.g}, B: {color.b}]")

            await color_role.edit(color=color)
            
            return
        else:
            logs.info(f"set_color - Unable to get color role, attempting to make new color role")
            
            color_role = await guild.create_role(name=role_name, color=color)
            logs.info("set_color - Successfully created new color role")
            
            if self.ROLES_AT_TOP:
                logs.info(f"set_color - Getting bot's highest role position - bot_id: {self.bot.user.id}")
                top_pos = guild.get_member(self.bot.user.id)
                
                # Make the top position 1 position under the highest role the bot has
                top_pos = top_pos.top_role.position - 1 
                
                logs.info(f"set_color - Top position for bot is {top_pos + 1} - placing color roles at position {top_pos}")
                
                # Fix color role position
                logs.info(f"set_color - fixing new role position")
                await color_role.edit(position=top_pos)
            
            # Add role to user
            logs.info(f"set_color - Adding new role to user: {user.name}")
            await user.add_roles(color_role)
            
    
    # Searches user roles for role:str and returns it as a discord.Role object
    # Returns None if role is not found
    async def get_role(self, user: discord.Member, user_role: str = None) -> discord.Role:
        if user_role is None:
            user_role = f"{user.name}-{self.color_role_postfix}"
        
        logs.info(f"get_role - trying to find role for user: {user.name}")
        
        for role in user.roles:
            if role.name == user_role:
                logs.info(f"get_role - found role for user: {role.name}")
                return role
            
        logs.info(f"get_role - no role found for user: {user.name}")
        return None
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Colors(bot))