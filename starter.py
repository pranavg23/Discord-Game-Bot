import discord
import json
from random import random, choice

data={
    'Flight1':{
        'Customer Satisfaction':0,
        'Overall Rating':0,
        'Value For Money':0
    }
}


client= discord.Client()

@client.event
async def on_ready():
    print("Ready")

def get_possible_cards():
    rand_val=random()
    chosen_type=''
    if rand_val>0.8:
        chosen_type='Gold'
    elif rand_val>0.5:
        chosen_type='Silver'
    else:
        chosen_type='Bronze'

    possible_cards=[]

    with open('Discord-Game-Bot/cards.json') as card_data:
        cards=json.load(card_data)
        for i in cards:
            if cards[i]['Rarity']==chosen_type:
                possible_cards.append(i)
    return possible_cards

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

    if message.content.startswith('.start'):
        with open('Discord-Game-Bot/user_data.json') as json_file:
            data = json.load(json_file)
            if str(message.author.id) in data.keys():
                print('already exists')
                await message.channel.send('You already have an account!')

            else:
                chosen_cards=[choice(get_possible_cards()) for i in range(2)]
                post_data={
                    message.author.id:{
                        'deckSize':0,
                        'Cards':{}
                    }
                }
                for i in range(len(chosen_cards)):
                    post_data[message.author.id]['deckSize']+=1
                    post_data[message.author.id]['Cards'][str(i)]=chosen_cards[i]
                data.update(post_data)
                with open('Discord-Game-Bot/user_data.json', 'w') as outfile:
                    json.dump(data, outfile)
                    await message.channel.send('User has now been initialized')
                    with open('Discord-Game-Bot/cards.json') as card_data:
                        cards=json.load(card_data)
                        for i in range(post_data[message.author.id]['deckSize']):
                            card=cards[post_data[message.author.id]['Cards'][str(i)]]['Airline Name']
                            await message.channel.send('You have been given: {0}!'.format(card))


token=open(r"Discord-Game-Bot/token.txt", 'r').read()
client.run(token)

{
    'user': {
        'deckSize':0,
        'cards':{
            '1':'001'
        }
    }
}