from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotLoaded


@commands.command(
    name="reload",
    help="reload commands on the fly"
)
async def reload(ctx, command):
    try:
        ctx.bot.reload_extension(f"plugins.{command}")
        print(f"[Reloaded] {command}.py")
    except ExtensionNotLoaded:
        ctx.bot.load_extension(f"plugins.{command}")
        print(f"[Loaded] {command}.py")
    await ctx.send(f"Reloaded: `{command}`")


def setup(bot):
    bot.add_command(reload)
