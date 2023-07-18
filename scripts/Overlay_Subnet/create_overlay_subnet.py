#script

import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_passwd = "@@{prism_central_passwd}@@".strip()

management_pc_username = "@@{management_pc_username}@@".strip()
management_pc_password = "@@{management_pc_password}@@".strip()

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

def _get_project_spec(project):
    url = _build_url(scheme="https", host="localhost",
                    resource_type="/projects_internal/{}".format(project))
    data = requests.get(url,auth=HTTPBasicAuth(management_pc_username, 
                                               management_pc_password),
                        timeout=None, verify=False)
    return data.json()
        
def update_project(subnet_uuid):
    project = {"uuid": "@@{project_uuid}@@"}
    payload = _get_project_spec(project['uuid'])

    for x in ['categories', 'categories_mapping', 'creation_time', 'last_update_time', 'owner_reference']:
        if x in payload['metadata'].keys():
            del payload['metadata'][x]
    del payload['status']

    payload['spec']['access_control_policy_list'][0]['operation'] = "UPDATE"
    
    payload["spec"]["project_detail"]["resources"]["external_network_list"].append(\
                                 {'name': "@@{vlan_name}@@", 'uuid': subnet_uuid})
    
    url = _build_url(scheme="https",host="localhost",
                    resource_type="/projects_internal/{}".format(project['uuid']))
    data = requests.put(url, json=payload,
                        auth=HTTPBasicAuth(management_pc_username, 
                                           management_pc_password),
                        timeout=None, verify=False)
    if data.ok:
        task = wait_for_completion_update(data)       
        print("Project %s updated successfully"%"@@{project_name}@@".strip())
    else:
        print("Error while updating project : %s"%data.json())
        exit(1)
    
def wait_for_completion_update(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https", host="localhost",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(management_pc_username, 
                                        management_pc_password),verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error in project update ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        print("Error in project update ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

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
        if "ip_pools" in ipam_config and ipam_config["ip_pools"] != []:
            pools = []
            ipam_spec["pool_list"] = []
            for ip_pools in ipam_config["ip_pools"]:
                if (ip_pools.get('start_ip', 'NA') != 'NA') and (ip_pools.get('end_ip', 'NA') != 'NA'):
                    pools.append({"range": "%s %s"%(ip_pools['start_ip'],
                                                    ip_pools['end_ip'])})
            ipam_spec["pool_list"] = pools
        if "dhcp_options" in ipam_config:
            dhcp_spec = _get_default_dhcp_spec()
            dhcp_config = ipam_config["dhcp_options"]
            if dhcp_config['domain_name_server_list'] != 'NA': 
                dhcp_spec["domain_name_server_list"] = dhcp_config["domain_name_server_list"]
            if dhcp_config["domain_search_list"] != ['NA']:
                dhcp_spec["domain_search_list"] = dhcp_config["domain_search_list"]
            if dhcp_config["domain_name"] != 'NA':
                dhcp_spec["domain_name"] = dhcp_config["domain_name"]
            if dhcp_config["boot_file_name"] != 'NA':
              dhcp_spec["boot_file_name"] = dhcp_config["boot_file_name"]
            if dhcp_config["tftp_server_name"] != 'NA':
                dhcp_spec["tftp_server_name"] = dhcp_config["tftp_server_name"]
            ipam_spec["dhcp_options"] = dhcp_spec
    return ipam_spec

def _get_default_ipconfig_spec():
    return (
        {
         "subnet_ip": None,
         "prefix_length": None,
         "default_gateway_ip": None,
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
  
def get_params(**params):
    params['vpc_reference'] = {"kind":"vpc", "uuid": params["overlay_subnet"]["vpc"]["uuid"]}
    payload = _get_default_spec()
    payload["spec"]['name'] = params['subnet_name']
    payload["spec"]["resources"]["subnet_type"] = "OVERLAY"
    payload["spec"]["resources"]["vpc_reference"] = params['vpc_reference']
    params['ipam_spec'] = _get_ipam_spec(**params)
    payload["spec"]["resources"]["ip_config"] = params['ipam_spec']
    return payload

def overlay_subnet(**params):
    payload = get_params(**params)
    url = _build_url(
                    scheme="https",
                    resource_type="/subnets")    
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_passwd),
                         timeout=None, verify=False)
    wait_for_completion(data)
    subnet_uuid = data.json()["metadata"]["uuid"]
    print("%s overlay subnet created successfully."%payload["spec"]["name"])
    print("Please note subnet UUID for future reference :- ",data.json()["metadata"]["uuid"])
    
    if "@@{add_subnet_to_project}@@".lower() == "yes":
        update_project(subnet_uuid)

def update_subnet(**payload):
    _uuid = ""
    _spec = ""
    
    _url = _build_url(scheme="https",
                    resource_type="/subnets/%s"%payload["vlan_uuid"])
    _data = requests.get(_url, auth=HTTPBasicAuth(pc_username, pc_passwd),verify=False)
    if _data.ok:
        if _data.json()['spec']['name'] != payload['subnet_name']:
            print("Input Error :- Provided UUID %s does not match with provided "\
                "VLAN name %s"%(payload["vlan_uuid"], payload['subnet_name']))
            exit(1)
        else:
            _uuid = payload["vlan_uuid"]
            _spec = _data.json()
    else:
        print(_data.json().get('message_list',_data.json().get('error_detail', _data.json())))
        exit(1)
        
    _params = {}
    del _spec["status"]
    for x in ["last_update_time", "creation_time", "spec_hash", "categories_mapping", "owner_reference", "categories"]:
        del _spec["metadata"][x]
        
    _payload = get_params(**payload)
    del _spec["spec"]
    _spec["spec"] = _payload["spec"]
    
    url = _build_url(
                    scheme="https",
                    resource_type="/subnets/%s"%_uuid)
    data = requests.put(url, json=_spec,
                         auth=HTTPBasicAuth(pc_username, pc_passwd),
                         timeout=None, verify=False)
    wait_for_completion(data)
    print("%s overlay subnet updated successfully."%payload["subnet_name"])
    
    if "@@{add_subnet_to_project}@@".lower() == "yes":
        update_project(subnet_uuid=payload["vlan_uuid"])

def delete_subnet(**params):
    _uuid = ""
    _url = _build_url(scheme="https",resource_type="/subnets/%s"%params["vlan_uuid"])
    _data = requests.get(_url, auth=HTTPBasicAuth(pc_username, pc_passwd),verify=False)
    if _data.ok:
        if _data.json()['spec']['name'] != params['subnet_name']:
            print("Input Error :- Provided UUID %s does not match with provided "\
                "VLAN name %s"%(params["vlan_uuid"], params['subnet_name']))
            exit(1)
        else:
            _uuid = params["vlan_uuid"]
    else:
        print(_data.json().get('message_list',_data.json().get('error_detail', _data.json())))
        exit(1)
        
    url = _build_url(scheme="https", resource_type="/subnets/%s"%_uuid)
    data = requests.delete(url, auth=HTTPBasicAuth(pc_username, pc_passwd),
                            timeout=None, verify=False)
    wait_for_completion(data)
    print("%s overlay subnet deleted successfully."%params["subnet_name"])

def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        if state == "DELETE_PENDING":
            state = "PENDING"
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username,pc_passwd), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print(responce.json().get('message_list',responce.json().get(\
                                          'error_detail', responce.json())))
                state = 'FAILED'
                exit(1)  
                
            else:
                state = "COMPLETE"
    else:
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1)
            
