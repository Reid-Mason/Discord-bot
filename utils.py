import os
import sys

import discord
from colorama import Fore, Style

from config import EMBED_COLOUR


def log(text, *style):
  """ Logs text with a specified style using colorama styles """
  sys.stdout.write((''.join(style) + text).ljust(100) + Style.RESET_ALL)
  sys.stdout.flush()


def load_cogs(bot, path):
  """ All cogs into the passed bot from the specified path.

  Cogs are categories for holding multiple commands from the 'discord.ext.commands.cog' class.

  :param bot: The bot to load cogs into. Instance of 'discord.ext.commands.bot'.
  :param path: The path to the folder where the cogs files are stored.
  """
  log(f"\n  Loading cogs", Fore.CYAN)
  # Browse all files in the path that end with '.py'
  files = [x for x in os.listdir(path) if x.endswith('.py')]
  # Load all files found
  list(map(lambda c: bot.load_extension('cogs.' + c[:-3]), files))
  log(f"\r  Loading cogs complete. {len(files)} cogs loaded", Fore.GREEN)


def embed(**kwargs):
  """ Creates an instance of 'discord.Embed' for consistent message formatting.

  :param kwargs: A list of properties that can be added to the embed:
    title - The title for the embed
    description - Smaller text under the title
    colour - The colour of the left bar (hex value)
    thumbnail - The small image that appears on the right of the embed (url)
    image - A large image that appears in the middle of the embed (url)
    author - The same as title but allows for the text to have a link attached
    author_url - The link attached to the author field
    author_icon - Small icon that appears on the left of the author text
    footer_text - Small text that appears at the bottom of the embed
    footer_icon - Small icon that appears on the left of the footer
  :return: The completed Embed object
  """

  # Create the Embed object
  em = discord.Embed(title=kwargs.get('title'), description=kwargs.get('description'))

  # Assign ass passed properties
  em.colour = kwargs.get('colour', EMBED_COLOUR)
  em.set_thumbnail(url=kwargs.get('thumbnail', ''))
  em.set_image(url=kwargs.get('image', ''))
  em.set_author(name=kwargs.get('author', ''), url=kwargs.get('author_url', ''),
                icon_url=kwargs.get('author_icon', ''))
  em.set_footer(text=kwargs.get('footer_text', ''), icon_url=kwargs.get('footer_icon', ''))

  return em


def format_time(time):
  """ Format time to my preferred display format. """
  return time.strftime("%a, %d %b %Y %I:%M:%S %p")
