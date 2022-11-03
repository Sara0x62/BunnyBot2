import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime, timedelta

import aiosqlite
import typing
import logging

# Setup logger
logs = logging.getLogger('discord').getChild("Reminders")
logs.name = "BunnyBot.commands.Reminders"
logs.setLevel(logging.INFO)

class Reminders(commands.Cog, name="Reminders"):
    
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        
        logs.info("Reminders ready.")
        
        self.db_connected = False
        self.db = None
        
        self.time_format = "%Y-%m-%d %H:%M:%S"
    
    
    async def connect_db(self):
        self.db = await aiosqlite.connect('dbs/BunnyBot.db')
        self.db_connected = True
    
    
    @tasks.loop()
    async def remindme_task(self):
        # Try to get the next upcoming reminder
        cursor = await self.db.execute("SELECT * FROM reminders WHERE NOT Completed ORDER BY time LIMIT 1")
        
        # row -> [row_id, user_id, channel_id, message, datetime, completed] 
        row = await cursor.fetchone()
        
        await cursor.close()
        
        # If all reminders are set to completed, cancel the task
        if row is None or len(row) != 6:
            self.remindme_task.cancel()
            return
        
        # Else: 
        
        # get_user often seems to return None after bot restart, so fetch_user is a bit of a backup but not always needed
        user = self.bot.get_user(row[1])
        if user is None:
            logs.info("Attempting fetch_user")
            user = await self.bot.fetch_user(row[1])

        # Get the channel where the bot has to post the message
        channel = self.bot.get_channel(row[2])
        
        # The message
        message = row[3]
        
        # Format the datetime string back to a datetime object
        sleep_till = datetime.strptime(row[4], self.time_format)
        
        
        # Wait untill either the sleep_until or an earlier task gets added from the remindme command
        logs.info(f"Reminder task for {user.name} - sleeping untill {sleep_till}")
        await discord.utils.sleep_until(sleep_till)
        
        # Sending the reminder message
        logs.info(f"Sending reminder to {user} | {channel} | Message: {message}")
        await channel.send(f"Hello {user.mention} you wanted me to remind you! You gave me this message:\n {message}")
        
        # Update the row we just completed to set the reminder we just finished as completed
        # logs.info(f"DEBUG - row[0] = {row[0]} | Type: {type(row[0])}")
        await self.db.execute("UPDATE reminders SET Completed = true WHERE id = ?", (row[0],))
        
        # Uncomment if we want to delete the reminder from the db after completion
        # await self.db.execute(f"DELETE FROM reminders WHERE id = ?", row[0])   # Delete after completion?
        
        # Commit the update/deletion to the database
        await self.db.commit()
    
    
    @app_commands.command(name="remindme", description="Sends a reminder after the given time")
    async def remindme(self, interaction: discord.Interaction, message:str,
                       seconds:typing.Optional[int] = 0, hours:typing.Optional[int] = 0, 
                       minutes:typing.Optional[int] = 0, days:typing.Optional[int] = 0):
        
        # If the user gave none of the possible time options
        if not seconds and not minutes and not hours and not days:
            await interaction.response.send_message("I require atleast one of possible types of time", ephemeral=True)
            return
        
        # The time untill the user wants the reminder to be sent
        sleep_time = timedelta(
            days = days,
            hours = hours,
            minutes = minutes,
            seconds = seconds
        )
        
        # We need to add it to the current time so the bot knows when to send it
        sleep_for = datetime.today() + sleep_time
        
        await interaction.response.send_message(f"Sending a reminder in {sleep_time.__str__()}", ephemeral=True)
        
        # Ease of access variables
        user, channel = interaction.user, interaction.channel
        
        # If db connection is not up yet -> connect
        if not self.db_connected:
            await self.connect_db()
        
        # Insert a new row into reminders with the provided values
        await self.db.execute(
            "INSERT INTO reminders (user_id, channel_id, message, time, Completed) VALUES (?, ?, ?, ?, ?)", (
                user.id, channel.id, message, sleep_for.strftime(self.time_format), 0,
            )
        )
        # Commit new row to database
        await self.db.commit()
        
        logs.info(f"New query commited - UID: {user.id}, channel_id: {channel.id}, message: {message}, time: {sleep_for.strftime(self.time_format)}")
        
        # If the task is already running -> restart it, incase our reminder is the earliest one on the database; else start up the task
        if self.remindme_task.is_running():
            self.remindme_task.restart()
        else:
            self.remindme_task.start()
    
async def setup(bot:commands.Bot):
    await bot.add_cog(Reminders(bot))
