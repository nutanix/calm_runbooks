# script
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

def _get_default_spec(vpc_uuid):
    priority = @@{priority}@@
    return ({
            "spec": {
                "name": "Policy with priority%s"%str(priority),
                "resources": {
                    "priority": priority,
                    "source": {},
                    "destination": {},
                    "protocol_type": "@@{protocol_type}@@".strip(),
                    "action": {
                        "action": "@@{action}@@"
                    },
                    "vpc_reference": {
                        "kind": "vpc",
                        "uuid": vpc_uuid
                    }
                }
            },
            "metadata": {
                "kind": "routing_policy"
            },
            "api_version": "3.1.0"
        })
  
def _get_vpc_details(vpc_name):
    vpc_details = {"kind": "vpc"}
    if vpc_name.lower() not in ["na", "none"]:
        vpc_details["filter"] = "name=={}".format(vpc_name)
        url = _build_url(
                    scheme="https",
                    resource_type="/vpcs/list")               
        data = requests.post(url, json=vpc_details,
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         verify=False)
        if data.ok:
            for _vpc in data.json()['entities']:
                if _vpc['spec']['name'] == vpc_name:
                    return _vpc['metadata']['uuid']
            print("Input Error ---> %s VPC not present on host"%vpc_name)
            exit(1)
        else:
            print("Input Error ---> %s VPC not present on host"%vpc_name)
            exit(1)
    else:
        print("Input Error :-- VPC name should not be NA or None")
        exit(1)
          
