import discord
import asyncio
import time

from time import strftime
from time import localtime
from discord import utils
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot
from asyncio import sleep

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='//', intents=intents)

token = ""

banwordson = 'true'

@client.event
async def on_message(message):
 if message.content.startswith('ваш префикс тут'): await client.process_commands(message)
 else:
    banwords = ["хуй", "блядина", "пизда", "пидр", "пидор", "пидар", "пидорас", "пидарас", "гандон", "сука", "даун", "дибил", "сучка", "ебать", "еблан", "ахуеть", "ебать", "нихуя", "пиздец", "блядь", "блять", "член", "залупа"]
    if banwordson == 'true':
        if message.author == client.user: return
        for word in banwords:
            if word in message.content.lower():
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(f'{message.author.mention}, мат запрещен!')
                break
    elif banwordson == 'false':
        pass

@client.command()
async def automoderation(ctx):
 global banwordson
 if banwordson == 'true':
     await ctx.reply('Здравствуйте, уважаемый администратор! Выключаю автоматическую модерацию...')
     banwordson = 'false' 
 else:
     await ctx.reply('Здравствуйте, уважаемый администратор! ~~Выключаю~~ Включаю автоматическую модерацию...')
     banwordson = 'true' 

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```Укажите аргументы```')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("```Вы не имеете права```")


@client.event
async def on_ready():
    print("start")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Security"))

@client.command()
async def support(ctx):
    await ctx.send(f"Commands:\n//support (команды бота)\n//info (информация)\n//ban [участник] [время] [причина]\n//hello (приветствие)\n//clear [число сообщений] (очистка сообщений)\n//code (код бота)")  #перенос строки осуществляется добавлением: \n без кнопки Enter!

@client.command()
async def info(ctx):
    await ctx.send(f"Я создан для Автомодерации\nЧто я могу?\n1.удалять маты и бранные слова!\n2.банить участников\n(бот находится в разработке!!!)")

@client.command()
async def code(ctx):
    await ctx.send(f"ссылка на код бота:")

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, time: int, reason):
  await ctx.send(f'{member.mention} **забанен** \n Продолжительность бана: *{time}d* \n Причина бана: *{reason}*')
  #отправить пользователю личное сообщение о бане "Тебя забанили на сервере {server} по причине {reason}
  await member.ban(reason=reason)
  await asyncio.sleep(time * 86400)
  await member.unban()
  await ctx.send(f'*У {member.mention} закончился бан*')
  #отправить пользователю личное сообщение о разбане "У тебя закончился бан на сервере {server} <ссылка на сервер>; Тебя разбанили на сервере {server} <ссылка на сервер>

@client.command()
async def hello(ctx):
    await ctx.author.send(f'Привет, бро!')
    await ctx.author.send(f':)')

@client.command()
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f"Очищено **{amount}** сообщений")

client.run(token)