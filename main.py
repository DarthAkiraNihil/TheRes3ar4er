import discord
import time
import logging
import rule34api
import config

from discord.ext import commands

bot = commands.Bot(command_prefix=config.config['prefix'], intents=discord.Intents.all())

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
            time.sleep(config.config['delay'])
        await ctx.send('Вывод закончен!')


@bot.command(name='add-tag')
async def addTag(ctx, tag):
    if ctx.author != bot.user:
        logging.info('Requested \"add-tag\" command [arg: %s]' % tag)
        activeTags.append(tag)
        await ctx.send(f'Тег \"{tag}\" был добавлен в список активных')
        logging.info('Successfully added the tag \"%s\"' % tag)


@bot.command(name='view-tagged')
async def viewTagged(ctx, amount):
    # print(amount)
    if ctx.author != bot.user:
        logging.info('Requested \"view-tagged\" command [arg: %s]' % amount)
        logging.info('Active tags: ' + ', '.join(activeTags))
        if amount.isdigit():
            await ctx.send('Осуществляется вывод пикч с тегами ' + ', '.join(activeTags))
            posts = rule34api.getTagged(activeTags, int(amount))
            for post in posts:
                await ctx.send(post)
                time.sleep(config.config['delay'])
            await ctx.send('Вывод закончен!')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount value: %s' % amount)
            await ctx.send('Я вас не понял. Введите команду как $r34er-view-tagged <Количество постов на вывод>')


@bot.command(name='view-tags')
async def viewTags(ctx):
    # print(amount)

    if ctx.author != bot.user:
        logging.info('Requested \"view-tags\" command')
        response = "Список активных тегов: " + " ".join(activeTags)
        await ctx.send(response)


@bot.command(name='reset-tags')
async def resetTags(ctx):
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
            recentPosts = rule34api.getRecent(int(amount))
            for recentPost in recentPosts:
                await ctx.send(recentPost)
                time.sleep(config.config['delay'])
            await ctx.send('Вывод закончен')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount value: %s' % amount)
            await ctx.send("Я вас не понял. Введите команду как $r34er-get-recent <Количество постов на вывод>")


@bot.command(name='add-filter-tag')
async def addTagToFilter(ctx, tag):
    if ctx.author != bot.user:
        logging.info('Requested \"add-filter-tag\" command')
        activeFilter.append(tag)
        await ctx.send(f'Тег \"{tag}\" был добавлен в фильтр')
        logging.info('Successfully added the tag \"%s\" to the filter' % tag)


@bot.command(name='view-filter')
async def viewFilter(ctx):
    # print(amount)

    if ctx.author != bot.user:
        logging.info('Requested \"view-filter\" command')
        response = "Список фильтруемых тегов: " + " ".join(activeFilter)
        await ctx.send(response)


@bot.command(name='reset-filter')
async def resetFilter(ctx):
    # print(amount)

    if ctx.author != bot.user:
        logging.info('Requested \"reset-filter\" command')
        activeFilter.clear()
        await ctx.send('Фильтр был успешно сброшен')


@bot.command(name='view-tagged-with-filter')
async def viewTaggedWithFilter(ctx, amount):
    # print(amount)
    if ctx.author != bot.user:
        logging.info('Requested \"view-tagged-with-filter\" command [arg: %s]' % amount)
        logging.info('Active tags: ' + ', '.join(activeTags))
        logging.info('Active filter: ' + ', '.join(activeFilter))
        if amount.isdigit():
            await ctx.send('Осуществляется вывод пикч с тегами ' + ', '.join(activeTags)
                           + ', исключая теги ' + ', '.join(activeFilter))
            posts = rule34api.getTaggedWithFilter(activeTags, activeFilter, int(amount))
            for post in posts:
                await ctx.send(post)
                time.sleep(config.config['delay'])
            await ctx.send('Вывод закончен!')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount value: %s' % amount)
            await ctx.send('Я вас не понял. Введите команду как $r34er-view-tagged-with-filter <Количество постов на вывод>')


@bot.command(name='view-tagged-page')
async def viewTaggedPage(ctx, amount, page):
    if ctx.author != bot.user:
        logging.info('Requested \"view-tagged-page\" command [arg: %s, page^ %s]' % (amount, page))
        logging.info('Active tags: ' + ', '.join(activeTags))
        # logging.info('Active filter: ' + ', '.join(activeFilter))
        if amount.isdigit() and page.isdigit():
            await ctx.send('Осуществляется вывод пикч с тегами ' + ', '.join(activeTags) + ', страница %s' % page)
            posts = rule34api.getTaggedWithFilterCurrentPage(activeTags, activeFilter, int(amount), int(page))
            for post in posts:
                await ctx.send(post)
                time.sleep(config.config['delay'])
            await ctx.send('Вывод закончен!')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount or page value: %s, %s' % (amount, page))
            await ctx.send(
                'Я вас не понял. Введите команду как' +
                '$r34er-view-tagged-page <Количество постов на вывод> <Страница постов>'
            )


@bot.command(name='view-tagged-page-with-filter')
async def viewTaggedPageWithFilter(ctx, amount, page):
    # print(amount)
    if ctx.author != bot.user:
        logging.info('Requested \"view-tagged-with-filter\" command [arg: %s. page: %s]' % (amount, page))
        logging.info('Active tags: ' + ', '.join(activeTags))
        logging.info('Active filter: ' + ', '.join(activeFilter))
        if amount.isdigit() and page.isdigit():
            await ctx.send('Осуществляется вывод пикч с тегами ' + ', '.join(activeTags)
                           + ', исключая теги ' + ', '.join(activeFilter) + ', страница %s' % page)
            posts = rule34api.getTaggedWithFilterCurrentPage(activeTags, activeFilter, int(amount), int(page))
            for post in posts:
                await ctx.send(post)
                time.sleep(config.config['delay'])
            await ctx.send('Вывод закончен!')
            logging.info('Successfully executed!')
        else:
            logging.error('User entered invalid amount or page value: %s' % amount)
            await ctx.send(
                'Я вас не понял. Введите команду как' +
                '$r34er-view-tagged-page-with-filter <Количество постов на вывод> <Страница вывода>'
            )


@bot.command(name='add-tags')
async def addTags(ctx, tagsCount, *args):
    if ctx.author != bot.user:
        logging.info('Requested \"add-tags\" command [arg: %s]' % str(args))
        for i in range(int(tagsCount)):
            activeTags.append(args[i])
        await ctx.send(f'Теги %s были добавлены в список активных' % ', '.join(args))
        logging.info('Successfully added the tags %s' % ', '.join(args))


@bot.command(name='add-tags-to-filter')
async def addTagsToFilter(ctx, tagsCount, *args):
    if ctx.author != bot.user:
        logging.info('Requested \"add-tags-to-filter\" command [arg: %s]' % str(args))
        for i in range(int(tagsCount)):
            activeFilter.append(args[i])
        await ctx.send(f'Теги %s были добавлены в фильтр' % ', '.join(args))
        logging.info('Successfully added the tags %s to filter' % ', '.join(args))


bot.run(config.config['botToken'])
