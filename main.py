import discord
import asyncio
import os
import r6sapi as api

client = discord.Client()
dataDict = {}

###----------------------------------------------------------------------------------------------
###起動確認
###----------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----------')

###----------------------------------------------------------------------------------------------    
###キーワードに対し応答する関数
###----------------------------------------------------------------------------------------------
@client.event
async def on_message(message):
    #r6s stats始まりで起動
    if message.content.startswith('r6s stats') and client.user != message.author:
        #入力されたユーザーネームを取得
        playername = message.content[10:]

        #R6Sのステータスを取得
        await setData(playername)

        #返答するメッセージ内容を取得
        sm = speakMessage(playername)

        #メッセージをDiscordで発言
        await message.channel.send(sm)

###----------------------------------------------------------------------------------------------
###メッセージ内容を生成する関数
###----------------------------------------------------------------------------------------------
def speakMessage(name):
    name = "**NAME（ユーザー名）**\n> " + name
    kd = "**KILL/DEATH（キルデス比）**\n> " + str('{:.3f}'.format(float(dataDict['kill'])/float(dataDict['death'])))
    time = "**PLAY TIME（プレイ時間）**\n> " + str('{:.3f}'.format(float(dataDict['time'])/3600)) + " h"
    level = "**LEVEL（クリアランスレベル）**\n> " + str(dataDict['level'])
    wp = "**WINNING PERCENTAGE（勝率）**\n> " + str('{:.3f}'.format(float(dataDict['win'])/float(dataDict['gamenum'])*100)) + " %"
    rank = "**RANK（ランク）**\n> " + dataDict['rank']
    hsp = "**HEAD SHOT KILL PERCENTAGE（ヘッドショットキル率）**\n> " + str('{:.3f}'.format(float(dataDict['hs'])/float(dataDict['kill'])*100)) + " %"
    survival_rate = "**SURVIVAL RATE（生存率）**\n> " + str('{:.3f}'.format((float(dataDict['total_round'])-float(dataDict['death']))/float(dataDict['total_round'])*100)) + " %"
    
    return name+"\n"+level+"\n"+time+"\n"+rank+"\n"+kd+"\n"+hsp+"\n"+survival_rate+"\n"+wp


###----------------------------------------------------------------------------------------------
###r6sのステータスをセットする関数
###----------------------------------------------------------------------------------------------
@asyncio.coroutine
def setData(playername):
    auth = api.Auth(os.environ.get('UPLAY_EMAIL'),os.environ.get('UPLAY_PASS'))
    
    player = yield from auth.get_player(playername, api.Platforms.UPLAY)
    yield from player.load_general()
    yield from player.load_level()
    rank = yield from player.get_rank("apac") #class Rank
    operators = yield from player.get_all_operators() #type dict[class Operator]、keyは不明、値にoperatorクラス
    
    global dataDict
    dataDict['name'] = player.userid
    dataDict['kill'] = player.kills
    dataDict['death'] = player.deaths
    dataDict['time'] = player.time_played
    dataDict['level'] = player.level
    dataDict['win'] = player.matches_won
    dataDict['gamenum'] = player.matches_played
    dataDict['rank'] = rank.rank
    dataDict['hs'] = player.headshots

    #全ラウンド数
    total_round = 0
    for operator in operators.values():
        total_round = total_round + operator.wins + operator.losses
        
    dataDict['total_round'] = total_round

    
#実行
client.run(os.environ.get('BOT_TOKEN'))
