import discord
from discord.ext import commands
import asyncio
import logging
import random
import netease_dl
import hitokoto
from configparser import ConfigParser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
config = ConfigParser()
config.read('config.ini', encoding="UTF-8")
Queue = netease_dl.Queue()
# lyric = ''


#windows
# if not discord.opus.is_loaded():
#     discord.opus.load_opus('opus')

# #linux
# if not discord.opus.is_loaded():
#     discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')


class MusicBox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    #加入语音
    async def join(self, ctx: commands.Context):
        """Joins a voice channel"""
        if ctx.message.author.voice is None:
            return await ctx.send('你必须连接一个语音频道。')
        # ctx.voice_client 返回VoiceProtocol 如果不为None,说明连上了某个语言频道
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is None:
            return await channel.connect()
        if ctx.voice_client is not None:#机器人已经在别的语音频道 切换到当前频道
            return await ctx.voice_client.move_to(channel)

    @commands.command()
    # 退出语音
    async def quit(self, ctx):
        if Queue.is_empty() is False:
            Queue.clear()
        await ctx.voice_client.disconnect()
        netease_dl.clean_cache()

    @commands.command()
    #根据官方文档，使用键值对变量参数可以用户输入什么我们得到什么
    async def play(self, ctx, *, music_kwords):
        if ctx.voice_client is None:
           return await ctx.send("先使用.join")
        # print(music_kwords)
        ids = netease_dl.search(music_kwords)
        if ids == None:
            embed = discord.Embed(title="Not Found", description="找不到这首歌", color=0xeee657)
            return await ctx.send(embed=embed)
        music_info = netease_dl.searchResult(ids)
        if music_info == None:
            embed = discord.Embed(title="播放失败", description="没有VIP或者该歌曲无版权", color=0xeee657)
            return await ctx.send(embed=embed)
        #正在播放 又有新的歌曲就添加到队列
        if ctx.voice_client.is_playing():
            Queue.enqueue(music_info)
            print("0：", Queue.music_list)
            return
        #没有播放 直接添加到队列
        Queue.enqueue(music_info)
        print("1：",Queue.music_list)

        while True:
            # 等待播放结束
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
            print("3：", Queue.music_list)
            if Queue.is_empty() is False:
                music_detail = Queue.dequeue()
                url = music_detail["url"]
                musicId = music_detail["musicId"]
                musicPic = music_detail["musicPic"]
                musicName = music_detail["musicName"]
                musicArtists = music_detail["musicArtists"]
                # global lyric
                # lyric = music_info['lyric']
                #播放
                musicFileName = netease_dl.download_music(musicId, url)
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(musicFileName), volume=0.6)
                embed = discord.Embed(title="正在播放: " + musicArtists + " - " + musicName, color=0xDC143C) \
                    .add_field(name="原始地址", value="[点这里](%s)" % music_info["163url"], inline=False) \
                    .set_thumbnail(url=musicPic)
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send(embed=embed)

            else:
                print("2：", Queue.music_list)
                return


    @commands.command()
    async def skip(self, ctx: commands.Context):
        ctx.voice_client.stop()
        if Queue.size() == 0:
            return await ctx.send("没了")
        await ctx.send("快进到下一首")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if Queue.is_empty() is False:
            Queue.clear()
        ctx.voice_client.stop()
        await ctx.send("停止播放音乐")

    @commands.command()
    async def queue(self, ctx: commands.Context):
        message = '接下来要播放的歌曲是：\n'
        #添加的歌曲在列表中的位置和播放顺序不同
        music_list = Queue.music_list[::-1]
        print(music_list)
        # enumerate类型获得下标+内容的组合 非常关键！
        Print_music_list = enumerate(music_list)
        for i in Print_music_list:
            message = message +str(i[0] + 1)+':'+ i[1]['musicName']+'-'+ i[1]['musicArtists'] + '\n'
        await ctx.send("```"+ message +"```")

    @commands.command()
    async def remove(self, ctx: commands.Context, index):
        try:
            index = int(index)
        except ValueError as e:
            return await ctx.send('输入序号！')
        #根据下标删除 因为显示顺序和实际顺序不一样 需要处理一下
        ind = len(Queue.music_list) - index
        if ind < 0:
            return await ctx.send("序号不存在")
        del Queue.music_list[ind]
        return await ctx.send('删除所选歌曲成功。')


    # @commands.command()
    # async def lyrics(self, ctx: commands.Context):
    #     print(lyric)
    #     await ctx.send(lyric)

    @commands.command()
    async def joker(self, ctx):
        result = hitokoto.hitokoto()
        embed = discord.Embed(title=result['hitokoto'], color=0xffb6c1) \
            .set_footer(text=result['from'], icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/271/clown-face_1f921.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def cleancache(self, ctx: commands.Context):
        if str(ctx.message.author) == config.get("config", "username"):
            await ctx.send("Command sent by `%s`, cleaning cache." % ctx.message.author)
            netease_dl.clean_cache()
        else:
            await ctx.send("Command sent by `%s`, you don't have permission to clean cache." % ctx.message.author)

    @commands.command()
    async def test(self, ctx):
        await ctx.send(ctx.message.author)



    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="命令表（由于网速和服务器的问题，等待bot作出反应后在进行下一步）", description="目前可以使用命令如下：", color=0xeee657)
        embed.add_field(name=".join", value="让机器人加入语音", inline=False)
        embed.add_field(name=".quit", value="让机器人退出语音", inline=False)
        embed.add_field(name=".caiquan", value="石头剪刀布小游戏", inline=False)
        embed.add_field(name=".fudu", value="复读。输入“结束复读”停止", inline=False)
        embed.add_field(name=".play 关键字", value="播放网易云上的音乐", inline=False)
        embed.add_field(name=".skip", value="切换到下一首歌", inline=False)
        embed.add_field(name=".queue", value="查看等待播放的歌曲", inline=False)
        embed.add_field(name=".remove 序号", value="删除所选歌曲", inline=False)
        embed.add_field(name=".stop", value="停止播放", inline=False)
        embed.add_field(name=".joker", value="悲伤春秋时间", inline=False)
        await ctx.send(embed=embed)



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('.help'))
    netease_dl.clean_cache()
    print('机器人已连接:{}'.format(bot.user.name))
    print('机器人ID:{}'.format(bot.user.id))



@commands.command()
async def caiquan(ctx):
    emoji = [':fist:', ':v:', ':raised_hand:']
    n = random.randint(1, 900) % 3
    await ctx.send(ctx.message.author.name+"出了"+emoji[n])


@bot.command()
async def roll(ctx):
    n = random.randint(1, 100)
    await ctx.send(ctx.message.author.name+" roll:"+str(n))



@bot.command()
async def fudu(ctx):
    channel = ctx.channel
    def check(m):
        return  m.channel == channel
    try:
        while True:
            msg = await bot.wait_for('message', check=check, timeout=10)
            if msg.content == '结束复读':
                return
            else:
                await ctx.send(msg.content)
    except asyncio.TimeoutError as e:
        await ctx.send("看来没人了")



if __name__ == '__main__':
    bot.add_cog(MusicBox(bot))
    bot.run(config.get("config", "TOKEN"))