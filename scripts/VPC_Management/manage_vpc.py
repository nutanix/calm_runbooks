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
    if params['uuid'] != "NA":
        payload["spec"]['uuid'] = params['uuid']
    payload["spec"]['name'] = params['name']
    if params.get("common_domain_name_server_ip_list", "NA") != "NA":
        payload["spec"]["resources"]["common_domain_name_server_ip_list"] = \
                                params["common_domain_name_server_ip_list"]
    payload["spec"]["resources"]["external_subnet_list"] = \
                                params["external_subnet_list"]
    if params.get("externally_routable_prefix_list", "NA") != "NA":
        payload["spec"]["resources"]["externally_routable_prefix_list"] = \
                                params["externally_routable_prefix_list"]
    if "@@{operation}@@" == "update":
        update_vpc(**payload["spec"])
    else:
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
            task_uuid = wait_for_completion(data)
            vpc = {"vpc_name": params['name'], 
                   "vpc_uuid":data.json()['metadata']['uuid']}
            print("Please make a note of VPC Details for furure refrerence.")
            print(vpc)

def update_vpc(**payload):
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s"%"@@{vpc_uuid}@@")    
    data = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
                         
    if not data.ok:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
        
    _spec = data.json()    
    for x in ["last_update_time", "creation_time", "spec_hash", "categories_mapping", "owner_reference", "categories"]:
        del _spec["metadata"][x]
        
    del _spec["status"]
    del _spec["spec"]
    
    _spec["spec"] = payload
    
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s"%"@@{vpc_uuid}@@")    
    data = requests.put(url, json=_spec,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
                         
    if not data.ok:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    else:
        task_uuid = wait_for_completion(data)
        print("%s VPC updated successfully."%"@@{vpc_name}@@".strip())
        
def delete_vpc(**params):
    url = _build_url(scheme="https",
                    resource_type="/vpcs/%s"%params["uuid"])
    
    data = requests.delete(url,auth=HTTPBasicAuth(pc_username, pc_password),
                           timeout=None, verify=False)
                         
    if not data.ok:
        print("Got Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)
    else:
        task_uuid = wait_for_completion(data)
        print("%s VPC Deleted successfully."%params["name"])
        
def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        if state == "DELETE_PENDING":
            state = "PENDING"
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED', 'DELETE_PENDING']:
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
    return data.json()['status']['execution_context']['task_uuid']
    
def validate_params():
    params = {}
    params_dict = @@{vpc_items}@@
    params['name'] = "@@{vpc_name}@@".strip()
    params['uuid'] = "@@{vpc_uuid}@@"
    if "@@{operation}@@" == "delete":
        delete_vpc(**params)
    else:
        print("##### Creating VPC %s #####"%params['name'])
        if params_dict.get("dns_servers", "NA") != "NA":
            params["common_domain_name_server_ip_list"] = [{}]
            params["common_domain_name_server_ip_list"][0]['ip'] = \
                                            params_dict.get('dns_servers', 'None')
        params["external_subnet_list"] = [{}]
        if params_dict.get("externally_routable_ip", "NA") != "NA":
            params["externally_routable_prefix_list"] = [{}]
            params["externally_routable_prefix_list"][0]["ip"] = \
                                            params_dict["externally_routable_ip"]
            params["externally_routable_prefix_list"][0]["prefix_length"] = \
                                            params_dict["externally_routable_ip_prefix"]
                                            
        if params_dict.get("external_subnet_name", "NA") != "NA":
            params["external_subnet_list"][0]["external_subnet_reference"] = {}
            params["external_subnet_list"][0]["external_subnet_reference"]["kind"] = "subnet"
            params["external_subnet_list"][0]["external_subnet_reference"]["name"] = \
                                            params_dict["external_subnet_name"]
            params["external_subnet_list"][0]["external_subnet_reference"]["uuid"] = \
                                            params_dict["external_subnet_uuid"]
                                            
        if params_dict.get("external_subnet_uuid", "NA") != "NA":
            params["external_subnet_list"][0]["external_subnet_reference"]["uuid"] = \
                                                    params_dict['external_subnet_uuid']
        create_vpc(**params)

validate_params()
