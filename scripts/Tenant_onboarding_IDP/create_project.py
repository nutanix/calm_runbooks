# script

import requests
from requests.auth import HTTPBasicAuth

ROLE_ADMIN = "Project Admin"
ROLE_OPERATOR = "Operator"
ROLE_DEVELOPER = "Developer"
ROLE_CONSUMER = "Consumer"
ROOT_OU = 'tenants'

PC_IP = "localhost"
management_username = "@@{management_pc_username}@@".strip()
management_password = "@@{management_pc_password}@@".strip()

def get_role_uuid(role_name):
    api_url = 'https://{}:9440/api/nutanix/v3/roles/list'.format(PC_IP)
    payload = {
      'filter': 'name=={}'.format(role_name),
      'kind': 'role',
      'offset': 0
    }
    r = requests.post(api_url, json=payload, 
                    auth=HTTPBasicAuth(management_username, management_password), 
                    timeout=None, verify=False)
    result = json.loads(r.content)
    if result.get('entities', 'None') != 'None':
        return result['entities'][0]['metadata']['uuid']
    else:
        print("Error :- {}".format(r.content))
        exit(1)

def get_project_specs(project):
    url = _build_url(scheme="https",
                    resource_type="/projects_internal/{}".format(project))
    data = requests.get(url,
                        auth=HTTPBasicAuth(management_username, management_password),
                        timeout=None, verify=False)
    if data.ok:
        return data.json()
    else:
        print(data.json())
    
def get_spec(role_uuid,user_uuid,user_name,idp_uuid,account_uuid,subnet_uuid,vpc_uuid,project_name,project_uuid,subnet_name):
    project_specs = get_project_specs(project_uuid)
    collection = "ALL"
    if "@@{allow_collaboration}@@".lower() == "false":
        collection = "SELF_OWNED"
    external_network = []
    subnet_reference = []
    if "@@{account_name}@@".strip() == "NTNX_LOCAL_AZ":
        subnet_reference = [
            {
            "kind": "subnet",
            "name": subnet_name,
            "uuid": subnet_uuid
            }
            ]
    else:
        external_network = [
            {
            "name": subnet_name,
            "uuid": subnet_uuid
            }
            ]
        
    return ({
    "spec": {
        "access_control_policy_list": [
            {
                "acp": {
                    "name": "ADMIN-ACP-@@{calm_now}@@",
                    "resources": {
                        "role_reference": {
                            "name": "Project Admin",
                            "uuid": role_uuid,
                            "kind": "role"
                        },
                        "user_group_reference_list": [],
                        "user_reference_list": [
                            {
                                "name": user_name,
                                "kind": "user",
                                "uuid": user_uuid
                            }
                        ],
                        "filter_list": {
                            "context_list": [
                                {
                                    "scope_filter_expression_list": [
                                        {
                                            "operator": "IN",
                                            "left_hand_side": "PROJECT",
                                            "right_hand_side": {
                                                "uuid_list": [
                                                    project_uuid
                                                ]
                                            }
                                        }
                                    ],
                                    "entity_filter_expression_list": [
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "ALL"
                                            },
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "entity_filter_expression_list": [
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "image"
                                            },
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "marketplace_item"
                                            },
                                            "right_hand_side": {
                                                "collection": "SELF_OWNED"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "identity_provider"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "directory_service"
                                            }
                                        },
                                        {
                                        "operator": "IN",
                                        "left_hand_side": {
                                            "entity_type": "custom_provider"
                                        },
                                        "right_hand_side": {
                                            "collection": "ALL"
                                        }
                                        },
                                        {
                                        "operator": "IN",
                                        "left_hand_side": {
                                            "entity_type": "virtual_network"
                                        },
                                        "right_hand_side": {
                                            "collection": "ALL"
                                        }
                                            },
                                        {
                                        "operator": "IN",
                                        "left_hand_side": {
                                            "entity_type": "resource_type"
                                        },
                                        "right_hand_side": {
                                            "collection": "ALL"
                                        }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "role"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "uuid_list": [
                                                    project_uuid
                                                ]
                                            },
                                            "left_hand_side": {
                                                "entity_type": "project"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "user"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "user_group"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "environment"
                                            },
                                            "right_hand_side": {
                                                "collection": "SELF_OWNED"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "app_icon"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            },
                                            "left_hand_side": {
                                                "entity_type": "category"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "app_task"
                                            },
                                            "right_hand_side": {
                                                "collection": "SELF_OWNED"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "app_variable"
                                            },
                                            "right_hand_side": {
                                                "collection": "SELF_OWNED"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "vm_recovery_point"
                                            },
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "cluster"
                                            },
                                            "right_hand_side": {
                                                "uuid_list": ["@@{cluster_uuid}@@"]
                                            }
                                        }
                                    ]
                                },
                                {
                                    "scope_filter_expression_list": [
                                        {
                                            "operator": "IN",
                                            "left_hand_side": "PROJECT",
                                            "right_hand_side": {
                                                "uuid_list": [
                                                    project_uuid
                                                ]
                                            }
                                        }
                                    ],
                                    "entity_filter_expression_list": [
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "blueprint"
                                            },
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "environment"
                                            },
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            }
                                        },
                                        {
                                            "operator": "IN",
                                            "left_hand_side": {
                                                "entity_type": "marketplace_item"
                                            },
                                            "right_hand_side": {
                                                "collection": "ALL"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    "description": "project admin acp @@{calm_now}@@"
                },
                "metadata": {
                    "kind": "access_control_policy"
                },
                "operation": "ADD"
            }
        ],
        "project_detail": {
            "name": project_name,
            "resources": {
                "external_network_list": external_network,
                "account_reference_list": [
                    {
                        "kind": "account",
                        "uuid": account_uuid
                    }
                ],
                "user_reference_list": [
                    {
                        "name": user_name,
                        "kind": "user",
                        "uuid": user_uuid
                    }
                ],
                "default_subnet_reference": {
                    "kind": "subnet",
                    "uuid": subnet_uuid
                },
                "vpc_reference_list": [
                    {
                        "kind": "vpc",
                        "uuid": vpc_uuid
                    }
                ],
                "tunnel_reference_list": [],
                "external_user_group_reference_list": [],
                "subnet_reference_list": subnet_reference,
                "resource_domain": {},
                "cluster_reference_list": [
                    {
                        "kind": "cluster",
                        "uuid": "@@{cluster_uuid}@@"
                    }
                ],
                "environment_reference_list": []
            },
            "description": "Tenant Onboarding Project"
        },
        "user_list": [],
        "user_group_list": []
    },
    "api_version": project_specs["api_version"],
    "metadata": {
        "kind": "project",
        "uuid":project_uuid,
        "spec_version":project_specs["metadata"]["spec_version"]
    }})

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

