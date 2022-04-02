import requests
import json
import discord
import time

SINGLE_MODE = 0
LIST_MODE = 1
NAME_MODE = 2
NONAME_MODE = 3

def Get_Singles(collection, properties):
    headers = {"Accept": "application/json"}
    url = "https://api.opensea.io/api/v1/collection/{}".format(collection)
    response = requests.get(url, headers=headers)
    res = []
    for p in properties:
        res.append(json.loads(response.text)['collection'][p])

    return res

def Bot_Res(collection, properties, values, mode):
    img = ["image_url"]
    res = Get_Singles(collection, img)
    headers = {"Accept": "application/json"}
    url = "https://api.opensea.io/api/v1/collection/{}".format(collection)
    response = requests.get(url, headers=headers)
    if mode == SINGLE_MODE:
        for p in properties:
            res.append(f"**{p}** : {json.loads(response.text)['collection'][p]}")
    elif mode == LIST_MODE: 
        for value in values:
            res.append(f"**{value}** : {json.loads(response.text)['collection'][properties][value]}")

    return res

def Bot_Res_list(collection, properties, values, mode):
    img = ["image_url"]
    res = Get_Singles(collection, img)
    headers = {"Accept": "application/json"}
    url = "https://api.opensea.io/api/v1/collection/{}".format(collection)
    response = requests.get(url, headers=headers)

    res_list = json.loads(response.text)['collection'][properties]
    if(mode == NONAME_MODE):
        for item_id in range(len(res_list)):
            for value in values:
                res.append(f"**{str(item_id + 1) + '.'}** {res_list[item_id][value]}")
    elif(mode == NAME_MODE):
        for item_id in range(len(res_list)):
            for value in values:
                res.append(f"**{value}** : {res_list[item_id][value]}")
    
    return res

client = discord.Client()
@client.event
async def on_ready():
    print('Current log in as：',client.user)

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    if message.content.startswith('-c -stats'):
        tmp = message.content.split(" ", 3)
        if len(tmp) < 3:
            await message.channel.send("WHAT DO YOU WANT TO FIND?")
        else:
            collection = tmp[2]         
            values = ["num_owners", "average_price", "total_sales", "total_volume", "total_supply", "floor_price"]
            res = Bot_Res(collection, 'stats', values, LIST_MODE)
            res.insert(1, f":point_right: __**The stats of '{collection}' collection are:**__\n")
            for r in range(len(res)):
                if(r <= 1):
                    await message.channel.send(res[r])
                else:
                    await message.channel.send(":bulb: " + res[r])

    elif message.content.startswith('-c -tokens'):
        tmp = message.content.split(" ", 3)
        if len(tmp) < 3:
            await message.channel.send("WHAT DO YOU WANT TO FIND?")
        else:
            collection = tmp[2]
            values = ["name"]
            res = Bot_Res_list(collection, 'payment_tokens', values, NONAME_MODE)
            res.insert(1, f":point_right: __**You can trade '{collection}' collection with following tokens:**__\n")
            for r in range(len(res)):
                if(r <= 1):
                    await message.channel.send(res[r])
                else:
                    await message.channel.send(":moneybag: " + res[r])

    elif message.content.startswith('-c -preview'):
        tmp = message.content.split(" ", 3)
        if len(tmp) < 3:
            await message.channel.send("WHAT DO YOU WANT TO FIND?")
        else:
            collection = tmp[2]
            properties = ["name", "created_date", "large_image_url"]
            res = Get_Singles(collection, properties)
            for r in res:
                await message.channel.send(r)

    elif message.content.startswith('-c -external'):
        tmp = message.content.split(" ", 3)
        if len(tmp) < 3:
            await message.channel.send("WHAT DO YOU WANT TO FIND?")
        else:
            collection = tmp[2]
            properties = ["discord_url", "external_url"]
            res = Bot_Res(collection, properties, None, SINGLE_MODE)
            for r in res:
                await message.channel.send(r)

    elif message.content.startswith('-c -contract'):
        tmp = message.content.split(" ", 3)
        if len(tmp) < 3:
            await message.channel.send("WHAT DO YOU WANT TO FIND?")
        else:
            collection = tmp[2]
            properties = "primary_asset_contracts"
            values = ["address", "schema_name", "payout_address", "dev_seller_fee_basis_points", "opensea_seller_fee_basis_points", "seller_fee_basis_points"]
            res = Bot_Res_list(collection, properties, values, NAME_MODE)
            res.insert(1, f":point_right: __**The contract info of '{collection}' collection are:**__\n")
            for r in range(len(res)):
                if(r <= 1):
                    await message.channel.send(res[r])
                else:
                    await message.channel.send(":key: " + res[r])
    else:
        await message.channel.send("Wrong Command!")

client.run('YOUR_BOT_TOKEN') 
