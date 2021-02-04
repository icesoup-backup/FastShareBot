from discord.ext import commands
import connect
import os
import sys
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def readConfig():
    with open("config.json") as f:
        config = json.load(f)
    return config


config = readConfig()
database = config["databaseLocation"]
conn = connect.createConnection(database)


@commands.command(
    name="changechannel",
    aliases=['setchannel', 'setc'],
    description="Change the default channel and category",
    help="changechannel [Channel]"
)
@commands.has_permissions(administrator=True)
async def changechannel(ctx, channel):
    author = str(ctx.author)
    subLevel = connect.getSubLevel(conn, [author])[0]

    if subLevel > 0:
        with open('config.json', 'r') as f:
            config = json.load(f)

        config["Channels"].update({str(ctx.guild.id): channel})

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Channel changed to: `{channel}`')
    else:
        await ctx.send("Please upgrade your subscription plan")


def setup(bot):
    bot.add_command(changechannel)
