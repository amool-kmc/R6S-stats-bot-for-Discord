import discord
import asyncio
import os
import r6sapi as api

client = discord.Client()
dataDict = {}

#起動確認
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----------')

#発言用
@client.event
async def on_message(message):
    #\r6s stats始まりで起動
    if message.content.startswith('r6s stats') and client.user != message.author:
        playername = message.content[10:]

        await setData(playername)

        sm = speakMessage(playername)
        await message.channel.send(sm)


        
#message内容
def speakMessage(name):
    name = "**NAME**\n> " + name
    kd = "**KILL/DEATH**\n> " + str('{:.3f}'.format(float(dataDict['kill'])/float(dataDict['death'])))
    time = "**PLAY TIME**\n> " + str('{:.3f}'.format(float(dataDict['time'])/3600)) + " h "
    level = "**LEVEL**\n> " + str(dataDict['level'])
    wp = "**WINNING PERCENTAGE**\n> " + str('{:.3f}'.format(float(dataDict['win'])/float(dataDict['gamenum'])))
    rank = "**RANK**\n> " + dataDict['rank']
    hsp = "**HEAD SHOT KILL PERCENTAGE**\n> " + str('{:.3f}'.format(float(dataDict['hs'])/float(dataDict['kill'])))
    
    return name+"\n"+level+"\n"+rank+"\n"+kd+"\n"+hsp+"\n"+wp+"\n"+time



#r6sstatsを取る
@asyncio.coroutine
def setData(playername):
    auth = api.Auth(os.environ.get('UPLAY_EMAIL'),os.environ.get('UPLAY_PASS'))
    
    player = yield from auth.get_player(playername, api.Platforms.UPLAY)
    yield from player.load_general()
    yield from player.load_level()
    rank = yield from player.get_rank("apac") #class Rank
    operators = yield from player.get_all_operators() #type dict[class Operator]
    
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
