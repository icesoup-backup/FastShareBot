from discord.ext.commands import Bot
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
config = readConfig()
TOKEN = config["botToken"]
database = config["databaseLocation"]
channelName = config["defaultChannel"]
categoryName = config["defaultCategory"]
conn = connect.createConnection(database)


@bot.event
async def on_guild_join(guild):
    # handling server prefixes
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    # creating a new channel for sharing servers
    serverOwner = str(guild.owner)[:-5]
    serverName = guild.name
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            send_messages=False),
        guild.owner: discord.PermissionOverwrite(read_messages=True)
    }
    category = await guild.create_category_channel(
        name=categoryName,
        overwrites=overwrites)
    inviteChannel = await guild.create_text_channel(
        name=channelName,
        overwrites=overwrites,
        category=category)
    serverInvite = str(await inviteChannel.create_invite())
    # print(f"Owner: {serverOwner} \n Name: {serverName} \n"
    #       f"Invite: {serverInvite}")
    # print(f"Owner: {type(serverOwner)} \n Name: {type(serverName)} \n"
    #       f"Invite: {type(serverInvite)}")

    # creating a databse entry for the server
    data = (serverOwner, serverName, serverInvite)
    connect.createUser(conn, data)


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
