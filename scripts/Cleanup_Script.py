sleep(2)
import requests
from requests.auth import HTTPBasicAuth

tenant = "@@{tenant_name}@@".strip()
PC_IP = "@@{PC_IP}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()
pc_passwd = "@@{prism_central_passwd}@@".strip()

management_username = "@@{management_pc_username}@@".strip()
management_password = "@@{management_pc_password}@@".strip()

vpc_name = "{}_VPC".format(tenant)
external_subnet_name = "{}_External_Subnet".format(tenant)
overlay_subnet_name = "{}_Overlay_Subnet".format(tenant)
project_name = "{}_project".format(tenant)

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

def delete_vpc(vpc_name):
    print("Fetching %s VPC information..."%vpc_name)
    vpc_name = vpc_name.strip()
    url = _build_url(scheme="https",resource_type="/vpcs/list")               
    data = requests.post(url, json={"kind": "vpc"},
                         auth=HTTPBasicAuth(pc_username, pc_passwd),verify=False)
    _uuid = ""
    if data.ok:
        if vpc_name in str(data.json()):
            for _vpc in data.json()['entities']:
                if _vpc['spec']['name'] == vpc_name:
                    _uuid = _vpc['metadata']['uuid']
        else:
            print("%s VPC not present on %s"%(vpc_name, PC_IP))
            exit(1)
    else:
        print("Failed to fetch %s VPC details"%vpc_name)
        print(data.json())
        exit(1)
        
    if _uuid != "":
        url = _build_url(scheme="https", resource_type="/vpcs/%s"%_uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(pc_username, pc_passwd),
                               timeout=None, verify=False)
        wait_for_completion(data, pc_username, pc_passwd, PC_IP)
        print("%s VPC deleted successfully."%vpc_name)
    else:
        print("Info : %s VPC not present on %s"%(vpc_name, PC_IP))
    
def delete_subnet(subnet_name):
    print("Fetching %s subnet information..."%subnet_name)
    subnet_name = subnet_name.strip()
    url = _build_url(scheme="https",resource_type="/subnets/list") 
    data = requests.post(url, json={"kind": "subnet", "filter":"name==%s"%subnet_name},
                         auth=HTTPBasicAuth(pc_username, pc_passwd),verify=False)
    _uuid = ""
    if data.ok:
        if subnet_name in str(data.json()):
            for _subnet in data.json()['entities']:
                if _subnet['spec']['name'] == subnet_name:
                    _uuid = _subnet['metadata']['uuid']
        else:
            print("%s Subnet not present on %s"%(subnet_name, PC_IP))
            exit(1)
    else:
        print("Failed to fetch %s Subnet details"%(subnet_name))
        print(data.json())
        exit(1)
    if _uuid != "":    
        url = _build_url(scheme="https", resource_type="/subnets/%s"%_uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(pc_username, pc_passwd),
                               timeout=None, verify=False)
        wait_for_completion(data, pc_username, pc_passwd, PC_IP)
        print("%s subnet deleted successfully."%subnet_name)
    else:
        print("Info : %s subnet not present on %s"%(subnet_name, PC_IP))
    
def _get_project_uuid(project_name):
    print("Fetching project information...")
    project_name = project_name.strip()
    url = _build_url(scheme="https",host="localhost",resource_type="/projects/list")               
    data = requests.post(url, json={"kind": "project"},
                         auth=HTTPBasicAuth(management_username, 
                                            management_password),
                         verify=False)
    if data.ok:
        if project_name in str(data.json()):
            for _project in data.json()['entities']:
                if _project['spec']['name'] == project_name:
                    return _project['metadata']['uuid']
            print("%s Project not present on localhost"%(project_name))
            exit(1)
        else:
            print("%s Project not present on localhost"%(project_name))
            exit(1)
    else:
        print("Failed to fetch %s project details"%(project_name))
        print(data.json())
        exit(1)
        
def delete_project(project_name):
    print("Deleting project %s"%project_name)
    project_name = project_name.strip()
    _uuid = _get_project_uuid(project_name)
    url = _build_url(scheme="https", host="localhost",resource_type="/projects/%s"%_uuid)
    data = requests.delete(url, auth=HTTPBasicAuth(management_username, 
                                                   management_password),
                           timeout=None, verify=False)
    wait_for_completion(data, management_username, management_password, "localhost")
    print("%s Project deleted successfully."%project_name)    
    
def delete_app_protection_policies(project_name):
    print("Fetching app protection policies information...")
    project_uuid = _get_project_uuid(project_name)
    url = "https://localhost:9440/api/calm/v3.0/app_protection_policies/list"
    data = requests.post(url, json={"filter":"project_reference==%s"%project_uuid,"length":20},
                         auth=HTTPBasicAuth(management_username, 
                                            management_password),
                           timeout=None, verify=False)
    uuid_list = []
    if data.ok:
        if data.json()["metadata"]["total_matches"] > 0:
            for _policy in data.json()["entities"]:
                uuid_list.append(_policy["metadata"]["uuid"])
        else:
            print("Info : No App protection policies present on Localhost for %s"%project_name)
    else:
        print("Failed to fetch app protection policies for %s project."%project_name)
        print(data.json())
        exit(1)
        
    for _uuid in uuid_list:
        url = "https://localhost:9440/api/calm/v3.0/app_protection_policies/%s"%_uuid
        data = requests.delete(url, auth=HTTPBasicAuth(management_username, 
                                                       management_password),
                               timeout=None, verify=False)
        if data.ok:
            if "App protection policy with uuid %s deleted"%_uuid not in data.json()["description"]:
                print("Failed to delete App snapshot policy.",data.json())
                exit(1)
        else:
            print("Error while deleting App snapshot policy.")
            print(data.json().get('message_list',data.json().get('error_detail', data.json())))
            exit(1)
            
    if uuid_list != []:    
        print("App protection policies for %s Project deleted successfully."%project_name)        
        
