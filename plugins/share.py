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
flagShare = False


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
    author = str(ctx.author)
    guild = connect.getGuild(conn, [author])[0]
    subLevel = connect.getSubLevel(conn, [author])[0]
    serverCount = len(ctx.bot.guilds)
    loopCount = 0
    for row in userTable:
        if(row[1] == author):
            inviteLink = row[4]
            if(subLevel > 1 and subLevel < 4):
                description = row[5]
                msgText = (f"**Server:** {guild} \n"
                           f"**Description:** {description} \n"
                           f"**Link:** {inviteLink}")
            else:
                msgText = (f"**Server:** {guild} \n"
                           f"**Link:** {inviteLink}")

    # return total servers with the bot
    print(f"Shared to {serverCount} servers")
    for server in ctx.bot.guilds:
        loopCount += 1
        print(f"Name: {server.name} \nID: {str(server.id)}")
        for channel in server.channels:
            if channel.name == config["Channels"].get(str(server.id)):
                unixTime = connect.getTime(conn, [author])[0]
                timeLeft = str(datetime.timedelta(seconds=unixTime)).split(":")
                # timeLeft[0] = re.sub(r"^\d+\s\w+\D\s", "", timeLeft[0])
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
    if loopCount == serverCount:
        if flagShare is True:
            connect.updateTime(conn, [author])


def setup(bot):
    bot.add_command(share)


async def checkTime(ctx, timeLeft, waitHours, username, msgText, channel):
    global flag
    global flagShare
    waitHours -= 1
    match = re.search(r"[a-z]", timeLeft[0])
    if match is not None:
        days = int(re.findall(r"^\d+", timeLeft[0])[0])
        # print(timeLeft)
        # print(days)
        # convert days to hours & add to hours
        timeLeft[0] = str((days*24) +
                          int(re.sub(r"^\d+\s\w+\D\s", "", timeLeft[0])))
        # print(timeLeft)

    if int(timeLeft[0]) >= waitHours:
        await channel.send(msgText)
        flagShare = True
    else:
        if flag is False:
            # print(f"Share: {flag}")
            flag = True
            flagShare = False
            # print(f"Share: {flagShare}")
            await ctx.send(f"Please wait: `{waitHours - int(timeLeft[0])}"
                           f" hours {59 - int(timeLeft[1])}"
                           f" minutes {60 - int(timeLeft[2])}"
                           " seconds`")