def set_params():
    params = @@{overlay_subnet_items}@@
    operation = "@@{operation}@@"
    params['subnet_name'] = "@@{vlan_name}@@".strip()
    params['vlan_uuid'] = "@@{vlan_uuid}@@"
    if operation == "delete":
        delete_subnet(**params)
    else:                                                     
        params['ipam'] = {}
        params['set_ipam'] = "yes"
        params['vpc_uuid'] = params['overlay_subnet']['vpc'].get('uuid', 'NA')
        params['vpc_name'] = params['overlay_subnet']['vpc'].get('name', 'NA')
        params['ipam']['network_ip'] = params['overlay_subnet']['ipam']['network_ip']
        params['ipam']['network_prefix'] = params['overlay_subnet']['ipam']['network_prefix']
        params['ipam']['gateway_ip'] = params['overlay_subnet']['ipam']['gateway_ip']
        params['ipam']['ip_pools'] = {}
        params['ipam']['ip_pools'] = params['overlay_subnet']['ipam'].get('ip_pools', [])
        if params['ipam']['network_ip'] != "NA":
            if 'dhcp' in params['overlay_subnet']['ipam'] and params['overlay_subnet']['ipam']['dhcp'] != {}:
                params['ipam']['dhcp_options'] = {}
                params['ipam']['dhcp_options']['domain_name_server_list'] = params['overlay_subnet']['ipam']['dhcp'].get('dns_servers', 'NA')
                params['ipam']['dhcp_options']['domain_search_list'] = params['overlay_subnet']['ipam']['dhcp'].get('domain_search', ['NA'])
                params['ipam']['dhcp_options']['domain_name'] = params['overlay_subnet']['ipam']['dhcp'].get('domain_name', 'NA')
                params['ipam']['dhcp_options']['boot_file_name'] = params['overlay_subnet']['ipam']['dhcp'].get('boot_file_name', "NA")
                params['ipam']['dhcp_options']['tftp_server_name'] = params['overlay_subnet']['ipam']['dhcp'].get('tftp_server', "NA")      
        if operation == "update":
            update_subnet(**params)
        else:
            overlay_subnet(**params)                                                      

set_params()
