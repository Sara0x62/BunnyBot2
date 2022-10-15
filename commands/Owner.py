import discord
from discord.ext import commands

import typing
import logging
import configparser

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
    @commands.is_owner()
    async def sleep(self, ctx: commands.Context):
        logs.info(f"sleep - user: {ctx.author.name}")
        await ctx.send(f"Understood going to sleep\nGood night everyone! {self.bunnyheart}")
        
        await self.bot.close()
        exit(0)

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


async def setup(bot:commands.Bot):
    await bot.add_cog(Owner(bot))