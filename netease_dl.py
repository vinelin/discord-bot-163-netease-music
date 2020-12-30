import os
import shutil #对os库的补充
import stat #os 状态
import requests #requests请求第三方库
from encode import aesEncrypt, createSecretKey, rsaEncrypt
import json


# def get_music_info(music_id: str):
#     searchResult = requests.get('')
url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
# url = 'http://music.163.com/weapi/search/suggest/web?csrf_token='
headers = {
    'Referer': 'http://music.163.com/'
}
#这个不知道是什么东西 跟着抄过来
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
#将json进行第一次aes加密的时候用这个作为密钥
nonce = '0CoJUm6Qyw8W8jud'
# rsa加密的公钥
pubKey = '010001'

# 获得一个16位的随机字符串，我们这里图省事给的是16个F
secKey = createSecretKey(16)

def search(s : str):
    text = {
            's': s,
            "limit": "8",
            'csrf_token': ''
        }
    # 构建json
    text = json.dumps(text)
    # 把上面构建的json数据使用nonce进行第一次aes加密
    encText = aesEncrypt(text, nonce)
    # 使用随机的十六位字符串作为密钥把上面的到的结果进行第二次加密
    encText = aesEncrypt(encText, secKey)
    # 把我们用作AES加密的密钥进行ras加密
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    # 由于我们这里使用的一直是使用十六个F作为密钥所以这个对于我们来说是不变的，所以只要加密一遍以后直接复制出来搞成一个常量就行，每次提交给服务器都一样
    data = {
        'params': str(encText),
        'encSecKey': encSecKey,
    }
    url = 'http://music.163.com/weapi/search/suggest/web?csrf_token='
    req = requests.post(url, headers=headers, data=data).json()
    try:
        ids = (req['result']['songs'][0]['id'], req['result']['songs'][1]['id'], )
    except IndexError as e:
        ids = (req['result']['songs'][0]['id'],)
    except KeyError as e:
        ids = None
    finally:
        return ids


def searchResult(ids):
    #使用官方API
    # text = {
    #     'ids': list(ids),
    #     'br': 128000,
    #     'csrf_token': ''
    # }
    # text = json.dumps(text)
    # # 把上面构建的json数据使用nonce进行第一次aes加密
    # encText = aesEncrypt(text, nonce)
    # # 使用随机的十六位字符串作为密钥把上面的到的结果进行第二次加密
    # encText = aesEncrypt(encText, secKey)
    # # 把我们用作AES加密的密钥进行ras加密
    # encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    # # 由于我们这里使用的一直是使用十六个F作为密钥所以这个对于我们来说是不变的，所以只要加密一遍以后直接复制出来搞成一个常量就行，每次提交给服务器都一样
    # data = {
    #     'params': str(encText),
    #     'encSecKey': encSecKey,
    # }
    # url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    # req = requests.post(url, headers=headers, data=data).json()  # 发送post请求
    # return req['data'][0]['url']


    #使用第三方API 通过ID获取更多信息 不用反复post请求
    real_id = 0
    url = ''
    for i in ids:
        url = requests.get('https://api.imjad.cn/cloudmusic/?type=song&id='+str(i)+'&br=128000').json()['data'][0]['url']
        if url != '':
            real_id = i
            break
    if url is '':
        return None
    searchDetail = requests.get('https://api.imjad.cn/cloudmusic/?type=detail&id=' + str(real_id) + '&br=128000').json()
    music_name = searchDetail['songs'][0]['name']
    music_pic = searchDetail['songs'][0]['al']['picUrl']
    artists = []
    for m in searchDetail['songs'][0]['ar']:
        artists.append(m['name'])
    # 字数太多discord 不支持
    # lyrics = requests.get('https://api.imjad.cn/cloudmusic/?type=lyric&id='+str(real_id)+'&br=128000').json()['lrc']['lyric']
    music_info = {
        "163url": "https://music.163.com/#/song?id=" + str(real_id),
        "url" : url,
        "musicId" : real_id,
        "musicPic" : music_pic,
        "musicName" : music_name,
        "musicPic" : music_pic,
        "musicArtists": ','.join(artists),
        # "lyric": lyrics
    }
    return music_info

#下载音乐文件到tmp文件夹
def download_music(music_id:int,music_url:str):
    fileName = 'tmp/'+ str(music_id)+'.mp3'
    # 如果 tmp 文件夹未被创建，则创建 tmp 文件夹
    if os.path.exists("tmp/") is not True:
        os.mkdir("tmp/")
    with open(fileName, 'wb') as music:
        music.write(requests.get(music_url).content)
    return str(fileName)


#清理缓存
def clean_cache():
    if os.path.exists('tmp'):
        for fileList in os.walk('tmp'):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
            shutil.rmtree('tmp')
        print("缓存清理完毕")

#队列类
class Queue:
    def __init__(self):
        self.music_list = []

    def is_empty(self):
        return self.music_list == []

    def enqueue(self, music_info):
        self.music_list.insert(0, music_info)

    def dequeue(self):
        return self.music_list.pop()

    def size(self):
        return len(self.music_list)

    def clear(self):
        self.music_list.clear()
