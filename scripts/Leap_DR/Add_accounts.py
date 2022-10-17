# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_user = "@@{prism_central_username}@@".strip()
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

def get_spec(**params):
    return (
    {
     "spec": {
        "name": "PC_%s"%params['url'],
        "resources": {
            "url": params['url'],
            "username": params['username'],
            "password": params['passwd'],
            "cloud_type": params.get("cloud_type", "ONPREM_CLOUD")
        },
        "description": ""
    },
    "metadata": {
      "kind": "cloud_trust"
    },
    "api_version": "3.1.0"
    })

def get_spec_account(**params):
    return (
   {
    "api_version": "3.0",
    "metadata": {
        "kind": "account"
    },
    "spec": {
        "name": params.get('name', "DR_%s"%params['url'].split(".")[-1]),
        "resources": {
             "type": params.get("pc_type", "nutanix_pc"),
            "data": {
                "server": params['url'],
                "username": params['username'],
                "password": {
                    "value": params['passwd'],
                "attrs": {
                    "is_secret_modified": True
                    }
                }
            },
            "sync_interval_secs": params.get("sync_interval_secs", 3600)
            }
        }
    })
  
def create_connection(PC=None, user=None, password=None,**params):
    payload = get_spec(**params)
    url = _build_url(scheme="https",resource_type="/cloud_trusts")
    _user = pc_user
    _password = pc_password
    _PC=PC_IP
    if PC != None:
        url = _build_url(scheme="https",host=PC, resource_type="/cloud_trusts")
        _user = user
        _password = password
        _PC=PC
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(_user,_password),
                        timeout=None, verify=False)
    wait_for_completion(data, _PC, _user, _password)
    
    _url = _build_url(scheme="https",resource_type="/groups")
    _payload = {
        "entity_type": "availability_zone_physical",
        "grouping_attribute": "type",
        "group_member_count": 1,
        "group_member_attributes": [
            {
                "attribute": "name"
            },
            {
                "attribute": "url"
            }
        ],
        "query_name": "prism:BaseGroupModel"}
        
    _data = requests.post(_url, json=_payload,
                             auth=HTTPBasicAuth(_user,_password),
                             timeout=None, verify=False)
    az_uuid = ""
    print(_data.json())
    print(params['url'])
    if _data.ok:
        if params['url'] in str(_data.json()):
            for cloud_trust in _data.json()["group_results"]:
                if cloud_trust["entity_results"][0]["data"][0]["values"][0]["values"][0] == "PC_"+params['url']:
                    az_uuid = cloud_trust["entity_results"][0]["data"][1]["values"][0]["values"][0]
        else:
            print("%s PC's availability zone not present on %s"%(params['url'], PC_IP))
            exit(1)
    else:
        print("Failed to retrive Availability Zone information.")
        print(data.json())
        exit(1)
    print("dest_az_uuid={}".format(az_uuid))
    
def add_account(PC=None, user=None, password=None, **params):
    payload = get_spec_account(**params)
    url = _build_url(scheme="https",resource_type="/accounts")
    _user = pc_user
    _password = pc_password
    _PC=PC_IP
    if PC != None:
        url = _build_url(scheme="https",host=PC, resource_type="/accounts")
        _user = user
        _password = password
        _PC=PC
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(_user,_password),
                        timeout=None, verify=False)
    if "DUPLICATE_ACCOUNT" in str(data.json()):
        print("Input Error :- Your provided account url - %s is "\
              "already a part of another account"%params['url'])
        _url = _build_url(scheme="https",resource_type="/accounts/%s"%data.json()["metadata"]["uuid"])
        _data = requests.delete(_url,auth=HTTPBasicAuth(_user,_password),timeout=None, verify=False)
        if _data.ok:
            exit(1)
        else:
            print("Getting error while deleting %s account."%payload["spec"]["name"])
            print(_data.json())
            exit(1)
    wait_for_completion(data, _PC, _user, _password)
    
def wait_for_completion(data, PC=None, user=None, password=None):
    if data.ok:
        state = data.json()['status'].get('state')
        while state == "PENDING":
            _uuid = data.json()['status']['execution_context']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            _user = pc_user
            _password = pc_password
            if PC != None:
                url = _build_url(scheme="https", host=PC,
                             resource_type="/tasks/%s"%_uuid)
                _user = user
                _password = password
            responce = requests.get(url, auth=HTTPBasicAuth(_user,_password),
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                if ("DUPLICATE_CLOUD_TRUST" in str(responce.json())) or ("DUPLICATE_NAME" in str(responce.json())):
                    pass
                else:
                    print("Got Error ---> ",responce.json().get('message_list', 
                                            responce.json().get('error_detail', responce.json())))
                    state = 'FAILED'
                    exit(1)
            else:
                state = "COMPLETE"
    else:
        if ("DUPLICATE_CLOUD_TRUST" in str(data.json())) or ("DUPLICATE_NAME" in str(data.json())):
            pass
        else:
            print("Got Error ---> ",data.json().get('message_list', 
                                    data.json().get('error_detail', data.json())))
            exit(1)

# Create account and connection at local PC
params = @@{dr_account_items}@@
create_connection(**params)
