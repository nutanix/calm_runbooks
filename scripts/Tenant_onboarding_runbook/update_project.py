# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@"
pc_username = "@@{prism_central_username}@@"
pc_password = "@@{prism_central_passwd}@@"

def _build_url(scheme, resource_type, host=PC_IP, **params):
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
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    return data.json()
  
def user_list(user_name, user_uuid, idp_uuid):
    return([
              {
                "metadata": {
                  "kind": "user",
                  "uuid": user_uuid
                },
                "user": {
                  "resources": {
                    "identity_provider_user": {
                      "username": user_name,
                      "identity_provider_reference": {
                        "uuid": idp_uuid,
                        "kind": "identity_provider"
                      }
                    }
                  }
                },
                "operation": "ADD"
              }
            ])
def get_user_uuid(user, **params):
    _payload = {"entity_type": "abac_user_capability",
                "group_member_attributes": [
               {
                   "attribute": "display_name"
               },
               {
                   "attribute": "user_uuid"
               },
               {
                   "attribute": "username"
               }
           ],
           "query_name": "prism:BaseGroupModel"
         }
    url = _build_url(scheme="https",
                    resource_type="/groups")
    data = requests.post(url, json=_payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    if data.ok:
        for user_data in data.json()["group_results"][0]["entity_results"]:
            if user_data["data"][2]["values"][0]["values"][0] == user.strip():
                return user_data["entity_id"]
    else:
        print("Error while fetching user details :- ",data.json())
        exit(1)
                
    url = _build_url(scheme="https",
                    resource_type="/idempotence_identifiers/salted")
    payload = {"name_list":[user]}
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)                   
    if data.ok:
        _uuid = data.json()["name_uuid_list"][0][user]
        print("user_uuid----> %s"%_uuid)
        return _uuid
    else:
        print("Error while fetching user details :- ",data.json())
        exit(1)
        
def update_project(**params):
    project = @@{project_details}@@
    project_items = @@{project_items}@@
    payload = _get_spec(project['uuid'])
    for x in ['categories', 'categories_mapping', 'creation_time', 'last_update_time', 'owner_reference']:
        del payload['metadata'][x]
    del payload['status']
    payload['spec']['access_control_policy_list'][0]['operation'] = "UPDATE"
    payload['spec']['access_control_policy_list'][0]['acp']\
        ['resources']['filter_list']['context_list'][0]\
        ['scope_filter_expression_list'][0]['right_hand_side']['uuid_list'] = [project['uuid']]
    
    payload['spec']['access_control_policy_list'][0]['acp']['resources']\
        ['filter_list']['context_list'][1]['entity_filter_expression_list']\
        [4]['right_hand_side']['uuid_list'] = [project['uuid']]
    
    
    payload['spec']['access_control_policy_list'][0]['acp']['resources']\
        ['filter_list']['context_list'][2]['scope_filter_expression_list']\
        [0]['right_hand_side']['uuid_list'] = [project['uuid']]
    
    env_uuid = @@{environment_details}@@
    payload['spec']['project_detail']['resources']['environment_reference_list'] = []
    if "@@{create_environment}@@" == "yes":
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
        
    url = _build_url(scheme="https",
                    resource_type="/projects_internal/{}".format(project['uuid']))
    data = requests.put(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    if data.ok:
        task = wait_for_completion(data)       
        print("Project %s updated successfully"%project['name'])
    else:
        print("Error while updating project : %s"%data.json())
        exit(1)
    
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(
                                    pc_username, pc_password),
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error in project update ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        print("Error in project update ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
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
  
def generate_acp(role, user_details, users=None, groups=None):
    project = @@{project_details}@@
    user_list = user_details
    projectUuid = project['uuid']
    user_name = @@{project_items}@@
    group_list = @@{group_details}@@

    collection = "SELF_OWNED"
    if @@{allow_collaboration}@@:
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
update_project(**params)
