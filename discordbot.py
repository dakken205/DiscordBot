# -*- coding: utf-8 -*-

import datetime
import os
import random

import discord
from discord.ext import tasks

DISCORD_BOT_ACCESS_TOKEN = os.environ["DISCORD_BOT_ACCESS_TOKEN"]  # 消すな

TEIREIKAI_CHANNEL_ID = 1056866893232885760  # 定例会チャンネルID
TEST_CHANNEL_ID = 1056870243739381810  # いーだチャンネルID
KEIEIJIN_CHANNEL_ID = 1092709824661295175  # 経営陣チャンネルID
KAISEKI_CHANNEL_ID = 1146443598783594536

SMILE_ICON = "\N{Smiling Face with Open Mouth and Smiling Eyes}"
CIRCLE_ICON = "\N{Heavy Large Circle}"
CROSS_ICON = "\N{CROSS MARK}"


intents = discord.Intents.all()
client = discord.Client(intents=intents)

da_mention = "<@&1060233582351757454>"
keiei_mention = "<@&1056864581517070449>"


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
        await message.channel.send(f"おはようございます、{message.author.mention}さん！{rd01}")


@client.event
async def on_message(message: discord.Message):
    mentioned_users = [user and user.id for user in message.mentions]

    # ボット自身がメンションされたかどうかを確認
    if (client.user and client.user.id) in mentioned_users:
        await reply(message)

    # ボット自身のメッセージには反応しない
    if message.author.bot:
        return

    # DA研というメッセージに反応
    if message.content == "DA研":
        da_ans = await message.channel.send("DA研ボットだよ！")
        await message.channel.send("😆")
        await da_ans.add_reaction(SMILE_ICON)

    # testから始まるメッセージに反応
    if message.content.startswith("/test_teirei"):
        embed = discord.Embed(
            title="**定例会が開催されます！**",
            description="**16:30～**定例会があります！\n みんな集合！",
            color=discord.Colour.from_rgb(0, 132, 234),
        )

        embed.set_thumbnail(
            url="https://c.tenor.com/KChHVc7BktYAAAAd/discord-loading.gif"
        )
        emb = await message.channel.send(embed=embed)
        await emb.add_reaction(CIRCLE_ICON)
        await emb.add_reaction(CROSS_ICON)

    if message.content.startswith("/test_keiei"):
        embed = discord.Embed(
            title="**(試)定例会の資料記入について**",
            description=f"{keiei_mention} 16:30～定例会\n資料記入をお願いします\n",
            color=discord.Colour.from_rgb(0, 132, 234),
        )
        embed.set_image(url="https://c.tenor.com/KChHVc7BktYAAAAd/discord-loading.gif")
        embed.add_field(
            name="定例会資料作成フォーム↓", value="https://pptx-maker.uoh-dakken.com/#/"
        )
        await message.channel.send(embed=embed)

    if message.content == "兵庫県":
        send_message = "Japan Plane Rectangular CS V"
        await message.channel.send(send_message)


@tasks.loop(minutes=1)
async def loop():
    await client.wait_until_ready()
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    week = int(dt.isoweekday())
    # 日本との時差
    hr = int(dt.hour)
    min = int(dt.minute)
    # 現在の日付と時刻を取得
    month = dt.month
    day = dt.day
    week_list = ["月", "火", "水", "木", "金", "土", "日"]  # 月曜日が1

    await client.wait_until_ready()

    if week == 4 and hr == 15 and min == 00:  # 定例会おしらせembed
        channel = client.get_channel(TEIREIKAI_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            return
        description = (
            f"{da_mention} **{month}**月**{day}**日(**{week_list[week-1]}**)\n"
            "**16:30～**定例会があります！\n"
            "みんな集合！"
        )
        embed = discord.Embed(
            title="**定例会が開催されます！**",
            description=description,
            color=discord.Colour.from_rgb(0, 132, 234),
        )
        embed.set_thumbnail(
            url="https://c.tenor.com/KChHVc7BktYAAAAd/discord-loading.gif"
        )
        await channel.send(embed=embed)

    if week == 4 and hr == 16 and min == 30:  # 定例会開始embed
        channel = client.get_channel(TEIREIKAI_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            return
        description = f"{da_mention} **{month}**月**{day}**日(**{week_list[week-1]}**)定例会"
        embed = discord.Embed(
            title="**定例会を開始します！**",
            description=description,
            color=discord.Colour.from_rgb(0, 132, 234),
        )
        embed.set_thumbnail(
            url="https://c.tenor.com/KChHVc7BktYAAAAd/discord-loading.gif"
        )
        await channel.send(embed=embed)

    if week == 4 and hr == 9 and min == 00:  # 定例会資料記入_経営陣embed
        channel = client.get_channel(KEIEIJIN_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            return

        embed = discord.Embed(
            title="**定例会の資料記入について**",
            description=f"{keiei_mention} 本日16:30～定例会です。\n各自、資料記入をお願いします\n",
            color=discord.Colour.from_rgb(0, 132, 234),
        )
        embed.add_field(
            name="定例会資料作成フォーム↓", value="https://pptx-maker.uoh-dakken.com/#/"
        )
        await channel.send(embed=embed)

    if week == 4 and hr == 20 and min == 00:  # 解析コンペ出欠embed
        kaiseki_dt = dt + datetime.timedelta(days=7)
        kaiseki_week = int(kaiseki_dt.isoweekday())
        channel = client.get_channel(KAISEKI_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            return
        embed = discord.Embed(
            title=f"**{kaiseki_dt.month}**/**{kaiseki_dt.day}**({week_list[kaiseki_week-1]})解析コンペ出欠調査",
            description=f"{da_mention} 次回の会議に \n 出席 ⇒ {CIRCLE_ICON}   欠席 ⇒ {CROSS_ICON}",
            color=discord.Colour.from_rgb(97, 216, 70),
        )
        embed.set_thumbnail(
            url="https://cdn.dribbble.com/users/1751759/screenshots/5460650/wifi_happiness.gif"
        )
        emb = await channel.send(embed=embed)
        await emb.add_reaction(CIRCLE_ICON)
        await emb.add_reaction(CROSS_ICON)


@client.event
async def on_member_join(member: discord.Member):  # 新規ユーザー参加時
    channel = client.get_channel(TEST_CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        embed = discord.Embed(
            title="**サーバーの入室を検知しました**",
            description="welcome to Dakken discord channel!",
            color=discord.Colour.from_rgb(0, 132, 234),
        )
        await channel.send(embed=embed)


client.run(DISCORD_BOT_ACCESS_TOKEN)
