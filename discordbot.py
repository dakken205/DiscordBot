# -*- coding: utf-8 -*-

import datetime
import os
import random

import discord
from discord.ext import tasks

DISCORD_BOT_ACCESS_TOKEN = os.environ["DISCORD_BOT_ACCESS_TOKEN"]  # 消すな

TEIREIKAI_CHANNEL_ID = 1056866893232885760  # 定例会チャンネルID
TEST_CHANNEL_ID = 1056870243739381810  # いーだチャンネルID

SMILE_ICON = "\N{Smiling Face with Open Mouth and Smiling Eyes}"
CIRCLE_ICON = "\N{Heavy Large Circle}"
CROSS_ICON = "\N{CROSS MARK}"

intents = discord.Intents.all()
client = discord.Client(intents=intents)

da_mention = "<@&1060233582351757454>"



@client.event
async def on_ready():
    loop.start()  # Botが準備完了した場合
    print("ログインしました")
    print("----------")
    await client.change_presence(activity=discord.Game(name="定例会", type=3))


# 前使ってたやつの残骸
MORNING_GREETINGS = [
    "今朝はよく眠れましたか？",
    "朝はコーヒーでも飲みましょう！",
    "今日も一日頑張りましょう！",
    "晴れていたら太陽の光を浴びましょう！",
    "楽しい一日の始まりです！",
    "背伸びをしてリラックスしましょう！",
]

AFTERNOON_GREETINGS = [
    "調子はいかがですか？",
    "背伸びをしてリラックスしてみましょう！",
    "今日もあと半分！頑張りましょう！",
    "晴れていたら太陽の光を浴びましょう！",
    "眠気に負けないで！頑張りましょう！",
    "今日はいいことがあるかもしれません！",
]

EVENING_GREETINGS = [
    "今日も一日お疲れ様です",
    "夜はリラックスしましょう！",
    "今日はいいことありましたか？",
    "(-_-)zzz",
    "私の家から見える夜景はとてもきれいです♪",
    "息抜きをしましょう！",
]


@client.event
async def reply(message: discord.Message):
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)  # 日本との時差
    hr = int(dt.hour)
    rd01 = random.choice(MORNING_GREETINGS)
    rd02 = random.choice(AFTERNOON_GREETINGS)
    rd03 = random.choice(EVENING_GREETINGS)

    if hr >= 17 or hr < 5:
        await message.channel.send(f"こんばんは、{message.author.mention}さん！{rd03}")
    if hr >= 11 and hr < 17:
        await message.channel.send(f"こんにちは、{message.author.mention}さん！{rd02}")
    if hr >= 5 and hr < 11:
        await message.channel.send(
            f"おはようございます、{message.author.mention}さん！{rd01}")


@client.event
async def on_message(message: discord.Message):
    mentioned_users = [user and user.id for user in message.mentions]
    if (client.user and client.user.id) in mentioned_users:
        await reply(message)
    elif message.author.bot:
        return
    if message.content == "DA研":
        await message.channel.send("DA研ボットだよ！")
        await message.channel.send("😆")

#　0706追加
@client.event
async def on_message(message):
    if message.author.bot:
        pass
    elif message.content.startswith('test'):
        send_message = f'{da_mention}てすとです'
        await message.channel.send(send_message)
# 0706追加分終


@tasks.loop(minutes=1)
async def loop():
    await client.wait_until_ready()

    w = datetime.date.today()
    week = int(w.isoweekday())
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)  # 日本との時差
    hr = int(dt.hour)
    min = int(dt.minute)

    await client.wait_until_ready()

    if week == 4 and hr == 15 and min == 00:
        channel = client.get_channel(TEIREIKAI_CHANNEL_ID)
        if isinstance(channel, discord.TextChannel):
            await channel.send("@DA研 本日16:30から定例会です！みんなラーニングコモンズに集合！")


@client.event
async def on_member_join(member: discord.Member):  # 新規ユーザー参加時

    channel = client.get_channel(TEST_CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        await channel.send(f"はじめまして！サーバーにようこそ！{SMILE_ICON}")


client.run(DISCORD_BOT_ACCESS_TOKEN)
