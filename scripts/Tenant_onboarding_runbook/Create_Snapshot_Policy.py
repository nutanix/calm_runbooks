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

def get_policy_spec(**params):
    url = _build_url(scheme="https",
                    resource_type="/idempotence_identifiers")
    data = requests.post(url, json={"count": 1,"valid_duration_in_minutes": 527040},
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)                   
    _uuid = ""
    if data.ok:
        _uuid = data.json()['uuid_list'][0]
    else:
        print("Error :- Failed to generate UUID for app_protection_rule")
        exit(1)
    return (
    {
    "api_version": "3.0",
    "metadata": {
        "kind": "app_protection_policy",
        "project_reference": {
            "kind": "project",
            "uuid": params['project_uuid']
        }
    },
    "spec": {
        "name": "Snapshot_Policy_@@{tenant_name}@@",
        "description": "",
        "resources": {
            "is_default": True,
            "ordered_availability_site_list": [
                {
                    "environment_reference": {
                        "kind": "environment",
                        "uuid": params['environment']
                    },
                    "infra_inclusion_list": {
                        "type": "nutanix_pc",
                        "account_reference": {
                            "kind": "account",
                            "uuid": params['account_uuid']
                        },
                        "cluster_references": [
                            {
                                "kind": "cluster",
                                "uuid": params['cluster_uuid']
                            }
                        ]
                    }
                }
            ],
            "app_protection_rule_list": [
                {
                    "name": "Protection_rule_@@{tenant_name}@@",
                    "enabled": True,
                    "local_snapshot_retention_policy": {
                        "snapshot_expiry_policy": {
                            "multiple": 0
                        }
                    },
                    "first_availability_site_index": 0,
                    "second_availability_site_index": 0,
                    "uuid": _uuid
                }
            ]
        }
    }
    })

def protection_policy(**params):
    payload = get_policy_spec(**params)
    url = "https://%s:9440/api/calm/v3.0/app_protection_policies"%PC_IP
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username,pc_password),
                        timeout=None, verify=False)
    #print("protection_policy_uuid={}".format(data.json()["metadata"]["uuid"]))
    #print("protection_rule_uuid={}".format(data.json()["spec"]\
    #                    ["resources"]["app_protection_rule_list"][0]["uuid"]))
    wait_for_completion(data)
    
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
                print("Failed to create Snapshot Policy ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        print("Failed to create Snapshot Policy ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
        
params = {}
project = @@{project_details}@@
environment = @@{environment_details}@@
account = @@{account_details}@@

params['project_uuid'] = project['uuid']
params['environment'] = environment.get('uuid', None)
params['account_uuid'] = account['uuid']
params['cluster_uuid'] = "@@{cluster_uuid}@@"

if environment:
    protection_policy(**params)
    print("Snapshot Policy Created Successfully.")
else:
    print("Add environments to start creating snapshot policies.")
