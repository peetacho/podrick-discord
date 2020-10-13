import discord
from discord.ext import commands, tasks
import time
from datetime import datetime, timedelta,timezone
import re
from dotenv import load_dotenv
import os

############################ IMPORTANT VARIABLES ############################
load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

client = commands.Bot(command_prefix="!")

############################ THE MESSAGE ############################

from send_Covid import *
from send_Quote import *
from send_Fact import *
from send_Weather import *

def get_main_message():
    #### COVID ####
    sc = sendCovid()
    messageCovid = sc.get_hk_stats()

    #### QUOTE ####
    sq = sendQuote()
    messageQuote = sq.get_quote()

    sw = sendWeather()
    messageWeather = sw.get_weather()

    sf = sendFact()
    messageFact = sf.get_fact()

    greeting = "Hello There!"

    main_message = '''
**{}**

**Current Weather Description:**
{}

**COVID 19 Updates:**
{}

**An Inspirational quote:**
{}

**A Random Fun Fact:**
{}

        '''.format(greeting, messageWeather, messageCovid, messageQuote, messageFact)
    return main_message

############################ Hidden Functons ############################

def checkTime():
    current_utc_time = datetime.now(tz=timezone.utc).strftime("%H:%M:%S")
    print("Checking Current UTC Time: " + current_utc_time)
    return current_utc_time


def convertTime(time_to_change):
    try:
        converted_time = (datetime.strptime(
            time_to_change, "%H:%M:%S") - timedelta(hours=8)).strftime("%H:%M:%S")
        print("Checking role time (converted): " + converted_time)
        return converted_time
    except:
        return "@everyone"

############################ SENDS ALL ############################
@tasks.loop(seconds=1)
async def s():
    await send_all()

async def send_all():
    channel = client.get_channel(CHANNEL_ID)
    for i in channel.members:
        if i.name != "Podrick":
            for role in i.roles:
                if convertTime(role.name) == checkTime():
                    print("sending message to: " + i.name)

                    try:
                        main_message = get_main_message()
                    except:
                        main_message = """
Hello There!

Current Weather Description:
Strong to gale fore east to northeasterly winds, weakening gradually overnight. Cloudy with rain and a few squally thunderstorms. Rain will ease off during the day tomorrow. Temperatures will range between 24 and 28 degrees. Seas will be very rough with swells. Sunny periods and one or two rain patches in the following few days.

COVID 19 Updates:
There are __ confirmed cases, __ deaths, and __ active today.

An Inspirational quote:
Inspiration exists, but it has to find us working.   ~Pablo Picasso

A Random Fun Fact:
To Ensure Promptness, one is expected to pay beyond the value of service – hence the later abbreviation: T.I.P.
"""
                    await i.send(main_message)

@client.event
async def on_ready():
    s.start()

############################ ON MEMBER JOIN ############################
@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL_ID)

    instructions = """
**Welcome to Podrick's Server, {}**
Please use the following commands. The variable __*time*__ (00:00:00 format) represents the time you want Podrick to message you.

```css
!role [time]
!deleterole [time]
```
Example:
```css
!role 04:20:00
```
""".format(member.name)
    await member.send(instructions)
    await channel.send(instructions)

############################ ADD/DELETE TIME ROLES ############################
def is_time(time_str):
    return re.match('\d{2}:\d{2}:\d{2}', time_str)

async def add_role(ctx, time_to_send):
    role = discord.utils.get(ctx.guild.roles, name=time_to_send)
    user = ctx.message.author
    await user.add_roles(role)

@client.command()
async def role(ctx, *, time_to_send):
    if is_time(time_to_send):
        # print(ctx.author)
        if not check_roles_exist(time_to_send):
            print("role does not exist: " + time_to_send)
            await ctx.guild.create_role(name = time_to_send)
            await add_role(ctx, time_to_send)
            
        # if does exist
        elif check_roles_exist(time_to_send):
            print("role does exist: " + time_to_send)
            await add_role(ctx, time_to_send)


@client.command()
async def deleterole(ctx, *, time_to_delete):
    # print(ctx.author)
    if is_time(time_to_delete) and check_user_has_role(ctx, time_to_delete):
        role = discord.utils.get(ctx.guild.roles, name=time_to_delete)
        user = ctx.message.author
        await user.remove_roles(role)

def check_user_has_role(ctx, role_name):
    for role in ctx.message.author.roles:
        if role.name == role_name:
            return True
    return False


def check_roles_exist(role_name):
    guild = client.get_guild(GUILD_ID)
    for role in guild.roles:
        if role.name == role_name:
            return True
    return False

############################ MOD COMMANDS ############################
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

############################ RUN CLIENT ############################

client.run(TOKEN)
