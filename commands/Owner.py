import discord
from discord.ext import commands

import typing
import logging
import configparser

from os import path

# Get emote from config
emote_cfg = configparser.ConfigParser()
emote_cfg.read('emojis.ini')

# Setup logger
logs = logging.getLogger('discord').getChild("Owner")
logs.name = "BunnyBot.commands.Owner"
logs.setLevel(logging.INFO)

class Owner(commands.Cog, name="Owner"):
    
    def __init__(self, bot: commands.Bot) -> None:
        # Owner commands - sync the bot, shut down the bot, etc.
        self.bot = bot
        
        logs.info("Owner ready.")
        
        self.bunnyheart = emote_cfg['EMOJIS']['bunnyheart']
        


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sleep(self, ctx: commands.Context):
        logs.info(f"sleep - user: {ctx.author.name}")
        await ctx.send(f"Understood going to sleep\nGood night everyone! {self.bunnyheart}")
        
        await self.bot.close()
        exit(0)


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def add_emote(self, ctx: commands.Context, emote_name: str, emote: discord.Emoji):
        logs.info("Adding emote to config - emote")
        
        emote_syntax = f"<:{emote.name}:{emote.id}>"
        
        emote_cfg.set('EMOJIS', emote_name, emote_syntax)
        
        with open('emojis.ini', 'w') as f:
            emote_cfg.write(f)
        
        await ctx.send(f"Added emote '{emote_name} - {emote_syntax} to config, restart required for emotes to be updated across Cogs.")

    """
        Extension handling - list all extensions, reload given extensions
    """
    @commands.command()
    @commands.is_owner()
    async def extensions(self, ctx: commands.Context):
        # Lists all current extensions
        extensions = self.bot.extensions
        output = "\n".join(key for key in extensions.keys())
        await ctx.send(f"Current extensions:\n{output}")


    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, module: str):
        try:
            await self.bot.reload_extension(module)
            
            await ctx.send(f"Extension '{module}' was reloaded successfully")
        except commands.ExtensionNotLoaded:
            await ctx.send("Extension has to be loaded before you can reload it.")
        except commands.ExtensionNotFound:
            await ctx.send("Extension not found.")
        except commands.NoEntryPointError:
            await ctx.send("Extension does not seem to have a setup function.")
        except commands.ExtensionFailed:
            await ctx.send("Extension failed, setup function had an execution error.")

            


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self,
            ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^", "?"]] = None
        ) -> None:
        
        logs.info(f"sync - user: {ctx.author.name} - spec: {spec}")
        
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                await ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            elif spec == "?":
                await ctx.send( \
                    "Usage:\n"
                    "'?sync'          -> Global sync\n"
                    "'?sync ~'        -> Sync current guild\n"
                    "'?sync *'        -> Copies all global app commands to current guild and syncs\n"
                    "'?sync ^'        -> Clears all commands from the current guild target and syncs (removes guild commands)\n"
                    "'?sync id_1 id_2 -> syncs guilds with id 1 and 2\n"
                    "'?sync ?'        -> Displays this how to use message\n"
                )
                return
            else:
                synced = await ctx.bot.tree.sync()
                
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return
        
        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1
                
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}")


    @commands.Cog.listener("on_command_error")
    async def owner_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            logs.warning(f"owner_error - {ctx.author} - error: {error}")
            
            file = discord.File(path.join("gifs", "supervisor.gif"))
            
            await ctx.send(file=file)
        else:
            logs.error("owner_error - Unknown error caught - {error}")
            raise error


async def setup(bot:commands.Bot):
    await bot.add_cog(Owner(bot))
