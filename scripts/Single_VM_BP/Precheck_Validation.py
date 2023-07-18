sleep(2)
import requests
from requests.auth import HTTPBasicAuth
PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
management_pc_username = "@@{management_pc_username}@@".strip()
management_pc_password = "@@{management_pc_password}@@".strip()

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
        
def get_project_details(project_name):
    url = _build_url(scheme="https",host="localhost",resource_type="/projects/list")
    data = requests.post(url, json={"kind":"project", "filter":"name==%s"%project_name},
                        auth=HTTPBasicAuth(management_pc_username, management_pc_password),
                        timeout=None, verify=False)
    if data.ok:
        if data.json()["metadata"]["total_matches"] == 1:
            print("project_uuid={}".format(data.json()["entities"][0]["metadata"]["uuid"]))
        else:
            print("Failed to get correct project details. Make sure project name is correct.")
            print(data.json().get('message_list',data.json().get('error_detail', data.json())))
            exit(1)
    else:
        print("Error in fetching project details.")
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1)
        
def get_cluster_details(cluster_name):
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
                return 
        print("Input Error :- Given cluster %s not present on %s"%(cluster_name, PC_IP))
        exit(1)
    else:
        print("Error while fetching %s cluster info"%cluster_name)
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1)
        
def get_subnet_uuid(subnet_name):
    url = _build_url(scheme="https",resource_type="/subnets/list")
    data = requests.post(url, json={"kind":"subnet", "filter":"name==%s"%subnet_name},
                         auth=HTTPBasicAuth(pc_username, pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s not present on %s"%(subnet_name, PC_IP))
            exit(1)
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one subnets with name - %s on - %s"%(subnet_name, PC_IP))
            print("Please delete it manually before executing runbook.")
            exit(1)
        else:
            print("subnet_uuid={}".format(data.json()['entities'][0]['metadata']['uuid']))
            print("vpc_uuid={}".format(data.json()["entities"][0]["spec"]\
                                ["resources"]["vpc_reference"]["uuid"]))
    else:
        print("Error while fetching subnet details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)
        
def get_image_uuid(image_name):
    url = _build_url(scheme="https",resource_type="/images/list")
    data = requests.post(url, json={"kind":"image", "filter":"name==%s"%image_name},
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    if data.ok:
        print("image_uuid={}".format(data.json()['entities'][0]['metadata']['uuid']))
    else:
        print("Error -- %s Image not present on %s"%(image_name, PC_IP))
        exit(1)
        
def get_account_uuid(account_name,cluster_name):
    url = _build_url(scheme="https",host="localhost",resource_type="/accounts/list")
    data = requests.post(url, json={"kind":"account"},
                        auth=HTTPBasicAuth(management_pc_username, management_pc_password),
                        timeout=None, verify=False)       
    if account_name in str(data.json()):
        for new_data in data.json()['entities']:
            if new_data['metadata']['name'] == account_name:
                for _cluster in new_data["status"]["resources"]["data"]["cluster_account_reference_list"]:
                    if _cluster["resources"]["data"]["cluster_name"] == cluster_name:
                        account_uuid = _cluster["uuid"]
                        print("account_uuid={}".format(account_uuid))
    else:
        print("Error : %s account not present on %s"%(account_name,PC_IP))
        exit(1)  
        
def get_environment_details(env_name):
    url = _build_url(scheme="https",host="localhost",resource_type="/environments/list")
    data = requests.post(url, json={"kind":"environment", "filter":"name==%s"%env_name},
                         auth=HTTPBasicAuth(management_pc_username, management_pc_password),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s environment not present on %s"%(env_name, PC_IP))
            exit(1)
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one environment with name - %s on - %s"%(env_name, PC_IP))
            exit(1)
        else:
            print("environment_uuid={}".format(data.json()['entities'][0]['metadata']['uuid']))
    else:
        print("Error while fetching environment details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)

get_project_details("@@{project_name}@@".strip())
get_cluster_details("@@{cluster_name}@@".strip())
get_subnet_uuid("@@{subnet_name}@@".strip())
get_image_uuid("@@{image_name}@@".strip())
get_account_uuid("@@{account_name}@@".strip(),"@@{cluster_name}@@".strip())
get_environment_details("@@{environment_name}@@".strip())
