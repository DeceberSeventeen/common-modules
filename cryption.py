"""字符串加解密模块"""


import json
# secrets 库是 Python 3.6 引入的伪随机数模块，适合生成随机密钥
from secrets import token_bytes
from pathlib import Path


class Cryption(object):

    """
    加解密类，字符串/文件
    """

    def random_key(self, length=9):
        """
        token_bytes 函数接受一个 int 参数，用于指定随机字节串的长度。
        int.from_bytes 把字节串转换为 int，也就是我们需要的二进制数
        """
        key = token_bytes(nbytes=length)
        key_int = int.from_bytes(key, 'big')
        return key_int

    def encrypt(self, row_str, key_int=None):
        """
        通过 encode 方法，我们将字符串编码成字节串。
        int.from_bytes 函数将字节串转换为 int 对象。
        最后对二进制对象和随机密钥进行异或操作，就得到了加密文本
        """
        raw_bytes = row_str.encode()
        raw_int = int.from_bytes(raw_bytes, 'big')
        key_int = key_int or self.random_key(len(raw_bytes))
        # 加密文本@随即密钥@加密时混入的字符串
        return str(raw_int ^ key_int) + '-' + str(key_int)

    def decrypt(self, cooked_str):
        """
        cooked_str：加密文本@随即密钥@加密时混入的字符串
        分别对加密文本（encrypted）和随机密钥（key_int）进行异或操作，计算解密出来的 int 对象所占比特数。
        decrypted.bit_length 函数得到的是二进制数的位数，除以 8 可以得到所占比特大小。
        为了防止，1 ~ 7 位的二进制数整除 8 得到 0，所以要加上 7，然后再进行整除 8 的操作。
        使用 int.to_bytes 函数将解密之后的 int 的对象转换成 bytes 对象。
        最后通过 decode 方法，将字节串转换成字符串。
        """
        encrypted, key_int = cooked_str.split('-')
        decrypted = int(encrypted) ^ int(key_int)
        length = (decrypted.bit_length() + 7) // 8
        decrypted_bytes = int.to_bytes(decrypted, length, 'big')
        return decrypted_bytes.decode()

    def encrypt_file(self, path, key_path=None, *, encoding='utf-8'):
        """
        path 为待加密文件的地址，如果不指定密钥地址，则在该目录下新建目录和文件
        """
        path = Path(path)
        cwd = path.cwd() / path.name.split('.')[0]
        path_encrypted = cwd / path.name
        if key_path is None:
            key_path = cwd / 'key'
        if not cwd.exists():
            cwd.mkdir()
            path_encrypted.touch()
            key_path.touch()

        with path.open('rt', encoding=encoding) as f1, \
            path_encrypted.open('wt', encoding=encoding) as f2, \
                key_path.open('wt', encoding=encoding) as f3:
            encrypted, key = self.encrypt(f1.read())
            json.dump(encrypted, f2)
            json.dump(key, f3)

    def decrypt_file(self, path_encrypted, key_path=None, *, encoding='utf-8'):
        path_encrypted = Path(path_encrypted)
        cwd = path_encrypted.cwd()
        path_decrypted = cwd / 'decrypted'
        if not path_decrypted.exists():
            path_decrypted.mkdir()
            path_decrypted /= path_encrypted.name
            path_decrypted.touch()
        if key_path is None:
            key_path = cwd / 'key'
        with path_encrypted.open('rt', encoding=encoding) as f1, \
            key_path.open('rt', encoding=encoding) as f2, \
                path_decrypted.open('wt', encoding=encoding) as f3:
            decrypted = self.decrypt(json.load(f1), json.load(f2))
            f3.write(decrypted)
