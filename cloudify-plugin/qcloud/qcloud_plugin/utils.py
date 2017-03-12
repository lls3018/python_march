import os
import time
import json


from aliyunsdkcore.acs_exception.exceptions import ClientException


def validate_node_property(key, ctx_node_properties):
    """Checks if the node property exists in the blueprint.

    :raises Exception: if key not in the node's properties
    """
    if key not in ctx_node_properties:
        raise Exception(
            '{0} is a required input. Unable to create.'.format(key))


def excute_action(client, request, params):
    request.set_accept_format('json')
    request.set_query_params(params)
    print(
        'Execute_action {0} with parameters: {1}'
            .format(request.get_action_name(), params))

    try:
        status, headers, body = client.get_response(request)
        result = json.loads(body)
        if status == 200:
            print('Execute success: {0} with result: {1}'
                             .format(request.get_action_name(), result))
            return result
        elif status == 409 and request.get_action_name() == 'AttachDisk':
            raise Exception('The attach disk action is still running. Retrying...',
                                   retry_after=15)
        else:
            error_msg = 'Exception: Action {0}: The status code: {1} with result: {2}'\
                .format(request.get_action_name(), status, result)
            raise Exception('{0}.'.format(error_msg))
    except ClientException as e:
        error_msg = "Exception: Action:" + request.get_action_name() + e.get_error_msg()
        raise Exception('{0}.'.format(error_msg))