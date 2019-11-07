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
    name = "NAME : " + name
    kd = "K/D : " + str('{:.3f}'.format(float(dataDict['kill'])/float(dataDict['death'])))
    time = "PLAY TIME : " + str('{:.3f}'.format(float(dataDict['time'])/3600)) + " h "
    level = "LEVEL : " + str(dataDict['level'])
    wp = "WP : " + str('{:.3f}'.format(float(dataDict['win'])/float(dataDict['gamenum'])))
    rank = "RANK : " + dataDict['rank']
    hsp = "HS/K : " + str('{:.3f}'.format(float(dataDict['hs'])/float(dataDict['kill'])))
    
    return name+"\n"+level+"    "+rank+"\n"+kd+"    "+hsp+"    "+wp+"\n"+time



#r6sstatsを取る
@asyncio.coroutine
def setData(playername):
    auth = api.Auth(tokens.mail,tokens.password)
    
    player = yield from auth.get_player(playername, api.Platforms.UPLAY)
    yield from player.load_general()
    yield from player.load_level()
    rank = yield from player.get_rank("apac")
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
            
#実行
client.run(os.environ.get('BOT_TOKEN'))
