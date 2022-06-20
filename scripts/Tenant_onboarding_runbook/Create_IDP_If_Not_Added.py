# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@"
pc_user = "@@{prism_central_username}@@"
pc_password = "@@{prism_central_passwd}@@"

#roles = ROLE_CLUSTER_VIEWER, ROLE_USER_ADMIN, ROLE_CLUSTER_ADMIN

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
    
def wait_for_completion(data):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_user, pc_password),
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error occured ---> ",data.json().get('message_list', 
                                        data.json().get('error_detail', data.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        print("Error occured ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

def get_spec():
    return ({
              "spec":{
                "name":"@@{idp_name}@@",
                "resources":{
                  "idp_metadata":""}},
              "metadata":{
                "kind":"identity_provider"
                },
              "api_version":"3.1.0"
            })

def identity_providers():
    payload = get_spec()
    payload["spec"]["resources"]["idp_metadata"] = """@@{idp_metadata}@@"""
    url = _build_url(scheme="https",
                    resource_type="/identity_providers")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    wait_for_completion(data)
    idp_uuid = data.json()["metadata"]["uuid"]
    print("idp_details={}".format({"name":"@@{idp_name}@@",
                                   "uuid":idp_uuid}))
    return idp_uuid
    
    
def create_role_mapping(idp_uuid):
    query_string = "&entityType=USER&role=ROLE_CLUSTER_VIEWER"
    url = "https://%s:9440/PrismGateway/services/rest/v1/"\
          "authconfig/identity_providers/%s/role_mappings?%s"%(PC_IP,
                                                              idp_uuid,
                                                              query_string)
    payload = {"role":"ROLE_CLUSTER_VIEWER","entityType":"USER",
               "idpUuid":idp_uuid,
               "entityValues":["idpuser10@calmsaastest.com"]}
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if not data.ok:
        print("Error :- ",data.json())
        exit(1)
    print(data.json())
    
url = _build_url(scheme="https",
                    resource_type="/identity_providers/list")
data = requests.post(url, json={"kind":"identity_provider"},
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)

if data.json()["metadata"]["total_matches"] >= 1:
    for IDP in data.json()["entities"]:
        if IDP["spec"]["name"] == "@@{idp_name}@@":
            print("idp_details={}".format({"name":"@@{idp_name}@@", 
                                           "uuid":IDP["metadata"]["uuid"]}))
else:
    idp_uuid = identity_providers()
    create_role_mapping(idp_uuid)
