# script

import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
mgmt_pc_username = "@@{prism_central_username}@@".strip()
mgmt_pc_password = "@@{management_pc_password}@@".strip()
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
        
def get_subnet_details(_uuid):
    url = _build_url(scheme="https",resource_type="/subnets/%s"%_uuid)
    data = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    if not data.ok:
        print("Error while fetching project subnet details.")
        print(data.json().get('message_list',\
            data.json().get('error_detail', data.json())))
        exit(1)
    else:
        print("project_subnet_address={}".format(data.json()['spec']\
            ['resources']['ip_config']['pool_list'][0]['range'].split( )[-1]))
        
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
        
def _get_project_uuid(project_name):
    global skip_delete
    url = _build_url(scheme="https",resource_type="/projects/list", host = "localhost")
    data = requests.post(url, json={"kind":"project", "filter":"name==%s"%project_name},
                         auth=HTTPBasicAuth(mgmt_pc_username, 
                                            mgmt_pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(project_name, "Management PC"))
            skip_delete = True
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one projects with name - %s on - %s"%(project_name, "Management PC"))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            skip_delete = False
            return data.json()['entities'][0]['metadata']['uuid']
    else:
        print("Error while fetching project details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)

def _get_tunnel_uuid(tunnel_name):
    global skip_delete
    tunnel_state = ["CONNECTING","NOT_VALIDATED" ]
    url = _build_url(scheme="https",resource_type="/tunnels/list",host="localhost")
    data = requests.post(url, json={"kind": "tunnel","filter":"name==%s"%tunnel_name},
                         auth=HTTPBasicAuth(mgmt_pc_username, 
                                            mgmt_pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s does not exist"%(tunnel_name))
            skip_delete = True
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one tunnel with name - %s"%(tunnel_name))
            print("Please delete it manually before executing runbook.")
            exit(1)
        elif data.json()['entities'][0]['status']['state'] in tunnel_state:
            print("tunnel is in NOT_VALIDATED,Please delete it manually before executing runbook.")
            exit(1)
        else:
            skip_delete = False
            tunnel_uuid = data.json()['entities'][0]['status']['resources']['uuid']
            return tunnel_uuid
    else:
        print("Error while fetching tunnel details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)

def _get_network_group_uuid(tunnel_name):
    global skip_delete
    url = _build_url(scheme="https",resource_type="/network_groups/list",host="localhost")
    data = requests.post(url, json={"kind": "network_group","filter":"name==%s"%tunnel_name},
                         auth=HTTPBasicAuth(mgmt_pc_username, 
                                            mgmt_pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s does not exist"%(tunnel_name))
            skip_delete = True
        else:
            skip_delete = False
            group_uuid = data.json()['entities'][0]['status']['resources']['uuid']
            return group_uuid
    else:
        print("Error while fetching network group details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)

def delete_project_environment(project_name):
    print("Fetching project environments information...")
    project_name = project_name.strip()
    url = _build_url(scheme="https", host="localhost",resource_type="/environments/list")
    data = requests.post(url, json={"kind":"environment"},
                         auth=HTTPBasicAuth(mgmt_pc_username, 
                                            mgmt_pc_password),
                           timeout=None, verify=False)
    uuid_list = []
    if data.ok:
        if data.json()["metadata"] > 0:
            for _env in data.json()["entities"]:
                if "project_reference" in _env["metadata"].keys():
                    if _env["metadata"]["project_reference"]["name"] == project_name:
                        uuid_list.append(_env["metadata"]["uuid"])
        else:
            print("Info : No environment found on localhost")
    else:
        print("Failed to fetch environment details.")
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1)
    
    for _uuid in uuid_list:
        url = _build_url(scheme="https", host="localhost",resource_type="/environments/%s"%_uuid)
        data = requests.delete(url,auth=HTTPBasicAuth(mgmt_pc_username, 
                                                  mgmt_pc_password),
                           timeout=None, verify=False)
        if data.ok:
            if "Environment with uuid %s deleted"%_uuid not in data.json()["description"]:
                print("Failed to project environment.",data.json())
                exit(1)
        else:
            print("Error while deleting project environment.")
            print(data.json().get('message_list',data.json().get('error_detail', data.json())))
            exit(1)
            
    if uuid_list != []:
        print("%s Project environment with %s uuid's deleted successfully."%(project_name, uuid_list))

def wait_for_completion(data):
    if data.ok:
        state = data.json().get('status', None).get('state', None)
        while state == "DELETE_PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if responce.json().get('status', None) in ['DELETE_PENDING']:
                state = 'DELETE_PENDING'
                sleep(5)                
            elif responce.json().get('status', None) == 'FAILED':
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
project_items = {}
idp_items = {}
account_items = {}
tunnel_items = {}

tenant = "@@{tenant_name}@@".strip()
cluster = "@@{cluster_name}@@".strip()
cluter_uuid = _get_cluster_details(cluster)
external_subnet = "@@{external_subnet_ip}@@".strip()
external_subnet_ip, external_subnet_prefix= external_subnet.split("/")
external_subnet_items['name'] = "@@{tenant_name}@@_External_Subnet"
external_subnet_items['cluster'] = cluster
external_subnet_items['enable_nat'] = @@{external_subnet_nat}@@
external_subnet_items['virtual_switch_name'] = "@@{virtual_switch}@@".strip()
_uuid = _get_virtual_switch_uuid(external_subnet_items['virtual_switch_name'], cluter_uuid)
external_subnet_items['gateway_ip'] = "@@{external_subnet_gateway_ip}@@".strip()
external_subnet_items['network_ip'] = external_subnet_ip
external_subnet_items['prefix'] = int(external_subnet_prefix)
IP_POOL = "@@{external_subnet_ip_pool}@@".strip().split("-")
external_subnet_items['ip_pools'] = {"range":"%s %s"%(IP_POOL[0],IP_POOL[1])}

vpc_items['name'] = "@@{tenant_name}@@_VPC"
vpc_items['external_subnet_name'] = external_subnet_items['name']
tunnel_items['name'] = "@@{tenant_name}@@_VPC_Tunnel"

overlay_subnet = "@@{overlay_subnet_ip}@@".strip()
overlay_subnet_ip, overlay_subnet_prefix = overlay_subnet.split("/")
overlay_subnet_items['subnet_name'] = "@@{tenant_name}@@_Overlay_Subnet"
overlay_subnet_items['vpc_name'] = vpc_items['name']
overlay_subnet_items['network_ip'] = overlay_subnet_ip
overlay_subnet_items['prefix'] = int(overlay_subnet_prefix)
overlay_subnet_items['gateway_ip'] = "@@{overlay_subnet_gateway_ip}@@".strip()
IP = _get_ip(overlay_subnet_ip)
overlay_subnet_items['ip_pool'] = [{"ip_pools_start_ip":IP[1], 
                                     "ip_pools_end_ip":IP[2]}]
print("project_subnet_address={}".format(IP[2]))

idp_items['name'] = "Tenant_{}_IDP".format("@@{tenant_name}@@".strip())
#idp_items['metadata'] = "@@{idp_metadata}@@".strip()

admin_user = "@@{project_admin_user}@@".strip()
project_subnet_uuid = ""
project_items['name'] = "{}_project".format(tenant)
project_items['tenant_users'] =  [{"admin": ["{}".format(admin_user)]}]
project_items['accounts'] = "@@{account_name}@@".strip()
project_items['allow_collaboration'] = False
#project_subnet = "@@{project_subnet_uuid}@@"
#get_subnet_details(project_subnet)
#print("project_subnet_uuid={}".format(project_subnet))
#project_items['subnets'] = ["{}".format(project_subnet)]
project_items['quotas'] = [{'storage_gb':@@{project_disk_size}@@,
                            'mem_gb':@@{project_memory}@@,
                            'vcpu':@@{project_vcpu}@@}]

account_items['cluster'] = cluster
account_items['quotas'] = [{'storage_gb':@@{project_disk_size}@@,
                            'mem_gb':@@{project_memory}@@,
                            'vcpu':@@{project_vcpu}@@}]

print("external_subnet_items={}".format(external_subnet_items))
print("vpc_items={}".format(vpc_items))
print("overlay_subnet_items={}".format(overlay_subnet_items))
print("project_items={}".format(project_items))
print("idp_items={}".format(idp_items))
print("account_items={}".format(account_items))
print("Tunnel_items={}".format(tunnel_items))


def _delete(type, uuid, **params):
    if(params.get("host",None)):
        host = params['host']
    else:
        host = PC_IP
    url = _build_url(scheme="https",host=host,resource_type="/%s/%s"%(type,uuid))
    if(params.get("username",None)):
        user_name = params['username']
    else:
        user_name = pc_username

    if(params.get("password",None)):
        pass_word = params['password']
    else:
        pass_word = pc_password
    
    data = requests.delete(url, auth=HTTPBasicAuth(user_name, pass_word),
                           timeout=None, verify=False)
    if not data.ok:
        print("Failed to delete existing %s with uuid %s."%(type, uuid))
        print("Error :- ",data.json())
        exit(1)
    else:
        wait_for_completion(data)
        
if "@@{delete_existing}@@".lower() == "yes":
    _group_uuid = _get_network_group_uuid(tunnel_name=tunnel_items['name'])
    _tunnel_uuid = _get_tunnel_uuid(tunnel_name=tunnel_items['name'])
    if skip_delete == False:
        _delete(type="network_groups/{}/tunnels".format(_group_uuid),uuid=_tunnel_uuid, username=mgmt_pc_username, password=mgmt_pc_password, host = "localhost")
        sleep(5)
    
    _uuid = _get_project_uuid(project_items['name'])

    if skip_delete == False:
        delete_project_environment(project_items['name'])
        _delete(type="projects", uuid=_uuid, host="localhost", username=mgmt_pc_username, password=mgmt_pc_password)
        
    _uuid = _get_subnet_uuid(subnet=overlay_subnet_items['subnet_name'], delete=True)
    if skip_delete == False:
        _delete(type="subnets", uuid=_uuid)
        sleep(5)
    
    _uuid = _get_vpc_uuid(vpc_items['name'])
    if skip_delete == False:
        _delete(type="vpcs", uuid=_uuid)
        sleep(5)
        
    _uuid = _get_subnet_uuid(subnet=external_subnet_items['name'], delete=True)
    if skip_delete == False:
        _delete(type="subnets", uuid=_uuid)