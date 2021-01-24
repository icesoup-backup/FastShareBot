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
    alias=['description'],
    description="Add or Update your servers description",
    usage=""
)
async def description(ctx, *args):
    description = " ".join(args)
    author = str(ctx.author)[:-5]
    connect.updateDescription(conn, (description, author))
    # for row in userTable:
    #     if(row[1] == author):
    #         inviteLink = row[3]
    #         if(row[2] > 1 and row[2] < 4):
    #             description = row[4]
    await ctx.send("Description updated !")


def setup(bot):
    bot.add_command(description)
