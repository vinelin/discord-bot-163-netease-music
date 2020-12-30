# discord-bot-163-netease-meusic
改机器人能播放网易云音乐

# 使用
### 1.首先安装 discord.py[voice]

     # Linux/macOS
     python3 -m pip install -U "discord.py[voice]"

     # Windows
     py -3 -m pip install -U discord.py[voice]

### 2.安装requests库和pycryptodome库

### 3.将自己的TOKEN和USERNAME加入config_forexample.ini，并修改文件名为config.ini

### 4.根据运行环境取消需要的注释
     #windows
     # if not discord.opus.is_loaded():
     #     discord.opus.load_opus('opus')

     # #linux
     # if not discord.opus.is_loaded():
     #     discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so.0')
     
### 5.运行
    python main.py
 
# 文件说明
main.py - bot主要代码
hitokoto.py - 一言功能代码
encode.py - 致谢文章中的为网易云请求加密和解密使用的代码
netease_dl.py - 音乐搜索，下载，删除代码
    
# 功能介绍
命令表（由于网速和服务器的问题，等待bot作出反应后在进行下一步） 
目前可以使用命令如下： 
.join 
让机器人加入语音
.quit  
让机器人退出语音  
.caiquan  
石头剪刀布小游戏  
.fudu  
复读。输入“结束复读”停止   **（有BUG）**
.play 关键字  
播放网易云上的音乐  
.skip  
切换到下一首歌  
.queue  
查看等待播放的歌曲  
.remove 序号  
删除所选歌曲  
.stop  
停止播放  
.joker  
发送一言  

# 注意事项
由于本人对异步编程不够熟练，致使该BOT有一些使用上的小BUG。对并发支持度几乎没有，适合单一频道使用。

# 致谢
### [discord.py](https://github.com/Rapptz/discord.py)
### [网易云API分析](https://www.dazhuanlan.com/2020/03/20/5e73cb9a327c6/?__cf_chl_jschl_tk__=471c5b62335149e81c0844e224e547b06998911b-1609310672-0-AWogFhy6hx7De_C7ocM30eF2xU2QZGY8Re8IgijBcNL_jNd5nrlZfpSXaLuYd1cuW0J_h2nud17vpCUpVI2ZOoCKlNZUL5aP6lenA-Xp3bqUa2ecZ-l0-WNuA0liP2Pu83OeE5yf_68fx9jo2xlxUq_MNfaprR2qY3nmXsLO88tI6JXSUqP8SqsV-KSWmeqB7afAGRHk7-gcZFRWx2QEF9hwPDcfET6hlKGjcAmADcgXzvgjWzuFzFRnUZAO3fbTzyIj9goXRamQ-LXigR8Eh-Pe_HI1HcfFzys-weB0wu61HW6f6cCndCZ51EXFaZhvU1VAznspeU_QLbgoB8quZno)
### [Netease Music Bot for Discord](https://github.com/vinelin/discord-netease-music-bot)
