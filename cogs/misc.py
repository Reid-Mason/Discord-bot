import random
import time

import discord
from discord.ext import commands

import utils


class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def profile(self, ctx, user: discord.Member = None):
    """ Get information about a Discord user.

    Argument 'user', if specified, is the user to get information about.
    'user' can be submitted using the users name, nickname, id or a mention.
    If 'user' isn't entered it will display your profile.

    Included information:
        Nickname
        Name
        ID
        Account creation date
        Date of joining the server
        Current status (online, offline, away, etc)
        The top role in the server
    """
    user = ctx.author if user is None else user

    # Create the embed object for the message
    em = utils.embed(title=f"{user.display_name} #{user.discriminator}", thumbnail=user.avatar_url,
                     colour=user.colour)
    # Add fields containing all the information
    em.add_field(name="Name", value=user.name)
    em.add_field(name="Id", value=user.id)
    em.add_field(name="Created", value=utils.format_time(user.created_at))
    em.add_field(name="Joined", value=utils.format_time(user.joined_at))
    em.add_field(name="Status", value=user.status)
    em.add_field(name="Top role", value=user.top_role)

    # Adding user activity information
    if user.activity is not None:
      activity = user.activity.type.name.title()
      activity_name = user.activity.name

      # Formatting for if the activity is listening to make grammar correct
      activity = activity + ' to' if activity == 'Listening' else activity

      # Add support for Spotify by displaying the song title and the artist
      if activity_name == 'Spotify':
        activity_name += f': {user.activity.title} by {user.activity.artist}'

      em.add_field(name=activity, value=activity_name)

    await ctx.send(embed=em)

  @commands.command()
  async def ping(self, ctx):
    """ Test the latency to the bot and see how fast it responds """

    # Create embed for message
    em = utils.embed(title=f"Ping", description="Pinging")

    start = time.perf_counter()
    message = await ctx.send(embed=em)
    end = time.perf_counter()
    # Work out Time difference and convert to milliseconds
    duration = (end - start) * 1000

    em.description = f'Pong! {round(duration, 2)}ms'
    await message.edit(embed=em)

  @commands.command(aliases=["hi", "sup", "hey", "yo", "howdy"])
  async def hello(self, ctx):
    """ Say hello and get a random greeting from the bot."""

    # Pick a random greeting to reply with from the aliases
    greeting = random.choice([x.aliases for x in self.bot.commands if x.name == 'hello'][0]).title()

    # Send greeting message
    await ctx.send(embed=utils.embed(title="Hello", description=f"{greeting} {ctx.author.mention}!",
                                     thumbnail='https://static.tumblr.com/gwp7jk3/QXAma9845/k-on_wave.gif'))

  @commands.command(aliases=["calc"])
  async def math(self, ctx, equation: str):
    """ Get the result to basic arithmetic. """
    try:
      # Send result
      await ctx.send(embed=utils.embed(title="Math", description=f"{equation.strip()} = {eval(equation)}"))
    except SyntaxError:
      # If a syntax error occured print the result as "SyntaxError"
      await ctx.send(embed=utils.embed(title="Math", description=f"{equation.strip()} = SyntaxError"))

  @commands.command(aliases=["inv"])
  async def invite(self, ctx):
    """ Get an invite link for the server.

    If a server doesn't have an invite link then a new one will be generated.
    Otherwise an existing one will be displayed.
    """

    # Check for invite links
    if len(await ctx.guild.invites()) < 1:
      await ctx.guild.channels[0].create_invite()

    # Send invite link
    await ctx.send((await ctx.guild.invites())[0].url)


def setup(bot):
  bot.add_cog(Misc(bot))
