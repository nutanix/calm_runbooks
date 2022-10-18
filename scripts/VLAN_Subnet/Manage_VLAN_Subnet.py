#script

import requests
from requests.auth import HTTPBasicAuth

PC_IP =  "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_passwd = "@@{prism_central_passwd}@@".strip()

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

def _get_virtual_switch_uuid(virtual_switch_name, cluter_uuid):
    payload = {"entity_type": "distributed_virtual_switch", 
               "filter": "name==%s"%virtual_switch_name}
    url = _build_url(scheme="https",
                    resource_type="/groups")                
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_passwd),
                         verify=False)
    if data.ok:
        _uuid = data.json()['group_results'][0]['entity_results'][0]['entity_id']
        _url = "https://%s:9440/api/networking/v2.a1/dvs/virtual-switches/%s?proxyClusterUuid=%s"%(PC_IP,
                                                                                                _uuid,
                                                                                                cluter_uuid)
        _data = requests.get(_url, auth=HTTPBasicAuth(pc_username, pc_passwd),verify=False)
        if _data.json()['data']['name'] == virtual_switch_name:
            print("virtual switch uuid ----> ",_uuid)
            return str(_uuid)
        else:
            print("Input Error :- %s virtual switch not present on %s"%(virtual_switch_name, PC_IP))
            exit(1)
    else:
        print("Error while fetching virtual switch details :- ",data.json().get('message_list',
                                                                                data.json().get('error_detail', 
                                                                                data.json())))
  
def _get_cluster_details(cluster_name):
    cluster_details = {'kind':'cluster'}
    payload = {"kind": "cluster"}
    url = _build_url(scheme="https",
                    resource_type="/clusters/list")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username,pc_passwd), 
                         verify=False)
    if data.ok:
        for _cluster in data.json()['entities']:
            if _cluster['status']['name'] == cluster_name:
                cluster_details['uuid'] = str(_cluster['metadata']['uuid'])
                return cluster_details
        print("Input Error :- Given cluster %s not present on %s"%(cluster_name, PC_IP))
        exit(1)
    else:
        print("Error while fetching %s cluster info"%cluster_name)
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
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

