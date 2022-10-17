# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_user = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
dr_username = "@@{dr_account_username}@@".strip()
dr_password = "@@{dr_account_password}@@".strip()
DR_PC_IP = "@@{dr_account_url}@@".strip()

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
    
def get_vm_uuid(vm):
    url = _build_url(scheme="https",
                    resource_type="/ngt/list")
    data = requests.post(url, json={"kind":"ngt"},
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if data.ok:
        for _vm in data.json()["entities"]:
            uuid = _vm["vm_uuid"]
            _url = _build_url(scheme="https",
                             resource_type="/vms/%s"%uuid)
            _data = requests.get(_url,auth=HTTPBasicAuth(pc_user,pc_password),
                                 timeout=None, verify=False)
            if _data.ok:
                if _data.json()["spec"]["name"] == vm:
                    if _vm["network_configuration"][0]["ip_info_list"][0]["ip_type"] == "STATIC": 
                        return _data.json()["metadata"]["uuid"]
                    else:
                        print("%s VM has not static IP configured. VM Should"\
                            " have Static IP configured for Static IP Mapping."%vm)
                        exit(1)
        print("Input Error :- %s VM is not present or NGT is not installed properly on VM."%vm)
        exit(1)
    else:
        print("Error while fetching VM details :- ",data.json())
        exit(1)
        
def _get_subnet_details(subnet, PC, user, password):
    url = _build_url(scheme="https",host=PC, resource_type="/subnets/list")
    data = requests.post(url, json={"kind":"subnet", "filter":"name==%s"%subnet},
                         auth=HTTPBasicAuth(user, password),
                         timeout=None, verify=False)
    subnet_uuid = ""
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(subnet, PC_IP))
            exit(1)
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one subnets with name - %s on - %s"%(subnet, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            subnet_uuid = data.json()['entities'][0]['metadata']['uuid']
    else:
        print("Error while fetching %s subnet details :- "%subnet,data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
        
    url = _build_url(scheme="https", host=PC, resource_type="/subnets/%s"%subnet_uuid)
    data = requests.get(url, auth=HTTPBasicAuth(user, password), verify=False)
    if data.ok:
        if "ip_config" in data.json()["spec"]["resources"].keys():
            gateway = data.json()["spec"]["resources"]["ip_config"]["default_gateway_ip"]
            prefix = data.json()["spec"]["resources"]["ip_config"]["prefix_length"]
            return gateway,prefix
        else:
            return "NA", "NA"
    else:
        print("Error while fetching subnet details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)    
        
def _get_cluster_details(cluster_name, host, username, password):
    payload = {"kind": "cluster"}
    url = _build_url(scheme="https", host=host,
                    resource_type="/clusters/list")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(username,password), 
                         verify=False)
    if data.ok:
        for _cluster in data.json()['entities']:
            if _cluster['status']['name'] == cluster_name:
                return _cluster['metadata']['uuid']
        print("Input Error :- Given cluster %s not present on %s"%(cluster_name, host))
        exit(1)
    else:
        print("Error while fetching %s cluster info"%cluster_name)
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1) 
        
primary_cluster_uuid = _get_cluster_details(cluster_name = "@@{primary_account_cluster}@@",
                                            host=PC_IP, username=pc_user, password=pc_password)
recovery_cluster_uuid = _get_cluster_details(cluster_name = "@@{dr_account_cluster}@@".strip(),
                                             host="@@{dr_account_url}@@".strip(), 
                                             username="@@{dr_account_username}@@".strip(), 
                                             password="@@{dr_account_password}@@".strip())

print("primary_cluster_uuid={}".format(primary_cluster_uuid))
print("recovery_cluster_uuid={}".format(recovery_cluster_uuid))

category = @@{vm_category}@@
policy_category = {}
for x in category.keys():
    policy_category[x] = [category[x]]

dr_account_items = {
                    "url" : "@@{dr_account_url}@@".strip(),
                    "username" : "@@{dr_account_username}@@".strip(),
                    "passwd" : "@@{dr_account_password}@@".strip(),
                    "sync_interval_secs" : 3500
                    }

print("dr_account_items={}".format(dr_account_items))

protection_policy_items = {
                            'name': "@@{protection_policy_name}@@".strip(),
                            'source_az': "@@{PC_IP}@@".strip(),
                            'dest_az': "@@{dr_account_url}@@".strip(),
                            'vm_category':policy_category
                           }
