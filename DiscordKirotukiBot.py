# coding:UTF-8
import discord
from discord.ext import tasks
from datetime import datetime
import requests
import json


TOKEN = ""  # Discordのトークン
CHANNEL_ID =  # 消去するチャンネルID

client = discord.Client()

##ここで指定したIDにしかmisskeyに投稿できないようになっています.
discordUserID = #DiscordのユーザーID

url = "https://misskey.io/api/notes/create" #misskeyインスタンスここではio

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

#指定した時間にCHANNNEL_IDで登録したCHのログが消されます。
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '12:00':
        channel = client.get_channel(CHANNEL_ID)
        await channel.purge(limit=None)
        await channel.send('全消去しました')
        await channel.send('毎日12:00に全消去されます')


@client.event
async def on_message(message):
    if message.content == '/cleanup':
        if message.author.id == discordUserID:
            await message.channel.purge()
            await message.channel.send('全消去しました')
        else:
            await message.channel.send('不可能')

    if message.content.startswith("/mis") and message.author.id == discordUserID:
        postText = message.content[4:]
        print(postText)

        json_data = {
            "i": "qdA8HXmPjj0hv0T8Sa6njQb5LRX3nfzj",
            "text": postText
        }

        requests.post(
            url,
            json.dumps(json_data),
            headers={'Content-Type': 'application/json'})
        await message.channel.send(postText + "を投稿しました")


# ループ処理実行
loop.start()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
