import discord
from discord.ext import commands
import requests
from xml.etree.ElementTree import XML, fromstring
#from config import settings

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$r34er-', intents=intents)

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

bot.run('MTExMDYzODI5ODg0Nzc3Njk1MA.Gcl4C9.KdstsyE3VjoTz1qz8smK0kCvyESdk5fgXoBZEY') # Обращаемся к словарю settings с ключом token, для получения токена