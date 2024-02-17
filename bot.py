import logging

from discord.ext import commands, tasks
from config import config
from logDumper import LogDumper
from r34API import R34API
from messages import messages, logTemplates
from activityList import activities

import discord
import time
import datetime
import random

dailyDoseTime = [
    datetime.time(12, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=3)))
]


class TheRes3ar4er(commands.Bot):
    def __init__(self, locale):
        self.API = R34API()
        self.__logDumper = LogDumper()
        self.locale = locale
        self.searchTags = set()
        self.filterTags = set()
        self.__logDumper.send('Bot successfully deployed!')
        super().__init__(command_prefix=config['bot']['prefix'], intents=discord.Intents.all())

    @tasks.loop(hours=8)
    async def dumpLogs(self):
        self.__logDumper.send("make a dumper, you lazy ass")
        pass

    @tasks.loop(time=dailyDoseTime)
    async def dailyDose(self):
        await self.wait_until_ready()
        chan = self.get_channel(int(config['bot']['daily_dose_chan']))
        await chan.send(messages[self.locale]['daily_dose'])
        recentPosts = self.API.getPosts(10)
        for recentPost in recentPosts:
            await chan.send(recentPost)
            time.sleep(config['bot']['sending_delay'])
        await chan.send(messages[self.locale]['finish'])

    @tasks.loop(hours=1)
    async def changePresence(self):
        await self.wait_until_ready()
        await self.change_presence(
            status=discord.Status.online,
            activity=random.choice(activities)
        )

    async def setup_hook(self):
        self.changePresence.start()
        self.dailyDose.start()
        self.dumpLogs.start()


async def sendPosts(ctx, messageBegin, messageFinish, posts):
    await ctx.send(messageBegin)
    for post in posts:
        await ctx.send(post)
        time.sleep(config['bot']['sending_delay'])
    await ctx.send(messageFinish)


logging.basicConfig(level=logging.INFO, filename='botLog.log', format="[%(asctime)s] [%(levelname)s] %(message)s")
bot = TheRes3ar4er(config['bot']['locale'])


# regular commands, result = posts
@bot.command(name='test')
async def test(ctx):
    if ctx.author != bot.user:
        logging.info(
            logTemplates['command'] % ('test', ctx.author)
        )
        posts = bot.API.getPosts(10, {'yuri'})

        await sendPosts(
            ctx,
            messages[bot.locale]['test'],
            messages[bot.locale]['finish'],
            posts
        )
        logging.info(
            logTemplates['success'] % (str(posts))
        )


@bot.command(name='recent')
async def getRecent(ctx, amount):
    if ctx.author != bot.user:
        logging.info(
            logTemplates['command'] % ('recent', ctx.author)
        )
        if amount.isdigit():
            posts = bot.API.getPosts(
                int(amount)
            )
            await sendPosts(
                ctx,
                messages[bot.locale]['recent'],
                messages[bot.locale]['finish'],
                posts
            )
            logging.info(
                logTemplates['success'] % (str(posts))
            )
        else:
            logging.error(
                logTemplates['failed'] % ('Invalid amount value: %s' % amount)
            )
            await ctx.send(
                messages[bot.locale]['error'] % (
                    '$r34er-get-recent',
                    messages[bot.locale]['posts_to_send']
                )
            )


@bot.command(name='tagged')
async def getTagged(ctx, amount):
    logging.info(
        logTemplates['command'] % ('tagged', ctx.author)
    )
    if amount.isdigit():
        posts = bot.API.getPosts(
            int(amount),
            bot.searchTags
        )
        await sendPosts(
            ctx,
            messages[bot.locale]['tagged'] % " ".join(bot.searchTags),
            messages[bot.locale]['finish'],
            posts
        )
        logging.info(
            logTemplates['success'] % (str(posts))
        )
    else:
        logging.error(
            logTemplates['failed'] % ('Invalid amount value: %s' % amount)
        )
        await ctx.send(
            messages[bot.locale]['error'] % (
                '$r34er-get-recent',
                messages[bot.locale]['posts_to_send']
            )
        )

# these commands add tags to some lists


