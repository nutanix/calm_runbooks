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
    
def _get_spec():
    tenantuuid = "@@{tenant_uuid}@@"
    account = @@{account_details}@@
    project = @@{project_details}@@
    vpc_details = @@{vpc_details}@@
    project_subnet = @@{overlay_subnet_details}@@
    env_memory = @@{project_memory}@@ * 1024
    subnet_references = []
    nic_list = []
    nics = {}
    nics['subnet_reference'] = {'uuid': project_subnet["uuid"]}
    subnet_references.append({'uuid': project_subnet["uuid"]})
    nic_list.append(nics)
    
    url = _build_url(scheme="https",
                    resource_type="/idempotence_identifiers")
    data = requests.post(url, json={"count": 2,"valid_duration_in_minutes": 527040},
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    creds_uuid = ""
    substrate_uuid = ""
    if data.ok:
        creds_uuid = data.json()['uuid_list'][0]
        substrate_uuid = data.json()['uuid_list'][1]

    _creds_type = "@@{credential_type}@@"
    credential_definition_list = [
                		{
                    		"name": "@@{tenant_name}@@_cred",
                    		"type": _creds_type,
                    		"username": "@@{credential_username}@@",
                    		"secret": {
                        		"attrs": {
                            		"is_secret_modified": True,
                                  	"secret_reference" : {}
                        		},
                        		"value": """@@{password_or_key}@@"""
                    		},
                    		"uuid": creds_uuid
                		}]
    
    if _creds_type == "KEY":
        _pass = {"passphrase": {
                    "attrs": {
                        "is_secret_modified": True,
                    },
                    "value": "@@{prism_central_passwd}@@"
                    }
                }
        credential_definition_list[0].update(_pass)

    gpu_list = []
    disk_list = []
    boot_type = "LEGACY"
    boot_adapter = "SCSI"
    image_uuid = ""
    boot_index = 0
    boot_adapter = "SCSI"
    url = _build_url(scheme="https",
        resource_type="/images/list")
    data = requests.post(url, json={"kind":"image", "filter":"name==%s"%"@@{image_name}@@"},
                            auth=HTTPBasicAuth("admin", "Nutanix.123"),
                            timeout=None, verify=False)
    if data.ok:
        if data.json()["metadata"]["total_matches"] == 1:
            image_uuid = data.json()['entities'][0]['metadata']['uuid']
        else:
            print("There are '%s' total images with name - @@{image_name}@@"%(\
                                     data.json()["metadata"]["total_matches"]))
            exit(1)
    else:
        print("Error -- %s Image not present on %s"%("@@{image_name}@@", PC_IP))
    disk_list.append({"data_source_reference": {
                        "kind": "image",
                        "name": "@@{image_name}@@",
                        "uuid": image_uuid
                        },
                        "device_properties": {
                        "device_type": "DISK",
                        "disk_address": {
                            "device_index": 0,
                            "adapter_type": "SCSI"
                        }},
                        "disk_size_mib": 10,
                        }
                    )

    serial_port = []
    serial_port.append({"index": 0, "is_connected": True})
        
    return ({
    		"api_version": "3.0",
    		"metadata": {
        		"kind": "environment",
        		"project_reference": {
            		"kind": "project",
            		"name": project['name'],
            		"uuid": project['uuid']
        		}
    		},
    		"spec": {
        		"name": project['name']+"_Environment",
        		"description": tenantuuid+project['name'],
        		"resources": {
            		"substrate_definition_list": [
                		{
                    		"variable_list": [],
                    		"type": "AHV_VM",
                    		"os_type": "@@{environment_os}@@",
                    		"action_list": [],
                    		"create_spec": {
                        		"name": project['name']+"_VM",
                                "categories": {},
                                "cluster_reference": {
                                    "kind": "cluster",
                                    "type": "",
                                    "name": "@@{cluster_name}@@",
                                    "uuid": "@@{cluster_uuid}@@"
                                },
                        		"resources": {
                            		"disk_list": disk_list,
                                    "gpu_list": gpu_list,
                                    "serial_port_list": serial_port,
                            		"nic_list": nic_list,
                                    "power_state": "ON",
                            		"boot_config": {
                                		"boot_device": {
                                    		"disk_address": {
                                        		"device_index": boot_index,
                                        		"adapter_type": boot_adapter
                                    		}
                                		},
                                		"boot_type": boot_type
                            		},
                            		"num_sockets": 2,
                            		"num_vcpus_per_socket": @@{project_vcpu}@@,
                            		"memory_size_mib": env_memory,
                            		"account_uuid": account['uuid'],
                                    
                        		},
                        		"categories": {"TenantName":"@@{tenant_name}@@"}
                    		},
                    		"readiness_probe": {
                        		"disable_readiness_probe": False,
                        		"connection_type": "SSH",
                        		"connection_port": 22,
                                "connection_protocol": "HTTP",
                                "delay_secs": "5",
                        		"login_credential_local_reference": {
                            		"kind": "app_credential",
                            		"uuid": creds_uuid
                        		},
                                "address": "@@{project_subnet_address}@@"
                    		},
                    		"name": "Untitled",
                            "uuid": substrate_uuid
                		}
            		],
            		"credential_definition_list": credential_definition_list,
            		"infra_inclusion_list": [
                		{
                    		"account_reference": {
                        		"uuid": account['uuid'],
                        		"kind": "account"
                    		},
                    		"type": "nutanix_pc",
                    		"subnet_references": subnet_references,
                    		"default_subnet_reference": subnet_references[0],
                            "vpc_references": [{"uuid":vpc_details["uuid"]}],
                            "cluster_references": [{"uuid":"@@{cluster_uuid}@@"}]
                		}
            		]
        		}
    		}})

def create_env():
    payload = _get_spec()
    guest_customization = {}
    if "@@{environment_os}@@" == "Windows":
        guest_customization = {"sysprep":{"install_type": 'FRESH',
                                              "unattend_xml": """@@{guest_customization_script}@@"""}}
    else:
        guest_customization = {"cloud_init":{"user_data": """@@{guest_customization_script}@@"""}}
    payload['spec']['resources']['substrate_definition_list'][0]['create_spec']\
             ['resources']['guest_customization'] = guest_customization
        
    url = _build_url(scheme="https",
                    resource_type="/environments")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    if not data.ok:
        print("Error while creating environment ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    return {"uuid": data.json()['metadata']['uuid'],
           			"name":payload['spec']['name'],
                    "default": True}
environment = ""
if "@@{create_environment}@@" == "yes":
    environment = create_env()
print("environment_details={}".format(environment))
