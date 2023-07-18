#script

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

def _get_default_spec():
    return(
            {
            "api_version": "3.1.0",
            "metadata": {"kind": "vpc", "categories": {}},
            "spec": {
                "name": None,
                "resources": {
                    "external_subnet_list": []
                    },
                },
            })

def create_vpc(**params):
    payload = _get_default_spec()
    if params['uuid'] != "None":
        payload["spec"]['uuid'] = params['uuid']
    payload["spec"]['name'] = params['name']
    if params.get("common_domain_name_server_ip_list", "None") != "None":
        payload["spec"]["resources"]["common_domain_name_server_ip_list"] = \
                                params["common_domain_name_server_ip_list"]
    payload["spec"]["resources"]["external_subnet_list"] = \
                                params["external_subnet_list"]
    if params.get("externally_routable_prefix_list", "None") != "None":
        payload["spec"]["resources"]["externally_routable_prefix_list"] = \
                                params["externally_routable_prefix_list"]
    url = _build_url(scheme="https",
                        resource_type="/vpcs")    
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_password ),
                         timeout=None, verify=False)
                         
    if not data.ok:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    else:
        wait_for_completion(data)
        vpc_uuid = data.json()['metadata']['uuid']
        print("vpc_uuid={}".format(vpc_uuid))
        create_static_route(vpc_uuid)
        
def _get_route_spec(vpc_uuid):
    subnet_name = "@@{external_subnet_name}@@".strip()
    subnet_uuid = "@@{external_subnet_uuid}@@"
    ip_prefix = "0.0.0.0/0"
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
        print("Error while fetching VPCs static route details.")
        exit(1)
    static_route = {"nexthop": {
                        "external_subnet_reference": {
                            "kind": "subnet",
                            "name": subnet_name,
                            "uuid": subnet_uuid
                        }
                    },
                    "destination": ip_prefix}
    responce["spec"]["resources"]["static_routes_list"].append(static_route)
    return responce

def create_static_route(vpc_uuid):
    subnet_uuid = "@@{external_subnet_uuid}@@"
    subnet_name = "@@{external_subnet_name}@@".strip()
    payload = _get_route_spec(vpc_uuid)
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s/route_tables"%vpc_uuid)
    data = requests.put(url, json=payload, 
                        auth=HTTPBasicAuth(pc_username, pc_password), verify=False)
    wait_for_completion(data)
    
def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Got Error ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

if @@{create_vpc}@@:
    params = {}
    print("##### creating VPC #####")
    params_dict = @@{vpc_items}@@
    params['name'] = params_dict['name']
    params['uuid'] = params_dict.get('uuid', "None")
    if params_dict.get("dns_servers", "None") != "None":
        params["common_domain_name_server_ip_list"] = [{}]
        params["common_domain_name_server_ip_list"][0]['ip'] = \
                                            params_dict.get('dns_servers', 'None')
    params["external_subnet_list"] = [{}]
    if params_dict.get("externally_routable_ip", "None") != "None":
        params["externally_routable_prefix_list"] = [{}]
        params["externally_routable_prefix_list"][0]["ip"] = \
                                            params_dict["externally_routable_ip"]
        params["externally_routable_prefix_list"][0]["prefix_length"] = \
                                            params_dict["externally_routable_ip_prefix"]
                                            
    if params_dict.get("external_subnet_name", "None") != "None":
        params["external_subnet_list"][0]["external_subnet_reference"] = {}
        params["external_subnet_list"][0]["external_subnet_reference"]["kind"] = "subnet"
        params["external_subnet_list"][0]["external_subnet_reference"]["name"] = \
                                            params_dict["external_subnet_name"]
        params["external_subnet_list"][0]["external_subnet_reference"]["uuid"] = "@@{external_subnet_uuid}@@"
                                            
    if params_dict.get("external_subnet_uuid", "None") != "None":
        params["external_subnet_list"][0]["external_subnet_reference"]["uuid"] = \
                                               params_dict['external_subnet_uuid']
    create_vpc(**params)
    
else:
    vpc_name = "@@{vpc_name}@@".strip()
    print("Retriving VPC details of %s"%vpc_name)
    url = _build_url(scheme="https",resource_type="/vpcs/list")
    data = requests.post(url, json={"kind":"vpc", "filter":"name==%s"%vpc_name},
                         auth=HTTPBasicAuth(pc_username, 
                                            pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(vpc_name, PC_IP))
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one VPC's with name - %s on - %s"%(vpc_name, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            print("vpc_uuid={}".format(data.json()['entities']\
                                       [0]['metadata']['uuid']))
    else:
        print("Error while fetching VPC details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
