# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_user = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
source_az_uuid = "@@{source_az_uuid}@@".strip()
dest_az_uuid = "@@{dest_az_uuid}@@".strip()
protection_policy = @@{protection_policy_items}@@

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

def _get_stage_spec(vm_category):
    url = _build_url(scheme="https",
                    resource_type="/idempotence_identifiers")
    data = requests.post(url, json={"count": 1,"valid_duration_in_minutes": 527040},
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)                   
    _uuid = ""
    if data.ok:
        _uuid = data.json()['uuid_list'][0]
    else:
        print("Failed to generate idemotence uuid, Please try again ...")
        exit(1)
        
    return ({
            "stage_work": {
                "recover_entities": {
                    "entity_info_list": [
                        {
                            "categories": vm_category,
                            "script_list": [{
                              "enable_script_exec": @@{enable_boot_script}@@
                            }]
                        }
                    ]
                }
            },
            "stage_uuid": _uuid,
            "delay_time_secs": @@{stage_delay}@@
        })
  
def get_spec(**params):
    stage_list = []
    for vm_category in params['power_on_sequence'].keys():
        _category = {vm_category:params['power_on_sequence'][vm_category]}
        stage_list.append(_get_stage_spec(_category))
    recovery_network = False
    if "@@{recovery_network_type}@@" == "stretched":
        recovery_network = True
    return (
    {"spec": {
        "name": params['name'],
        "resources": {
            "stage_list": stage_list,
            "parameters": {
                "primary_location_index": 0,
                "availability_zone_list": [
                    {
                        "availability_zone_url": source_az_uuid,
                        "cluster_reference_list": []
                    },
                    {
                        "availability_zone_url": dest_az_uuid,
                        "cluster_reference_list": []
                    }
                ],
                "network_mapping_list": [
                    {
                        "are_networks_stretched": recovery_network,
                        "availability_zone_network_mapping_list": [
                            {
                                "recovery_network": {
                                    "name": params['recovery_network_prod']['name']
                                },
                                "availability_zone_url": source_az_uuid,
                                "test_network": {
                                    "name": params['recovery_network_test']['name']
                                }
                            },
                            {
                                "recovery_network": {
                                    "name": params['dr_network_prod']['name']
                                },
                                "availability_zone_url": dest_az_uuid,
                                "test_network": {
                                    "name": params['dr_network_test']['name']
                                }
                            }
                        ]
                    }
                ],
                "floating_ip_assignment_list": []
            }
        },
        "description": params.get('description', '')
    },
    "metadata": {
        "kind": "recovery_plan",
        "spec_version": 0
    },
    "api_version": "3.1.0"
    })

def get_static_map_spec(IP, vm):
    return ({
      "vm_reference": {
          "kind": "vm",
          "name": vm,
          "uuid": get_vm_uuid(vm)
          },
      "ip_config_list": [{
          "ip_address": IP.strip()
          }
       ]})
  
def subnet_list_spec(network, **params):
    return [{
             "external_connectivity_state": "DISABLED",
              "gateway_ip": params[network]['gateway'],
              "prefix_length": int(params[network]['prifix'])
             }]
  
def create_recovery_plan(**params):
    payload = get_spec(**params)
    recovery_prod = []
    recovery_dr = []
    test_prod = []
    test_dr = []
    if @@{static_ip_mapping}@@:
        for x,_vm in enumerate(params["vm_name"].split(",")):
            recovery_prod.append(get_static_map_spec("@@{primary_network_prod_static_ip}@@".strip().split(",")[x], _vm.strip()))
            recovery_dr.append(get_static_map_spec("@@{dr_network_prod_static_ip}@@".strip().split(",")[x], _vm.strip()))
            test_prod.append(get_static_map_spec("@@{primary_network_test_static_ip}@@".strip().split(",")[x], _vm.strip()))
            test_dr.append(get_static_map_spec("@@{dr_network_test_static_ip}@@".strip().split(",")[x], _vm.strip()))
            
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
               ["availability_zone_network_mapping_list"][0]\
               ["recovery_ip_assignment_list"] = recovery_prod
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
               ["availability_zone_network_mapping_list"][0]\
               ["test_ip_assignment_list"] = test_prod
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
               ["availability_zone_network_mapping_list"][1]\
               ["recovery_ip_assignment_list"] = recovery_dr
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
               ["availability_zone_network_mapping_list"][1]\
               ["test_ip_assignment_list"] = test_dr
        
    if params["recovery_network_prod"]["gateway"] != "NA":
        _spec = subnet_list_spec(network="recovery_network_prod", **params)
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
            ["availability_zone_network_mapping_list"][0]["recovery_network"]\
            ["subnet_list"] = _spec
        
    if params["recovery_network_test"]["gateway"] != "NA":
        _spec = subnet_list_spec(network="recovery_network_test", **params)
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
            ["availability_zone_network_mapping_list"][0]["test_network"]\
            ["subnet_list"] = _spec
        
    if params["dr_network_prod"]["gateway"] != "NA":
        _spec = subnet_list_spec(network="dr_network_prod", **params)
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
            ["availability_zone_network_mapping_list"][1]["recovery_network"]\
            ["subnet_list"] = _spec
        
    if params["dr_network_test"]["gateway"] != "NA":
        _spec = subnet_list_spec(network="dr_network_test", **params)
        payload["spec"]["resources"]["parameters"]["network_mapping_list"][0]\
            ["availability_zone_network_mapping_list"][1]["test_network"]\
            ["subnet_list"] = _spec
        
    url = _build_url(scheme="https",resource_type="/recovery_plans")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    wait_for_completion(data)
    print("SUCCESS !!!")

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
                print("Error while creating Recovery plan ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        print("Error while creating recovery plan ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

def get_vm_uuid(vm):
    url = _build_url(scheme="https",
                    resource_type="/ngt/list")
    data = requests.post(url, json={"kind":"ngt"},
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if data.ok:
        for _vm in data.json()["entities"]:
            uuid = _vm["vm_uuid"]
            _url = _build_url(scheme="https",
                             resource_type="/vms/%s"%uuid)
            _data = requests.get(_url,auth=HTTPBasicAuth(pc_user,pc_password),
                                 timeout=None, verify=False)
            if _data.ok:
                if _data.json()["spec"]["name"] == vm:
                    if _vm["network_configuration"][0]["ip_info_list"][0]["ip_type"] == "STATIC": 
                        return _data.json()["metadata"]["uuid"]
                    else:
                        print("%s VM has not static IP configured. VM Should"\
                            " have Static IP configured for Static IP Mapping."%vm)
                        exit(1)
        print("Input Error :- %s VM is not present or NGT is not installed properly on VM."%vm)
        exit(1)
    else:
        print("Error while fetching VM details :- ",data.json())
        exit(1)
        
params_dict = @@{recovery_plan_items}@@
params_dict["vm_name"] = "@@{vm_name}@@".strip()
create_recovery_plan(**params_dict)
