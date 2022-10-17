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
    return (
        {
          "api_version": "3.1.0",
          "metadata": {"kind": "subnet"},
          "spec": {
                  "name": "",
                  "resources": {
                      "ip_config": {},
                      "subnet_type": None,
                      },
                  },
              }
          )

def _get_ipam_spec(**params):
    ipam_spec = {}
    if params['set_ipam'] == 'yes':
        ipam_spec = _get_default_ipconfig_spec()
        ipam_config = params["ipam"]
        ipam_spec["subnet_ip"] = ipam_config["network_ip"]
        ipam_spec["prefix_length"] = ipam_config["network_prefix"]
        ipam_spec["default_gateway_ip"] = ipam_config["gateway_ip"]
        pools = []
        for ip_pools in params['ip_pool']:
            pools.append({"range": "%s %s"%(ip_pools['ip_pools_start_ip'], 
                                            ip_pools['ip_pools_end_ip'])})                                
        ipam_spec["pool_list"] = pools
        if "dhcp_options" in ipam_config:
            dhcp_spec = _get_default_dhcp_spec()
            dhcp_config = ipam_config["dhcp_options"]
            if dhcp_config['domain_name_server_list'] != 'None': 
                dhcp_spec["domain_name_server_list"] = dhcp_config["domain_name_server_list"]
            if dhcp_config["domain_search_list"] != 'None':
                dhcp_spec["domain_search_list"] = dhcp_config["domain_search_list"]
            if dhcp_config["domain_name"] != 'None':
                dhcp_spec["domain_name"] = dhcp_config["domain_name"]
            if dhcp_config["boot_file_name"] != 'None':
              dhcp_spec["boot_file_name"] = dhcp_config["boot_file_name"]
            if dhcp_config["tftp_server_name"] != 'None':
                dhcp_spec["tftp_server_name"] = dhcp_config["tftp_server_name"]
            ipam_spec["dhcp_options"] = dhcp_spec
    return ipam_spec

def _get_default_ipconfig_spec():
    return (
        {
         "subnet_ip": None,
         "prefix_length": None,
         "default_gateway_ip": None,
         "pool_list": [],
        }
      )

def _get_default_dhcp_spec():
    return (
      {
        "domain_name_server_list": [],
        "domain_search_list": [],
        "domain_name": "",
                "boot_file_name": "",
                "tftp_server_name": "",
       }
    )

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
    return data.json()['status']['execution_context']['task_uuid']  
                                     
def create_overlay_subnet():
    params = {}
    print("##### Creating Overlay Subnets #####")
    params_dict = @@{overlay_subnet_items}@@
    params['vpc_name'] = params_dict.get('vpc_name', 'None')
    params['ipam'] = {}
    params['set_ipam'] = "yes"
    params['ipam']['network_ip'] = params_dict.get('network_ip', 'None')
    params['ipam']['network_prefix'] = params_dict.get('prefix', 'None')
    params['ipam']['gateway_ip'] = params_dict.get('gateway_ip', 'None')
    params['ip_pool'] = params_dict['ip_pool']
    params['dhcp'] = params_dict.get('dhcp', 'None')
    params['ipam']['dhcp_options'] = {}
    params['ipam']['dhcp_options']['domain_name_server_list'] = params_dict.get('dns_servers', 'None')
    params['ipam']['dhcp_options']['domain_search_list'] = params_dict.get('domain_search', 'None')
    params['ipam']['dhcp_options']['domain_name'] = params_dict.get('domain_name', 'None')
    params['ipam']['dhcp_options']['boot_file_name'] = params_dict.get('boot_file', "None")
    params['ipam']['dhcp_options']['tftp_server_name'] = params_dict.get('tftp_server', "None")
            
    payload = _get_default_spec()
    if params_dict.get('vpc_name', 'None') != 'None':
        vpc_details = @@{vpc_details}@@
        params['vpc_reference'] = {"kind": "vpc", "uuid": vpc_details["uuid"]}
        payload["spec"]["resources"]["vpc_reference"] = params['vpc_reference']
    payload["spec"]['name'] = params_dict['subnet_name']
    payload["spec"]["resources"]["subnet_type"] = "OVERLAY"
            
    if params_dict.get('network_ip', 'None') != 'None':
        params['ipam_spec'] = _get_ipam_spec(**params)
        print("Overlay Subnet IP range - %s"%params['ip_pool'])
        payload["spec"]["resources"]["ip_config"] = params['ipam_spec']


    url = _build_url(scheme="https",
                    resource_type="/subnets")    
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         timeout=None, verify=False)
    task_uuid = wait_for_completion(data)
    details = {"uuid":data.json()['metadata']['uuid'],
                               "name": params_dict['subnet_name'],
                               "create_subnet_task_uuid": task_uuid}
    print("overlay_subnet_details={}".format(details))
create_overlay_subnet()
