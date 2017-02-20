from Crypto.Cipher import AES

password = 'f48286d47146e7f21914c2a9e3c28b5406730970e1d6b761a9824bdebb9ea6d25912c896bc4d143ce7b4aaada1efd9dc'

password = '9244d23f660a93b2607ffd51cba904f4'
password_org = 'Passw0rd'


def decrypt_password(password):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]
    key = "cloudchefcloudch"  # the length can be (16, 24, 32)
    cipher = AES.new(key)
    decrypted = unpad(cipher.decrypt(password.decode('hex')))

    return decrypted

print (decrypt_password(password))