@bot.command(name='manage-tags')
async def manageTags(ctx, command, tagType, tag):
    if ctx.author != bot.user:
        logging.info(
            logTemplates['command'] % ('manage-tags', ctx.author)
        )
        match command:
            case 'add':
                match tagType:
                    case 'search':
                        bot.searchTags.add(tag)
                        logging.info(
                            logTemplates['success'] % (
                                'tag %s added to %s tags' % (
                                    tag, tagType
                                )
                            )
                        )
                        await ctx.send(
                            messages[bot.locale]['add_search'] % (
                                tag
                            )
                        )
                    case 'filter':
                        bot.filterTags.add(tag)
                        logging.info(
                            logTemplates['success'] % (
                                'tag %s added to %s tags' % (
                                    tag, tagType
                                )
                            )
                        )
                        await ctx.send(
                            messages[bot.locale]['add_filter'] % (
                                tag
                            )
                        )
                    case _:
                        logging.error(
                            logTemplates['failed'] % ('Invalid tag type: %s' % str(tagType))
                        )
                        await ctx.send(
                            messages[bot.locale]['error_mt']
                        )

            case 'delete':
                match tagType:
                    case 'search':
                        if tag in bot.searchTags:
                            bot.searchTags.remove(tag)
                        logging.info(
                            logTemplates['success'] % (
                                'tag %s deleted from %s tags' % (
                                    tag, tagType
                                )
                            )
                        )
                        await ctx.send(
                            messages[bot.locale]['delete_search'] % (
                                tag
                            )
                        )
                    case 'filter':
                        if tag in bot.filterTags:
                            bot.filterTags.remove(tag)
                        logging.info(
                            logTemplates['success'] % (
                                'tag %s deleted from %s tags' % (
                                    tag, tagType
                                )
                            )
                        )
                        await ctx.send(
                            messages[bot.locale]['delete_filter'] % (
                                tag
                            )
                        )
                    case _:
                        logging.error(
                            logTemplates['failed'] % ('Invalid tag type: %s' % str(tagType))
                        )
                        await ctx.send(
                            messages[bot.locale]['error_mt']
                        )
            case _:
                logging.error(
                    logTemplates['failed'] % ('Invalid command type: %s' % str(command))
                )
                await ctx.send(
                    messages[bot.locale]['error_mt']
                )


@bot.command('reset-tags')
async def resetTags(ctx, tagType):
    if ctx.author != bot.user:
        logging.info(
            logTemplates['command'] % ('reset-tags', ctx.author)
        )
        match tagType:
            case 'search':
                bot.searchTags.clear()
                logging.info(
                    logTemplates['success'] % (
                        '%s tags have been reset' % (
                            tagType
                        )
                    )
                )
                await ctx.send(
                    messages[bot.locale]['reset_search']
                )
                pass
            case 'filter':
                bot.searchTags.clear()
                logging.info(
                    logTemplates['success'] % (
                        '%s tags have been reset' % (
                            tagType
                        )
                    )
                )
                await ctx.send(
                    messages[bot.locale]['reset_filter']
                )
            case 'all':
                bot.searchTags.clear()
                logging.info(
                    logTemplates['success'] % (
                        'all tags have been reset'
                    )
                )
                await ctx.send(
                    messages[bot.locale]['reset_all']
                )
            case _:
                logging.error(
                    logTemplates['failed'] % ('Invalid tag type: %s' % str(tagType))
                )
                await ctx.send(
                    messages[bot.locale]['error_rvt'] % (
                        '$r34er-reset-tags'
                    )
                )


@bot.command('view-tags')
async def resetTags(ctx, tagType):
    if ctx.author != bot.user:
        logging.info(
            logTemplates['command'] % ('view-tags', ctx.author)
        )
        match tagType:
            case 'search':
                await ctx.send(
                    messages[bot.locale]['view_search'] % (
                        " ".join(bot.searchTags)
                    )
                )
                logging.info(
                    logTemplates['success'] % (
                        " ".join(bot.searchTags)
                    )
                )
            case 'filter':
                await ctx.send(
                    messages[bot.locale]['view_filter'] % (
                        " ".join(bot.filterTags)
                    )
                )
                logging.info(
                    logTemplates['success'] % (
                        " ".join(bot.filterTags)
                    )
                )
            case 'all':
                await ctx.send(
                    messages[bot.locale]['view_all'] % (
                        " ".join(bot.searchTags),
                        " ".join(bot.filterTags)
                    )
                )
                logging.info(
                    logTemplates['success'] % (
                        " ".join(bot.searchTags) + ';' + " ".join(bot.filterTags)
                    )
                )
            case _:
                logging.error(
                    logTemplates['failed'] % ('Invalid tag type: %s' % str(tagType))
                )
                await ctx.send(
                    messages[bot.locale]['error_rvt'] % (
                        '$r34er-view-tags'
                    )
                )

bot.run(config['bot']['token'])
