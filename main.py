import discord
import requests
import time
import logging
import rule34api
import config

from discord.ext import commands
from xml.etree.ElementTree import fromstring

# intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$r34er-', intents=discord.Intents.all())

activeTags = []

activeFilter = []

logging.basicConfig(level=logging.INFO, filename='botLog.log', format="[%(asctime)s] [%(levelname)s] %(message)s")


@bot.command(name='test')
async def test(ctx):
    if ctx.author != bot.user:
        await ctx.send('Выполняю тестовую команду')
        logging.info('Requested \"test\" command')
        posts = rule34api.getTagged(['yuri'], 10)
        for post in posts:
            await ctx.send(post)
            time.sleep(1)
        await ctx.send('Вывод закончен!')


@bot.command(name='add-tag')
async def addTag(ctx, tag):
    if ctx.author != bot.user:
        logging.info('Requested \"add-tag\" command [arg: %s]' % tag)
        activeTags.append(tag)
        await ctx.send(f'Тег \"{tag}\" был добавлен в список активных')
        logging.info('Successfully added the tag \"%s\"' % tag)


@bot.command(name='view-tagged')
async def addTag(ctx, amount):
    print(amount)
    if ctx.author != bot.user:
        logging.info('Requested \"view-tagged\" command [arg: %s]' % amount)
        logging.info('Active tags: ' + ', '.join(activeTags))
        if amount.isdigit():
            await ctx.send('Осуществляется вывод пикч с тегами' + ', '.join(activeTags))
            posts = rule34api.getTagged(activeTags, amount)
            for post in posts:
                await ctx.send(post)
                time.sleep(1)
            await ctx.send('Вывод закончен!')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount value: %s' % amount)
            await ctx.send('Я вас не понял. Введите команду как $r34er-view-tagged <Количество постов на вывод>')


@bot.command(name='view-tags')
async def addTag(ctx):
    # print(amount)

    if ctx.author != bot.user:
        logging.info('Requested \"view-tags\" command')
        response = "Список активных тегов: " + " ".join(activeTags)
        await ctx.send(response)


@bot.command(name='reset-tags')
async def addTag(ctx):
    if ctx.author != bot.user:
        logging.info('Requested \"reset-tags\" command')
        activeTags.clear()
        await ctx.send('Список активных тегов был успешно очищен')


@bot.command(name='get-recent')
async def getRecent(ctx, amount):
    if ctx.author != bot.user:
        logging.info('Requested \"get-recent\" command')
        if amount.isdigit():
            await ctx.send('Вывожу недавние посты с сайта')
            recentPosts = rule34api.getRecent(amount)
            for recentPost in recentPosts:
                await ctx.send(recentPost)
                time.sleep(1)
            await ctx.send('Вывод закончен')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount value: %s' % amount)
            await ctx.send("Я вас не понял. Введите команду как $r34er-get-recent <Количество постов на вывод>")


bot.run(config.config['botToken'])
