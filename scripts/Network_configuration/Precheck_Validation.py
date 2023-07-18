# script

import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
skip_delete = False

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
    payload = {"kind": "cluster"}
    url = _build_url(scheme="https",
                    resource_type="/clusters/list")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_password), 
                         verify=False)
    if data.ok:
        for _cluster in data.json()['entities']:
            if _cluster['status']['name'] == cluster_name:
                print("cluster_uuid={}".format(_cluster['metadata']['uuid']))
                return str(_cluster['metadata']['uuid'])
        print("Input Error :- Given cluster %s not present on %s"%(cluster_name, PC_IP))
        exit(1)
    else:
        print("Error while fetching %s cluster info"%cluster_name)
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1)
            
def _get_virtual_switch_uuid(virtual_switch_name, cluster_uuid): 
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

def _get_subnet_uuid(subnet, delete=False):
    global skip_delete
    url = _build_url(scheme="https",resource_type="/subnets/list")
    data = requests.post(url, json={"kind":"subnet", "filter":"name==%s"%subnet},
                         auth=HTTPBasicAuth(pc_username, 
                                            pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(subnet, PC_IP))
            skip_delete = True
            if not delete:
                exit(1)
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one subnets with name - %s on - %s"%(subnet, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            skip_delete = False
            return data.json()['entities'][0]['metadata']['uuid']
    else:
        print("Error while fetching subnet details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
        
def _get_vpc_uuid(vpc_name):
    global skip_delete
    url = _build_url(scheme="https",resource_type="/vpcs/list")
    data = requests.post(url, json={"kind":"vpc", "filter":"name==%s"%vpc_name},
                         auth=HTTPBasicAuth(pc_username, 
                                            pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(vpc_name, PC_IP))
            skip_delete = True
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one VPC's with name - %s on - %s"%(vpc_name, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            skip_delete = False
            return data.json()['entities'][0]['metadata']['uuid']
    else:
        print("Error while fetching VPC details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
        
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "DELETE_PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json()['status'] in ['DELETE_PENDING']:
                state = 'DELETE_PENDING'
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
        
def _get_ip(IP):
    ip_list = IP.split(".")
    gatewat_digit = int(ip_list[-1]) + 1
    start_digit = gatewat_digit + 1
    end_digit = start_digit + 50
    gateway_ip = ip_list[:3]
    gateway_ip.append(str(gatewat_digit))
    gateway_ip = ".".join(gateway_ip)
    start_ip = ip_list[:3]
    start_ip.append(str(start_digit))
    start_ip = ".".join(start_ip)
    end_ip = ip_list[:3]
    end_ip.append(str(end_digit))
    end_ip = ".".join(end_ip)
    return (gateway_ip, start_ip, end_ip)
    
external_subnet_items = {}
vpc_items = {}
overlay_subnet_items = {}


#tenant = "@@{tenant_name}@@"
cluster = "@@{cluster_name}@@".strip()
cluter_uuid = _get_cluster_details(cluster)
if @@{create_external_subnet}@@:
    for x in [ "@@{external_subnet_ip}@@".strip(), "@@{external_subnet_name}@@".strip(),
               "@@{virtual_switch}@@".strip(), "@@{external_subnet_gateway_ip}@@".strip(),
                "@@{external_subnet_ip_pool}@@"]:
        if x.lower() in ["", "none", "na"]:
            print("Input Error :- Need all required parameters to create External Subnet as shown below.")
            print("External Subnet Name, External VLAN ID, External Subnet IP with Prefix, "\
                  "External Subnet IP Pool Range, External Subnet Gateway IP")
            exit(1)
            
    external_subnet = "@@{external_subnet_ip}@@".strip()
    if "/" not in external_subnet:
        print("Input Error :-- External subnet IP with Prefix should be in below format.")
        print("10.10.10.0/24")
        exit(1)
    external_subnet_ip, external_subnet_prefix = external_subnet.split("/")
    external_subnet_items['name'] = "@@{external_subnet_name}@@".strip()
    external_subnet_items['cluster'] = cluster
    external_subnet_items['enable_nat'] = @@{external_subnet_nat}@@
    external_subnet_items['virtual_switch_name'] = "@@{virtual_switch}@@".strip()
    _uuid = _get_virtual_switch_uuid(external_subnet_items['virtual_switch_name'], cluter_uuid)
    external_subnet_items['gateway_ip'] = "@@{external_subnet_gateway_ip}@@".strip()
    external_subnet_items['network_ip'] = external_subnet_ip
    external_subnet_items['prefix'] = int(external_subnet_prefix)
    IP_POOL = "@@{external_subnet_ip_pool}@@".split("-")
    external_subnet_items['ip_pools'] = {"range":"%s %s"%(IP_POOL[0],IP_POOL[1])}
    print("external_subnet_items={}".format(external_subnet_items))
else:
    print("external_subnet_items=False")

if @@{create_vpc}@@:
    vpc_items['name'] = "@@{vpc_name}@@".strip()
    vpc_items['external_subnet_name'] = "@@{external_subnet_name}@@".strip()
    print("vpc_items={}".format(vpc_items))
else:
    print("vpc_items=False")

if @@{create_overlay_subnet}@@:
    for x in ["@@{overlay_subnet_ip}@@".strip(), "@@{overlay_subnet_name}@@".strip(),
              "@@{overlay_subnet_gateway_ip}@@".strip()]:
        if x.lower() in ["", "none", "na"]:
            print("Input Error :- Need all required parameters to create Overlay Subnet as shown below.")
            print("Overlay Subnet Name, Overlay Subnet IP With Prefix, Overlay Subnet Gateway IP")
            exit(1)
            
    overlay_subnet = "@@{overlay_subnet_ip}@@".strip()
    if "/" not in overlay_subnet:
        print("Input Error :-- Overlay subnet IP with Prefix should be in below format.")
        print("10.10.10.0/24")
        exit(1)
        
    overlay_subnet_ip, overlay_subnet_prefix = overlay_subnet.split("/")
    overlay_subnet_items['subnet_name'] = "@@{overlay_subnet_name}@@".strip()
    overlay_subnet_items['vpc_name'] = "@@{vpc_name}@@".strip()
    overlay_subnet_items['network_ip'] = overlay_subnet_ip
    overlay_subnet_items['prefix'] = int(overlay_subnet_prefix)
    overlay_subnet_items['gateway_ip'] = "@@{overlay_subnet_gateway_ip}@@".strip()
    IP = _get_ip(overlay_subnet_ip)
    overlay_subnet_items['ip_pool'] = [{"ip_pools_start_ip":IP[1], 
                                     "ip_pools_end_ip":IP[2]}]
    print("overlay_subnet_items={}".format(overlay_subnet_items))
else:
    print("overlay_subnet_items=False")
