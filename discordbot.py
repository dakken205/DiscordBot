# -*- coding: utf-8 -*-

import os
import discord

DISCORD_BOT_ACCESS_TOKEN = os.environ['DISCORD_BOT_ACCESS_TOKEN']


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == 'hello':
            await message.channel.send('world^^')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(DISCORD_BOT_ACCESS_TOKEN)
