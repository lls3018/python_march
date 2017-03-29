
# config
ECS_CONFIG_PROPERTY = 'aliyun_config'
ECS_EXTERNAL_TYPE = 'external_type'
ECS_EXTERNAL_NAME = 'external_name'
ECS_EXTERNAL_ID = 'external_id'
#EXTERNAL_RESOURCE_ID = 'ecs_resource_id'

NODE_INSTANCE = 'node-instance'
RELATIONSHIP_INSTANCE = 'relationship-instance'
ECS_CONFIG_PATH_ENV_VAR_NAME = "ECS_CONFIG_PATH"

# instance module constants
INSTANCE_RUNNING = "Running"
INSTANCE_STARTING = "Starting"
INSTANCE_STOPPED = "Stopped"
#INSTANCE_DELETED = "Deleted"
INSTANCE_DELETED = None

ISMONITORED = 'isMonitored'
ISAGENTINSTALLED = 'isAgentInstalled'

INSTANCE_REQUIRED_PROPERTIES = ['ImageId', 'InstanceType', 'SecurityGroupId']

INSTANCE_INTERNAL_ATTRIBUTES = \
    ['dns_name', 'inner_ip_address',
     'public_ip_address', 'vpc_attributes']

INSTANCE_PUBLIC_IP_ADDRESS = 'ip'

INSTANCE_INTERNAL_ATTRIBUTES_POST_CREATE = \
    ['vpc_id', 'subnet_id', 'placement']

RUN_INSTANCE_PARAMETERS = {
    'image_id': None, 'key_name': None, 'security_groups': None,
    'user_data': None, 'addressing_type': None,
    'instance_type': 'm1.small', 'placement': None, 'kernel_id': None,
    'ramdisk_id': None, 'monitoring_enabled': False, 'subnet_id': None,
    'block_device_map': None, 'disable_api_termination': False,
    'instance_initiated_shutdown_behavior': None,
    'private_ip_address': None, 'placement_group': None,
    'client_token': None, 'security_group_ids': None,
    'additional_info': None, 'instance_profile_name': None,
    'instance_profile_arn': None, 'tenancy': None, 'ebs_optimized': False,
    'network_interfaces': None, 'dry_run': False
}

INSTANCE_SECURITY_GROUP_RELATIONSHIP = 'instance_connected_to_security_group'
INSTANCE_LOAD_BALANCER_RELATIONSHIP = 'instance_connected_to_load_balancer'
INSTANCE_KEYPAIR_RELATIONSHIP = 'instance_connected_to_keypair'
INSTANCE_SUBNET_RELATIONSHIP = 'instance_contained_in_subnet'
DISK_INSTANCE_RELATIONSHIP = 'disk_connected_to_instance'
SECURITY_GROUP_VPC_RELATIONSHIP = 'security_group_contained_in_vpc'

ADMIN_PASSWORD_PROPERTY = 'password'  # the server's password


##############################
PARAMS_CHECK_ERROR_RESULT = ""

# disk module constants
DISK_INUSE = "In_use"
DISK_AVAILABLE = "Available"
DISK_ATTACHING = "Attaching"
DISK_DETACHING = "Detaching"
DISK_CREATING = "Creating"
DISK_REINITING = "ReIniting"
DISK_ALL = "All"

# disk type
DISK_TYPE_ALL = "all"
DISK_TYPE_SYSTEM = "system"
DISK_TYPE_DATA = "data"

# disk category
DISK_CATEGORY_CLOUD = "cloud"
DISK_CATEGORY_CLOUD_EFFICIENCY = "cloud_efficiency"
DISK_CATEGORY_CLOUD_SSD = "cloud_ssd"


DISK_REQUIRED_PROPERTIES = ['ZoneId']

# snapshot module constants
SNAPSHOT_PROGRESSING = "progressing"
SNAPSHOT_ACCOMPLISHED = "accomplished"
SNAPSHOT_FAILED = "failed"
SNAPSHOT_ALL = "all"

# image module constants
IMAGE_CREATING = "Creating"
IMAGE_AVAILABLE = "Available"
IMAGE_UNAVAILABLE = "UnAvailable"
IMAGE_CREATEFAILED = "CreateFailed"

# elastic ip module
EIP_ASSOCIATING = "Associating"
EIP_UNASSOCIATING = "Unassociating"
EIP_INUSE = "InUse"
EIP_AVAILABLE = "Available"

# vpc ip module
VPC_AVAILABLE = "Available"
VPC_PENDING = "Pending"

ZONE = 'ZoneId'

# regions
# REGION_ID = "cn-hangzhou"
# REGION_ID="cn-beijing"
# REGION_ID="cn-qingdao"
REGION_ID="cn-shenzhen"
# REGION_ID="cn-shanghai"
# REGION_ID="cn-hongkong"
# REGION_ID="us-west-1"
# REGION_ID="us-east-1"
# REGION_ID="ap-southeast-1"

# auth
SECRETID= "AKIDFOM9ny8oPwHQNBuOG9rNhtumTAj7GJuM"
SECRETKEY = "ObdU9bsysa2LvJVXPPErY6RbZMyXu66u"
#ACCESS_KEY = "LTAIlVjImgIWYWOQ"
#ACCESS_SECRET = "bLyhSMD1rDUklaU7f3LQepp7KwK7rA"
