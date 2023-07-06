sleep(2)
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
    
def wait_for_completion(data):
    if data.ok:
        print("Test in progress ..")
        state = "PENDING"
        while state == "PENDING":
            _uuid = data.json()['api_response_list'][0]['api_response']['task_uuid']
            url = _build_url(scheme="https",
                             resource_type="/tasks/%s"%_uuid)
            responce = requests.get(url, auth=HTTPBasicAuth(pc_user, pc_password),
                                    verify=False)                      
            if responce.json()['status'] in ['PENDING', 'RUNNING', 'QUEUED']:
                state = 'PENDING'
                sleep(5)                
            elif responce.json()['status'] == 'FAILED':
                print("Error occured ---> ",responce.json().get('message_list', 
                                            responce.json().get('error_detail', responce.json())))
                state = 'FAILED'
                exit(1)
            else:
                state = "COMPLETE"
    else:
        print("Error occured ---> ",data.json().get('message_list', 
                                data.json().get('error_detail', data.json())))
        exit(1)

def get_spec(**params):
    return (
    {"action_on_failure": "CONTINUE",
    "execution_order": "NON_SEQUENTIAL",
    "api_request_list": [
        {
            "operation": "POST",
            "path_and_params": "/api/nutanix/v3/recovery_plan_jobs",
            "body": {
                "spec": {
                    "name": "Test Failover - @@{calm_now}@@",
                    "resources": {
                        "recovery_plan_reference": {
                            "kind": "recovery_plan",
                            "name": params["recovery_plan_name"],
                            "uuid": params["recovery_plan_uuid"]
                        },
                        "execution_parameters": {
                            "action_type": "TEST_FAILOVER",
                            "failed_availability_zone_list": [
                                {
                                    "availability_zone_url": params["failed_availability_zone_uuid"]
                                }
                            ],
                            "recovery_availability_zone_list": [
                                {
                                    "availability_zone_url": params["recovery_availability_zone_uuid"]
                                }
                            ],
                            "should_continue_on_validation_failure": True
                        }
                    }
                },
                "metadata": {
                    "kind": "recovery_plan_job"
                },
                "api_version": "3.1.0"
            }}],
            "api_version": "3.1.0"
        })

def test_failover(**params):
    payload = get_spec(**params)
    url = _build_url(scheme="https",
                    resource_type="/batch")
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if not data.ok:
        print("Error :- ",data.json())
        exit(1)
    if data.json()["api_response_list"][0]["status"] not in ['200', '202', '203']:
        print("Error :- ",data.json())
        exit(1)

    wait_for_completion(data)
    print("%s recovery plan tested successfully, Its working as "\
                          "expected."%params["recovery_plan_name"])
    
def get_account_info(az_url):
    url = _build_url(scheme="https",resource_type="/groups")
    payload = {
        "entity_type": "availability_zone_physical",
        "grouping_attribute": "type",
        "group_member_attributes": [
            {
                "attribute": "name"
            },
            {
                "attribute": "url"
            }
        ],
        "query_name": "prism:BaseGroupModel"
    }
    
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if data.ok:
        for cloud_trust in data.json()["group_results"]:
            if cloud_trust["entity_results"][0]["data"][0]["values"][0]["values"][0] == az_url:
                return cloud_trust["entity_results"][0]["data"][1]["values"][0]["values"][0]
        print("%s availability zone not present on %s"%(az_url, PC_IP))
        exit(1)
    else:
        print("Failed to retrive availability zone info of %s"%az_url)
        print(data.json())
        exit(1)
        
def recovery_plan_info(plan_name):
    print(plan_name)
    url = _build_url(scheme="https",resource_type="/recovery_plans/list")
    data = requests.post(url, json={"kind":"recovery_plan", "filter":"name==%s"%plan_name},
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        verify=False)
    print(url)
    print(data)
    if len(data.json()['entities']) != 0:
        recovery_plan_uuid = data.json()["entities"][0]["metadata"]["uuid"]
        return recovery_plan_uuid
    else:
        print("Got Error while fetching recovery plan info - %s"%plan_name)
        print("Please make sure recovery plan name is correct and active.")
        print(data.json())
        exit(1)

params = {"recovery_plan_name":"@@{recovery_plan_name}@@".strip(),
          "recovery_plan_uuid":recovery_plan_info("@@{recovery_plan_name}@@".strip()),
          "failed_availability_zone_uuid":get_account_info("@@{production_availability_zone_name}@@".strip()),
          "recovery_availability_zone_uuid":get_account_info("@@{recovery_availability_zone_name}@@".strip())
         }
test_failover(**params)
