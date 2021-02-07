from discord.ext import tasks
from discord.ext import commands
import connect
import json


class AutoTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.share.start()

    def cog_unload(self):
        self.share.cancel()

    def readConfig(self):
        with open("config.json") as f:
            config = json.load(f)
        return config

    @tasks.loop(hours=4.0)
    async def share(self):
        config = self.readConfig()
        database = config["databaseLocation"]
        conn = connect.createConnection(database)
        msgList = connect.getAutoMsgData(conn)
        for msg in msgList:
            msgText = (f"**Server:** {msg[0]} \n"
                       f"**Description:** {msg[2]} \n"
                       f"**Link:** {msg[1]}")
            for server in self.bot.guilds:
                for channel in server.channels:
                    if channel.name == config["Channels"].get(str(server.id)):
                        await channel.send(msgText)

    @share.before_loop
    async def beforeShare(self):
        print('Loading.....')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(AutoTasks(bot))
