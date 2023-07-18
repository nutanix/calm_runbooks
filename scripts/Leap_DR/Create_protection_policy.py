# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_user = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()

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

def get_spec(**params):
    rpo_time_replication = int(@@{custom_rpo_interval_replication}@@) * 60 * 60
    if @@{custom_rpo_interval_replication}@@ <= 1:
        rpo_time_replication = 3600
        
    category_filter = {}
    for x in params["vm_category"]:
        category_filter[x] = params["vm_category"][x]
    return (
    {"spec": {
        "name": params['name'],
        "resources": {
            "ordered_availability_zone_list": [
                {
                    "availability_zone_url": params["source_az_uuid"],
                    "cluster_uuid": "@@{primary_cluster_uuid}@@".strip()
                },
                {
                    "availability_zone_url": params["dest_az_uuid"],
                    "cluster_uuid": "@@{recovery_cluster_uuid}@@".strip()
                }
            ],
            "availability_zone_connectivity_list": [
                {
                    "source_availability_zone_index": 0,
                    "destination_availability_zone_index": 1,
                    "snapshot_schedule_list": [
                        {
                            "recovery_point_objective_secs": rpo_time_replication,
                            "snapshot_type": params.get("snapshot_type","CRASH_CONSISTENT"),
                            "local_snapshot_retention_policy": {
                                "num_snapshots": int(@@{number_of_snapshot_retention}@@)
                            },
                            "remote_snapshot_retention_policy": {
                                "num_snapshots": int(@@{number_of_snapshot_retention}@@)
                            }
                        }
                    ]
                },
                {
                    "source_availability_zone_index": 1,
                    "destination_availability_zone_index": 0,
                    "snapshot_schedule_list": [
                        {
                            "recovery_point_objective_secs": rpo_time_replication,
                            "snapshot_type": params.get("snapshot_type","CRASH_CONSISTENT"),
                            "local_snapshot_retention_policy": {
                                "num_snapshots": int(@@{number_of_snapshot_retention}@@)
                            },
                            "remote_snapshot_retention_policy": {
                                "num_snapshots": int(@@{number_of_snapshot_retention}@@)
                            }
                        }
                    ]
                }
            ],
            "category_filter": {"params":category_filter},
            "primary_location_list": [
                0
            ]
        }
    },
    "metadata": {
        "kind": "protection_rule"
    },
    "api_version": "3.1.0"
    })

def local_schedule(_index, **params):
    rpo_time_local = int(@@{custom_rpo_interval_local}@@) * 60 * 60
    if @@{custom_rpo_interval_local}@@ <= 1:
        rpo_time_local = 3600
    return {
                "source_availability_zone_index": _index,
                "snapshot_schedule_list": [
                    {
                        "recovery_point_objective_secs": rpo_time_local,
                        "snapshot_type": params.get("snapshot_type","CRASH_CONSISTENT"),
                        "local_snapshot_retention_policy": {
                            "num_snapshots": int(@@{number_of_snapshot_retention}@@)
                        }
                    }
                ]
            }
            
def create_protection_policy(**params):
    params['source_az_uuid'] = get_account_info("Local AZ")
    params['dest_az_uuid'] = "@@{dest_az_uuid}@@".strip()
    
    print("source_az_uuid={}".format(params['source_az_uuid']))
    payload = get_spec(**params)
    if @@{local_schedule}@@:
        payload['spec']['resources']['availability_zone_connectivity_list'].append(local_schedule(_index=0))
        payload['spec']['resources']['availability_zone_connectivity_list'].append(local_schedule(_index=1))
    if "@@{policy_schedule_time}@@".strip() != "Immediate":
        payload['spec']['resources']['start_time'] = "@@{policy_schedule_time}@@".strip()
    url = _build_url(scheme="https",resource_type="/protection_rules")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)    
    wait_for_completion(data)
    if data.ok:
        _uuid = data.json()['metadata']['uuid']
        batch_call(_uuid)

def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_user,pc_password), 
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        print("Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

def batch_call(entity_uuid):
    payload = {
                "action_on_failure": "CONTINUE",
                "execution_order": "NON_SEQUENTIAL",
                "api_request_list": [
                    {
                        "operation": "POST",
                        "path_and_params": "/api/nutanix/v3/groups",
                        "body": {
                            "entity_type": "protection_rule",
                            "entity_ids": [entity_uuid],
                            "group_member_attributes": [
                                {
                                    "attribute": "name"
                                }
                            ],
                            "query_name": "prism:EBQueryModel"
                        }
                    }
                ],
                "api_version": "3.0"
            }
    url = _build_url(scheme="https",resource_type="/batch")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if not data.ok:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
    
def get_account_info(az_url):
    url = _build_url(scheme="https",resource_type="/groups")
    payload = {
        "entity_type": "availability_zone_physical",
        "grouping_attribute": "type",
        "group_member_count": 1,
        "group_member_attributes": [
            {
                "attribute": "name"
            },
            {
                "attribute": "url"
            }
        ],
        "query_name": "prism:BaseGroupModel"
    }
    
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
                        
    if data.ok:
        for cloud_trust in data.json()["group_results"]:
            if cloud_trust["entity_results"][0]["data"][0]["values"][0]["values"][0] == az_url:
                return cloud_trust["entity_results"][0]["data"][1]["values"][0]["values"][0]
        print("%s availability zone not present on %s"%(az_url, PC_IP))
        exit(1)
    else:
        print("Failed to retrive availability zone info of %s"%az_url)
        print("Please make sure PC url is correct and rechable.")
        print(data.json())
        exit(1)

params_dict = @@{protection_policy_items}@@
create_protection_policy(**params_dict)
