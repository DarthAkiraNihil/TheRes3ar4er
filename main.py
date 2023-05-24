import discord
from discord.ext import commands
import requests
from xml.etree.ElementTree import XML, fromstring
import time
#from config import settings

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$r34er-', intents=intents)

activeTags = []

@bot.command(name='test') # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def test(ctx, arg):
    #print(ctx.content)
    #content = ctx.message # Создаём функцию и передаём аргумент ctx.
    #command = ctx.content.split()
    if ctx.author != bot.user:
        parsedResponse = fromstring(requests.get("https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=yuri").text)
        counter = 0
        for child in parsedResponse:
            await ctx.send(child.attrib['file_url'])
            counter += 1
            if counter == int(arg):
                break
        #await ctx.reply(ctx.content)
        #print(ctx.content) # Выводим сообщение с упоминанием автора, обращаясь к переменной author.

@bot.command(name='add-tag')
async def addTag(ctx, tag):
    if ctx.author != bot.user:
        activeTags.append(tag)
        await ctx.send(f'Тег \"{tag}\" был добавлен в список активных')

@bot.command(name='view-tagged')
async def addTag(ctx, amount):
    print(amount)
    if ctx.author != bot.user and amount.isdigit():
        await ctx.send('Осуществляется вывод пикч с тегами' + ', '.join(activeTags))
        apiRequestTemplate = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags='
        for tag in activeTags:
            apiRequestTemplate += (tag + '+')
        #apiRequestTemplate = apiRequestTemplate[:-1]
        print(apiRequestTemplate)
        parsedResponse = fromstring(requests.get(apiRequestTemplate).text)
        counter = 0
        if parsedResponse.attrib['count'] == '0':
            await ctx.send('Я не нашёл постов с данными тегами. Попробуйте поменять набор')
        else:
            for child in parsedResponse:
                await ctx.send(child.attrib['file_url'])
                time.sleep(0.4)
                counter += 1
                if counter == int(amount):
                    break
            await ctx.send('Вывод закончен!')
    else:
        await ctx.send('Я вас не понял. Введите команду как $r34er-view-tagged <Количество постов на вывод>')

@bot.command(name='view-tags')
async def addTag(ctx):
    #print(amount)
    
    if ctx.author != bot.user:
        
        response = "Список активных тегов: " + " ".join(activeTags)
        await ctx.send(response)

@bot.command(name='reset-tags')
async def addTag(ctx):
    if ctx.author != bot.user:
        #activeTags = list()
        activeTags.clear()
        await ctx.send('Список активных тегов был успешно очищен')
bot.run('MTExMDYzODI5ODg0Nzc3Njk1MA.Gcl4C9.KdstsyE3VjoTz1qz8smK0kCvyESdk5fgXoBZEY') # Обращаемся к словарю settings с ключом token, для получения токена