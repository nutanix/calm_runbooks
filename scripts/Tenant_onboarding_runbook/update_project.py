# script
import requests
from requests.auth import HTTPBasicAuth


def _build_url(scheme, resource_type, host=@@{PC_IP}@@, **params):
    _base_url = "/api/nutanix/v3"
    url = "{proto}://{host}".format(proto=scheme, host=host)
    port = params.get('nutanix_port', '9440')
    if port:
        url = url + ":{0}".format(port) + _base_url
    if resource_type.startswith("/"):
        url += resource_type
    else:
        url += "/{0}".format(resource_type)
    return url
    
def _get_spec(project):
    url = _build_url(scheme="https",
                    resource_type="/projects_internal/{}".format(project))
    data = requests.get(url,
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)
    return data.json()
  
def update_project(**params):
    project = @@{project_details}@@
    project_items = @@{project_items}@@
    users = @@{user_details}@@
    groups_list = @@{group_details}@@
    payload = _get_spec(project['uuid'])
    for x in ['categories', 'categories_mapping', 'creation_time', 'last_update_time', 'owner_reference']:
        del payload['metadata'][x]
    del payload['status']
    env_uuid = @@{environment_details}@@
    payload['spec']['project_detail']['resources']['environment_reference_list'] = []

    default_env_uuid = env_uuid[0]['uuid']
    for env in env_uuid:
        if env.get('default', False) == True:
            default_env_uuid = env['uuid']
        payload['spec']['project_detail']['resources']\
            ['environment_reference_list'].append({"kind":"environment",
                                                   "uuid":env['uuid']})
    payload['spec']['project_detail']['resources']\
        ["default_environment_reference"] = {"kind":"environment",
                                      "uuid":default_env_uuid}   
    env = @@{environment_items}@@
    for role in project_items[0]['tenant_users']:           
        acp = {}
        if 'admin' in role.keys():
            acp = generate_acp(role="admin", users=role['admin'])
                                
        elif 'developer' in role.keys():
            acp = generate_acp(role="developer", users=role['developer'])
                                
        elif 'operator' in role.keys():
            acp = generate_acp(role="operator", users=role['operator'])
                                
        elif 'consumer' in role.keys():
            acp = generate_acp(role="consumer", users=role['consumer'])
        payload['spec']['access_control_policy_list'].append(acp)
        
    if project_items[0].get('tenant_group', 'None') != 'None':
        for role in project_items[0]['tenant_group']:           
            acp = {}
            if 'admin' in role.keys():
                acp = generate_acp(role="admin", groups=role['admin'])
                                
            elif 'developer' in role.keys():
                acp = generate_acp(role="developer", groups=role['developer'])
                                
            elif 'operator' in role.keys():
                acp = generate_acp(role="operator", groups=role['operator'])
                                
            elif 'consumer' in role.keys():
                acp = generate_acp(role="consumer", groups=role['consumer'])
            payload['spec']['access_control_policy_list'].append(acp)
                        
    pprint(payload)
    url = _build_url(scheme="https",
                    resource_type="/projects_internal/{}".format(project['uuid']))
    data = requests.put(url, json=payload,
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)
    if data.ok:
        task = wait_for_completion(data)       
        print("Project %s updated successfully"%project['name'])
    else:
        print("Error while updating project : %s"%data.json())
    
def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(
                                    @@{prism_central_username}@@, 
                                    @@{prism_central_passwd}@@),
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        print("Got %s while updating project ---> "%state, data.json())
        exit(1)

def generate_filter_list_admin(project_uuid, collection):
    acl = []
    acl.append({"entity_filter_expression_list":[
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "image"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "directory_service"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "role"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"uuid_list": [project_uuid]},
                "left_hand_side": {"entity_type": "project"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "user"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "user_group"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "SELF_OWNED"},
                "left_hand_side": {"entity_type": "environment"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "app_icon"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "category"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_task"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_variable"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
        ]})

    acl.append({
        "scope_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": "PROJECT",
                "right_hand_side": {"uuid_list": []},
            }
        ],
        "entity_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "ALL"},
                "right_hand_side": {"collection": collection},
            }
        ],
    })
    return acl

def generate_filter_list_operator(project_uuid, collection):
    acl = []
    acl.append({"entity_filter_expression_list":[
        {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "app_icon"},
        },
        {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "category"},
        },
    ]})

    acl.append({
        "scope_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": "PROJECT",
                "right_hand_side": {"uuid_list": [project_uuid]},
            }
        ],
        "entity_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "ALL"},
                "right_hand_side": {"collection": collection},
            }
        ],
    })
    return acl   

