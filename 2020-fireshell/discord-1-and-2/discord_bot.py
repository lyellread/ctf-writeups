import requests

key = "<your key here, lol, im not gonna share my key that easily :)>"
response = requests.get("https://discordapp.com/api/v6/guilds/688190172793536536/channels",
        headers = {"authorization" : key})

print(response.content)