def create_policy_routing(**params):
    vpc_uuid = _get_vpc_details(params["vpc_name"])
    payload = _get_default_spec(vpc_uuid)
    
    if (params["source_ip_prefix"] != None) and ("@@{source_address_type}@@" == "CUSTOM"):
        s_ip, s_prefix = params["source_ip_prefix"].split("/")
        payload["spec"]["resources"]["source"] = {"ip_subnet":{"ip":s_ip,
                                                 "prefix_length":int(s_prefix)}}
    else:
        payload["spec"]["resources"]["source"]["address_type"] = "@@{source_address_type}@@".strip()
        
    if (params["dest_ip_prefix"] != None) and ("@@{dest_address_type}@@" == "CUSTOM"):
        d_ip, d_prefix = params["dest_ip_prefix"].split("/")
        payload["spec"]["resources"]["destination"] = {"ip_subnet":{"ip":d_ip,
                                                      "prefix_length":int(d_prefix)}}
    else:
        payload["spec"]["resources"]["destination"]["address_type"] = "@@{dest_address_type}@@".strip()
        
    if ("@@{protocol_type}@@" == "PROTOCOL_NUMBER") and (@@{protocol_number}@@ != 0):
        payload["spec"]["resources"]["protocol_parameters"] = \
                            {"protocol_number": @@{protocol_number}@@}
      
    if "@@{action}@@" == "REROUTE":
        payload["spec"]["resources"]["action"]["service_ip_list"] = ["@@{service_ip_list}@@".strip()]
        
    if @@{bidirection}@@:
        payload["spec"]["resources"]["is_bidirectional"] = True
        
    if "@@{protocol_type}@@" == "ICMP":
        if "@@{icmp_protocol_parameter_type}@@".strip().lower() not in ["na", "none", "any", ""]:
            payload["spec"]["resources"]["protocol_parameters"] = {}
            payload["spec"]["resources"]["protocol_parameters"]["icmp"] = {}
            if "@@{icmp_protocol_parameter_code}@@".strip().lower() not in ["na", "none", "any", ""]:
                payload["spec"]["resources"]["protocol_parameters"]["icmp"]["icmp_code"] = \
                                            int("@@{icmp_protocol_parameter_code}@@".strip())
                
            payload["spec"]["resources"]["protocol_parameters"]["icmp"]["icmp_type"] = \
                                            int("@@{icmp_protocol_parameter_type}@@".strip())
    
    if "@@{protocol_type}@@" in ["TCP", "UDP"]:
        _protocol = "tcp"
        if "@@{protocol_type}@@" == "UDP":
            _protocol = "udp"
        payload["spec"]["resources"]["protocol_parameters"] = {_protocol:{}}
        if "@@{source_port_range_list}@@".strip().lower() not in ["", "na", "none"]:
            start_port = end_port = "@@{source_port_range_list}@@".strip()
            if "-" in "@@{source_port_range_list}@@":
                start_port, end_port = "@@{source_port_range_list}@@".split("-")
            payload["spec"]["resources"]["protocol_parameters"][_protocol]["source_port_range_list"] = []
            payload["spec"]["resources"]["protocol_parameters"][_protocol]\
                ["source_port_range_list"].append({"start_port": int(start_port.strip()), 
                                                   "end_port": int(end_port.strip())})
            
        if "@@{destination_port_range_list}@@".strip().lower() not in ["", "na", "none"]:
            start_port = end_port = "@@{destination_port_range_list}@@".strip()
            if "-" in "@@{destination_port_range_list}@@":
                start_port, end_port = "@@{destination_port_range_list}@@".split("-")
            payload["spec"]["resources"]["protocol_parameters"][_protocol]["destination_port_range_list"] = []
            payload["spec"]["resources"]["protocol_parameters"][_protocol]\
                ["destination_port_range_list"].append({"start_port": int(start_port.strip()),
                                                        "end_port": int(end_port.strip())})
            
        if payload["spec"]["resources"]["protocol_parameters"][_protocol] == {}:
            del payload["spec"]["resources"]["protocol_parameters"]
            
    pprint(payload)
    url = _build_url(scheme="https",
                    resource_type="/routing_policies")
    data = requests.post(url, json=payload, 
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    wait_for_completion(data)

def delete_policy_routing():
    vpc_uuid = _get_vpc_details("@@{vpc_name}@@".strip())
    priority = @@{priority}@@
    policy_name = "Policy with priority%s"%str(priority)
    url = _build_url(scheme="https",
                    resource_type="/routing_policies/list")
    data = requests.post(url, json={"kind":"routing_policy"},
                         auth=HTTPBasicAuth(pc_username, pc_password), 
                         verify=False)
    uuid = ""
    if data.ok:
        if policy_name in str(data.json()["entities"]):
            for _policy in data.json()["entities"]:
                if (_policy["spec"]["resources"]["priority"] == priority) and \
                        (_policy["spec"]["resources"]["vpc_reference"]["uuid"] == vpc_uuid):
                    uuid = _policy["metadata"]["uuid"]
        else:
            print("Input Error :-- Routing policy with %s priority does not exists "\
                  "for @@{vpc_name}@@ VPC."%str(priority))
            exit(1)
    else:
        print("Error while fetching policy details with priority - %s."%str(priority))
        print(data.json())
        exit(1)
        
    url = _build_url(scheme="https",
                    resource_type="/routing_policies/%s"%uuid)
    data = requests.delete(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                           verify=False)
    wait_for_completion(data)
    
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            response = requests.get(url, auth=HTTPBasicAuth(pc_username, pc_password), 
                                    verify=False)
            if response.json()['status'] in ['PENDING', 'RUNNING', 'DELETE_PENDING']:
                state = 'PENDING'
                sleep(5)                
            elif response.json()['status'] == 'FAILED':
                print("Error while Routing Policy Opearion---> ",response.json())
                state = 'FAILED'
                exit(1)
            else:
                state = 'SUCCESSED'
    else:
        state = data.json().get('state')
        print("Error while Routing Policy Operation --->",data.json())
        exit(1)

priority = @@{priority}@@
if (priority < 10) or (priority > 1000):
    print("Input Erorr :-- Priority Should be between 10 and 1000.")
    exit(1)
    
if "@@{operation}@@" == "CREATE":
    source_ip_prefix = "@@{source_ip_prefix}@@".strip()
    if source_ip_prefix.lower() not in ["", "na", "none"]:
        if "/" in source_ip_prefix:
            ip, prefix = source_ip_prefix.split("/")
            if len(ip.split(".")) != 4:
                print("Input Error :-- Please provide Source IP with Prefix in correct format as below.")
                print("Example := 10.10.10.0/24")
                exit(1)
        else:
            print("Input Error :-- Please provide Source IP with Prefix in correct format as below.")
            print("Example := 10.10.10.0/24")
            exit(1)
    else:
        source_ip_prefix = None
    
    dest_ip_prefix = "@@{destination_ip_prefix}@@".strip()
    if dest_ip_prefix.lower() not in ["", "na", "none"]:
        if "/" in dest_ip_prefix:
            ip, prefix = dest_ip_prefix.split("/")
            if len(ip.split(".")) != 4:
                print("Input Error :-- Please provide Destination IP with Prefix in correct format as below.")
                print("Example := 10.10.10.0/24")
                exit(1)
        else:
            print("Input Error :-- Please provide Destination IP with Prefix in correct format as below.")
            print("Example := 10.10.10.0/24")
            exit(1)
    else:
        dest_ip_prefix = None
    
    if "@@{action}@@" == "REROUTE":
        if "@@{service_ip_list}@@".lower() in ["", "na", "none"]:
            print("Input Error :-- Service IP for REROUTE should not be NA, None or empty for Action=REROUTE")
            print("Please provide IP in correct format. IE : 10.10.10.10")
            exit(1)

    if ("@@{protocol_type}@@" == "PROTOCOL_NUMBER") and (@@{protocol_number}@@ == 0):
        print("Input Error :-- PROTOCOL NUMBER should not be Zero [ 0 ].")
        exit(1)
    
    params = {
              "vpc_name":"@@{vpc_name}@@".strip(),
              "source_ip_prefix": source_ip_prefix,
              "dest_ip_prefix": dest_ip_prefix
             }
    print("##### Createing Policy based routing for %s VPC #####"%params["vpc_name"])
    create_policy_routing(**params)
    print("Success !!!")
else:
    print("##### Deleting Policy based routing with %s Priority #####"%priority)
    try:
        delete_policy_routing()
        print("Success !!!")
    except Exception as e:
        print("Failed to delete policy based route of VPC.")
        raise(e)   
