# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
workload_pc_config = {
    "username": pc_username,
    "password": pc_password,
    "ip": PC_IP
}

management_pc_username = "@@{management_pc_username}@@".strip()
management_pc_password = "@@{management_pc_password}@@".strip()
management_pc_ip = "@@{management_pc_ip}@@".strip()
management_pc_config = {
    "username": management_pc_username,
    "password": management_pc_password,
    "ip": management_pc_ip
}

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

def get_spec(app_profile_uuid,app_name,app_description):
    return ({
            "spec": {
                "app_profile_reference": {
                    "kind": "app_profile",
                    "uuid": app_profile_uuid
                },
            "app_description": app_description,
            "app_name": app_name
            }
          })

def launch_blueprint(pc_config, **params):
    url = _build_url(scheme="https",
                    resource_type="/blueprints/%s"%params['bp_uuid'],
                    host=pc_config['ip'])
    data = requests.get(url, auth=HTTPBasicAuth(pc_config['username'], pc_config['password']),verify=False)
    if data.ok:
        app_profile_uuid = data.json()["spec"]["resources"]["app_profile_list"][0]["uuid"]
    else:
        print("Error while fetching Blueprint with UUID - %s "%params['bp_uuid'])
        exit(1)
        
    payload = get_spec(app_profile_uuid,
                       app_name=params["application_name"],
                       app_description=params["application_name"])
    
    url = _build_url(scheme="https",
                    resource_type="/blueprints/%s/simple_launch"%params['bp_uuid'],
                    host=pc_config['ip'])
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_config['username'], pc_config['password']),
                        timeout=None, verify=False)
    wait_for_completion(data, pc_config)
    
def wait_for_completion(data, pc_config):
    if data.ok:
        _uuid = data.json()['status']["request_id"]
        print("Request_Id={}".format(_uuid))
        state = "PENDING"
        while state == "PENDING":
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid,
                             host=pc_config['ip'])
            responce = requests.get(url, auth=HTTPBasicAuth(pc_config['username'], pc_config['password']),
                                    verify=False)
            if not responce.ok:
                if ("message_list" in responce.json()) and ("ACCESS_DENIED" in responce.json()["message_list"][0]["reason"]):
                    print("Warning :- User don't have access to fetch backend execution details.")
                    print("User will need to check App details Manually.")
                    print(responce.json()["message_list"])
                    exit(0)
                else:
                    print("Error :-- ",responce.json())
                    exit(1)
                    
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error occured ---> ",data.json().get('message_list', 
                                        data.json().get('error_detail', data.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        print("Error occured ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

params = {
    "project_uuid" : "@@{project_uuid}@@",
    "environment": "@@{environment_uuid}@@",
    "account_uuid":"@@{account_uuid}@@",  # NTNX_LOCAL_AZ
    "cluster_uuid":"@@{cluster_uuid}@@",
    "subnet_uuid": "@@{subnet_uuid}@@",
    "vm_name":"VM_@@{app_name}@@",
    "image_uuid":"@@{image_uuid}@@",
    "blueprint_name":"@@{blueprint_name}@@",
    #"protection_policy_uuid":"@@{protection_policy_uuid}@@",
    #"protection_rule_uuid":"@@{protection_rule_uuid}@@",
    "bp_uuid":"@@{bp_uuid}@@",
    "application_name":"@@{app_name}@@"
}
#launch_blueprint(management_pc_config, **params)