def _get_default_spec():
    return (
        {
          "api_version": "3.1.0",
          "metadata": {"kind": "project"},
          "spec": {
              "project_detail" : {
                  "name": "",
                  "resources": {}
                  }
                }
            }
        )
            
def _get_user_spec():
    return ({
        "api_version": "3.1.0",
        "metadata": {
            "kind" : "user"
            },
        "spec": {
            "resources": {}
            }
        })
def is_user_exist_in_pc(user):
    _url = _build_url(scheme="https",resource_type="/users/list")                        
    _data = requests.post(_url, json={"kind":"user", "filter":"username==%s"%user},
                                 auth=HTTPBasicAuth(management_username, 
                                                    management_password),
                                 timeout=None, verify=False)
    if _data.ok:
        if _data.json()['metadata']['total_matches'] == 1:
            return _data.json()['entities'][0]['metadata']['uuid']
        elif _data.json()['metadata']['total_matches'] > 1:
            print("Found more than one user with samename in PC")
            exit(1)
        else:
            return None
    else:
        print("Error while Fetching user details----> ",_data.json())
        exit(1)

def get_user_uuid(user, **params):

    user_uuid = is_user_exist_in_pc(user)
    if not user_uuid:
        payload = _get_user_spec()   
        ad = @@{idp_details}@@
        payload['spec']['resources']['identity_provider_user'] = {}
        payload['spec']['resources']['identity_provider_user']\
                                    ['username'] =  user.strip()

        payload['spec']['resources']['identity_provider_user']\
                ['identity_provider_reference'] = {}
        payload['spec']['resources']['identity_provider_user']\
                ['identity_provider_reference']['kind'] = "identity_provider"
        payload['spec']['resources']['identity_provider_user']\
                    ['identity_provider_reference']['uuid'] = ad["uuid"]
                    
        url = _build_url(scheme="https",resource_type="/users")
        data = requests.post(url, json=payload,
                            auth=HTTPBasicAuth(management_username, 
                                            management_password),
                            timeout=None, verify=False)

        if data.ok:
            wait_for_completion(data)
            return data.json()['metadata']['uuid']
        else:
            print("Error while Creating user details----> ",data.json())
            exit(1)
    else:
        return user_uuid
        
    # url = _build_url(scheme="https",
    #                 resource_type="/idempotence_identifiers/salted")
    # payload = {"name_list":[user]}
    # data = requests.post(url, json=payload,
    #                     auth=HTTPBasicAuth(management_username, management_password),
    #                     timeout=None, verify=False)                   
    # if data.ok:
    #     _uuid = data.json()["name_uuid_list"][0][user]
    #     print("user_uuid----> %s"%_uuid)
    #     return _uuid
    # else:
    #     print("Error while fetching user details :- ",data.json())
    #     exit(1)
        
