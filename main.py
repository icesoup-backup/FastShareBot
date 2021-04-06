from discord.ext.commands import Bot
from pretty_help import PrettyHelp, Navigation
import discord
import os
import json
import connect


def readConfig():
    with open("config.json") as f:
        config = json.load(f)
    return config


def getPrefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix=getPrefix, intents=intents)

nav = Navigation()
color = discord.Color.dark_gold()
bot.help_command = PrettyHelp(
    navigation=nav, color=color, active_time=5, no_category="Default")

config = readConfig()
TOKEN = config["botToken"]
database = config["databaseLocation"]
defaultChannel = config["defaultChannel"]
defaultCategory = config["defaultCategory"]
conn = connect.createConnection(database)


@bot.event
async def on_guild_join(guild):
    # handling server prefixes
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    # handling custom sharing channels
    with open('config.json', 'r') as f:
        config = json.load(f)
    config["Channels"].update({str(guild.id): defaultChannel})
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    # creating a new channel for sharing servers
    serverOwner = str(guild.owner)
    serverName = guild.name
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            send_messages=False),
        guild.owner: discord.PermissionOverwrite(read_messages=True)
    }
    category = await guild.create_category_channel(
        name=defaultCategory,
        overwrites=overwrites)
    inviteChannel = await guild.create_text_channel(
        name=defaultChannel,
        overwrites=overwrites,
        category=category)
    serverInvite = str(await inviteChannel.create_invite())
    # print(f"Owner: {serverOwner} \n Name: {serverName} \n"
    #       f"Invite: {serverInvite}")
    # print(f"Owner: {type(serverOwner)} \n Name: {type(serverName)} \n"
    #       f"Invite: {type(serverInvite)}")

    # creating a database entry for the server
    data = (serverOwner, serverName, serverInvite)
    connect.createUser(conn, data)


@bot.event
async def on_guild_remove(guild):
    # handling server prefixes
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    # handling custom sharing channels
    with open('config.json', 'r') as f:
        config = json.load(f)
    config["Channels"].pop(str(guild.id))
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)


@bot.event
async def on_ready():
    print("\033[0;33m""▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬""\033[0m")
    print("\033[0;92m""{0.user} bot is online!""\033[0m".format(bot))
    print("\033[0;33m""▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬""\033[0m")
    # bot.remove_command('help')
    for command in os.listdir("./plugins"):
        if command.endswith(".py"):
            print(f"[Loaded] {command}")
            bot.load_extension(f"plugins.{command[:-3]}")

bot.run(TOKEN)
