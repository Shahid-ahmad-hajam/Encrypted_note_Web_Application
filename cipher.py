from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64

# AESCipher class
class AESCipher:
    def __init__(self, key):
        # Hash the password to produce a 16-byte key
        self.key = SHA256.new(key.encode()).digest()[:16]
        self.block_size = AES.block_size # prepares a fixed-size key for AES encryption.(16 bytes defualt)

    def pad(self, data):
        padding = self.block_size - len(data) % self.block_size
        return data + padding * chr(padding)

    def unpad(self, data):
        return data[:-ord(data[len(data)-1:])]

    def encrypt(self, raw):
        raw = self.pad(raw) # pad() function
        iv = get_random_bytes(AES.block_size) # get_random_bytes() function
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw.encode())
        return base64.b64encode(iv + encrypted).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = self.unpad(cipher.decrypt(enc[AES.block_size:]))
        return decrypted.decode('utf-8')