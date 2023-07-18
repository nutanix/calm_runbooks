# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()

management_username = "@@{management_pc_username}@@".strip()
management_password = "@@{management_pc_password}@@".strip()

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

def create_blueprint(**params):
    url = _build_url(scheme="https", host="localhost",
                    resource_type="/idempotence_identifiers")
    data = requests.post(url, json={"count": 39,"valid_duration_in_minutes": 527040},
                        auth=HTTPBasicAuth(management_username, management_password),
                        timeout=None, verify=False)
    uuid = []
    if data.ok:
        uuid = data.json()['uuid_list']
        #print("bp_spec_uuid={}".format(uuid))
    else:
        print("Error :- Failed to generate UUID's for app_protection_rule")
        exit(1)
        
    connection_type = "POWERSHELL"
    connection_port = 5985
    connection_protocol = "http"
    if "@@{vm_os}@@" == "Linux":
        connection_type = "SSH"
        connection_port = 22
        connection_protocol = ""
        
    ip_list = []
    if "@@{custom_ip_for_vm}@@".strip().lower() not in ["", "na", "none"]:
        ip_list = [{"ip": "@@{custom_ip_for_vm}@@".strip()}]

    payload = {
    "api_version": "3.0",
    "metadata": {
        "kind": "blueprint",
        "categories": {
            "TemplateType": "Vm"
        },
        "project_reference": {
            "kind": "project",
            "uuid": params["project_uuid"]
        }
    },
    "spec": {
        "resources": {
            "client_attrs": {},
            "type": "USER",
            "app_profile_list": [
                {
                    "name": "Default",
                    "action_list": [
                        {
                            "description": "",
                            "name": "Snapshot_@@{app_name}@@",
                            "critical": False,
                            "runbook": {
                                "task_definition_list": [
                                    {
                                        "timeout_secs": "",
                                        "variable_list": [],
                                        "attrs": {
                                            "edges": []
                                        },
                                        "retries": "",
                                        "name": "Default_Snapshot_Config_@@{app_name}@@_Dag",
                                        "child_tasks_local_reference_list": [
                                            {
                                                "kind": "app_task",
                                                "name": "Snapshot_Config_@@{app_name}@@_Task",
                                                "uuid": uuid[0]
                                            }
                                        ],
                                        "type": "DAG",
                                        "description": "",
                                        "uuid": uuid[1]
                                    },
                                    {
                                        "timeout_secs": "",
                                        "variable_list": [],
                                        "attrs": {
                                            "config_spec_reference": {
                                                "kind": "app_config_spec",
                                                "name": "Snapshot_Config_@@{app_name}@@",
                                                "uuid": uuid[2]
                                            }
                                        },
                                        "retries": "",
                                        "name": "Snapshot_Config_@@{app_name}@@",
                                        "target_any_local_reference": {
                                            "kind": "app_blueprint_deployment",
                                            "uuid": uuid[3]
                                        },
                                        "child_tasks_local_reference_list": [],
                                        "type": "CALL_CONFIG",
                                        "description": "",
                                        "uuid": uuid[0]
                                    }
                                ],
                                "description": "",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "name": "Default_Snapshot_Config_@@{app_name}@@_Dag",
                                    "uuid": uuid[1]
                                },
                                "name": "Default_Snapshot_Config_@@{app_name}@@_Runbook",
                                "uuid": uuid[4]
                            },
                            "type": "user",
                            "uuid": uuid[5]
                        },
                        {
                            "description": "",
                            "name": "Restore_@@{app_name}@@",
                            "critical": False,
                            "runbook": {
                                "task_definition_list": [
                                    {
                                        "timeout_secs": "",
                                        "variable_list": [],
                                        "attrs": {
                                            "edges": []
                                        },
                                        "retries": "",
                                        "name": "Default_Restore_Config_@@{app_name}@@_Dag",
                                        "child_tasks_local_reference_list": [
                                            {
                                                "kind": "app_task",
                                                "name": "Restore_Config_@@{app_name}@@_Task",
                                                "uuid": uuid[6]
                                            }
                                        ],
                                        "type": "DAG",
                                        "description": "",
                                        "uuid": uuid[7]
                                    },
                                    {
                                        "timeout_secs": "",
                                        "variable_list": [],
                                        "attrs": {
                                            "config_spec_reference": {
                                                "kind": "app_config_spec",
                                                "name": "Restore_Config_@@{app_name}@@",
                                                "uuid": uuid[8]
                                            }
                                        },
                                        "retries": "",
                                        "name": "Restore_Config_@@{app_name}@@_Task",
                                        "target_any_local_reference": {
                                            "kind": "app_blueprint_deployment",
                                            "uuid": uuid[3]
                                        },
                                        "child_tasks_local_reference_list": [],
                                        "type": "CALL_CONFIG",
                                        "description": "",
                                        "uuid": uuid[6]
                                    }
                                ],
                                "description": "",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "name": "Default_Restore_Config_@@{app_name}@@_Dag",
                                    "uuid": uuid[7]
                                },
                                "name": "Default_Restore_Config_@@{app_name}@@_Runbook",
                                "uuid": uuid[9]
                            },
                            "type": "user",
                            "uuid": uuid[10]
                        }
                    ],
                    "variable_list": [],
                    "deployment_create_list": [
                        {
                            "variable_list": [],
                            "action_list": [],
                            "min_replicas": "1",
                            "name": "@@{calm_random}@@_deployment",
                            "max_replicas": "1",
                            "substrate_local_reference": {
                                "kind": "app_substrate",
                                "uuid": uuid[11]
                            },
                            "default_replicas": "1",
                            "type": "GREENFIELD",
                            "package_local_reference_list": [
                                {
                                    "kind": "app_package",
                                    "uuid": uuid[12]
                                }
                            ],
                            "uuid": uuid[3]
                        }
                    ],
                    "environment_reference_list": [
                        params["environment"]
                    ],
                    "snapshot_config_list": [
                        {
                            "description": "",
                            "attrs_list": [
                                {
                                    "target_any_local_reference": {
                                        "kind": "app_blueprint_deployment",
                                        "uuid": uuid[3]
                                    },
                                    "snapshot_location_type": "LOCAL",
                                    "num_of_replicas": "ONE"
                                }
                            ],
                            "type": "AHV_SNAPSHOT",
                            "variable_list": [
                                {
                                    "attrs": {},
                                    "is_mandatory": True,
                                    "name": "snapshot_name",
                                    "editables": {
                                        "value": True
                                    },
                                    "data_type": "BASE",
                                    "value": "snapshot-@@{calm_array_index}@@-@@{calm_time}@@",
                                    "label": "",
                                    "val_type": "STRING",
                                    "type": "LOCAL",
                                    "description": "",
                                    "is_hidden": False,
                                    "uuid": uuid[13]
                                },
                                {
                                    "attrs": {},
                                    "is_mandatory": True,
                                    "name": "snapshot_type",
                                    "editables": {
                                        "value": True
                                    },
                                    "data_type": "BASE",
                                    "value": "CRASH_CONSISTENT",
                                    "label": "",
                                    "val_type": "STRING",
                                    "type": "LOCAL",
                                    "description": "",
                                    "is_hidden": False,
                                    "uuid": uuid[14]
                                }
                            ],
                            "name": "Snapshot_Config_@@{app_name}@@",
                            "config_reference_list": [
                                {
                                    "kind": "app_config_spec",
                                    "uuid": uuid[8]
                                }
                            ],
                            "uuid": uuid[2]
                        }
                    ],
                    "restore_config_list": [
                        {
                            "description": "",
                            "attrs_list": [
                                {
                                    "target_any_local_reference": {
                                        "kind": "app_blueprint_deployment",
                                        "uuid": uuid[3]
                                    },
                                    "delete_vm_post_restore": True,
                                    "snapshot_location_type": "LOCAL"
                                }
                            ],
                            "type": "AHV_RESTORE",
                            "variable_list": [
                                {
                                    "attrs": {},
                                    "is_mandatory": True,
                                    "name": "snapshot_uuids",
                                    "editables": {
                                        "value": True
                                    },
                                    "data_type": "BASE",
                                    "value": "",
                                    "label": "",
                                    "val_type": "STRING",
                                    "type": "LOCAL",
                                    "description": "",
                                    "is_hidden": False,
                                    "uuid": uuid[16]
                                }
                            ],
                            "name": "Restore_Config_@@{app_name}@@",
                            "uuid": uuid[8]
                        }
                    ],
                    "uuid": uuid[17]
                }
            ],
            "substrate_definition_list": [
                {
                    "variable_list": [],
                    "action_list": [],
                    "name": "VM1",
                    "editables": {},
                    "os_type": "@@{vm_os}@@",
                    "type": "AHV_VM",
                    "readiness_probe": {
                        "connection_type": connection_type,
                        "retries": "5",
                        "connection_protocol": connection_protocol,
                        "disable_readiness_probe": True,
                        "address": "",
                        "delay_secs": "5",
                        "connection_port": connection_port,
                        "login_credential_local_reference": {
                            "kind": "app_credential",
                            "uuid": uuid[18]
                        }
                    },
                    "description": "",
                    "create_spec": {
                        "name": params["vm_name"],
                        "categories": @@{tenant_category}@@,
                        "availability_zone_reference": None,
                        "backup_policy": None,
                        "type": "",
                        "cluster_reference": {
                            "kind": "cluster",
                            "uuid": params["cluster_uuid"]
                        },
                        "resources": {
                            "disk_list": [
                                {
                                    "data_source_reference": {
                                        "kind": "image",
                                        "name": "@@{image_name}@@".strip(),
                                        "uuid": params["image_uuid"]
                                    },
                                    "type": "",
                                    "disk_size_mib": 0,
                                    "volume_group_reference": None,
                                    "device_properties": {
                                        "type": "",
                                        "device_type": "DISK",
                                        "disk_address": {
                                            "adapter_type": "SCSI",
                                            "device_index": 0,
                                            "type": ""
                                        }
                                    }
                                }
                            ],
                            "hardware_clock_timezone": "",
                            "memory_size_mib": @@{vm_memory}@@ * 1024,
                            "num_sockets": @@{vm_vcpus}@@,
                            "num_vcpus_per_socket": 1,
                            "account_uuid": params["account_uuid"],
                            "boot_config": {
                                "boot_device": {
                                    "type": "",
                                    "disk_address": {
                                        "adapter_type": "SCSI",
                                        "device_index": 0,
                                        "type": ""
                                    }
                                },
                                "type": "",
                                "boot_type": "LEGACY",
                                "mac_address": ""
                            },
                            "gpu_list": [],
                            "serial_port_list": [
                                {
                                    "index": 0,
                                    "type": "",
                                    "is_connected": True
                                }
                            ],
                            "guest_tools": None,
                            "nic_list": [
                                {
                                    "nic_type": "NORMAL_NIC",
                                    "vpc_reference": None,
                                    "ip_endpoint_list": ip_list,
                                    "network_function_chain_reference": None,
                                    "network_function_nic_type": "INGRESS",
                                    "mac_address": "",
                                    "subnet_reference": {
                                        "kind": "subnet",
                                        "uuid": params["subnet_uuid"]
                                    },
                                    "type": ""
                                }
                            ],
                            "parent_reference": None,
                            "power_state": "ON",
                            "type": ""
                        }
                    },
                    "uuid": uuid[11]
                }
            ],
            "package_definition_list": [
                {
                    "type": "DEB",
                    "variable_list": [],
                    "options": {
                        "install_runbook": {
                            "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                            "variable_list": [],
                            "main_task_local_reference": {
                                "kind": "app_task",
                                "uuid": uuid[19]
                            },
                            "task_definition_list": [
                                {
                                    "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                    "target_any_local_reference": {
                                        "kind": "app_package",
                                        "uuid": uuid[12]
                                    },
                                    "variable_list": [],
                                    "child_tasks_local_reference_list": [],
                                    "type": "DAG",
                                    "attrs": {
                                        "edges": []
                                    },
                                    "uuid": uuid[19]
                                }
                            ],
                            "uuid": uuid[20]
                        },
                        "uninstall_runbook": {
                            "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                            "variable_list": [],
                            "main_task_local_reference": {
                                "kind": "app_task",
                                "uuid": uuid[21]
                            },
                            "task_definition_list": [
                                {
                                    "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                    "target_any_local_reference": {
                                        "kind": "app_package",
                                        "uuid": uuid[12]
                                    },
                                    "variable_list": [],
                                    "child_tasks_local_reference_list": [],
                                    "type": "DAG",
                                    "attrs": {
                                        "edges": []
                                    },
                                    "uuid": uuid[21]
                                }
                            ],
                            "uuid": uuid[22]
                        }
                    },
                    "service_local_reference_list": [
                        {
                            "kind": "app_service",
                            "uuid": uuid[23]
                        }
                    ],
                    "name": "Package1",
                    "uuid": uuid[12]
                }
            ],
            "service_definition_list": [
                {
                    "name": "Service1",
                    "depends_on_list": [],
                    "variable_list": [],
                    "port_list": [],
                    "action_list": [
                        {
                            "name": "action_create",
                            "runbook": {
                                "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "uuid": uuid[24]
                                },
                                "task_definition_list": [
                                    {
                                        "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                        "target_any_local_reference": {
                                            "kind": "app_service",
                                            "uuid": uuid[23]
                                        },
                                        "variable_list": [],
                                        "child_tasks_local_reference_list": [],
                                        "type": "DAG",
                                        "attrs": {
                                            "edges": []
                                        },
                                        "uuid": uuid[24]
                                    }
                                ],
                                "uuid": uuid[25]
                            },
                            "type": "system",
                            "uuid": uuid[26]
                        },
                        {
                            "name": "action_delete",
                            "runbook": {
                                "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "uuid": uuid[27]
                                },
                                "task_definition_list": [
                                    {
                                        "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                        "target_any_local_reference": {
                                            "kind": "app_service",
                                            "uuid": uuid[23]
                                        },
                                        "variable_list": [],
                                        "child_tasks_local_reference_list": [],
                                        "type": "DAG",
                                        "attrs": {
                                            "edges": []
                                        },
                                        "uuid": uuid[27]
                                    }
                                ],
                                "uuid": uuid[28]
                            },
                            "type": "system",
                            "uuid": uuid[29]
                        },
                        {
                            "name": "action_start",
                            "runbook": {
                                "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "uuid": uuid[30]
                                },
                                "task_definition_list": [
                                    {
                                        "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                        "target_any_local_reference": {
                                            "kind": "app_service",
                                            "uuid": uuid[23]
                                        },
                                        "variable_list": [],
                                        "child_tasks_local_reference_list": [],
                                        "type": "DAG",
                                        "attrs": {
                                            "edges": []
                                        },
                                        "uuid": uuid[30]
                                    }
                                ],
                                "uuid": uuid[31]
                            },
                            "type": "system",
                            "uuid": uuid[32]
                        },
                        {
                            "name": "action_stop",
                            "runbook": {
                                "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "uuid": uuid[33]
                                },
                                "task_definition_list": [
                                    {
                                        "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                        "target_any_local_reference": {
                                            "kind": "app_service",
                                            "uuid": uuid[23]
                                        },
                                        "variable_list": [],
                                        "child_tasks_local_reference_list": [],
                                        "type": "DAG",
                                        "attrs": {
                                            "edges": []
                                        },
                                        "uuid": uuid[33]
                                    }
                                ],
                                "uuid": uuid[34]
                            },
                            "type": "system",
                            "uuid": uuid[35]
                        },
                        {
                            "name": "action_restart",
                            "runbook": {
                                "name": "@@{calm_random}@@_@@{calm_random}@@_runbook",
                                "variable_list": [],
                                "main_task_local_reference": {
                                    "kind": "app_task",
                                    "uuid": uuid[36]
                                },
                                "task_definition_list": [
                                    {
                                        "name": "@@{calm_random}@@_@@{calm_random}@@_dag",
                                        "target_any_local_reference": {
                                            "kind": "app_service",
                                            "uuid": uuid[23]
                                        },
                                        "variable_list": [],
                                        "child_tasks_local_reference_list": [],
                                        "type": "DAG",
                                        "attrs": {
                                            "edges": []
                                        },
                                        "uuid": uuid[36]
                                    }
                                ],
                                "uuid": uuid[37]
                            },
                            "type": "system",
                            "uuid": uuid[38]
                        }
                    ],
                    "uuid": uuid[23]
                }
            ],
            "credential_definition_list": [
                {
                    "name": "Creds_@@{app_name}@@".strip(),
                    "type": "PASSWORD",
                    "cred_class": "static",
                    "username": "@@{credential_user}@@".strip(),
                    "secret": {
                        "attrs": {
                            "is_secret_modified": True
                        },
                        "value": "@@{credential_password}@@".strip()
                    },
                    "uuid": uuid[18]
                }
            ],
            "default_credential_local_reference": {
                "kind": "app_credential",
                "uuid": uuid[18],
                "name": "Creds_@@{app_name}@@".strip()
            }
        },
        "name": params["blueprint_name"]
    }}

    url = _build_url(scheme="https", host="localhost",
                     resource_type="/blueprints")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(management_username, management_password),
                         timeout=None, verify=False)
    wait_for_completion(data)
    print("bp_uuid={}".format(data.json()['metadata']['uuid']))
    
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https", host="localhost",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(management_username, 
                                                            management_password),
                                    verify=False)                      
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
    "vm_name":"VM_@@{app_name}@@".strip(),
    "image_uuid":"@@{image_uuid}@@".strip(),
    "blueprint_name":"@@{blueprint_name}@@".strip()
}

create_blueprint(**params)
