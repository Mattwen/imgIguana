import discord
import asyncio
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from random import randint

from discord.ext.commands import Bot

iguana = Bot(command_prefix="!")


with open('bot.token', 'r') as f:
	token = f.readline()
f.close()

@iguana.event
async def on_read():
    print("Client logged in")
@iguana.event
async def on_message(message):
	if message.content.startswith('!img'):
		########### Python 3.2 #############
		
		msg = message.content
		# Remove the !img prefix
		msg = message.content.split(' ', 1)[1]
		headers = {
			# Request headers
			'Content-Type': 'multipart/form-data',
			'Ocp-Apim-Subscription-Key': 'XXXXX',
		}

		params = urllib.parse.urlencode({
			# Request parameters
			'q': msg,
		})

		try:
			
			conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
			conn.request("POST", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
			
			# parse the json data
			response = conn.getresponse()
			data = response.read()
			parsed = json.loads(data)
			
			# Randomly generate 0-15 for random image picks
			randVal = randint(0, 15)

			# print out the name and link the thumbnail url
			result_list = parsed['value'][randVal]['thumbnailUrl']
			result_name = parsed['value'][randVal]['name']
			
			# Send info to the channel
			await iguana.send_message(message.channel, "Found: " + "`" + result_name + "`")
			await iguana.send_message(message.channel, result_list)
			conn.close()
		
		# Error handling
		except Exception as e:
			print("[Errno {0}] {1}".format(e.errno, e.strerror))

		####################################

iguana.run('XXXX')
