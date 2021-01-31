import connect
import os
import sys
import json
import re
import datetime
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
flag = False


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
    global flag
    flag = False
    # print(f"Share: {flag}")
    userTable = connect.getData(conn)
    author = str(ctx.author)[:-5]
    guild = str(ctx.guild)
    subLevel = connect.getSubLevel(conn, [author])[0]
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

    # return total servers with the bot
    print("Servers: " + str(len(ctx.bot.guilds)))
    for server in ctx.bot.guilds:
        for channel in server.channels:
            if channel.name == "bot-testing":
                unixTime = connect.getTime(conn, [author])[0]
                timeLeft = str(datetime.timedelta(seconds=unixTime)).split(":")
                # print(timeLeft)
                timeLeft[0] = re.sub(r"^\d+\s\w+\D\s", "", timeLeft[0])
                # print(timeLeft)
                if subLevel == 0:
                    await checkTime(ctx, timeLeft, 24, author, msgText,
                                    channel)
                elif subLevel == 1:
                    await checkTime(ctx, timeLeft, 12, author, msgText,
                                    channel)
                elif subLevel == 2:
                    await checkTime(ctx, timeLeft, 8, author, msgText,
                                    channel)
                else:
                    await channel.send(msgText)
                # if int(timeLeft[0]) >= 12:
                #     await channel.send(msgText)
                # else:
                #     if share is False:
                #         share = True
                #         await ctx.send("**Please wait:** "
                #                        + f"`{12 - int(timeLeft[0])}"
                #                        + f" hours {60 - int(timeLeft[1])}"
                #                        + f" minutes {60 - int(timeLeft[2])}"
                #                        + " seconds`")
                # await ctx.send("Please wait: `" +
                #                str(12 - hoursPast) + " hours ")
    # connect.updateTime(conn, [author])


def setup(bot):
    bot.add_command(share)


async def checkTime(ctx, timeLeft, waitHours, username, msgText, channel):
    global flag
    timeLeft
    if int(timeLeft[0]) >= waitHours:
        await channel.send(msgText)
    else:
        if flag is False:
            # print(f"Share: {flag}")
            flag = True
            # print(f"Share: {flag}")
            await ctx.send(f"Please wait: `{waitHours - int(timeLeft[0])}"
                           f" hours {60 - int(timeLeft[1])}"
                           f" minutes {60 - int(timeLeft[2])}"
                           " seconds`")
