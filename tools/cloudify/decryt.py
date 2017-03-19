from Crypto.Cipher import AES

password_org = 'password'
en_password = '9244d23f660a93b2607ffd51cba904f4'


def decrypt_password(password):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]
    key = "cloudchefcloudch"  # the length can be (16, 24, 32)
    cipher = AES.new(key)
    decrypted = unpad(cipher.decrypt(password.decode('hex')))

    return decrypted

print (decrypt_password(en_password))


key = 'Cc12345678'

def encrypt_password(password):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]
    key = "cloudchefcloudch"  # the length can be (16, 24, 32)
    cipher = AES.new(key)

    encrypted = cipher.encrypt(pad(password)).encode('hex')
    return encrypted

print encrypt_password(key)