def create_empty_project(project_name):
    payload = {
        "api_version": "3.0",
        "metadata": {
            "kind": "project"
        },
        "spec": {
            "project_detail": {
                "name": project_name,
                "resources": {}
            },
            "user_list": [],
            "user_group_list": [],
            "access_control_policy_list": []
        }
    }
    
    url = _build_url(scheme="https",resource_type="/projects_internal")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(management_username, management_password),
                        timeout=None, verify=False)
    if data.ok:
        wait_for_completion(data)
    else:
        print("Failed with Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    
    return data.json()["metadata"]["uuid"]
    
def build_project(**params):    
    vpc_details = @@{vpc_details}@@
    admin_role_uuid = get_role_uuid(ROLE_ADMIN)
    operator_role_uuid = get_role_uuid(ROLE_OPERATOR)
    developer_role_uuid = get_role_uuid(ROLE_DEVELOPER)
    consumer_role_uuid = get_role_uuid(ROLE_CONSUMER)
    print('ROLE_ADMIN_UUID={}'.format(admin_role_uuid))
    print('ROLE_OPERATOR_UUID={}'.format(operator_role_uuid))
    print('ROLE_DEVELOPER_UUID={}'.format(developer_role_uuid))
    print('ROLE_CONSUMER_UUID={}'.format(consumer_role_uuid))
        
    overlay_subnets = @@{overlay_subnet_details}@@
    subnet_uuid = overlay_subnets["uuid"]
    subnet_name = overlay_subnets["name"]
    
    account_uuid = ""
    if params.get('accounts', 'None') != "None":
        url = _build_url(scheme="https",resource_type="/accounts/list")
        data = requests.post(url, json={"kind":"account", "filter":"name==%s"%params['accounts']},
                        auth=HTTPBasicAuth(management_username, management_password),
                        timeout=None, verify=False)       
        if params['accounts'] in str(data.json()):
            for new_data in data.json()['entities']:
                if new_data['metadata']['name'] == params['accounts']: 
                    account_uuid = new_data['metadata']['uuid']
                    print("account_details={}".format({"uuid": account_uuid}))
        else:
            print("Error : %s account not present on %s"%(params['accounts'],PC_IP))
            exit(1)         
                                   
    user_details = []
    all_users = []
    user = "@@{project_admin_user}@@".strip()
    user_uuid = get_user_uuid(user, **params)
    if user_uuid != "None":
        user_details.append({'name':user, 'uuid':user_uuid})
    print("user_details={}".format(user_details))
    
    idp_uuid =  @@{idp_details}@@

    #idp_uuid = idp['uuid']
    print("group_details={}".format([]))
    vpc_uuid = @@{vpc_details}@@
    project_uuid = create_empty_project(project_name=params['name'])
    payload = get_spec(role_uuid=admin_role_uuid, 
                       user_uuid=user_details[0]["uuid"], 
                       user_name=user_details[0]["name"], 
                       idp_uuid=idp_uuid["uuid"], 
                       account_uuid=account_uuid, 
                       subnet_uuid=subnet_uuid,
                       vpc_uuid=vpc_uuid["uuid"],
                       project_name=params['name'],
                       project_uuid=project_uuid,
                       subnet_name=subnet_name)
    if params.get("quotas", "None") != "None":
        payload["spec"]["project_detail"]["resources"]["resource_domain"] = {}  
        resources = []
        for resource in params['quotas']:
            if resource.get("mem_gb", 0) != 0:
                mem_gb = resource["mem_gb"] * 1024 * 1024 * 1024
                resources.append({"resource_type":"MEMORY", "limit":mem_gb})
            if resource.get("storage_gb", 0) != 0:
                storage_gb = resource['storage_gb'] * 1024 * 1024 * 1024
                resources.append({"resource_type":"STORAGE", "limit":storage_gb})
            if resource.get("vcpu", 0) != 0:
                resources.append({"resource_type":"VCPUS", "limit":resource['vcpu']})
        payload["spec"]["project_detail"]["resources"]["resource_domain"] = {"resources": resources}
        
    url = _build_url(scheme="https",resource_type="/projects_internal/%s"%project_uuid)
    data = requests.put(url, json=payload,
                        auth=HTTPBasicAuth(management_username, management_password),
                        timeout=None, verify=False)
    if data.ok:
        wait_for_completion(data)
    else:
        print("Failed with Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    
    if 'status' not in data.json():
        print("Project %s not created successfully."%params['name'])
        print(data.json())
        exit(1)
    task_uuid = data.json()['status']['execution_context']['task_uuid']
    if 'metadata' in data.json():
        print("project_details={}".format({"uuid":data.json()['metadata']['uuid'],
                                       "name": params['name'],
                                       "create_project_task_uuid": task_uuid}))
    else:
        print("Project not created successfully, Check inputs and payload")
        print(data.json())
        exit(1)
  
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(management_username,management_password), 
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Got Error ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        if "DUPLICATE_ENTITY" not in str(data.json()):
            print("Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
            exit(1)

print("##### Creating a Project #####")
params = @@{project_items}@@
build_project(**params)                                       