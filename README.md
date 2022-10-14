# BunnyBot
BunnyBot is a discord bot that runs on the discordpy library - docs are located here: https://discordpy.readthedocs.io/en/stable/


### Easily extendable
It uses the "discord.Cog" system so you can easily add more commands.
BunnyBot.py automatically loads any file it finds in the 'commands' folder as an extension (except our template of course)

The template can be used to quickstart a new command group.
You will want to make a new file inside the commands folder 'anything.py'.
Then do a simple copy-paste from the template file and then replace all "__TEMPLATE__" occurences within your new file
Do note; these files have to be a .py file and nesting more folders inside the 'commands' folder is not supported!


### Configuration
To have this bot run locally simply use the example config to make a "config.ini" file
Keep it inside the BunnyBot folder, you might to check which Token and Client ID it's loading in "BunnyBot.py"
This is located near the start of the file at the `# Loading Config`


### gifs folder
This is to store any gifs such as the "steal" gif, used with the "color steal" command
any file in here should be easily accessed (although this might not be very "cross-platform right now, due to lack of testing on anything besides linux)

It works simple like this because it technically runs from the folder "BunnyBot" and not "BunnyBot/commands";
example;
```python
my_file = discord.File("gifs/steal.gif")
await interaction.response.send("optional, extra text message", file=my_file)
```


### Logging
Every command file has it's own logger, as seen in the template file
the setup is simple
```python
# One line;
new_logger = logging.getLogger('discord').getChild("my_commands")
# Explained
new_logger = logging.getLogger('discord')       # Gets the main logger - if we simply used our own the output does not seem to work
new_logger = new_logger.getChild("my_commands") # Makes a new child logger if it does not exist yet

# Change these to fit what you want
new_logger.name = "BunnyBot.my_commands"        # Optional - i like renaming it so it looks cleaner for me on the output
new.logger.setLevel(logging.INFO)               # Set this to the logging level you want to run the bot at
```
