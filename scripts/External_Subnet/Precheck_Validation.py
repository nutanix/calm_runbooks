
import requests
from requests.auth import HTTPBasicAuth

PC_IP =  "@@{PC_IP}@@".strip()
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
  
def _get_vlan_id():
    url = _build_url(scheme="https",resource_type="/subnets/list")
    data = requests.post(url, json={"kind":"subnet"},
                         auth=HTTPBasicAuth(pc_username, 
                                            pc_password),
                         timeout=None, verify=False)
    if data.ok:
        vlan_id = []
        for x in data.json()['entities']:
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
        
if "@@{operation}@@" in ["update", "delete"]:
    if "@@{vlan_uuid}@@" == "NA":
        print("Input Error :- External VLAN UUID is "\
              "mandatory for Update and Delete Operation.")
        exit(1)

external_subnet_items = {}
if "@@{operation}@@" != "delete":
    mandatory_list = {"Cluster Name":"@@{cluster_name}@@".strip(), 
                      "Subnet Name":"@@{vlan_name}@@".strip(), 
                      "Gateway IP":"@@{gateway_ip}@@".strip(), 
                      "Network IP with Prefix":"@@{network_ip}@@".strip()}
    for x in mandatory_list.keys():
        if mandatory_list[x] == "NA":
            print("Input Error :- %s is mandatory for Create and Update operations."%x)
            exit(1)
    ip_pool = []
    ip_pools = "@@{ip_pools}@@".strip().split(",")
    for ip in ip_pools:
        if "-" not in ip:
            print("Input Error :- Please provide IP Pool in below format.")
            print("Example :- 10.10.10.2-10.10.10.9")
            exit(1)
        start_ip, end_ip = ip.split("-")
        ip_pool.append({"start_ip":start_ip, "end_ip":end_ip})
        
    if "/" not in "@@{network_ip}@@":
        print("Input Error :- Please provide Network IP with Prefix in below format.")
        print("Example :- 10.10.10.0/24")
        exit(1)
    network_ip, network_prefix = "@@{network_ip}@@".strip().split("/")
    external_subnet_items = {
                              "external_subnet": {
                              "vlan_uuid" : "@@{vlan_uuid}@@",
                              "vlan_id": @@{vlan_id}@@,
                               "cluster": {
                                   "name": "@@{cluster_name}@@".strip()
                                },
                                "enable_nat": @@{enable_nat}@@,
                                "ipam": {
                                    "gateway_ip": "@@{gateway_ip}@@".strip(),
                                    "network_ip": network_ip,
                                    "network_prefix": int(network_prefix),
                                    "ip_pools": ip_pool
                                	}
                                }
                            }
print("external_subnet_items={}".format(external_subnet_items))
