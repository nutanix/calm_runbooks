import requests
from requests.auth import HTTPBasicAuth

management_pc_ip = "@@{management_pc_ip}@@".strip()
management_username = "@@{management_pc_username}@@".strip()
management_password = "@@{management_pc_password}@@".strip()
management_pc_config = {
    "username": management_username,
    "password": management_password,
    "ip": management_pc_ip
}

PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_passwd = "@@{prism_central_passwd}@@".strip()
workload_pc_config = {
    "username": pc_username,
    "password": pc_passwd,
    "ip": PC_IP
}

pc_config = {
    "workload": workload_pc_config,
    "management": management_pc_config
}

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

def _get_vpc_details(vpc_name, pc_config):
    vpc_name = vpc_name.strip()
    vpc_details = {"kind": "vpc"}
    url = _build_url(scheme="https",resource_type="/vpcs/list", host=pc_config['ip'])               
    data = requests.post(url, json=vpc_details,
                         auth=HTTPBasicAuth(pc_config["username"], pc_config["password"]),verify=False)
    if vpc_name in str(data.json()):
        for _vpc in data.json()['entities']:
            if _vpc['spec']['name'] == vpc_name:
                return _vpc['metadata']['uuid']
        print("%s VPC not present on %s"%(vpc_name, PC_IP))
        exit(1)
    else:
        print("Input Error ---> %s VPC not present on %s"%(vpc_name, PC_IP))
        exit(1)
        
def _get_subnet_details(subnet_name, pc_config):
    subnet_name = subnet_name.strip()
    url = _build_url(scheme="https",resource_type="/subnets/list", host=pc_config['ip'])               
    data = requests.post(url, json={"kind": "subnet", "filter":"name==%s"%subnet_name},
                         auth=HTTPBasicAuth(pc_config["username"], pc_config["password"]),verify=False)
    if subnet_name in str(data.json()):
        for _subnet in data.json()['entities']:
            if _subnet['spec']['name'] == subnet_name:
                return _subnet['metadata']['uuid']
        print("%s Subnet not present on %s"%(subnet_name, PC_IP))
        exit(1)
    else:
        print("Input Error ---> %s Subnet not present on %s"%(subnet_name, PC_IP))
        exit(1)
        
def _get_project_details(project_name, pc_config):
    project_name = project_name.strip()
    url = _build_url(scheme="https",resource_type="/projects/list", host=pc_config['ip'])               
    data = requests.post(url, json={"kind": "project"},
                         auth=HTTPBasicAuth(pc_config["username"], pc_config["password"]),
                         verify=False)
    if project_name in str(data.json()):
        for _project in data.json()['entities']:
            if _project['spec']['name'] == project_name:
                return _project['metadata']['uuid']
        print("%s Project not present on %s"%(project_name, pc_config.get('ip')))
        exit(1)
    else:
        print("Input Error ---> %s Project not present on %s"%(project_name, pc_config.get('ip')))
        exit(1)

if "@@{add_subnet_to_project}@@".lower() == "yes":
    if "@@{project_name}@@".strip() not in ["","na", "none"]:
        project_uuid = _get_project_details("@@{project_name}@@", pc_config.get("management"))
        print("project_uuid={}".format(project_uuid))
    else:
        print("Input Error :- Provide Valid Project Name to map Overlay subnet into project.")
        exit(1)
        
overlay_subnet_items = {}
subnet_uuid = ""
if "@@{operation}@@" in ["update", "delete"]:
    subnet_uuid = _get_subnet_details("@@{vlan_name}@@", pc_config.get("workload"))
    print("vlan_uuid={}".format(subnet_uuid))
        
if "@@{vlan_name}@@".strip().lower() in ["", "na", "none"]:
    print("Input Error :- Provide valid Overlay Subnet Name.")
    exit(1)
    
if "@@{operation}@@" != "delete":
    if ("@@{network_ip}@@".strip().lower() in ["", "na", "none"]) or ( "/" not in "@@{network_ip}@@"):
        print("Please provide valide network IP with Prefix.")
        print("Example :- 10.10.10.0/24")
        exit(1)
    network_ip, prefix = "@@{network_ip}@@".split("/")
    
    dns_servers = "@@{dns_servers}@@".split(",")
    if "@@{dns_servers}@@".strip().lower() in ["", "na", "none"]:
        dns_servers = []
        
    domain_search = "@@{domain_search}@@".split(",")
    if "@@{gateway_ip}@@" == "NA":
        print("Input Error :- Gateway IP is a mandatory parameter.")
        exit(1)
        
    if "@@{vpc_name}@@".strip().lower() in ["", "na", "none"]:
        print("Input Error :- Provide valid VPC name for Create and Update operations.")
        exit(1)
        
    ip_pool = []
    start_ip = end_ip = "NA"
    if "@@{ip_pool}@@".strip().lower() not in ["", "na", "none"]:
        ip_pools = "@@{ip_pool}@@".strip().split(",")
        for ip in ip_pools:
            if "-" not in ip:
                print("Input Error :- Please Provide IP Pool in below format.")
                print("Example :- 10.10.10.2-10.10.10.8")
                exit(1)
            start_ip, end_ip = ip.split("-")
            ip_pool.append({"start_ip":start_ip.strip(), "end_ip":end_ip.strip()})
            
    overlay_subnet_items =  {
                              "overlay_subnet": {
                                "vlan_uuid":subnet_uuid,
                                "vpc": {"uuid": _get_vpc_details("@@{vpc_name}@@", pc_config.get("workload"))},
                                "ipam": {
                                  "dhcp": {
                                    "dns_servers": dns_servers,
                                    "domain_name": "@@{domain_name}@@".strip(),
                                    "domain_search": domain_search,
                                    "boot_file_name":"@@{boot_file_name}@@".strip(),
                                    "tftp_server":"@@{tftp_server}@@".strip()
                                  },
                                  "ip_pools": ip_pool,
                                  "gateway_ip": "@@{gateway_ip}@@".strip(),
                                  "network_ip": network_ip,
                                  "network_prefix": int(prefix)
                                  }
                               }
                            }
print("overlay_subnet_items={}".format(overlay_subnet_items))
