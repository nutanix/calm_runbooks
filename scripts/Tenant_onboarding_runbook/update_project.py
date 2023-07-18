# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "localhost"
pc_username = "@@{management_pc_username}@@".strip()
pc_password = "@@{management_pc_password}@@".strip()

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
        
def update_project(**params):
    project = @@{project_details}@@
    project_items = @@{project_items}@@
    payload = _get_spec(project['uuid'])
    for x in ['categories', 'categories_mapping', 'creation_time', 'last_update_time', 'owner_reference']:
        del payload['metadata'][x]
    del payload['status']
    payload['spec']['access_control_policy_list'][0]['operation'] = "UPDATE"
    
    environment_details = @@{environment_details}@@
    payload['spec']['project_detail']['resources']['environment_reference_list'] = []
    if "@@{create_environment}@@".lower() == "yes":
        payload['spec']['project_detail']['resources']\
                ['environment_reference_list'].append({"kind":"environment",
                                                   "uuid":environment_details['uuid']})
        payload['spec']['project_detail']['resources']\
            ["default_environment_reference"] = {"kind":"environment",
                                      "uuid":environment_details['uuid']}
    
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

params = @@{project_items}@@
update_project(**params)
