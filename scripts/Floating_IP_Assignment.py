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

def _get_default_spec(external_subnet_uuid, **params):
    return ({
              "spec": {
                "description": params.get('description', "Floating IP for @@{vm_ip}@@"),
                "resources": {
                  "external_subnet_reference": {
                    "kind": "subnet",
                    "uuid": external_subnet_uuid
                  }
                }
              },
              "api_version": "3.1.0",
              "metadata": {
                "kind": "floating_ip"
                  }
            })

def get_subnet_uuid(subnet):
    url = _build_url(scheme="https",resource_type="/subnets/list")
    data = requests.post(url, json={"kind":"subnet", "filter":"name==%s"%subnet},
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(subnet, PC_IP))
            exit(1)
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one subnets with name - %s on - %s"%(subnet, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            return data.json()['entities'][0]['metadata']['uuid']
    else:
        print("Error while fetching subnet details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
        
def get_vpc_uuid(vpc):
    url = _build_url(scheme="https",resource_type="/vpcs/list")
    data = requests.post(url, json={"kind":"vpc", "filter":"name==%s"%vpc},
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(vpc, PC_IP))
            exit(1)
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one VPCs with name - %s on - %s"%(vpc, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            return data.json()['entities'][0]['metadata']['uuid']
    else:
        print("Error while fetching VPC details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
        
def get_nic_uuid(vm_name):
    url = _build_url(scheme="https", resource_type="/vms/list")
    data = requests.post(url, json={"kind":"vm"},
                        auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    if data.ok:
        if vm_name in str(data.json()):
            for _vm in data.json()["entities"]:
              if _vm["spec"]["name"] == vm_name:
                  vm_uuid = _vm["metadata"]["uuid"]
        else:
            print("%s VM not present on %s"%(vm_name, PC_IP))
            print("Please check provided VM details.")
            exit(1)
    else:
        print("Error while fetching VM details.",data.json())
        exit(1)
        
    payload = {"entity_type":"virtual_nic",
               "group_member_attributes":[{"attribute":"assigned_ipv4_addresses"}],
               "group_member_count":50,
               "group_member_offset":0,
               "filter_criteria":"vm==%s"%vm_uuid}
    
    url = _build_url(scheme="https",
                    resource_type="/groups")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    
    if data.ok:
        return data.json()["group_results"][0]["entity_results"][0]["entity_id"]
    else:
        print("Error while fetching NIC uuid.",data.json())
        exit(1)
        
def generate_floating_ip(**params):
    external_subnet_uuid = get_subnet_uuid(params["external_subnet"])
    print("======================================")     
    payload = _get_default_spec(external_subnet_uuid, **params)
    
    if "IP" in params.keys():
        vpc_uuid = get_vpc_uuid(params["vpc_name"])
        payload["spec"]["resources"]["private_ip"] = "@@{vm_ip}@@"
        payload["spec"]["resources"]["vpc_reference"] = {
                                                         "kind":"vpc",
                                                         "uuid":vpc_uuid
                                                        }
    elif "VM_Name" in params.keys():
        nic_uuid = get_nic_uuid(params["VM_Name"])
        payload["spec"]["resources"]["vm_nic_reference"] = {
                                                            "kind": "vm_nic",
                                                            "uuid":nic_uuid
                                                           }
    else:
        print("Input Error :- User should provide VM IP in 'VM IP'")
        exit(1)
        
    url = _build_url(scheme="https",
                    resource_type="/floating_ips")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    wait_for_completion(data)
    print("floating_ip_details={}".format({"IP_uuid": data.json()['metadata']['uuid']}))
    
    sleep(5)
    _url = _build_url(scheme="https",
                     resource_type="/floating_ips/%s"%(data.json()['metadata']['uuid']))
    _data = requests.get(_url, auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    if (_data.ok) and ("status" in _data.json()):
        print("Floating IP assigned to '%s' is :- %s"%("@@{vm_ip}@@",
                          _data.json()["status"]["resources"]["floating_ip"]))
    else:
        print("Failed to fetch details of newly created floating IP.")
        print("Please check it manually.")
        exit(1)

def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Got error while generating floating IP ---> ",responce.json())
                state = 'FAILED'
                exit(1)
            else:
                state = 'SUCCESSED'
    else:
        state = data.json().get('state')
        print("Got error while generating floating IP --->",data.json())
        exit(1)
        
params = {
              "external_subnet":"@@{external_subnet_name}@@"
         }

if "@@{assignment_type}@@" == "IP":
    params["IP"] = "@@{vm_ip}@@"
    params["vpc_name"] = "@@{vpc_name}@@"
    if params["vpc_name"].lower() in ["", "na", "none"]:
        print("Input Error :- VPC Name is Mandatory for 'Floating IP Assignment Type = IP'.")
        exit(1)

print("##### Generating Floating IP #####")
generate_floating_ip(**params)