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
        print("Input Error :- VLAN UUID is a mandatory parameter"\
            " for Update and Delete operations.")
        exit(1)

vlan_subnet_items = {}
if "@@{operation}@@" != "delete":
    if "@@{cluster_name}@@".strip() == "NA":
        print("Input Error :- Cluster Name is a mandatory parameter"\
            " for Create and Update operations.")
        exit(1)
    if "@@{virtual_switch_name}@@".strip() == "NA":
        print("Input Error :- Virtual Switch Name is a mandatory parameter"\
            " for Create and Update operations.")
        exit(1)
    network_ip = start_ip = end_ip = "NA"
    domain_search = dns_servers = ['NA']
    network_prefix = 0
    if "/" not in "@@{network_ip}@@".strip():
        print("Input Error :- Please Provide Network IP and Prefix in below format.")
        print("Example :- 10.10.10.0/24")
        exit(1)
    if "@@{network_ip}@@".strip() != "NA":
        #print("Input Error :- Network Ip with Prefix is a mandatory parameter.")
        #exit(1)
        network_ip, network_prefix = "@@{network_ip}@@".split("/")
    if "@@{dns_servers}@@".strip() != "NA":
    	dns_servers = "@@{dns_servers}@@".strip().split(",")
    IP = "@@{ip_pools}@@".strip()
    if "-" not in IP:
        print("Input Error :- Please Provide IP Pool in below format.")
        print("Example :- 10.10.10.2-10.10.10.8")
        exit(1)
    if IP != "NA":
        start_ip, end_ip = IP.split("-")
    if "@@{domain_search}@@".strip() != "NA":
        domain_search = "@@{domain_search}@@".strip().split(",")
    vlan_subnet_items = {
                      "vlan_subnet": {
                        "vlan_uuid" : "@@{vlan_uuid}@@",
                        "cluster": {
                            "name": "@@{cluster_name}@@".strip()
                        },
                        "virtual_switch_name": "@@{virtual_switch_name}@@".strip(),
                        "vlan_id": @@{vlan_id}@@,
                        "ipam": {
                            "dhcp": {
                                "dns_servers": dns_servers,
                                "domain_name": "@@{domain_name}@@".strip(),
                                "domain_search": domain_search,
                                "boot_file_name":"@@{boot_file_name}@@".strip(),
                                "tftp_server":"@@{tftp_server}@@".strip()
                              },
                              "ip_pools": [
                                {
                                  "end_ip": end_ip,
                                  "start_ip": start_ip
                                }
                              ],
                          "gateway_ip": "@@{gateway_ip}@@".strip(),
                          "network_ip": network_ip,
                          "network_prefix": int(network_prefix)
      
                        }
                      }
                    }
                    
print("vlan_subnet_items={}".format(vlan_subnet_items))
