#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @author: fangnan

import time
# TODO 这里使用pip install pycryptodome
# TODO 才能支持python3.6及以上
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class prpcrypt():
    def __init__(self, key, iv):
        self.key = bytes(key, 'utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'abcd134556abcedf')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        count = len(text)
        print('原长度', count)
        text = self.pkcs7padding(text)
        print('补充后长度', len(text))
        self.ciphertext = cryptor.encrypt(bytes(text, 'utf-8'))
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'abcd134556abcedf')
        try:
            plain_text = str(cryptor.decrypt(a2b_hex(text)), 'utf-8')
        except:
            plain_text = str(cryptor.decrypt(text), 'utf-8')

        return bytes(self.pkcs7unpadding(plain_text), 'utf-8')

    def pkcs7padding(self, data):
        # AES.block_size 16位
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = chr(padding) * padding
        return data + padding_text

    def pkcs7unpadding(self, data):
        lengt = len(data)
        unpadding = ord(data[lengt - 1])
        return data[0:lengt - unpadding]


def decodeAESin67(e, key):
    """
    调研AES加密，怎么也得不到相同结果，总是尾巴有所不同。晚上时候研究了一下CBC算法，发现是每一块与前一块按位异或得，分析是结尾补充有误。因此查询了代码，发现他的补充算法不是补空格，是PKCS7Padding填充方法，修正后得以实现。
    测试:
    decodeAESin67(e,key)
    decodeAESin67(b'EDF94C7F0E33DDD4BC7C7A824C0322F1C57901F10C909DF8C2BCBA8871DB34D8F08009B6207512D79609AB945E2B04AFC7E6F9DAF16E28CFCEF42F54783C89380697609A8BEB01F8BBBC21A6588537C695A826B0E53D7A14C2462E2EC77ADC15F0095D253E7A846147DFF8EF644B7D1D','108cc39a8de542188f13624ae3194dde')
    :param inputByte:
    :return:
    """
    pc = prpcrypt(key, 'abcd134556abcedf')  # 初始化密钥
    d = pc.decrypt(e)  # 解密
    # print("解密1", d)
    # print('理论1', b'92E4AC813EF1AF95225313005190D6FD357FEDB77E9576DEBAB42839448132DE0BC735D1C24903935B3E496C9559CF40')
    # time.sleep(0.1)
    d2 = pc.decrypt(d)  # 解密
    # print("解密2", d2)
    # print('理论2', b'532bd8ed-4ba8-48b7-ad70-0063f64ede05')
    return str(d2, encoding='utf-8')


if __name__ == '__main__':
    decodeAESin67(
        b'EDF94C7F0E33DDD4BC7C7A824C0322F1C57901F10C909DF8C2BCBA8871DB34D8F08009B6207512D79609AB945E2B04AFC7E6F9DAF16E28CFCEF42F54783C89380697609A8BEB01F8BBBC21A6588537C695A826B0E53D7A14C2462E2EC77ADC15F0095D253E7A846147DFF8EF644B7D1D',
        '108cc39a8de542188f13624ae3194dde')

    # src = b'XxVx8ULXbpvPRjh7edFbt9BYrHPnwhFBrsKKkqUXSAadExpLVOtY17/c0T89xK+PH1lCQsB6D+g9q8euKxzoayUviQI1kJH6cAQLNLC4QZO0eLOv0Qr6j5G17qRV7rHim/jJv6AMuDY3gGdv7CV7yA=='
    # src2 = decodeAES(src)
    # print(src2)
    # src3 = decodeAES(src)
    # print(src3)
# 43ED58D244B50B4444AE3C02E3341B3DEF1B7269A1CDA5945048216CEDFB649C3B40BFA70B2435E822DDC2BA819E70CA
# 43ED58D244B50B4444AE3C02E3341B3DEF1B7269A1CDA5945048216CEDFB649C3B40BFA70B2435E822DDC2BA819E70CA


# "Q+1Y0kS1C0RErjwC4zQbPe8bcmmhzaWUUEghbO37ZJw7QL+nCyQ16CLdwrqBnnDK"
