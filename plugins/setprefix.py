from discord.ext import commands
import json


@commands.command(
    name="setprefix",
    aliases=['changeprefix', 'prefixset'],
    description="Change the default prefix",
    help="setfprefix [prefix]"
)
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: `{prefix}`')


def setup(bot):
    bot.add_command(setprefix)
