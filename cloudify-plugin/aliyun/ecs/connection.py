# Builtin Imports
from functools import wraps
from aliyunsdkcore import client
from ecs import constants


def with_ecs_client(f):
    @wraps(f)
    def wrapper(*args, **kw):
        ecs_client = ECSConnectionClient().client()
        kw['ecs_client'] = ecs_client
        return f(*args, **kw)
    return wrapper


class ECSConnectionClient():
    """Provides functions for getting the ECS Client
    """

    def __init__(self):
        self.connection = None

    def client(self):
        """Represents the ECSConnection Client
        """
        ECSConnection = client.AcsClient(str(constants.ACCESS_KEY),
                                         str(constants.ACCESS_SECRET),
                                         str(constants.REGION_ID))

        return ECSConnection
