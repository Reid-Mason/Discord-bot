import difflib
import re

from colorama import Back, Fore
from discord.ext import commands
from discord.ext.commands import Bot

import config as cfg
# Create bot with preferences
import utils
from config import TEMP_MSG_TIME
from utils import log

bot = Bot(command_prefix=commands.when_mentioned_or(cfg.command_prefix), description=cfg.description)


@bot.event
async def on_ready():
  """ Function runs when the bot has fully started and connected """
  log(f"\r----- {bot.user.name} online -----", Back.GREEN, Fore.BLACK)


@bot.event
async def on_command_error(ctx, error):
  """ When a command error is raied and not caught in the command this method will handle it.

  If the command was a 'discord.ext.commands.CommandNotFound' error then the user is
  presented with options for other commands that are similar.
  Otherwise the error is just formatted and sent.

  :param ctx: The context object for where the error was raised
  :param error: The error message
  """
  # Get the attempted command
  attempt_cmd = re.findall(r'\?+\w+', str(ctx.message.content))[0]

  if isinstance(error, commands.CommandNotFound):
    # List of possible commands
    poss_cmd = [x.name for x in bot.commands if x.hidden != True]
    # Find closest command match
    suggested_commands = difflib.get_close_matches(str(attempt_cmd), poss_cmd, cutoff=0)
    suggested_commands = '\n    '.join(suggested_commands)

    # Create properties for the embed
    title = f'Command "{attempt_cmd}" not found'
    desc = f'Suggested commands:\n\n    {suggested_commands}'
    # Suggest commands are sent
    await ctx.send(embed=utils.embed(title=title, description=desc), delete_after=TEMP_MSG_TIME)
  else:
    # Error message is sent
    await ctx.send(f"```{error}```", delete_after=TEMP_MSG_TIME)


log("----- Initializing -----", Back.CYAN, Fore.BLACK)
# Load all cogs from the cogs file
utils.load_cogs(bot, 'cogs')

log(f"\n\n----- Starting bot -----", Back.YELLOW, Fore.BLACK)
bot.run(cfg.token)