def delete_applications(project_name):
    print("Fetching applications information...")
    project_name = project_name.strip()
    project_uuid = _get_project_uuid(project_name)
    url = _build_url(scheme="https", host="localhost",resource_type="/apps/list")
    data = requests.post(url, json={"kind":"app"},
                         auth=HTTPBasicAuth(management_username, 
                                            management_password),
                           timeout=None, verify=False)
    uuid_list = []
    if data.ok:
        if data.json()["metadata"]["total_matches"] > 0:
            for _app in data.json()["entities"]:
                if (_app["metadata"]["project_reference"]["name"] == "_internal") \
                      and (_app["metadata"]["name"] == "%s_VPC_Tunnel_application"%tenant):
                    uuid_list.append(_app["metadata"]["uuid"])
                
                if _app["metadata"]["project_reference"]["name"] == project_name:
                    uuid_list.append(_app["metadata"]["uuid"])
        else:
            print("Info : No applications found on localhost")
    else:
        print("Failed to fetch application details -- ",data.json())
        exit(1)
        
    for _uuid in uuid_list:
        url = _build_url(scheme="https", host="localhost",resource_type="/apps/%s"%_uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(management_username, 
                                                       management_password),
                               timeout=None, verify=False)    
        task_uuid = data.json()["status"]["ergon_task_uuid"]
        wait_for_completion(data, management_username, management_password, "localhost", task_uuid)
    if uuid_list != []:
        print("%s Project Applications deleted successfully."%project_name)
    
def delete_blueprints(project_name):
    print("Fetching blueprints information...")
    project_name = project_name.strip()
    url = _build_url(scheme="https", host="localhost",resource_type="/blueprints/list")
    data = requests.post(url, json={"kind":"blueprint"},
                         auth=HTTPBasicAuth(management_username, 
                                            management_password),
                           timeout=None, verify=False)
    uuid_list = []
    if data.ok:
        if data.json()["metadata"]["total_matches"] > 0:
            for _app in data.json()["entities"]:
                if _app["metadata"]["project_reference"]["name"] == project_name:
                    uuid_list.append(_app["metadata"]["uuid"])
        else:
            print("Info : No Blueprints found on localhost")
    else:
        print("Failed to fetch blueprints details -- ",data.json())
        exit(1)
        
    for _uuid in uuid_list:
        url = _build_url(scheme="https", host="localhost",resource_type="/blueprints/%s"%_uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(management_username, 
                                                       management_password),
                               timeout=None, verify=False)    
        if data.ok:
            url = _build_url(scheme="https", host="localhost",resource_type="/blueprints/list")
            data = requests.post(url, json={"length":20,"offset":0,"filter":"state!=DELETED"},
                                 auth=HTTPBasicAuth(management_username, 
                                                    management_password),
                                 timeout=None, verify=False)
            if data.ok:
                state = "pending"
                while state == "pending":
                    if _uuid in str(data.json()):
                        sleep(5)
                        print("waiting for blueprint to delete")
                    else:
                        print("Blueprint %s deleted successfully."%_uuid)
                        state = "done"
            else:
                print("Warning : Failed to fetch delete blueprint details, kindly check ..")
        else:
            print("Failed to delete blueprints", data.json())
            exit(1)
    if uuid_list != []:
        print("%s Project's blueprint deleted successfully."%project_name)

def delete_project_environment(project_name):
    print("Fetching project environments information...")
    project_name = project_name.strip()
    _uuid = _get_project_uuid(project_name)
    url = _build_url(scheme="https", host="localhost",resource_type="/environments/list")
    data = requests.post(url, json={"kind":"environment"},
                         auth=HTTPBasicAuth(management_username, 
                                            management_password),
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
        data = requests.delete(url,auth=HTTPBasicAuth(management_username, 
                                                  management_password),
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
    
def wait_for_completion(data, user, password, PC, task_uuid=None):
    if data.ok:
        state = "DELETE_PENDING"
        while state == "DELETE_PENDING":
            if task_uuid == None:
                task_uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",host=PC,
                             resource_type="/tasks/%s"%task_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(user, password), 
                                    verify=False)
            if responce.json()['status'] in ['DELETE_PENDING', 'RUNNING', 'QUEUED']:
                state = 'DELETE_PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error ---> ",responce.json().get('message_list', 
                                        responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE" 
    else:
        print("Error ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

if "@@{delete_only_network}@@" == "False":
    try:
        delete_applications(project_name)
        delete_blueprints(project_name)
        delete_app_protection_policies(project_name)
        delete_project_environment(project_name)
        delete_project(project_name)
        delete_subnet(overlay_subnet_name)
        delete_vpc(vpc_name)
        delete_subnet(external_subnet_name)
    except Exception as e:
      raise e
else:
    try:
        delete_subnet(overlay_subnet_name)
        delete_vpc(vpc_name)
        delete_subnet(external_subnet_name)
    except Exception as e:
      raise e
