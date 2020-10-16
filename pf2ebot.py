# bot.py
import os, random, datetime, asyncio

import discord.ext.commands
from dotenv import load_dotenv
from discord.ext.commands import Bot

bot = Bot(command_prefix='!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

add_hero_point = "Add a hero point to your character sheet.  Remember they go away at the end of the session so don't be greedy!"
client = discord.Client()


async def hourly_hero_point():
    while True:
        await asyncio.sleep(3600)
        await client.get_channel(704486212353785878).send(add_hero_point)
        
        

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    await client.get_channel(704486212353785878).send(add_hero_point)
    await client.get_channel(704486212353785878).send('This bot will give you a hero point every 60 minutes once it is started')
    bot.loop.create_task(hourly_hero_point())
    
    

@client.event
async def on_member_join(member):
    await member.create.dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the Friday Night RPG Game!')

@client.event
async def on_message(message):
    message_str = str(message.content)
    if message.author == client.user:
        return

    if message.content == '!hero point':
        await message.channel.send(add_hero_point)

    if message_str[0] == "!" and "d" in message_str:
        new_rolls= []
        modifier = 0
        #mod_start = len(message_str)
        if "+" in message_str:
            modifier = int(message_str[message_str.index("+")+1:])
            print("+ is here and the modifier is: "+ str(modifier))
            
        break_point = int(message_str.index("d"))
        print(break_point)
        num_times = int(message_str[1:break_point])
        print(num_times)
        die_type = int(message_str[break_point + 1:message_str.index("+")])
                
        for _ in range(num_times):
            new_rolls.append(random.randint(1, die_type))
        await message.channel.send("Dice Rolls: " + str(new_rolls)+ " + "+  str(modifier) + " Total: " + str(sum(new_rolls)+modifier)) 
        
       

client.run(TOKEN)

