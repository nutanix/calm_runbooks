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

def is_cloud_trust_present(PC=None, user=None, password=None,**params):
    dr_pc_ip = params['url']
    payload = {
        "kind": "cloud_trust",
        "length":999,
        "filter":"url=={}".format(dr_pc_ip)
        }
    url = _build_url(scheme="https",host=PC, resource_type="/cloud_trusts/list")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(user,password),
                        timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 1:
            uuid = data.json()['entities'][0]['metadata']['uuid']
            conn_uuid = data.json()['entities'][0]['status']['resources']['remote_connection_reference']['uuid']
            print("Cloud trust already added to pc with uuid {} and remote conection uuid is {}".format(uuid,conn_uuid))
            return uuid,conn_uuid
        else:
            print("cloud trust is not present")
            return None,None
    else:
        print("Failed to retrive cloud trust information.")
        print(data.json())
        exit(1)

def is_az_present(PC=None, user=None, password=None, remote_uuid=None, **params):
    dr_pc_ip = params['url']
    payload = {
        "kind": "availability_zone",
        "length": 999
        }
    url = _build_url(scheme="https",host=PC, resource_type="/availability_zones/list")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(user,password),
                        timeout=None, verify=False)
    if data.ok:
        for az in data.json()["entities"]:
            if az['spec']['resources'].get('credentials',None):
                if az['spec']['resources']['credentials']['pc']['remote_connection_reference']['uuid']==remote_uuid:
                    return az['spec']['resources']['management_url']
    else:
        print("Failed to retrive Availability Zone information.")
        print(data.json())
        exit(1)

        

def create_connection(PC=None, user=None, password=None,**params):
    payload = get_spec(**params)
    url = _build_url(scheme="https",resource_type="/cloud_trusts")
    _user = pc_user
    _password = pc_password
    _PC=PC_IP
    cloud_trust_uuid,remote_conn_uuid = is_cloud_trust_present(PC=_PC, user=_user, password=_password,**params)
    if PC != None:
        url = _build_url(scheme="https",host=PC, resource_type="/cloud_trusts")
        _user = user
        _password = password
        _PC=PC
    if cloud_trust_uuid == None:
        print("adding cloud aviablity zone")
        data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(_user,_password),
                        timeout=None, verify=False)
        if data.ok:
            print(data.json())
            wait_for_completion(data, _PC, _user, _password)
        else:
            print(data)
    
    cloud_trust_uuid,remote_conn_uuid = is_cloud_trust_present(PC=_PC, user=_user, password=_password,**params)
    az_uuid = is_az_present(PC=_PC, user=_user, password=_password, remote_uuid=remote_conn_uuid, **params)
        
    if az_uuid:
        print("dest_az_uuid={}".format(az_uuid))
    else:
        print("%s PC's availability zone not present on %s"%(params['url'], PC_IP))
        exit(1)

    
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
    print(responce.json())

# Create account and connection at local PC
params = @@{dr_account_items}@@
create_connection(**params)
#add_account(**params)

# Create account and connection at DR PC
#_params = {"name" : "Production_%s"%PC_IP.split(".")[-1],
#          "url" : PC_IP,
#          "username" : pc_user,
#          "passwd" : pc_password,
#          "sync_interval_secs" : params.get("sync_interval_secs", 3600)}
#add_account(PC=params['url'], 
#            user=params['username'],
#            password=params['passwd'],
#            **_params)
