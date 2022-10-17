import requests
from requests.auth import HTTPBasicAuth

PC_IP = "localhost"
pc_username ="@@{management_pc_username}@@".strip()
pc_password = "@@{management_pc_password}@@".strip()

def _build_url(scheme, resource_type, host="localhost", **params):
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
    return ({
            "api_version": "3.1.0",
            "metadata": {
                "kind": "directory_service"
                },
            "spec": {
                "name": "",
                "resources": {
                    "url": "",
                    "domain_name": "",
                    "directory_type": "",
                    "service_account": {
                        "username": "string",
                        "password": "string"
                        }
                    }
                }
            })

def _get_spec_acp():
    return ({
            "api_version": "3.1.0",
            "metadata": {
            "kind" : "access_control_policy"
                    },
            "spec": {
                "name": "string",
                "role_reference": {"uuid": ""}
                }
            })
            
def create_AD(**params):
    payload = _get_default_spec()
    payload['spec']['name'] = params['name']
    payload['spec']['resources']['url'] = params['directory_url']
    payload['spec']['resources']['domain_name'] = params['domain_name']
    payload['spec']['resources']['directory_type'] = params['directory_type']
    payload['spec']['resources']['service_account']['username'] = \
                                    params['service_account_username']
    if params.get('group_search_type', 'None') != 'None':
        payload['spec']['resources']['groupSearchType'] = \
                             params.get('group_search_type', 'NON_RECURSIVE')
    payload['spec']['resources']['service_account']['password'] = \
                                    params['service_account_password']
    url = _build_url(scheme="https",
                    resource_type="/directory_services")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    if 'DUPLICATE_ENTITY' in str(data.json()):
        url = _build_url(scheme="https",
                         resource_type="/directory_services/list")
        data = requests.post(url, json={"kind":"directory_service"},
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
        for x in data.json()['entities']:
            if x['status']['resources']['domain_name'] == params['domain_name']:
                print("ad_details={}".format({"ad_uuid":x['metadata']['uuid']}))
    else:
        task_uuid = wait_for_completion(data, params['name'])
        print("ad_details={}".format({"ad_uuid": data.json()['metadata']['uuid'],
                                  "ad_creation_task_uuid": task_uuid,
                                  "name":params['name']}))

def wait_for_completion(data, name):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
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
                _url = _build_url(scheme="https",resource_type="/directory_services/list")
                _data = requests.post(_url, json={"kind":"directory_service"},
                                        auth=HTTPBasicAuth(pc_username, pc_password),
                                        timeout=None, verify=False)
                if name in str(_data.json()):
                    state = "COMPLETE"
                else:
                    state = 'PENDING'
                    sleep(5) 
    else:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    return data.json()['status']['execution_context']['task_uuid']


params = @@{AD_items}@@
print("##### Configuring Active Directory #####")
create_AD(**params)                                                      