def generate_filter_list_developer(project_uuid, collection):
    acl = []
    acl.append({"entity_filter_expression_list":[
        {
            "operator": "IN",
            "left_hand_side": {"entity_type": "image"},
            "right_hand_side": {"collection": "ALL"},
        },
        {
            "operator": "IN",
            "left_hand_side": {"entity_type": "marketplace_item"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
        {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "app_icon"},
        },
        {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "category"},
        },
        {
            "operator": "IN",
            "left_hand_side": {"entity_type": "app_task"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
        {
            "operator": "IN",
            "left_hand_side": {"entity_type": "app_variable"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
    ]})

    acl.append({
        "scope_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": "PROJECT",
                "right_hand_side": {"uuid_list": [project_uuid]},
            }
        ],
        "entity_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "ALL"},
                "right_hand_side": {"collection": collection},
            }
        ],
    })
    return acl

def generate_filter_list_consumer(project_uuid, collection):
    acl = []
    acl.append({"entity_filter_expression_list":[
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "image"},
                "right_hand_side": {"collection": "ALL"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "marketplace_item"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "app_icon"},
            },
            {
                "operator": "IN",
                "right_hand_side": {"collection": "ALL"},
                "left_hand_side": {"entity_type": "category"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_task"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "app_variable"},
                "right_hand_side": {"collection": "SELF_OWNED"},
            },
        ]})
    acl.append({
        "scope_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": "PROJECT",
                "right_hand_side": {"uuid_list": [project_uuid]},
            }
        ],
        "entity_filter_expression_list": [
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "ALL"},
                "right_hand_side": {"collection": collection},
            }
        ]})
    return acl 
  
def generate_acp(role, users=None, groups=None):
    project = @@{project_details}@@
    group_list = @@{group_details}@@
    user_list = @@{user_details}@@
    projectUuid = project['uuid']
    user_name = @@{project_items}@@

    collection = "SELF_OWNED"
    if user_name[0]['allow_collaboration']:
        collection = "ALL"
    role_uuid = "@@{ROLE_OPERATOR_UUID}@@"
    filter_list = generate_filter_list_operator(projectUuid, collection)
    if role == "admin":
        role_uuid = "@@{ROLE_ADMIN_UUID}@@"
        filter_list = generate_filter_list_admin(projectUuid, collection)
    elif role == "developer":
        role_uuid = "@@{ROLE_DEVELOPER_UUID}@@"
        filter_list = generate_filter_list_developer(projectUuid, collection)
    elif role == "consumer":
        role_uuid = "@@{ROLE_CONSUMER_UUID}@@"
        filter_list = generate_filter_list_consumer(projectUuid, collection)
        
    acp = {}
    if groups == None:
        _type = 'users'
        user_reference_list = []
        for _user in users:
            for us in user_list:
                if _user in us['name']:
                    user_reference_list.append(\
                        {"kind":"user", "uuid": us['uuid']})
        acp_list = {
            'acp': {
                'name': 'ACP-TENANT-{}-{}'.format(role,_type),
                'resources': {
                    'role_reference': {
                        'kind': 'role',
                        'uuid': role_uuid
                        },
                         "user_reference_list": user_reference_list,
                         "filter_list": {'context_list': filter_list}
                    },
                    'description': 'Admin role for {}'.format(projectUuid)
                },
                'metadata': {
                    'kind': 'access_control_policy'
                },
                'operation': 'ADD'
            }
        access_control_policy_list = acp_list
    else:
        _type = 'groups'
        group_reference_list = []
        for _user in groups:
            for us in group_list:
                if _user in us['name']:
                    group_reference_list.append(\
                        {"kind":"user_group", "uuid": us['uuid']})
        acp_list = {
            'acp': {
                'name': 'ACP-TENANT-{}-{}'.format(role, _type),
                'resources': {
                    'role_reference': {
                        'kind': 'role',
                        'uuid': role_uuid
                        },
                         "user_group_reference_list": group_reference_list,
                         "filter_list": {'context_list': filter_list}
                    },
                    'description': 'Admin role for {}'.format(projectUuid)
                },
                'metadata': {
                    'kind': 'access_control_policy'
                },
                'operation': 'ADD'
            }
        access_control_policy_list = acp_list
    return access_control_policy_list

params = @@{project_items}@@
for _params in params:
    update_project(**_params)
