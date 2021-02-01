from discord.ext.commands import Bot
import discord
import os
import json


def readConfig():
    with open("config.json") as f:
        config = json.load(f)
    return config


def getPrefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


config = readConfig()

intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix=getPrefix, intents=intents)
TOKEN = config["botToken"]


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_ready():
    print("\033[0;33m""▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬""\033[0m")
    print("\033[0;92m""{0.user} bot is online!""\033[0m".format(bot))
    print("\033[0;33m""▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬""\033[0m")
    bot.remove_command('help')
    for command in os.listdir("./plugins"):
        if command.endswith(".py"):
            print(f"[Loaded] {command}")
            bot.load_extension(f"plugins.{command[:-3]}")

bot.run(TOKEN)
