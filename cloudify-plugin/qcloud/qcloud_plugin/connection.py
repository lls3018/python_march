# Builtin Imports
from functools import wraps

from QcloudApi.qcloudapi import QcloudApi
from Crypto.Cipher import AES


def with_qcloud_client(module):
    def func_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kw):
            qcloud_client = QcloudConnectionClient(module).client()
            client_name = 'qcloud_client_' + module
            kw[client_name] = qcloud_client
            return f(*args, **kw)
        return wrapper
    return func_wrapper


def decrypt_password(password):
    if not password:
        return None
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]
    key = "cloudchefcloudch"  # the length can be (16, 24, 32)
    cipher = AES.new(key)
    decrypted = unpad(cipher.decrypt(password.decode('hex')))

    return decrypted


class QcloudConnectionClient():
    """Provides functions for getting the Qcloud Client
    """

    def __init__(self, module):
        self.module = module
        self.connection = None

    def client(self):
        """Represents the ECSConnection Client
        """

        qcloud_config = {
            'Region': 'sh',
            'secretId': 'AKIDFOM9ny8oPwHQNBuOG9rNhtumTAj7GJuM',
            'secretKey': 'ObdU9bsysa2LvJVXPPErY6RbZMyXu66u',
            'method': 'get'
        }

        client = QcloudApi(module=self.module, config=qcloud_config)

        return client
