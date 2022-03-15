# script
import requests
from requests.auth import HTTPBasicAuth


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
    
def _get_spec(_count, **params):
    tenantuuid = @@{UID}@@
    account = @@{account_details}@@
    project = @@{project_details}@@
    env_passwd = @@{prism_central_passwd}@@
    external_subnets = @@{external_subnet_details}@@
    overlay_subnets = @@{overlay_subnet_details}@@
    environment = params
    subnet_references = []
    nic_list = []
    for subnet in environment['subnets']:
        nics = {}
        nics['subnet_reference'] = {'uuid': subnet['uuid']}
        subnet_references.append({'uuid': subnet['uuid']})
        if "static_ip" in subnet:
            try:
        	    nics["ip_endpoint_list"] = [{"ip": subnet['static_ip']}]
            except Exception as e:
                print(e)
                exit(1)
        nic_list.append(nics)
    
    url = _build_url(scheme="https",
                    resource_type="/idempotence_identifiers")
    data = requests.post(url, json={"count": 2,"valid_duration_in_minutes": 527040},
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)
    creds_uuid = ""
    substrate_uuid = ""
    if data.ok:
        creds_uuid = data.json()['uuid_list'][0]
        substrate_uuid = data.json()['uuid_list'][1]

    _creds_type = "PASSWORD"
    _value = environment['creds'].get('passwd', 'None')
    if environment['creds'].get('secret_key', 'None') != "None":
        _creds_type = ""
        _value = environment['creds']['secret_key']
    credential_definition_list = [
                		{
                    		"name": "@@{calm_random}@@_cred",
                    		"type": _creds_type,
                    		"username": environment['creds']['username'],
                    		"secret": {
                        		"attrs": {
                            		"is_secret_modified": True,
                                  	"secret_reference" : {}
                        		},
                        		"value": _value
                    		},
                    		"uuid": creds_uuid
                		}]

    guest_customization = {}
    if environment.get('guest_customization', 'no') != 'no' :
        if environment.get('os_type').lower() == 'windows' :
            guest_customization = {"sysprep":{"install_type": environment.get('install_type', 'FRESH'),
                                              "unattend_xml": """@@{guest_customization_script}@@"""}}
        else:
            guest_customization = {"cloud_init":{"user_data": """@@{guest_customization_script}@@"""}}
            
    gpu_list = []
    if environment.get("gpu_details", "None") != "None":
        device_id = -1
        for vgpu in environment['gpu_details']:
            gpu_list.append({"vendor":vgpu['vendor'],
                             "mode": vgpu.get("mode","PASSTHROUGH_GRAPHICS"),
                             "device_id": device_id+1})
                             
    disk_list = []
    boot_type = environment.get("boot_type", "LEGACY")
    device_index = 0
    boot_index = 0
    boot_adapter = "SCSI"
    for _environment in environment['disks']:
        if _environment.get('image', "None") != "None":
            image_uuid = ""
            if _environment.get('bootable', False) != False:
                boot_index = device_index
                boboot_adapterot = _environment.get("adapter_type","SCSI")
            url = _build_url(scheme="https",
                    resource_type="/images/list")
            data = requests.post(url, json={"kind":"image", "filter":"name==%s"%_environment['image']},
                                    auth=HTTPBasicAuth("admin", "Nutanix.123"),
                                    timeout=None, verify=False)
            if data.ok:
                image_uuid = data.json()['entities'][0]['metadata']['uuid']
            else:
                print("Error -- %s Image not present on %s"%(_environment['image'], @@{PC_IP}@@))
            disk_list.append({"data_source_reference": {
                        "kind": "image",
                        "name": _environment['image'],
                        "uuid": image_uuid
                        },
                        "device_properties": {
                        "device_type": _environment.get("device_type", "DISK"),
                        "disk_address": {
                            "device_index": device_index,
                            "adapter_type": _environment.get("adapter_type","SCSI")
                        }},
                        "disk_size_mib": _environment.get('disk_size_mib', 1),
                        })
        elif  _environment.get('device_type', "None") == "CDROM":
            if _environment.get('bootable', False) != False:
                boot_index = device_index
                boot_adapter = _environment.get("adapter_type","SCSI")
            disk_list.append({"data_source_reference": {},
                        "device_properties": {
                        "device_type": _environment.get("device_type", "DISK"),
                        "disk_address": {
                            "device_index": device_index,
                            "adapter_type": _environment.get("adapter_type","SCSI")
                        }},
                        "disk_size_mib": _environment.get('disk_size_mib', 1),
                        })
        else:
            if _environment.get('bootable', False) != False:
                boot_index = device_index
                boot_adapter = _environment.get("adapter_type","SCSI")
            disk_list.append({"device_properties": {
                        "device_type": _environment.get("device_type", "DISK"),
                        "disk_address": {
                            "device_index": device_index,
                            "adapter_type": _environment.get("adapter_type","SCSI")
                        }},
                        "disk_size_mib": _environment.get('disk_size_mib', 1),
                        })
        device_index += 1

    serial_port = []
    if environment.get('serial_port', 'None') != 'None':
        for port in environment['serial_port']:
            serial_port.append({"index": port['index'], "is_connected": port['is_connected']})
        
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
        		"name": tenantuuid['tenant_uuid']+"_"+project['name']+"_%s"%_count,
        		"description": tenantuuid['tenant_uuid']+project['name'],
        		"resources": {
            		"substrate_definition_list": [
                		{
                    		"variable_list": [],
                    		"type": "AHV_VM",
                    		"os_type": environment['os_type'],
                    		"action_list": [],
                    		"create_spec": {
                        		"name": "vm_"+tenantuuid['tenant_uuid'],
                                "categories": {},
                        		"resources": {
                            		"disk_list": disk_list,
                                    "gpu_list": gpu_list,
                                    "serial_port_list": serial_port,
                                    "guest_customization":guest_customization,
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
                            		"num_sockets": environment['num_sockets'],
                            		"num_vcpus_per_socket": environment['num_vcpus_per_socket'],
                            		"memory_size_mib": environment['memory_size_mb'],
                            		"account_uuid": account['uuid'],
                                    
                        		},
                        		"categories": {@@{tenant_name}@@: tenantuuid['tenant_uuid']}
                    		},
                    		"readiness_probe": {
                        		"disable_readiness_probe": False,
                        		"connection_type": environment.get("connection_type", "SSH"),
                        		"connection_port": environment.get("connection_port", 22),
                                "connection_protocol": environment.get("connection_protocol", "HTTP"),
                                "delay_secs": environment.get("delay", "1"),
                        		"login_credential_local_reference": {
                            		"kind": "app_credential",
                            		"uuid": creds_uuid
                        		},
                                "address": environment['subnets'][0].get('static_ip', "None")
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
                    		"default_subnet_reference": subnet_references[0]
                		}
            		]
        		}
    		}})

def create_env(_count, **params):
    payload = _get_spec(_count, **params)
    url = _build_url(scheme="https",
                    resource_type="/environments")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        timeout=None, verify=False)
    if not data.ok:
        print("Got error while creating environment", data.json()['message_list'])
        exit(1)
    default = True
    if params.get('default', False) == False:
        default = False
    return {"uuid": data.json()['metadata']['uuid'],
           			"name":payload['spec']['name'],
                    "default": default}
params = @@{environment_items}@@
environments = []
_count = 1
for _params in params:
    environments.append(create_env(_count, **_params))
    sleep(5)
    _count += 1
print("environment_details={}".format(environments))
