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
    name="description",
    aliases=['sd'],
    description="Add or Update your servers description",
    usage=""
)
async def description(ctx, *args):
    description = " ".join(args)
    author = str(ctx.author)
    subLevel = connect.getSubLevel(conn, [author])[0]
    if subLevel >= 2:
        connect.updateDescription(conn, (description, author))
        await ctx.send("Description updated !")
    else:
        await ctx.send("Please upgrade your subscription plan")


def setup(bot):
    bot.add_command(description)
