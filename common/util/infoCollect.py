#!/usr/bin/python

import config
import Connection
import Env

#get microcode version of target system
def get_microcode_version(runner):
    para = config.parameters().get_executor(runner=runner)
    target_ip = para.keys()
    print target_ip
    SSH = Connection.Connection(host=target_ip[0], username="root", private_key=Env.id_rsa)
    ver = SSH.execute("xcli.py version_get|tail -n1")[0].strip()
    return ver
