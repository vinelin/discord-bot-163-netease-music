import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii


def aesEncrypt(text, secKey):
    """
    aes加密
    :param text: 要加密的文本
    :param pubKey:密钥
    :return:返回加密过后的文本（aes加密完后在进行一遍base64）
    """
    blockSize = 16
    encryptor = AES.new(secKey.encode(), AES.MODE_CBC, b'0102030405060708')

    text = pad(text.encode(), blockSize)  # 将texe的长度填充到16的倍数，不然后面的加密回报错

    ciphertext = encryptor.encrypt(text)  # 进行AES加密

    ciphertext = base64.b64encode(ciphertext)  # 把加密后的结果再进行一遍base64

    return str(ciphertext, encoding='utf-8')  # 由于上面得到的是一个bytes 所以将它转换为字符串


def rsaEncrypt(text, pubKey, modulus):
    """
    将密钥进行rsa加密
    :param text: 16位随机字符
    :param pubKey:公钥
    :param modulus:modulus
    :return:
    """
    text = text[::-1]
    rs = int(binascii.b2a_hex(text.encode()), base=16) ** int(pubKey, base=16) % int(modulus, base=16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    """
    返回一个长度为size的随机字符串 这里直接返回n个F了
    :param size: 生成字符串的长度
    :return:返回一个长度为size的随机字符串
    """
    return 'F' * size