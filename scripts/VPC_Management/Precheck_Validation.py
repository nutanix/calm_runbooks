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
  
def _get_vlan_details():
    existing_subnet = "@@{external_subnet_uuid}@@"
    if existing_subnet == "NA":
        print("Input Error :- External Subnet UUID is mandatory parameter.")
        exit(1)
    _url = _build_url(scheme="https",
                    resource_type="/subnets/%s"%existing_subnet)
    _data = requests.get(_url, auth=HTTPBasicAuth(pc_username, pc_password),verify=False)
    if _data.ok:
        if _data.json().get('state', _data.json()['status']['state']) != "COMPLETE":
            print("Input Error :- Please Provide Valide External Subnet UUID")
            exit(1)      
        return _data.json()['spec']['name']
    else:
        print("Input Error :- Please Provide Valide External Subnet UUID")
        print(_data.json().get("message_list", _data.json()))
        exit(1)

if "@@{operation}@@" in ["update", "delete"]:
    if "@@{vpc_uuid}@@" == "NA":
        print("Input Error :- VPC UUID is mandatory for Update and Delete operations.")
        exit(1)

vpc_items = {}
if "@@{operation}@@" != "delete":
    if "@@{externally_routable_ip}@@".strip() == "NA":
        external_ip = "NA"
        prefix = 0
    else:
    	external_ip, prefix = "@@{externally_routable_ip}@@".strip().split("/")
    vpc_items =  {
                    "name": "@@{vpc_name}@@".strip(),
                    "dns_servers" : "@@{dns_server}@@".strip(),
                    "external_subnet_name": _get_vlan_details(),
                    "external_subnet_uuid" : "@@{external_subnet_uuid}@@",
                    "externally_routable_ip": external_ip,
                    "externally_routable_ip_prefix": int(prefix)
                }
print("vpc_items={}".format(vpc_items))
