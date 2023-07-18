# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "localhost"
pc_username = "@@{management_pc_username}@@".strip()
pc_password = "@@{management_pc_password}@@".strip()

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

def cluster_details(cluster=None):
    cluster_name = "@@{cluster_name}@@".strip()
    if cluster != None:
        cluster_name = cluster
    payload = {"kind": "cluster"}
    url = _build_url(scheme="https",
                    resource_type="/clusters/list")
    data = requests.post(url, json=payload,
                         auth=HTTPBasicAuth(pc_username, pc_password), 
                         verify=False)
    if data.ok:
        for _cluster in data.json()['entities']:
            if _cluster['status']['name'] == cluster_name:
                return(str(_cluster['metadata']['uuid']))
        print("Input Error :- Given cluster %s not present on %s"%(cluster_name, PC_IP))
        exit(1)
    else:
        print("Error while fetching %s cluster info"%cluster_name)
        print(data.json().get('message_list',data.json().get('error_detail', data.json())))
        exit(1)
        
def add_quotas(account,**params):
    if params.get("quotas", "None") != "None":
        memory = 0
        disk = 0
        vcpus = 0
        for resource in params['quotas']:
            if resource.get("mem_gb", 0) != 0:
                mem_gb = resource["mem_gb"] * 1024 * 1024 * 1024
                memory = mem_gb
            if resource.get("storage_gb", 0) != 0:
                storage_gb = resource['storage_gb'] * 1024 * 1024 * 1024
                disk = storage_gb
            if resource.get("vcpu", 0) != 0:
                vcpus = resource['vcpu']
                
        cluster_uuid = "@@{cluster_uuid}@@"
        project_details = @@{project_details}@@
        account_details = @@{account_details}@@
        entities = {}
        entities["account"]=account_details['uuid']
        entities["cluster"]=cluster_uuid
        entities["project"]=project_details['uuid']

        if not account:
            entities = {"project": project_details['uuid']}
            
        url = _build_url(scheme="https",
                        resource_type="/idempotence_identifiers")
        data = requests.post(url, json={"count": 1,"valid_duration_in_minutes": 527040},
                            auth=HTTPBasicAuth(pc_username, pc_password),
                            timeout=None, verify=False)
        _uuid = data.json()['uuid_list'][0]
        payload = ({
            "metadata": {
            "kind": "quota",
            "project_reference": {
                    "kind": "project",
                    "name": project_details['name'],
                    "uuid": project_details['uuid']
                },
            "uuid": _uuid
            },
            "spec": {
                "resources": {
                    "data": {
                        "disk": disk,
                        "vcpu": vcpus,
                        "memory": memory
                    },
                    "entities": entities,
                    "metadata": {},
                    "uuid": _uuid
                }
            }})
    
        url = "https://{}:9440/api/calm/v3.0/quotas".format(PC_IP)
        data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, 
                                           pc_password),
                        timeout=None, verify=False)
        wait_for_completion(data) 
    else:
        print("Quota not set for project %s"%project_details['name'])
        
    enable_quota_state(account_details['uuid'], project_details['uuid'])
        
def enable_quota_state(account, project):
    payload = {"spec":{
                      "resources":{
                                   "entities":{
                                               "project":project},
                      "state":"enabled"
                      }
                  }
              }
            
    url = "https://{}:9440/api/calm/v3.0/quotas/update/state".format(PC_IP)
    data = requests.put(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    wait_for_completion(data) 
      
    payload = {"spec":{
                      "resources":{
                                   "entities":{
                                               "account":account,
                                               "project":project},
                      "state":"enabled"
                      }
                  }
              }
            
    url = "https://{}:9440/api/calm/v3.0/quotas/update/state".format(PC_IP)
    data = requests.put(url, json=payload,
                        auth=HTTPBasicAuth(pc_username, pc_password),
                        timeout=None, verify=False)
    wait_for_completion(data) 
      
def wait_for_completion(data):
    if data.status_code in [200, 202]:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_username,pc_username), 
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
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

if (@@{project_vcpu}@@ != 0) or (@@{project_memory}@@ != 0) or (@@{project_disk_size}@@ != 0):
    params = @@{project_items}@@
    add_quotas(account=False,**params)
    params = @@{account_items}@@
    add_quotas(account=True,**params)
else:
    print("Info : Not setting Projects Quota, All Quota values are zero.")