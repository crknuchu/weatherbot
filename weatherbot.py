import requests
import discord
import os

client = discord.Client()

def search(city_name,message):
  base_url = "https://www.metaweather.com/api/location/search/?query="

  complete_url = base_url + city_name

  response = requests.get(complete_url)

  if response.json() == []:
    await message.channel.send("City doesnt exist or we dont have it in our database")
    return None

  for location in response.json():
    await message.channel.send(location["title"])

def print_weather_info(day,message):
  await message.channel.send("Weather for " + str(day["applicable_date"]))
  await message.channel.send("Current temp: " + str(day["min_temp"]) + "°C")
  await message.channel.send("Minimum temp: " + str(day["min_temp"]) + "°C")
  await message.channel.send("Maximum temp: "+ str(day["max_temp"]) + "°C")
  await message.channel.send("Sky: " + day["weather_state_name"])
  await message.channel.send("-------------------------")


def weather(city_name,message):
  base_url = "https://www.metaweather.com/api/location/"

  search_url = "https://www.metaweather.com/api/location/search/?query=" + city_name

  response = requests.get(search_url)

  city_id = response.json()[0]["woeid"]

  response = requests.get(base_url + str(city_id))

  days = response.json()["consolidated_weather"]
  for day in days:
    print_weather_info(day,message)


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("$search"):
    city_name = message.content.split(" ")[1]
    search(city_name,message)

  if message.content.startswith("$weather"):
    city_name = message.content.split(" ")[1]
    weather(city_name,message)
  
  my_secret = os.environ['discord_bot_token']
token = os.getenv('discord_bot_token')
client.run(token)
    
