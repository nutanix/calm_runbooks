# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
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

def _get_default_spec(vpc_uuid, subnet_uuid, ip_prefix):
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s/route_tables"%vpc_uuid)
    data = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    if data.ok:
        responce = data.json()
        del responce["status"]
        for x in ["last_update_time","creation_time","spec_hash","categories_mapping","owner_reference","categories"]:
            if x in responce["metadata"].keys():
                del responce["metadata"][x]
    else:
        print("Error while fetching @@{vpc_name}@@ VPCs static route details.")
        exit(1)
    static_route = {"nexthop": {
                        "external_subnet_reference": {
                            "kind": "subnet",
                            "name": "@@{external_subnet_name}@@".strip(),
                            "uuid": subnet_uuid
                        }
                    },
                    "destination": ip_prefix}
    responce["spec"]["resources"]["static_routes_list"].append(static_route)
    return responce

def _get_delete_spec(vpc_uuid, subnet_uuid, ip_prefix):
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s/route_tables"%vpc_uuid)
    data = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    if data.ok:
        responce = data.json()
        del responce["status"]
        for x in ["last_update_time","creation_time","spec_hash","categories_mapping","owner_reference","categories"]:
            if x in responce["metadata"].keys():
                del responce["metadata"][x]
    else:
        print("Error while fetching @@{vpc_name}@@ VPCs static route details.")
        exit(1)

    for x,_route in enumerate(responce["spec"]["resources"]["static_routes_list"]):
        if (_route["destination"] == ip_prefix) and (_route["nexthop"]["external_subnet_reference"]["uuid"] == subnet_uuid):
            del responce["spec"]["resources"]["static_routes_list"][x]
            return responce
    print("Input Error :-- @@{ip_prefix}@@ IP prefix with "\
          "@@{external_subnet_name}@@ external subnet not found.")
    exit(1)
  
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
        
def _get_vpc_details(vpc_name):
    vpc_details = {"kind": "vpc"}
    if vpc_name.lower() not in ["na", "none"]:
        url = _build_url(
                    scheme="https",
                    resource_type="/vpcs/list")               
        data = requests.post(url, json=vpc_details,
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         verify=False)
        if vpc_name in str(data.json()):
            for _vpc in data.json()['entities']:
                if _vpc['spec']['name'] == vpc_name:
                    return _vpc['metadata']['uuid']
        else:
            print("Input Error ---> %s VPC not present on host"%vpc_name)
            exit(1)
    else:
        print("Input Error :-- VPC name should not be NA or None")
        exit(1)
          
def create_static_route(**params):
    vpc_uuid = _get_vpc_details(params["vpc_name"])
    subnet_uuid = get_subnet_uuid(params["external_subnet"])
    payload = _get_default_spec(vpc_uuid, subnet_uuid, params["ip_prefix"])
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s/route_tables"%vpc_uuid)
    data = requests.put(url, json=payload, 
                        auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    wait_for_completion(data)

def delete_static_route(**params):
    vpc_uuid = _get_vpc_details(params["vpc_name"])
    subnet_uuid = get_subnet_uuid(params["external_subnet"])
    payload = _get_delete_spec(vpc_uuid, subnet_uuid, params["ip_prefix"])
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s/route_tables"%vpc_uuid)
    data = requests.put(url, json=payload, 
                        auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    wait_for_completion(data)
    
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'DELETE_PENDING']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error while creating Statis route ---> ",responce.json())
                state = 'FAILED'
                exit(1)
            else:
                state = 'SUCCESSED'
    else:
        state = data.json().get('state')
        print("Error while creating Statis route --->",data.json())
        exit(1)

ip_prefix = "@@{ip_prefix}@@".strip()
if "/" in ip_prefix:
    ip, prefix = ip_prefix.split("/")
    if len(ip.split(".")) != 4:
        print("Input Error :-- Please provide IP with Prefix in correct format as below.")
        print("Example := 10.10.10.0/24")
        exit(1)
else:
    print("Input Error :-- Please provide IP with Prefix in correct format as below.")
    print("Example := 10.10.10.0/24")
    exit(1)
    
params = {
              "vpc_name":"@@{vpc_name}@@".strip(),
              "external_subnet":"@@{external_subnet_name}@@".strip(),
              "ip_prefix": ip_prefix
         }
print("##### Updating Static routes of %s VPC #####"%params["vpc_name"])
if "@@{operation}@@" == "UPDATE":
    create_static_route(**params)
    print("Success !!!")
else:
    delete_static_route(**params)
    print("Success !!!")