print("protection_policy_items={}".format(protection_policy_items))

IP1, prefix1 = _get_subnet_details("@@{primary_network_prod_name}@@".strip(),PC_IP, pc_user, pc_password)
IP2, prefix2 = _get_subnet_details("@@{primary_network_test_name}@@".strip(),PC_IP, pc_user, pc_password)
IP3, prefix3 = _get_subnet_details("@@{dr_network_prod_name}@@".strip(),DR_PC_IP, dr_username, dr_password)
IP4, prefix4 = _get_subnet_details("@@{dr_network_test_name}@@".strip(),DR_PC_IP, dr_username, dr_password)

recovery_plan_items = {
                        'name' : "@@{recovery_plan_name}@@".strip(),
                        'power_on_sequence' : category,
                        'recovery_network_prod' : {'name' : "@@{primary_network_prod_name}@@".strip(),
                                                   'gateway' : IP1,
                                                   'prifix' : prefix1
                        },
                        'recovery_network_test' : {'name' : "@@{primary_network_test_name}@@".strip(),
                                                   'gateway' : IP2,
                                                   'prifix' : prefix2
                        },
                        'dr_network_prod' : {'name' : "@@{dr_network_prod_name}@@".strip(),
                                             'gateway' : IP3,
                                             'prifix' : prefix3
                        },
                        'dr_network_test' : {'name' : "@@{dr_network_test_name}@@".strip(),
                                             'gateway' : IP4,
                                             'prifix' : prefix4
                        }
                      }
print("recovery_plan_items={}".format(recovery_plan_items))

if (@@{static_ip_mapping}@@) and ("@@{vm_name}@@".strip().lower() not in ["", "none", "na"]):
    VM = "@@{vm_name}@@".strip()
    primary_prod = "@@{primary_network_prod_static_ip}@@".strip().split(",")
    primary_test = "@@{primary_network_test_static_ip}@@".strip().split(",")
    dr_prod = "@@{dr_network_prod_static_ip}@@".strip().split(",")
    dr_test = "@@{dr_network_test_static_ip}@@".strip().split(",")
    for x in VM.split(","):
        uuid = get_vm_uuid(x.strip())
    for x in [primary_prod, primary_test, dr_prod, dr_test]:
        if len(VM.split(",")) != len(x):
            print("Input Error :- Please provide proper static IP mapping between VM's list and %s"%x)
            print("Number of quama separated VM's should be equal to number of Primary Network Prod Static IP," \
                      "Primary Network Test Static IP, DR Network Prod Static IP, DR Network Test Static IP")
            exit(1)
        
delay = @@{stage_delay}@@
replication = @@{custom_rpo_interval_replication}@@
if replication < 1:
    print("custom_rpo_interval_replication=1")
    print("Info : Replication RPO Interval is less than '1' hence using default value of '1'.")
    
local = @@{custom_rpo_interval_local}@@
if local < 1:
    if @@{local_schedule}@@:
        print("custom_rpo_interval_local=1")
        print("Info : Local RPO Interval is less than '1' hence using default value of '1'.")
        
retention = @@{number_of_snapshot_retention}@@
if retention < 1:
    print("number_of_snapshot_retention=1")
    print("Info : Number of Snapshot Retention is less than '1' hence using default value of '1'.")

time = "@@{policy_schedule_time}@@".strip()
if time != "Immediate":
    if ":" in time:
        t1, t2 = time.split(":")
        try:
            if (t1[-1] != "h") or (t2[-1] != "m"):
                print("Input Error :- Please provide 'Policy Schedule Time From Now' in Proper format.")
                print("Example :- 10h:30m")
                exit(1)
            hours = int(t1[:-1])
            minutes = int(t2[:-1])
            if not hours:
                hours = "00"
            if minutes:
                print("policy_schedule_time={}".format("@@{policy_schedule_time}@@".strip()))
            else:
                print("policy_schedule_time={}".format("@@{policy_schedule_time}@@".strip()))
        except Exception as ValueError:
            print("Input Error :- Please provide 'Policy Schedule Time From Now' in Proper format.")
            print("Example :- 10h:30m")
            exit(1)
    else:
        print("Input Error :- Please provide 'Policy Schedule Time From Now' in below format.")
        print("Example :- 10h:30m")
        exit(1)
    
