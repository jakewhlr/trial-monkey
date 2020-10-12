"""
This module is used as a discord bot interface for the Trial class.
"""


import re
import random
from time import sleep
import logging
import os

import discord
from discord.ext import commands

from .trial import TrialMonkey

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

EMOJI = ['🤺', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣']

GIFS = [
    "https://media.giphy.com/media/5Zesu5VPNGJlm/giphy.gif",
    "https://media.giphy.com/media/pFwRzOLfuGHok/giphy.gif",
    "https://media.giphy.com/media/X7NFveezX68Cc/giphy.gif",
    "https://media.giphy.com/media/T8Dhl1KPyzRqU/giphy.gif",
    "https://media.giphy.com/media/jR8EDxMbqi1QQ/giphy.gif",
    "https://media.giphy.com/media/VjAB0fOmK15Ze/giphy.gif",
    "https://media.giphy.com/media/MVwMFGdw1KIuI/giphy.gif",
    "https://media.giphy.com/media/URW2lPzihY5fq/giphy.gif",
    "https://media.giphy.com/media/RETg1tippXtNm/giphy.gif",
    "https://media.giphy.com/media/wGlm5NGNBcyI0/giphy.gif",
    "https://media.giphy.com/media/st7q18mjEvCbm/giphy.gif",
    "https://media.giphy.com/media/l4FGFT5D4NKA9rGxy/giphy.gif",
    "https://media.giphy.com/media/3oEdv1EbS2Ss1NvrUc/giphy.gif",
    "https://media.giphy.com/media/3o85xC73J7y0c9wJWM/giphy.gif",
    "https://media.giphy.com/media/xTiTnnGAwpXyng7pny/giphy.gif",
    "https://media.giphy.com/media/jR8EDxMbqi1QQ/giphy.gif",
    "https://media.giphy.com/media/wGlm5NGNBcyI0/giphy.gif",
    "https://media.giphy.com/media/GVLcJTdkaCSD6/giphy.gif",
    "https://media.giphy.com/media/LnaO0DlxGsHZK/giphy.gif",
    "https://media.giphy.com/media/2tRBdHz4Wwhyw/giphy.gif",
    "https://media.giphy.com/media/1slz5O6wPTR96/giphy.gif",
    "https://media.giphy.com/media/H4zeDO4ocDYqY/giphy.gif",
    "https://media.giphy.com/media/OLY40BwPRUWic/giphy.gif",
    "https://media.giphy.com/media/BhW85yDQ1TA3u/giphy.gif",
    "https://media.giphy.com/media/10ORk7l5EDa4JG/giphy.gif",
    "https://media.giphy.com/media/jAhQUPJwoFVK/giphy.gif",
    "https://media.giphy.com/media/SDeVLvFCqFsSA/giphy.gif",
    "https://media.giphy.com/media/BhW85yDQ1TA3u/giphy.gif",
    "https://media.giphy.com/media/bLHJ71uLsgqWI/giphy.gif",
    "https://media.giphy.com/media/xTtWfzDYKUW6uFdC5w/giphy.gif",
    "https://media.giphy.com/media/RlhQbYtETaRfG/giphy.gif",
    "https://media.giphy.com/media/1229mlttgo8aR2/giphy.gif",
    "https://media.giphy.com/media/5xaOcLQr8f0BDMf5FT2/giphy.gif",
    "https://media.giphy.com/media/ToMjGpA1hOaWo1LoWgE/giphy.gif",
    "https://media.giphy.com/media/Ujgg3ApoTGoKs/giphy.gif",
    "https://media.giphy.com/media/OLY40BwPRUWic/giphy.gif",
    "https://media.giphy.com/media/1316cEyMAtS3GE/giphy.gif",
    "https://media.giphy.com/media/5cdenDXni65aM/giphy.gif",
    "https://media.giphy.com/media/8yyJH4yzqgx0Y/giphy.gif",
    "https://media.giphy.com/media/R8s2pWPslY0dG/giphy.gif",
    "https://media.giphy.com/media/8nhgZZMKUicpi/giphy.gif",
    "https://media.giphy.com/media/l3q2ZNVuqIHQaJ464/giphy.gif",
    "https://media.giphy.com/media/yLZQKurQvmIAo/giphy.gif",
    "https://media.giphy.com/media/vBzDAe90oDE3u/giphy.gif",
    "https://media.giphy.com/media/5UpJKX2gwruqk/giphy.gif",
    "https://media.giphy.com/media/YKinVqdj8ZOA8/giphy.gif",
    "https://media.giphy.com/media/YKFnKWYbKREHu/giphy.gif",
    "https://media.giphy.com/media/1wqYonEBtues7jlngs/giphy.gif",
    "https://media.giphy.com/media/QNFhOolVeCzPQ2Mx85/giphy.gif",
    "https://media.giphy.com/media/mRdI3FMUexmuc/giphy.gif"
]


class TrialBot:
    """
    Discord bot interface for Trial class
    """
    client = discord.Client()
    bot = commands.Bot(command_prefix='trialmonkey!', case_insensitive=True)
    trials = []
    current_trial_index = None
    token = None
    assigned_emoji = {}
    assigned_emoji_inv = {}
    trial_monkey = TrialMonkey()
    current_status_message = None

    def __init__(self, token):
        self.token = token
        self.current_status_message = None

    async def start(self):
        """
        Login to discord and connect to the server.
        """
        await self.bot.login(self.token, bot=True)
        await self.bot.connect()

    def gen_status_embed(self, trial):
        """
        Returns a discord.Embed object from the status of the current trial.

        Positional arguments:
                trial (Trial): The current trial object
        """
        status_dict = trial.status()
        status_embed = discord.Embed()
        status_embed.title = status_dict['title']
        status_embed.description = status_dict['description']
        for item in status_dict['votes'].keys():
            if item == "fence":
                name = "The Fence " + self.assigned_emoji_inv[item]
                if status_dict['votes'][item]:
                    value = ', '.join(status_dict['votes'][item])
                else:
                    value = '‌‌ '
                status_embed.insert_field_at(
                    index=0,
                    name=name,
                    value=value,
                    inline=False
                )
            else:
                name = self.assigned_emoji_inv[item] + " " + item.title()
                if status_dict['votes'][item]:
                    value = '\n'.join(status_dict['votes'][item])
                else:
                    value = '‌‌ '
                status_embed.add_field(name=name, value=value)
        return status_embed

    def set_command_prefix(self, new_command_prefix):
        """
        Sets the command prefix of the bot to the given string (typically the
        bot user's username).

        Positional arguments:
                new_command_prefix (str): The command prefix to set,
                        typically the username of the bot user.
        """
        if new_command_prefix:
            self.bot.command_prefix = new_command_prefix
            logging.info(
                "Set bot prefix to: '{}'".format(self.bot.command_prefix)
            )
        else:
            logging.error("Failed to set bot prefix")
            raise ValueError

    def check_valid_reaction(
        self,
        bot_user_id=None,
        user_id=None,
        status_message_id=None,
        message_id=None,
        emoji=None
    ):
        """
        Checks the the reaction for valididty. The reaction is valid if:
        the reacting user is not the bot user, the message reacted to is
        the current status message, and the emoji reacted with is associated
        with a vote.

        Keyword arguments:
            bot_user_id (int): User id of the bot user.
            status_message_id (int): Message id of the status message.
            message_id (int): Message id of the message reacted to.
            user_id (int): User id of the reacting user.
            emoji (char): Emoji the user reacted with.

        TODO: Lower amount of arguments, maybe use kwargs.
        TODO: Accept that this won't be properly tested
                    and bake this into on_reaction_add.
        """
        if message_id != status_message_id:
            return False
        if user_id == bot_user_id:
            return False
        if emoji not in self.assigned_emoji.keys():
            logging.info(
                "Ignoring invalid emoji {} on message {}".format(
                    emoji,
                    message_id
                )
            )
            return False
        return True

    def valid_reaction(self, reaction, user):
        if reaction.message.id != self.current_status_message.id:
            return False
        if user == self.bot.user:
            return False
        return True

    def split_args(self, args_string):
        """
        Splits a string denoting a trial (i.e. Good vs. Evil) into a
        workable list, returns that list.

        Positional arguments:
            args_string (str): String to split.

        TODO: Maybe move this to Trial class.
        """
        split_options = re.split(' v | v. | vs | vs. | versus ', args_string)
        if len(split_options) < 2:
            return None
        return split_options

    @bot.event
    async def on_ready():
        """
        Function is called when the bot has successfully connected to a server.
        """
        TrialBot.set_command_prefix(TrialBot, "<@!{}> ".format(
            TrialBot.bot.user.id)
        )

    @bot.event
    async def on_reaction_add(reaction, user):
        """
        Function is called when a reaction is added to a message.

        Positional arguments:
                reaction: The reaction object that was added.
                user: The user object who added the reaction.

        """
        if TrialBot.valid_reaction(TrialBot, reaction, user):
            try:
                TrialBot.trial_monkey.vote(reaction.emoji, user.display_name)
                await reaction.remove(user)
                embed_object = discord.Embed.from_dict(
                    TrialBot.trial_monkey.status()
                )
                await TrialBot.current_status_message.edit(
                    embed=embed_object)
                return 0
            except discord.DiscordException as err:
                logging.error(err)
                return 1
        else:
            return 1

    @bot.command(help="Sends mokney gif")
    async def gif(ctx):
        """
        Sends random gif from gifs.txt.
        """
        monkey_gif = random.choice(GIFS)
        await ctx.send(monkey_gif)

    @bot.command(
        pass_context=True,
        help="Creates new trial",
        usage="(<plaintiff> <defendant>)"
    )
    async def new(ctx, *, arg):
        """
        Creates new trial from arg string.
        """
        logging.info("New trial: {}".format(arg))
        await TrialBot.gif.invoke(ctx)
        sleep(random.randint(3, 10))

        TrialBot.trial_monkey.new_trial(arg)

        await TrialBot.status.invoke(ctx)

    @bot.command(
        help="Shows status of given trial (default=current)",
        usage="[<trial_number>]"
    )
    async def status(ctx):
        """
        Sends Embed object of current trial status.
        """
        status_dict = TrialBot.trial_monkey.status()
        embed_object = discord.Embed.from_dict(status_dict)
        TrialBot.current_status_message = await ctx.send(embed=embed_object)
        assigend_emoji = TrialBot.trial_monkey.get_emoji()
        for item in assigend_emoji:
            await TrialBot.current_status_message.add_reaction(item)
            sleep(0.5)

    @bot.command(aliases=["adjourned", "end", "close"])
    async def adjourn(ctx):
        """
        Ends the current trial, tallies votes, and announces a winner.

        TODO: Fix tallying.
        TODO: Deselect trial/Set index to None.
        """
        TrialBot.trial_monkey.adjourn()
        await ctx.send('COURT ADJOURNED')

    @bot.command()
    async def list(ctx):
        """
        Sends a list of the curent available trials, with indexes.

        TODO: Prettify message.
        """
        list_dict = TrialBot.trial_monkey.list()
        embed_object = discord.Embed.from_dict(list_dict)
        await ctx.send(embed=embed_object)

    @bot.command()
    async def select(ctx, index):
        """
        Changes current trial to the given index, if it is valid.

        Positional arguments:
                index (int): Index of trial to select, from self.list()

        TODO: Fix long lines.
        """
        TrialBot.trial_monkey.select(index)
        await TrialBot.status.invoke(ctx)

    @bot.command()
    async def rename(ctx, old_name, new_name):
        TrialBot.trial_monkey.rename(old_name, new_name)
        await TrialBot.status.invoke(ctx)
