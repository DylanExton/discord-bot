## TODO LIST: ##
# - remove temperature
# - create category name to be something more important
# - create request logic

## Import Statements ##
import discord
import configparser
import os
import psutil
import datetime
import requests
import json
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from discord.ext import commands
from discord.ext import tasks

## Parse Config File ##
config = configparser.ConfigParser()
config.read('/home/bot/conf/discordConfig.cfg')

token = config['DISCORD']['token']

current_state = []

client = commands.Bot(command_prefix='!')

def cpu_usage():
    usage = psutil.cpu_percent()
    return usage

def ram_usage():
    usage = psutil.virtual_memory()
    used_free = str(round(usage.used /1024/1024/1024,2)) +"GB/"+ str(round(usage.total/1024/1024/1024,2))+"GB"
    return used_free

@client.command()
async def CPU(ctx):
    cpuUsage = cpu_usage()
    ram = ram_usage()
    Cat = client.get_channel(955316272290218035)
    newName = "CPU: {0}% | RAM: {1}".format(cpuUsage,ram)
    await Cat.edit(name=newName)


@client.command(pass_context=True)
async def cc(ctx, base, convert, multiplier=1.0):
    # Get the two currencies
    baseCurr = base.upper()
    convertCurr = convert.upper()
    #Send the request
    url = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}".format(convertCurr,baseCurr,multiplier)
    payload = {}
    headers= {
      "apikey": "hVl1QA5fDQNwjm385msOnA1mQKFvkS0Z"
    }
    print("URL is: {}".format(url))
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
    currEmbed.set_footer(text=emFooter, icon_url=ctx.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=currEmbed)

@client.command()
async def cci(ctx):
    await ctx.send(
        "Select a thing",
        components = [
            Select(
                placeholder = "Select something!",
                options = [
                    SelectOption(label = "A", value = "A"),
                    SelectOption(label = "B", value = "B")
                ]
            )
        ]
    )

    interaction = await client.wait_for("select_option")
    print(interaction.values[0])
    await interaction.send(content = f"{interaction.values[0]} selected!")

@client.command(pass_context=True)
async def embed(ctx, car, date):
    name = ctx.message.author
    desc = str(name) + " would like a " + str(car) + " livery by " + str(date)
    embed=discord.Embed(title=name, url="", description=desc, color=0xFF0000)
    await ctx.send(embed=embed)

client.run(token)
