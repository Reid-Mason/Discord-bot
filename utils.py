import os
import sys

import discord
from colorama import Style, Fore

from config import EMBED_COLOUR


def log(text, *style):
  """ Logs text with a specified style using colorama styles """
  sys.stdout.write((''.join(style) + text).ljust(100) + Style.RESET_ALL)
  sys.stdout.flush()


def load_cogs(bot, path):
  """ All cogs into the passed bot from the specified path.

  Cogs are categories for holding multiple commands from the 'discord.ext.commands.cog' class.

  :param bot:
  :param path:
  :return:
  """
  log(f"\n  Loading cogs", Fore.CYAN)
  files = [x for x in os.listdir(path) if x.endswith('.py')]
  list(map(lambda c: bot.load_extension('cogs.' + c[:-3]), files))
  log(f"\r  Loading cogs complete. {len(files)} cogs loaded", Fore.GREEN)


def embed(**kwargs):
  em = discord.Embed(title=kwargs.get('title'), description=kwargs.get('description'))

  em.colour = kwargs.get('colour', EMBED_COLOUR)
  em.set_thumbnail(url=kwargs.get('thumbnail', ''))
  em.set_image(url=kwargs.get('image', ''))
  em.set_author(name=kwargs.get('author', ''), url=kwargs.get('author_url', ''),
                icon_url=kwargs.get('author_icon', ''))
  em.set_footer(text=kwargs.get('footer_text', ''), icon_url=kwargs.get('footer_icon', ''))

  return em


def format_time(time):
  """Format time to my preferred display format."""
  return time.strftime("%a, %d %b %Y %I:%M:%S %p")
