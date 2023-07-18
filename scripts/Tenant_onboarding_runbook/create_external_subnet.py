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
  
def _get_cluster_details(cluster_name):
    cluster_details = {'kind':'cluster'}
    payload = {"kind": "cluster"}
    url = _build_url(scheme="https",
                    resource_type="/clusters/list")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_password), 
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
    
def _get_virtual_switch_uuid(virtual_switch_name):
    cluster = "@@{cluster_name}@@".strip()
    _cluster = _get_cluster_details(cluster)
    cluster_uuid = _cluster['uuid']
    payload = {"entity_type": "distributed_virtual_switch", 
               "filter": "name==%s"%virtual_switch_name}
    url = _build_url(scheme="https",
                    resource_type="/groups")                
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         verify=False)
    if data.ok:
        _uuid = data.json()['group_results'][0]['entity_results'][0]['entity_id']
        _url = "https://%s:9440/api/networking/v2.a1/dvs/virtual-switches/%s?proxyClusterUuid=%s"%(PC_IP,
                                                                                                _uuid,
                                                                                                cluster_uuid)
        _data = requests.get(_url, auth=HTTPBasicAuth(pc_username, pc_password),verify=False)
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
        pools.append(params["ip_pools"])
        ipam_spec["pool_list"] = pools
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

def create_external_subnet(**params):
    params['ipam_spec'] = _get_ipam_spec(**params)
    cluster_details = _get_cluster_details(cluster_name=params['cluster_name'])
    payload = _get_default_spec()
    if params['uuid'] != "None":
        payload["spec"]['uuid'] = params['uuid']
    payload["spec"]['name'] = params['name']
    payload["spec"]["resources"]["subnet_type"] = "VLAN"
    payload["spec"]["resources"]["vlan_id"] = params['vlan_id']
    payload["spec"]["resources"]["ip_config"] = params['ipam_spec']
    payload["spec"]["cluster_reference"] = cluster_details
    if params['enable_nat'] == False:
        switch_details = _get_virtual_switch_uuid(params['virtual_switch_name'])
        payload["spec"]["resources"]["virtual_switch_uuid"] = switch_details
    payload["spec"]["resources"]["is_external"] = True
    payload["spec"]["resources"]["enable_nat"] = params['enable_nat']
    url = _build_url(scheme="https",
                        resource_type="/subnets")
    while True:
        data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username,pc_password),
                         timeout=None, verify=False)
        if data.ok:
            task_uuid = wait_for_completion(data=data, vlan_id=params['vlan_id'])
            if task_uuid == {}:
                _uuid = data.json()['metadata']['uuid']
                _name = params['name']
            else:
                _uuid = task_uuid["uuid"]
                _name = task_uuid["name"]
            return {"uuid": _uuid, "name": _name}

        elif "subnet exists with vlan id" in str(data.json()).lower():
            _url = _build_url(scheme="https",resource_type="/subnets/list")
            _data = requests.post(_url, json={"kind":"subnet"},
                                 auth=HTTPBasicAuth(pc_username,pc_password),
                                 verify=False)
            if _data.ok:
                if _data.json()['metadata']['total_matches'] > 0:
                    for _subnet in _data.json()['entities']:
                        if "vlan_id" not in _subnet['spec']['resources'].keys():
                            continue
                        if _subnet['spec']['resources']['vlan_id'] == params['vlan_id']:
                            return {"uuid":_subnet['metadata']['uuid'], "name":_subnet["spec"]["name"]}
                    print("Error :- No subnet found on host with VLAN ID %s"%params['vlan_id'])
                    exit(1)
                else:
                    print("Error :- No subnet found on host")
                    exit(1)
            else:
                print("Error while fetching external subnet details.")
                print(data.json().get('message_list', data.json().get('error_detail', data.json())))
                exit(1)
        else:
            print("Failed to create external subnet ---> ",data.json().get('message_list', 
                                    data.json().get('error_detail', data.json())))
            exit(1)

def wait_for_completion(data, vlan_id=None):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json()['status'] in ['PENDING', 'RUNNING','QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                if "subnet exists with vlan id" in str(responce.json()).lower():
                    print("Another external subnet exist with sam VLAN ID, fetching details..")
                    _url = _build_url(scheme="https",resource_type="/subnets/list")
                    _data = requests.post(_url, json={"kind":"subnet"},
                                 auth=HTTPBasicAuth(pc_username,pc_password),
                                 verify=False)
                    if _data.ok:
                        if _data.json()['metadata']['total_matches'] > 0:
                            for _subnet in _data.json()['entities']:
                                if "vlan_id" not in _subnet['spec']['resources'].keys():
                                    continue
                                if _subnet['spec']['resources']['vlan_id'] == vlan_id:
                                    return {'uuid':_subnet['metadata']['uuid'],"name":_subnet['spec']['name']}
                            print("Error :- No subnet found on host with VLAN ID %s"%vlan_id)
                            exit(1)
                        else:
                            print("Error :- No subnet found on host")
                            exit(1)
                    else:
                        print("Error while fetching external subnet details.")
                        print(data.json().get('message_list', data.json().get('error_detail', data.json())))
                        exit(1)
                else:
                    print("Error ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                    state = 'FAILED'
                    exit(1)
            else:
                state = "COMPLETE"
    return {}
            
def _get_vlan_id():
    url = _build_url(scheme="https",resource_type="/subnets/list")
    data = requests.post(url, json={"kind":"subnet"},
                         auth=HTTPBasicAuth(pc_username, 
                                            pc_password),
                         timeout=None, verify=False)
    if data.ok:
        vlan_id = []
        for x in data.json()['entities']:
            print(x['spec']['resources'])
            vlan_id.append(x['spec']['resources'].get('vlan_id', 0))
        id = 10
        while True:
            if id in vlan_id:
                id+=1
            else:
                break
        return id
    else:
        print("Error while fetching subnet list :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
def set_params():
    params_dict = @@{external_subnet_items}@@
    params['name'] = params_dict['name']
    params['uuid'] = params_dict.get('uuid', "None")
    params['enable_nat'] = params_dict.get('enable_nat', False)
    params['cluster_name'] = params_dict.get('cluster', "None")
    params['vlan_id'] = @@{external_vlan_id}@@
    params['virtual_switch_name'] = params_dict.get('virtual_switch_name', "None")
    params['ipam'] = {}
    params['set_ipam'] = "yes"
    params['ipam']['network_ip'] = params_dict.get('network_ip', 'None')
    params['ipam']['network_prefix'] = params_dict.get('prefix', 'None')
    params['ipam']['gateway_ip'] = params_dict['gateway_ip']
    params['ip_pools'] = params_dict['ip_pools']

params = {}
set_params()
subnet = create_external_subnet(**params)
print("external_subnet_details={}".format(subnet))
