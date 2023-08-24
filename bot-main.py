## TODO LIST: ##
# - remove temperature
# - create category name to be something more important
# - create request logic
# - refactor and use new libraries

## Import Statements ##
import discord
import configparser
import os
import psutil
import datetime
import requests
import json
from discord.ext import commands
from discord.ext import tasks
import logging
import logging.handlers

## Setup Logging ##

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='/home/dexton/logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=31,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

## Parse Config File ##
config = configparser.ConfigParser()
config.read('/home/dexton/conf/bot.cfg')

token = config['DISCORD']['token']
ccAPIToken = config['DISCORD']['ccAPIKey']

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

def cpu_usage():
    usage = psutil.cpu_percent()
    print(f'{usage}')
    logger.info(f'CPU Usage: {usage}')
    return usage

def ram_usage():
    usage = psutil.virtual_memory()
    used_free = str(round(usage.used /1024/1024/1024,2)) +"GB/"+ str(round(usage.total/1024/1024/1024,2))+"GB"
    print(f'{usage} | {used_free}')
    logger.info(f'RAM Usage: {usage} | {used_free}')
    return used_free

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for guild in client.guilds:
        print(f'{client.user} has joined {guild.name} - {guild.id}')
        logger.info(f'{client.user} has joined {guild.name} - {guild.id}')


@client.command()
async def CPU(ctx):
    print(f'CPU Command Recieved')
    cpuUsage = cpu_usage()
    ram = ram_usage()
    print(f'{cpuUsage} | {ram}')
    resourceUsage = "CPU: {0}% | RAM: {1}".format(cpuUsage,ram)
    logger.info(f'CPU Command executed by {ctx.author} returned {resourceUsage}')
    await ctx.channel.send(resourceUsage)






@client.command(pass_context=True)
async def cc(ctx, base, convert, multiplier=1.0):
    # Get the two currencies
    baseCurr = base.upper()
    convertCurr = convert.upper()
    #Send the request
    url = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}".format(convertCurr,baseCurr,multiplier)
    payload = {}
    headers= {
      "apikey": ccAPIToken
    }
    logger.info("URL is: {}".format(url))
    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code
    result = response.text
    data = response.json()
    print(data)
    us = data['result']
    now = datetime.datetime.now()
    nowTime= now.strftime("%Y-%m-%d %H:%M:%S")
    emTitle = '{} to {} Conversion'.format(baseCurr,convertCurr)
    emFooter = 'Retrieved at {} NZT'.format(nowTime)
    fmTotal = '{}'.format(us)
    currEmbed=discord.Embed(title=emTitle, description="Currency Converter", color=0x00bbff)
    currEmbed.add_field(name=baseCurr, value='{}'.format(float(multiplier)), inline=False)
    currEmbed.add_field(name=convertCurr, value=fmTotal, inline=False)
    currEmbed.set_footer(text=emFooter, icon_url=ctx.author.avatar.url)
    logger.info(f'Currency Converter command called by {ctx.author} which returned HTTP{status_code} : {emTitle}: {result}')
    await ctx.message.delete()
    await ctx.send(embed=currEmbed)

client.run(token, log_handler=None)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         print(f'{message.author} says Hello')
#         await message.channel.send('Hello!')