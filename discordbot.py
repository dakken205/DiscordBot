# -*- coding: utf-8 -*-

import os
import discord
import datetime
import random
from discord.ext import tasks
import time
import threading
import asyncio

DISCORD_BOT_ACCESS_TOKEN = os.environ["DISCORD_BOT_ACCESS_TOKEN"]  # 消すな

free_talk_ID = 1056870243739381810
event_atend_ID = 1056870243739381810
test_ID = 1056870243739381810

smile = "\N{Smiling Face with Open Mouth and Smiling Eyes}"
maru = "\N{Heavy Large Circle}"
batu = "\N{CROSS MARK}"

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    loop.start()  # Botが準備完了した場合
    print("ログインしました")
    print("----------")
    await client.change_presence(activity=discord.Game(name="定例会", type=3))


# 　前使ってたやつの残骸
morninggreeting = [
    "今朝はよく眠れましたか？",
    "朝はコーヒーでも飲みましょう！",
    "今日も一日頑張りましょう！",
    "晴れていたら太陽の光を浴びましょう！",
    "楽しい一日の始まりです！",
    "背伸びをしてリラックスしましょう！",
]

afternoongreeting = [
    "調子はいかがですか？",
    "背伸びをしてリラックスしてみましょう！",
    "今日もあと半分！頑張りましょう！",
    "晴れていたら太陽の光を浴びましょう！",
    "眠気に負けないで！頑張りましょう！",
    "今日はいいことがあるかもしれません！",
]

eveninggreeting = [
    "今日も一日お疲れ様です",
    "夜はリラックスしましょう！",
    "今日はいいことありましたか？",
    "(-_-)zzz",
    "私の家から見える夜景はとてもきれいです♪",
    "息抜きをしましょう！",
]


@client.event
async def reply(message):
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)  # 日本との時差
    hr = int(dt.hour)
    rd01 = random.choice(morninggreeting)
    rd02 = random.choice(afternoongreeting)
    rd03 = random.choice(eveninggreeting)

    if hr >= 17 or hr < 5:
        reply = f"こんばんは、{message.author.mention}さん！{rd03}"
    if hr >= 11 and hr < 17:
        reply = f"こんにちは、{message.author.mention}さん！{rd02}"
    if hr >= 5 and hr < 11:
        reply = f"おはようございます、{message.author.mention}さん！{rd01}"

    await message.channel.send(reply)


@client.event
async def on_message(message):
    if client.user in message.mentions:
        await reply(message)
    elif message.author.bot:
        return
    if message.content == "DA研":
        await message.channel.send("DA研ボットだよ！")
        await message.channel.send("😆")


@tasks.loop(minutes=1)
async def loop():
    await client.wait_until_ready()

    w = datetime.date.today()
    week = int(w.isoweekday())
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)  # 日本との時差
    hr = int(dt.hour)
    min = int(dt.minute)

    await client.wait_until_ready()

    if hr == 9 and min == 00:
        channel = client.get_channel(free_talk_ID)
        await channel.send(f"1時間目が始まりました。みなさんちゃんと出席していますか？")


@client.event
async def on_member_join(member):  # 新規ユーザー参加時
    print("新規ユーザー参加")

    smile = "\N{Smiling Face with Open Mouth and Smiling Eyes}"

    channel = client.get_channel(free_talk_ID)

    await channel.send(f"はじめまして！サーバーにようこそ！{smile}")


client.run(DISCORD_BOT_ACCESS_TOKEN)