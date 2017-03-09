#!/usr/bin/env python
# encoding: utf-8
import sys
import argparse
from ecs import instance


def usage():
    usage_str = """
    python %s --help : to get help info
    """ % (sys.argv[0])
    return usage_str


def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for cloudchef tool')

    parser.add_argument('-i', '--instance',
                        action='store',
                        help='the instance id')

    args = parser.parse_args()
    return args


def delete_vm(instance_id):
    print "the instance id is {} ".format(instance_id)
    instance.get_state(instance_id)
    instance.stop(instance_id=instance_id)
    instance.terminate(instance_id=instance_id)


def main():
    """
    Let this thing fly
    """
    print usage()
    args = get_args()
    if args.instance:
        instance_id = args.instance
        delete_vm(instance_id)


if __name__ == "__main__":
    main()
