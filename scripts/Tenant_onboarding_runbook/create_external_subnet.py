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
  
def _get_cluster_details(cluster_name):
    cluster_details = {'kind':'cluster'}
    payload = {"entity_type": "cluster", "filter": "name==%s"%cluster_name}
    url = _build_url(scheme="https",
                    resource_type="/groups")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(@@{prism_central_username}@@, @@{prism_central_passwd}@@), 
                         verify=False)
    if data.ok:
        cluster_details['uuid'] = str(data.json()['group_results'][0]['entity_results'][0]['entity_id'])
        return cluster_details
    else:
        print("Failed to get %s cluster details"%cluster_name)
        exit(1)
    
def _get_virtual_switch_uuid(virtual_switch_name):
    payload = {"entity_type": "distributed_virtual_switch", 
               "filter": "name==%s"%virtual_switch_name}
    url = _build_url(scheme="https",
                    resource_type="/groups")                
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(@@{prism_central_username}@@, @@{prism_central_passwd}@@),
                         verify=False)
    if data.ok:
        print("virtual switch uuid ----> ",data.json()['group_results'][0]['entity_results'][0]['entity_id'])
        return str(data.json()['group_results'][0]['entity_results'][0]['entity_id'])
    else:
        print("Failed to get %s virtual switch uuid."%virtual_switch_name)
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
        pools = []
        if params['dhcp'] != 'None':
            for ip_pools in params['dhcp']:
                pools.append({"range": "%s %s"%(ip_pools['ip_pools_start_ip'], 
                                                ip_pools['ip_pools_end_ip'])})                                
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
    payload = _get_default_spec()
    if params['uuid'] != "None":
        payload["spec"]['uuid'] = params['uuid']
    payload["spec"]['name'] = params['name']
    payload["spec"]["resources"]["subnet_type"] = "VLAN"
    payload["spec"]["resources"]["vlan_id"] = params['vlan_id']
    payload["spec"]["resources"]["ip_config"] = params['ipam_spec']
    payload["spec"]["cluster_reference"] = params.get('cluser_reference',\
                                _get_cluster_details(cluster_name=params['cluster_name']))
    if params['enable_nat'] == False:
        params['virtual_switch_uuid'] = params.get('virtual_switch_uuid',\
                _get_virtual_switch_uuid(params['virtual_switch_name']))
        payload["spec"]["resources"]["virtual_switch_uuid"] = params['virtual_switch_uuid']
    payload["spec"]["resources"]["is_external"] = True
    payload["spec"]["resources"]["enable_nat"] = params['enable_nat']
    pprint(payload)
    if params['operation'] == "create":
        url = _build_url(scheme="https",
                        resource_type="/subnets")    
        data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(@@{prism_central_username}@@, 
                                            @@{prism_central_passwd}@@),
                         timeout=None, verify=False)
        if data.ok:
            task_uuid = wait_for_completion(data)
            task = {"uuid": data.json()['metadata']['uuid'],
                   "create_subnet_task_uuid":task_uuid,
                   "name": params['name']}
            return task
        else:
            print("Failed to create %s external subnet"%params['name'])
            exit(1)

def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(@@{prism_central_username}@@, @@{prism_central_passwd}@@), 
                                    verify=False)
            print(responce.json())
            if responce.json()['status'] in ['PENDING', 'RUNNING','QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Got error while creating subnet ---> ",responce.json())
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        state = data.json().get('state')
        print("Got %s while creating subnet ---> "%state, data.json())
        exit(1)
    return data.json()['status']['execution_context']['task_uuid']
            
def validate_params():
    params = {}
    params['operation'] = @@{operation}@@
    if params['operation'] == "delete":
        exit(0)
    else:
        print("##### creating external subnet #####")
        _params = @@{external_subnet_items}@@
        params['operation'] = @@{operation}@@
        subnets = []
        for x in range(len(_params)):
            sleep(5)
            params_dict = _params[x]
            params['name'] = params_dict['name']
            params['uuid'] = params_dict.get('uuid', "None")
            params['enable_nat'] = params_dict.get('enable_nat', False)
            params['cluster_name'] = params_dict.get('cluster', "None")
            params['vlan_id'] = params_dict.get('vlan_id')
            params['virtual_switch_name'] = params_dict.get('virtual_switch_name', "None")
            params['ipam'] = {}
            params['set_ipam'] = "yes"
            params['ipam']['network_ip'] = params_dict.get('network_ip', 'None')
            params['ipam']['network_prefix'] = params_dict.get('prefix', 'None')
            params['ipam']['gateway_ip'] = params_dict['gateway_ip']
            params['dhcp'] = params_dict.get('dhcp', "None")
            subnet = create_external_subnet(**params)
            subnets.append(subnet)
        print("external_subnet_details={}".format(subnets))
validate_params()
