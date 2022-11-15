import discord
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def json_to_list():
    f = open('db.json')  
    data = json.load(f)
    persons = []
    for person in data:
        persons.append(data[person])
    f.close()
    return persons 

persons = json_to_list()

def birthdays_in(date):
    date = date.split('/')
    today_birthday = []
    for person in persons:
        bday = person['bday'].split('/')
        if bday[0] == date[0] and bday[1] == date[1] :
            today_birthday.append('@'+person['name'])
    return today_birthday

def birthday_of(name):
    if name:
        for person in persons:
            if person['name'] == name :
                return f"The birthday of {name} is {person['bday']}"
        
    return 'Please Enter a valid name'

def first_birthday(date):
    if date:
        date = date.split('/')
        next = ''
        for person in persons:
            bday = person['bday'].split('/')
            if bday[1] > date[1] or (bday[1] == date[1] and bday[0] > date[0]):
                if not next:
                    response = person
                    next = response['bday'].split('/')
                elif bday[1] < next[1] or (bday[1] == next[1] and bday[0] < next[0]):
                    response = person
                    next = response['bday'].split('/')
    if response :
        return f"The first birthday  is {response['bday']}, nta3 {response['name']}"
    else :
        # this case may happen when you enter parex 12/12/... and if ther's no 
        # personse's birthday after this in the same year 
        for person in persons:
            bday = person['bday'].split('/')
            if bday[1] < date[1] or (bday[1] == date[1] and bday[0] > date[0]):
                if not next:
                    response = person
                    next = response['bday'].split('/')
                elif bday[1] > next[1] or (bday[1] == next[1] and bday[0] > next[0]):
                    response = person
                    next = response['bday'].split('/')
        


@client.event
async def on_ready():
    welcome =""""
    I could listens for the following commands:
        /TodayBirthday             :returns all the people's names who have their birthday today.
        /NextBirthday              :returns the first birthday starting from tomorrow.
        /BirthdaysIn {{date}}      :returns the names of all the people who have their birthday in the specified date.
        /WhenIsMyBirthday {{name}} :returns the birthday of a specific person.
    """
    
    await client.get_channel().send(welcome)
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('/TodayBirthday'):
        today_date = datetime.date(datetime.now()).strftime("%d/%m/%Y")
        today_bday = birthdays_in(today_date)
        if today_bday:
            response = ' , '.join([per for per in today_bday]) + '.'
        else:
            response = 'There is no persone'
        await message.channel.send(response)


    elif message.content.startswith('/NextBirthday'):
        today_date = datetime.date(datetime.now()).strftime("%d/%m/%Y")
        response = first_birthday(today_date)
        await message.channel.send(response)

    elif message.content.startswith('/BirthdaysIn'):
        date = message.content.split('/BirthdaysIn ', 1)[1]
        today_bday = birthdays_in(date)
        if today_bday:
            response = ' , '.join([per for per in today_bday]) + '.'
        else:
            response = 'There is no personse'
        await message.channel.send(response)
    
    elif message.content.startswith('/WhenIsMyBirthday'):
        name = message.content.split('/WhenIsMyBirthday ', 1)[1]
        response = birthday_of(name)

        await message.channel.send(response)

    else: 
        await message.channel.send("Please Enter a valid command!")
    
    

client.run()