def _get_default_spec_update():
    return (
        {
          "api_version": "3.1.0",
          "metadata": {
                        "spec_version" : 5,
                        "kind": "subnet"
                      },
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
        if "ip_pools" in ipam_config and ipam_config["ip_pools"] != "NA":
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
            if dhcp_config['domain_name_server_list'] != ['NA']: 
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
         "prefix_length": 0,
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
    params['cluster_reference'] = _get_cluster_details(
                                    cluster_name=params['cluster_name'])
    params['virtual_switch_uuid'] = params.get('virtual_switch_uuid',\
                _get_virtual_switch_uuid(params['Virtual_switch_name'],
                                         params['cluster_reference']['uuid']))
    payload = _get_default_spec()
    if params['ipam']['network_ip'] != "NA":
        params['ipam_spec'] = _get_ipam_spec(**params)
        payload["spec"]["resources"]["ip_config"] = params['ipam_spec']
    payload["spec"]['name'] = "@@{vlan_name}@@".strip()
    payload["spec"]["resources"]["subnet_type"] = "VLAN"
    payload["spec"]["resources"]["vlan_id"] = params['vlan_id']
    payload["spec"]["resources"]["is_external"] = False
    payload["spec"]["resources"]["virtual_switch_uuid"] = params['virtual_switch_uuid']
    payload["spec"]["cluster_reference"] = params['cluster_reference']
    return payload
  
def vlan_subnet(**params):
    payload = get_params(**params)
    url = _build_url(scheme="https",
                    resource_type="/subnets")        
    data = requests.post(url, json=payload,
                             auth=HTTPBasicAuth(pc_username, pc_passwd),
                             timeout=None, verify=False)
    wait_for_completion(data)
    print("%s subnet created successfully"%payload["spec"]['name'])
    print("Please note UUID for future reference :- %s"%data.json()["metadata"]["uuid"])

def update_subnet(**payload):
    _uuid = ""
    _spec = ""
    if payload["vlan_uuid"] == "NA" or payload["vlan_uuid"] == "" :
        print("Input Error :- Please Provide proper UUID of %s subnet to update it."%payload['subnet_name'])
        print("Your provided UUID :- %s"%payload["vlan_uuid"])
        exit(1)
    else:
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

    del payload["vlan_uuid"]
    _params = {}
    del _spec["status"]
    for x in ["last_update_time", "creation_time", "spec_hash", "categories_mapping", "owner_reference", "categories"]:
        del _spec["metadata"][x]
        
    _payload = get_params(**payload)
    _spec["spec"] = _payload["spec"]
    url = _build_url(scheme="https",
                    resource_type="/subnets/%s"%_uuid)
    data = requests.put(url, json=_spec,
                         auth=HTTPBasicAuth(pc_username, pc_passwd),
                         timeout=None, verify=False)
    wait_for_completion(data)
    print("%s subnet updated successfully"%payload['subnet_name'])

def delete_subnet(**params):
    _uuid = ""
    if params["vlan_uuid"] == "NA" or params["vlan_uuid"] == "" :
        print("Input Error :- Please Provide proper UUID of %s subnet to update it."%params['subnet_name'])
        print("Your provided UUID :- %s"%params["vlan_uuid"])
        exit(1)
    else:
        _url = _build_url(scheme="https",
                    resource_type="/subnets/%s"%params["vlan_uuid"])
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

    url = _build_url(scheme="https",
                    resource_type="/subnets/%s"%_uuid)
    data = requests.delete(url, auth=HTTPBasicAuth(pc_username, pc_passwd),
                            timeout=None, verify=False)
    wait_for_completion(data)
    print("%s subnet deleted successfully"%params['subnet_name'])

def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
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
            
def validate_params():
    params = @@{vlan_subnet_items}@@
    operation = "@@{operation}@@"
    params['subnet_name'] = "@@{vlan_name}@@".strip()
    params["vlan_uuid"]  = "@@{vlan_uuid}@@"
    if operation == "delete":
        delete_subnet(**params)
    else:
        params['ipam'] = {}
        params['set_ipam'] = "no"
        if 'ipam' in params['vlan_subnet'] and params['vlan_subnet']['ipam'] != {}:
            params['set_ipam'] = "yes"
            params['ipam']['network_ip'] = params['vlan_subnet']['ipam']['network_ip']
            params['ipam']['network_prefix'] = params['vlan_subnet']['ipam']['network_prefix']
            params['ipam']['gateway_ip'] = params['vlan_subnet']['ipam']['gateway_ip']
            params['cluster_name'] = params['vlan_subnet']['cluster']['name']
            params['Virtual_switch_name'] = params['vlan_subnet']['virtual_switch_name']
            params['vlan_id'] = params['vlan_subnet']['vlan_id']
            params['ipam']['ip_pools'] = {}
            params['ipam']['ip_pools'] = params['vlan_subnet']['ipam'].get('ip_pools', "NA")
            if 'dhcp' in params['vlan_subnet']['ipam'] and params['vlan_subnet']['ipam']['dhcp'] != {}:
                params['ipam']['dhcp_options'] = {}
                params['ipam']['dhcp_options']['domain_name_server_list'] = params['vlan_subnet']['ipam']['dhcp']['dns_servers']
                params['ipam']['dhcp_options']['domain_search_list'] = params['vlan_subnet']['ipam']['dhcp']['domain_search']
                params['ipam']['dhcp_options']['domain_name'] = params['vlan_subnet']['ipam']['dhcp']['domain_name']
                params['ipam']['dhcp_options']['boot_file_name'] = params['vlan_subnet']['ipam']['dhcp'].get('boot_file_name', "NA")
                params['ipam']['dhcp_options']['tftp_server_name'] = params['vlan_subnet']['ipam']['dhcp'].get('tftp_server', "NA")
                params['ipam']['dhcp_options']['dhcp_server_ip'] = params['vlan_subnet']['ipam']['dhcp'].get('dhcp_server_ip', "NA")
        if operation == "update":
            update_subnet(**params)
        else:
            vlan_subnet(**params)

validate_params()
