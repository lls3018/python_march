# Third-party Imports

from aliyunsdkecs.request.v20140526 import CreateInstanceRequest, DeleteInstanceRequest, DescribeInstancesRequest, \
    StartInstanceRequest, StopInstanceRequest, RebootInstanceRequest, ModifyInstanceAttributeRequest, \
    DescribeInstanceStatusRequest, JoinSecurityGroupRequest, LeaveSecurityGroupRequest, ModifyInstanceVpcAttributeRequest, \
    DescribeInstanceVncUrlRequest, ModifyInstanceVncPasswdRequest, AllocatePublicIpAddressRequest, RenewInstanceRequest

from ecs import utils

from connection import *


def get_state(instance_id, **_):
    print("Entering instance state validation procedure.")

    if instance_id is None:
        raise Exception("Cannot get info - instance doesn't exist")

    instance_status = describe_instance_status_from_id(instance_id)
    print instance_status


@with_ecs_client
def start(ecs_client, instance_id, **_):

    instance_status = describe_instance_status_from_id(instance_id)

    if instance_status == constants.INSTANCE_RUNNING:
        return

    print('Attempting to start instance: {0}.'.format(instance_id))
    request = StartInstanceRequest.StartInstanceRequest()
    utils.excute_action(ecs_client, request, dict(InstanceId=instance_id))
    print('Attempted to start instance {0}.'.format(instance_id))

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status != constants.INSTANCE_RUNNING:
        _wait_for_server_to_be_targetstatus(instance_id, constants.INSTANCE_RUNNING)

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status == constants.INSTANCE_RUNNING:
        print('Started instance {0}.'.format(instance_id))
    else:
        raise Exception('Start {0} failed.'.format(instance_id))


@with_ecs_client
def stop(ecs_client, instance_id, **_):
    instance_status = describe_instance_status_from_id(instance_id)

    if instance_status == constants.INSTANCE_STOPPED:
        return

    print(
        'Attempting to stop ECS Instance. {0}.)'.format(instance_id))
    request = StopInstanceRequest.StopInstanceRequest()
    utils.excute_action(ecs_client, request, dict(InstanceId=instance_id))
    print('Attempted to stop instance {0}.'.format(instance_id))

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status != constants.INSTANCE_STOPPED:
        _wait_for_server_to_be_targetstatus(instance_id, constants.INSTANCE_STOPPED)

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status == constants.INSTANCE_STOPPED:
        print('Stopped instance {0}.'.format(instance_id))
    else:
        raise Exception('Stop {0} failed.'.format(instance_id))


@with_ecs_client
def reboot(ecs_client, instance_id, **kwargs):
    kwargs["InstanceId"] = instance_id

    print(
        'Attempting to reboot ECS Instance. {0}.)'.format(instance_id))
    request = RebootInstanceRequest.RebootInstanceRequest()
    utils.excute_action(ecs_client, request, kwargs)
    print('Attempted to reboot instance {0}.'.format(instance_id))

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status != constants.INSTANCE_RUNNING:
        _wait_for_server_to_be_targetstatus(instance_id, constants.INSTANCE_RUNNING)

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status == constants.INSTANCE_RUNNING:
        print('Reboot instance {0}.'.format(instance_id))
    else:
        raise Exception('Reboot {0} failed.'.format(instance_id))


@with_ecs_client
def terminate(ecs_client, instance_id, **_):
    print(
        'Attempting to terminate ECS Instance. {0}.)'.format(instance_id))
    request = DeleteInstanceRequest.DeleteInstanceRequest()
    utils.excute_action(ecs_client, request, dict(InstanceId=instance_id))
    print('Attempted to delete instance {0}.'.format(instance_id))

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status != constants.INSTANCE_DELETED:
        _wait_for_server_to_be_targetstatus(instance_id, constants.INSTANCE_DELETED)

    instance_status = describe_instance_status_from_id(instance_id)
    if instance_status == constants.INSTANCE_DELETED:
        print('Deleted instance {0}.'.format(instance_id))
    else:
        raise Exception('Stop {0} failed.'.format(instance_id))


def _wait_for_server_to_be_targetstatus(instance_id, targetstatus, timeout=600, sleep_interval=60):
    import time
    timeout = time.time() + timeout
    while time.time() < timeout:
        instance_status = describe_instance_status_from_id(instance_id)
        print('Waiting for server "{0}" to be {1}. current'
                         ' status: {2}'.format(instance_id, targetstatus, instance_status))
        time.sleep(sleep_interval)

        if instance_status == targetstatus:
            return
    # raise RuntimeError('Server {} has not been deleted. waited for {} seconds'.format(instance_id, timeout))
    return


@with_ecs_client
def describe_instances_status(ecs_client, **params):
    '''
    :param RegionId
    :param ZoneId
    :param PageNumber
    :param PageSize
    :return: TotalCount, PageNumber, PageSize, InstanceStatuses
    '''
    request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    result = utils.excute_action(ecs_client, request, params)
    return result['InstanceStatuses']['InstanceStatus']


def describe_instance_status_from_id(instance_id):
    """Gets the instance ID of a ECS Instance

    :param instance_id: The ID of an ECS Instance
    :param ctx:  The Cloudify ctx context.
    :returns an ID of a an EC2 Instance or None.
    """

    statuses = describe_instances_status()
    for status in statuses:
        if instance_id in status['InstanceId']:
            return status['Status']
    return None