# coding:UTF-8
import discord
from discord.ext import tasks
from datetime import datetime
from mastodon import Mastodon
import requests
import json


TOKEN = ""  # トークン
CHANNEL_ID =   # チャンネルID
# 接続に必要なオブジェクトを生成
client = discord.Client()

url = "https://misskey.m544.net/api/notes/create"

# 起動動作処理
@client.event
async def on_ready():
    # 起動通知の表示
    print('ログインしました')


# 特定のチャンネルを定時消去する
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '12:00':  # 任意の時刻
        channel = client.get_channel(CHANNEL_ID)
        await channel.purge(limit=None)
        await channel.send('全消去しました')
        await channel.send('毎日12:00に全消去されます')


@client.event
async def on_message(message):
    # 任意のチャンネルの履歴消去
    if message.content == '/cleanup':
        if message.author.id ==:  # ユーザーID
            await message.channel.purge()
            await message.channel.send('全消去しました')
        else:
            await message.channel.send('不可能')

    # pawooの投稿処理
    if message.content.startswith("/pawoo") and message.author.id ==:# ユーザーID
        postText = message.content[6:]
        print(postText)

        mastodon = Mastodon(
            client_id="app_key.txt",
            access_token="user_key.txt",
        )
        mastodon.toot(postText)

        await message.channel.send(postText + 'を投稿しました')

    # メイスキーの投稿処理
    if message.content.startswith("/mei") and message.author.id == :  # ユーザーID
        postText = message.content[4:]
        print(postText)

        json_data = {
            "i": "",  # メイスキーのToken
            "text": postText
        }

        requests.post(
            url,
            json.dumps(json_data),
            headers={'Content-Type': 'application/json'})
        await message.channel.send(postText + "を投稿しました")

    # pawooとメイスキーの同時投稿処理
    if message.content.startswith("/pawmei") and message.author.id ==:  # ユーザーID
        postText = message.content[7:]
        print(postText)

        json_data = {
            "i": "",  # メイスキーのToken
            "text": postText
        }

        requests.post(
            url,
            json.dumps(json_data),
            headers={'Content-Type': 'application/json'})

        mastodon = Mastodon(
            client_id="app_key.txt",
            access_token="user_key.txt",
        )
        mastodon.toot(postText)
        await message.channel.send(postText + 'を投稿しました')

# ループ処理実行
loop.start()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
