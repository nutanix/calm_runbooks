#script

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
    if params['operation'] == "create":
        url = _build_url(scheme="https",
                        resource_type="/vpcs")    
        data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                            @@{prism_central_passwd}@@),
                         timeout=None, verify=False)
        task_uuid = wait_for_completion(data)
        vpc = {"name": params['name'], 
               "uuid":data.json()['metadata']['uuid'],
               "create_vpc_task_uuid": task_uuid}
        return vpc

def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                                            @@{prism_central_passwd}@@), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Got error while creating VPC ---> ",responce.json())
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        print("Got %s while creating VPC ---> "%state, data.json())
        exit(1)
    return data.json()['status']['execution_context']['task_uuid']
    
def _get_vlan_uuid(**params):
    vlan_name = params["external_subnet_name"]
    existing_subnet = @@{external_subnet_details}@@
    for _subnet in existing_subnet:
        if _subnet['name'] == vlan_name:
            return _subnet['uuid']
    _url = _build_url(scheme="https",
                    resource_type="/subnets/list")
    _data = requests.post(_url, json={"kind": "subnet"},
                        auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                           @@{prism_central_passwd}@@),
                        verify=False)
    _uuid = ""
    if vlan_name in str(_data.json()):
        for x in range(len(_data.json()['entities'])):
            if str(_data.json()['entities'][x]['spec']['name']) == vlan_name:
                _uuid = str(_data.json()['entities'][x]['metadata']['uuid'])
                return _uuid
    else:
        print("Error ---> %s subnet not present on host"%vlan_name)
        exit(1)

def validate_params():
    params = {}
    params['operation'] = @@{operation}@@
    if params['operation'] == "delete":
        exit(0)
    else:      
        print("##### creating VPC #####")
        vpc_details = []
        _params = @@{vpc_items}@@
        params['operation'] = @@{operation}@@
        for x in range(len(_params)):
            sleep(5)
            params_dict = _params[x]
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
            if params_dict.get("external_subnet_uuid", "None") == "None":
                params["external_subnet_list"][0]["external_subnet_reference"]["uuid"] = \
                                            _get_vlan_uuid(**params_dict)
            vpc_details.append(create_vpc(**params))
        print("vpc_details={}".format(vpc_details))

validate_params()
