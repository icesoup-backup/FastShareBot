from discord.ext import commands


@commands.command(
    name="clear",
    help="Clear recent messages"
)
async def clear(ctx, ammount=5):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.channel.purge(limit=int(ammount)+1)
    else:
        await ctx.send("**You do not have the required permissions clear"
                       " messages **")


def setup(bot):
    bot.add_command(clear)
