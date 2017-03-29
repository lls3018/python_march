# Builtin Imports
from functools import wraps

from qingcloud import iaas
from Crypto.Cipher import AES


def with_qingcloud_client(f):
    @wraps(f)
    def wrapper(*args, **kw):
        qingcloud_client = QingcloudConnectionClient().client()
        kw['qingcloud_client'] = qingcloud_client
        return f(*args, **kw)
    return wrapper


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


class QingcloudConnectionClient():
    """Provides functions for getting the Qcloud Client
    """

    def __init__(self):
        pass

    def client(self):
        """Represents the ECSConnection Client
        """
        qingcloud_config = {
            'zone': 'pek2',
            'access_key_id': 'DTSPSSQSXVVFHYLXANTX',
            'secret_access_key': 'Vr6qvbM8Pvhyil2h6IIHffC8UXVs5esLeG1Xh1xX'
        }

        client = iaas.connect_to_zone(zone=qingcloud_config.get('zone'),
                                      access_key_id=qingcloud_config.get('access_key_id'),
                                      secret_access_key=qingcloud_config.get('secret_access_key'))

        return client
