import connect
import os
import sys
import json
from discord.ext import commands
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def readConfig():
    with open("config.json") as f:
        config = json.load(f)
    return config


config = readConfig()

# Connecting to the user database
database = config["databaseLocation"]
conn = connect.createConnection(database)


@commands.command(
    name="share",
    aliases=['server'],
    description="Share your server with every server with this bot installed",
    usage=""
)
async def share(ctx):
    inviteLink = ""
    description = ""
    msgText = ""
    userTable = connect.getData(conn)
    author = str(ctx.author)[:-5]
    guild = str(ctx.guild)
    for row in userTable:
        if(row[1] == author):
            inviteLink = row[3]
            if(row[2] > 1 and row[2] < 4):
                description = row[4]
                msgText = ("**Server:** " + guild + "\n"
                           + "**Description:** " + description + "\n"
                           + "**Link:** " + inviteLink)
            else:
                msgText = ("**Server:** " + guild + "\n"
                           + "**Link:** " + inviteLink)

    for server in ctx.bot.guilds:
        for channel in server.channels:
            if channel.name == "bot-testing":
                await channel.send(msgText)


def setup(bot):
    bot.add_command(share)
