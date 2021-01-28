from discord.ext import commands
import json


def readConfig():
    with open("config.json") as f:
        config = json.load(f)
    return config


config = readConfig()
prefix = config["commandPrefix"]


@commands.command(
    name="clear",
    description="Clear recent messages",
    help=f"{prefix}clear [ammount]"
)
async def clear(ctx, ammount=5):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.channel.purge(limit=int(ammount)+1)
    else:
        await ctx.send("**You do not have the required permissions to create"
                       + " a channel **")


def setup(bot):
    bot.add_command(clear)
