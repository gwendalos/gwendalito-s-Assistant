import discord
import discord.utils
import json
import asyncio
import subprocess
import colorama
import os.path

from colorama import *

from discord import Game
from discord.ext import commands
from discord.ext import tasks

token = "" # Insert your bot token here
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="g-", activity=discord.Game(name=f'''g-info | g-commands'''), intents=intents)
bot.remove_command('help') # The basic help command is removed because of the custom one

@bot.event
async def on_ready():
    subprocess.call("cls", shell=True)
    init()
    print(Fore.MAGENTA + f'''gwendalito's Assistant loaded\n-----''' + Fore.RESET) # Print to know when the bot is online

@bot.event
async def on_command_error(ctx, error): # Error handler
    if isinstance(error, commands.CommandNotFound): # If command is not found
        await ctx.send("**`Command does not exist!`**")
        embed=discord.Embed(color = 0x9C1796)\
        .add_field(name="g-suggest", value="Have a command/feature idea you'd like to see in gwendalito? Let us know!", inline=False)\
        .add_field(name="g-bug", value="Wanna report a bug to our developers? Do it now!", inline=False)
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandOnCooldown): # If command is on cooldown
        coolerrr = (ctx.author.mention) + "` You are on cooldown for {:.2f}s. Please be patient!`**".format(error.retry_after)
        await ctx.send(coolerrr)
        return

    raise error

@bot.command(aliases=["h", "commands"])
async def help(ctx, command=None): # Custom help command
	if command is None:
		embed = discord.Embed(color = 0x9C1796)\
				.add_field(name="g-suggest", value="Have a command/feature idea you'd like to see in gwendalito? Let us know!", inline=False)\
				.add_field(name="g-bug", value="Wanna report a bug to our developers? Do it now!", inline=False)\
				.add_field(name="g-contact", value="Message gwendal remotely about issues (or if you want to give some compliments). If you use this excessively, you will be blacklisted from the bot.")
		await ctx.send(embed=embed)
	elif command == "suggest":
		embed = discord.Embed(title=f"{command}", color=0x9C1796)\
				.add_field(name="• __suggest__", value="g-[suggest|sug] [Category] [Suggestion] (split by a comma)")
		await ctx.send(embed=embed)
	elif command == "bug":
		embed = discord.Embed(title=f"{command}", color=0x9C1796)\
				.add_field(name="• __bug__", value="g-[bug] [Command] [Bug Description] (split by a comma)")
		await ctx.send(embed=embed)
	elif command == "contact":
		embed = discord.Embed(title=f"{command}", color=0x9C1796)\
				.add_field(name="• __contact__", value="g-[contact] [Message]")


@bot.command(aliases=["i", 'information'], description="Check gwendalito's infos")
async def info(ctx): # Similar to a 'links' command
    embed = discord.Embed(title="Info Page:", description="If the bot is offline, feel free to join our Discord server. We say why/when the bot is down.", color=0x9C1796)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/874781547851546625/875995647185125406/gwendalito_artwork_mini.png')
    embed.set_footer(text=f"Main Page")
    embed.add_field(name='📜 Commands', value='**g-commands** for all commands', inline=False)
    embed.add_field(name='❓ Support', value='Join the official [support server](https://discord.gg/YGsZfSCTqC) of gwendalito', inline=False)
    embed.add_field(name='<:upvote:879397319475343420> Upvote', value='Please, if you like gwendalito, [upvote](https://top.gg/bot/854828194653011978/vote) it. This is really important for us.', inline=False)
    embed.add_field(name='🔗 Invite', value='[Invite gwendalito](https://discord.com/oauth2/authorize?client_id=854828194653011978&permissions=8&scope=applications.commands%20bot) in your server', inline=False)
    my_msg = await ctx.send(embed = embed)

@bot.command(aliases=["sug"])
@commands.cooldown(1, 60, commands.BucketType.user)
async def suggest(ctx, *, suggestion: str): # Suggestion command, the category and the suggestion get split by a comma
	await ctx.message.delete()
	channel = bot.get_channel(862484478214930432)
	upvote = "<:upvote:879397319475343420>"
	suggestion = suggestion.replace(' ,', ',').split(',')
	embed = discord.Embed(title=f"Suggested by {ctx.author}:", color=0x9C1796)\
			.add_field(name="Catergory", value=f"{suggestion[0]}", inline=False)\
			.add_field(name="Suggestion", value=f"{suggestion[1]}", inline=False)\
			.set_footer(text="Suggestion forwarded to developers")
	embed_message = await channel.send(embed=embed)
	await embed_message.add_reaction(upvote)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def bug(ctx, *, bug_report: str): # Bug report command, the category and the bug gets split by a comma
	await ctx.message.delete()
	channel = bot.get_channel(876226295896354826) # Bot gets the bug reports channel of gwendalito's support server
	upvote = "<:upvote:879397319475343420>"
	bug_report = bug_report.replace(', ', ',').split(',')
	embed = discord.Embed(title=f"Bug Reported by {ctx.author}:", color=0x9C1796)\
			.add_field(name="Command", value=f"{bug_report[0]}", inline=False)\
			.add_field(name="Bug Definition", value=f"{bug_report[1]}", inline=False)\
			.set_footer(text="Bug forwarded to developers")
	embed_message = await channel.send(embed=embed)
	await embed_message.add_reaction(upvote)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def contact(ctx, *, message): # Command to send a DM to gwendal (me lmao)
	await ctx.message.delete()
	gwendal = bot.get_user(437265873401544705) # Bot gets my user ID to send me a DM

	embed = discord.Embed(title=f"Message sent by '{ctx.author}'")\
			.add_field(name="User ID:", value=f"{ctx.author.id}")\
			.add_field(name="Message:", value=f"{message}")

	await gwendal.send(embed=embed)

bot.run(token) # Run the bot
