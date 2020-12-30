import requests

def hitokoto():
    result = requests.get('http://v1.hitokoto.cn?encode=json&charset=utf-8?').json()
    return result

