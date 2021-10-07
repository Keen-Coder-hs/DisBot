import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()


# List of Sad words and encouragements
sad_words = ["depressed","unhappy","miserable","angry","depressing"]

starter_encouragements = [
  "Hang in there", "Learn to Forgive Yourself","You matter a lot", "You are great","Take a deep breathe and clear your conscience" 
]

if "responding" not in db.keys():
  db["responding"] = True

  
#To get quote from website's API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']

  return(quote)

#For the list of encouraging words
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db[encouragements] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Command for the bot to respond to a message
  
  msg = message.content

  if msg.startswith('!!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])


    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

      
   # To add and delete new elements in the encouragement list   
  if msg.startswith("!!new"):
    encouraging_message = msg.split("!!new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("!!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!!del ",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("!!list"):  
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("!!res"):
    value = msg.split("!!res ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on") 
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")

keep_alive()
client.run(os.getenv('TOKEN'))
