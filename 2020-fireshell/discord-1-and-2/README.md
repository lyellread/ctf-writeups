# Against the Perfect discord Inquisitor 1, 2

### Prompt 1

You're on a journey and come to the Tavern of a Kingdom Enemy, you need to get information of a secret organization for the next quest. Be careful about the Inquisitor! He can ban you from this world.

TL;DR find the flag

[Kingdom Chall](https://discord.gg/fHHyU6g)

HINT: Title/Chall name

### Prompt 2

There is a mage in the tavern that reveals secrets from the place. He is friendly, so he can help you! Be careful about the Inquisitor! He can ban you from this world.

TL;DR use the bot to get the flag

[Kingdom Chall](https://discord.gg/fHHyU6g)

### Solution 1

Starting out, we clicked the link to [Kingdom Chall](https://discord.gg/fHHyU6g), and joined the discord. There, we identified a long stream of other people joining, as well as a bot account named `Gandalf`. `Gandalf`'s status reads:

> You're welcome~ Free reveals with command: $reveal_secret (channel.id) (message.id)

Obviously, we need to test this:

```
lyellread
$reveal_secret 688190172793536545 691089964401819759
Gandalf [BOT]
@everyone say hello to @Gandalf !
```

Great! Looks like `Gandalf` will be our oracle for any messages that we have ID's for but cannot read ourselves. What's next?

Someone had a plugin enabled that saw there was a hidden channel on the Discord, with ID `688190289814618213`, with name `hidden-round-table`. We would have found this in our API search below, but this helped refine where we were headed wiht `Gandalf` and the API.

Now onto that hint: The challenge name is "Against the Perfect discord Inquisitor" - that makes acronym "API"... I know where this is going. We need to make some API request to get some information.

After quite a bit of looking (Discord, your docs suck big time!!), we came up with [this script] which will make a `GET` request to the API. We needed a token, too, and thankfully, GitHub user Tyrrrz provides [this guide](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs) to getting tokens and channel (and message and guild) ID's. Now we can work with that. We tried:
- `/api/v6/channel/688190172793536545/messages`: returns all the messages - nothing new, as we can read all messages in that channel.
- `/api/v6/channel/688190289814618213/messages`: returns not authorized to view messages in hidden channel - no suprise there.
- `/api/v6/guilds/688190172793536536`: returns much of what we already knew about this guild
- `/api/v6/guilds/688190172793536536/channels`: 
```json
[{"id": "688190172793536539", "type": 4, "name": "Kingdom", "position": 0, "parent_id": null, "guild_id": "688190172793536536", "permission_overwrites": [], "nsfw": false}, {"id": "688190172793536545", "last_message_id": "691368465201758319", "type": 0, "name": "tavern", "position": 0, "parent_id": "688190172793536539", "topic": "A place of business where people gather to drink alcoholic beverages and be served food, and in most cases, where travelers receive lodging.", "guild_id": "688190172793536536", "permission_overwrites": [{"id": "688190172793536536", "type": "role", "allow": 0, "deny": 2048}], "nsfw": false, "rate_limit_per_user": 0}, 

{"id": "688190289814618213", "last_message_id": "688214063595258088", "type": 0, "name": "hidden-round-table", "position": 1, "parent_id": "688190172793536539", "topic": "F#{The_Table_of_King_Arthur}", "guild_id": "688190172793536536", "permission_overwrites": [{"id": "688190172793536536", "type": "role", "allow": 0, "deny": 3072}, {"id": "688190424124227590", "type": "role", "allow": 3072, "deny": 0}], "nsfw": false, "rate_limit_per_user": 0}]
```

That's the first flag! `F#{The_Table_of_King_Arthur}` - the description of `#hidden_round_table`! Now onto the next one...

### Solution 2

We have not even used `Gandalf` yet, so we will need to. The output above tells us something interesting (and exactly what we need to use `Gandalf`) - the last message id in `#hidden_round_table`: `688214063595258088`. Now we can ask our "Mage" `Gandalf` about this:

```
lyellread
$reveal_secret 688190289814618213 688214063595258088
Gandalf [BOT] 
RiN7UzRiM1JfMTVfVGgzX0sxbmdfQXJ0aHVyfQ==
```

That looks like base64... One sec, [we can fix that](https://www.base64decode.org/), and we get `F#{S4b3R_15_Th3_K1ng_Arthur}`!

Thank you Fireshell Team and @K4L1!!

~Lyell Read, Phillip Mestas, Robert Detjens
