# script

import requests
from requests.auth import HTTPBasicAuth

ROLE_ADMIN = "Project Admin"
ROLE_OPERATOR = "Operator"
ROLE_DEVELOPER = "Developer"
ROLE_CONSUMER = "Consumer"
ROOT_OU = 'tenants'

def get_role_uuid(role_name):
    api_url = 'https://{}:9440/api/nutanix/v3/roles/list'.format(@@{PC_IP}@@)
    payload = {
      'filter': 'name=={}'.format(role_name),
      'kind': 'role',
      'offset': 0
    }
    r = requests.post(api_url, json=payload, 
                    auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                       @@{prism_central_passwd}@@), 
                    timeout=None, verify=False)
    result = json.loads(r.content)
    if result.get('entities', 'None') != 'None':
        return result['entities'][0]['metadata']['uuid']
    else:
        print("Error :- {}".format(r.content))
        exit(1)

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

def _get_default_spec():
    return (
        {
          "api_version": "3.1.0",
          "metadata": {"kind": "project"},
          "spec": {
            "name": "",
            "resources": {}
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

def _get_group_spec():
	return ({
  			"api_version": "3.1.0",
  			"metadata": {
    			"kind": "user_group"
  				},
 			"spec": {
    			"resources": {
      				"directory_service_user_group": {
        				"distinguished_name": ""
      					}
    				}
  				}
			})
            
def convert_domain_to_ad_path(group_name):
    path = ''
    g_name, domain = group_name.split("@")
    path = "cn=%s,cn=users"%g_name
    for i in domain.split("."):
        path = path + ',DC={}'.format(i)
    
    return path
    
def create_group(group):
    payload = _get_group_spec()
    group_name = convert_domain_to_ad_path(group)
    if group != "None":
        payload['spec']['resources']['directory_service_user_group']\
        			['distinguished_name'] = group_name
    url = _build_url(scheme="https",resource_type="/user_groups")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth("admin", 
                                           "Nutanix.123"),
                        timeout=None, verify=False)    
    wait_for_completion(data)
    
    if not data.ok:
        if "DUPLICATE" in str(data.json()):
            return "ok"
        else:
            print("Error while creating user_group ----> ",data.json()['message_list'])
            return "None"
    else:
        return "ok"    
            
def create_user(user, **params):
    payload = _get_user_spec()   
    if params.get('tenant_users', "None") != "None":
        payload['spec']['resources']['directory_service_user'] = {}
        payload['spec']['resources']['directory_service_user']\
                                ['user_principal_name'] =  user
    else:
        print("Error --> Please ADD at-least one tenant user !!")
        exit(1)

    if params.get('ad_name', "None") == "None":
        payload['spec']['resources']['directory_service_user']\
            ['directory_service_reference'] = {}
        payload['spec']['resources']['directory_service_user']\
            ['directory_service_reference']['kind'] = "directory_service"
        sleep(10)
        ad_details = @@{ad_details}@@
        payload['spec']['resources']['directory_service_user']\
                ['directory_service_reference']['uuid'] = ad_details['ad_uuid']
      
    url = _build_url(scheme="https",
                    resource_type="/idempotence_identifiers")
    data = requests.post(url, json={"count": 1,"valid_duration_in_minutes": 527040},
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)                   
    user_uuid = ""
    if data.ok:
        user_uuid = data.json()['uuid_list'][0]
        payload['metadata']['uuid'] = user_uuid
    url = _build_url(scheme="https",resource_type="/users")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)    
    
    wait_for_completion(data)
    if not data.ok:
        if "DUPLICATE" in str(data.json()['message_list']):
            return "ok"
        else:
            print("Error while creating user ----> ",data.json()['message_list'])
            return "None"
    else:
        return user_uuid

def build_project(**params):
    payload = _get_default_spec()
    payload['spec']['name'] = params['name']
    payload['spec']['description'] = params.get("description", "Tenant Onboarding Project")
    admin_role_uuid = get_role_uuid(ROLE_ADMIN)
    operator_role_uuid = get_role_uuid(ROLE_OPERATOR)
    developer_role_uuid = get_role_uuid(ROLE_DEVELOPER)
    consumer_role_uuid = get_role_uuid(ROLE_CONSUMER)
    print('ROLE_ADMIN_UUID={}'.format(admin_role_uuid))
    print('ROLE_OPERATOR_UUID={}'.format(operator_role_uuid))
    print('ROLE_DEVELOPER_UUID={}'.format(developer_role_uuid))
    print('ROLE_CONSUMER_UUID={}'.format(consumer_role_uuid))
    
    if params.get("quotas", "None") != "None":
        payload['spec']['resources']['resource_domain'] = {}    
        resources = []
        for resource in params['quotas']:
            if resource.get("mem_gb", "None") != "None":
                mem_gb = resource["mem_gb"] * 1024 * 1024 * 1024
                resources.append({"resource_type":"MEMORY", "limit":mem_gb})
            if resource.get("storage_gb", "None") != "None":
                storage_gb = resource['storage_gb'] * 1024 * 1024 * 1024
                resources.append({"resource_type":"STORAGE", "limit":storage_gb})
            if resource.get("vcpu", "None") != "None":
                resources.append({"resource_type":"VCPUS", "limit":resource['vcpu']})
        payload['spec']['resources']['resource_domain']['resources'] = resources
        
    subnet_list = []
    for _uuid in params['subnets']:
        subnet_list.append({"kind":"subnet", "uuid": _uuid})
    payload['spec']['resources']["subnet_reference_list"] = subnet_list
    
    if params.get('accounts', 'None') != "None":
        payload['spec']['resources']["account_reference_list"] = []
        url = _build_url(scheme="https",resource_type="/accounts/list")
        data = requests.post(url, json={"kind":"account"},
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)

        for account in params['accounts']:
            account_uuid = ""
            if account in str(data.json()):
                for new_data in data.json()['entities']:
                    if new_data['metadata']['name'] == account: 
                        account_uuid = new_data['metadata']['uuid']
                        payload['spec']['resources']\
                            ["account_reference_list"].append({\
                            "kind": "account","uuid": account_uuid})
                        print("account_details={}".format({"uuid": account_uuid}))
            else:
                print("Error : %s account not present on %s"%(account,@@{PC_IP}@@))
                exit(1)            
                                   
    payload['spec']['resources']['user_reference_list'] = []
    user_details = []
    all_users = []
    for x in range(len(params['tenant_users'])):
        all_users.append(params['tenant_users'][x].get('admin',\
                      params['tenant_users'][x].get('operator',\
                      params['tenant_users'][x].get('developer',\
                      params['tenant_users'][x].get('consumer')))))
    for _user in all_users:
        for user in _user:
            user_uuid = create_user(user, **params)
            if user_uuid != "None":
                url = _build_url(scheme="https",resource_type="/users/list")                        
                data = requests.post(url, json={"kind":"user", "length":9999},
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)   
                _uuid = ""
                if user in str(data.json()):
                    for new_data in data.json()['entities']:
                        if new_data['status']['name'] == user:
                            _uuid = new_data['metadata']['uuid']
                            payload['spec']['resources']\
                                ['user_reference_list'].append({\
                                "kind": "user",'uuid': _uuid})
                            user_details.append({'name':user, 'uuid':_uuid})
    
    print("user_details={}".format(user_details)) 

    group_details = []
    all_groups = []
    if params.get('tenant_group', 'None') != 'None':
        payload['spec']['resources']['external_user_group_reference_list'] = []
        for x in range(len(params['tenant_group'])):
            all_groups.append(params['tenant_group'][x].get('admin',\
                      params['tenant_group'][x].get('operator',\
                      params['tenant_group'][x].get('developer',\
                      params['tenant_group'][x].get('consumer')))))
        for group in all_groups:
            for user in group:
                user_uuid = create_group(user)
                if user_uuid != "None":
                    url = _build_url(scheme="https",resource_type="/user_groups/list")                        
                    data = requests.post(url, json={"kind":"user_group", "length":9999},
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)   
                    _uuid = ""
                    if user.split("@")[0] in str(data.json()):
                        for new_data in data.json()['entities']:
                            if new_data['status']['resources']['display_name'] == user.split("@")[0]:
                                _uuid = new_data['metadata']['uuid']
                                payload['spec']['resources']\
                                    ['external_user_group_reference_list'].append({\
                                    "kind": "user_group",'uuid': _uuid})
                                group_details.append({'name':user, 'uuid':_uuid})
    
        print("group_details={}".format(group_details))
    
    url = _build_url(scheme="https",resource_type="/projects") 
    print("Final Payload for creating project")                  
    pprint(payload)
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)
    if data.ok:
        wait_for_completion(data)
    
    if 'status' not in data.json():
        print("Project %s not created successfully."%params['name'])
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
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth("admin","Nutanix.123"), 
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Got error while creating Project ---> ",responce.json())
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        if "DUPLICATE_ENTITY" not in str(data.json()):
            print("Got %s ---> "%state, data.json())
            exit(1)

def validate_params():
    params = @@{project_items}@@
    print("##### Creating a Project #####")
    for _params in params:
        build_project(**_params)                                                     

validate_params()
