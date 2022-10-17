# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@".strip()
pc_password = "@@{prism_central_passwd}@@".strip()
pc_username = "@@{prism_central_username}@@".strip()

tenant = @@{UID}@@
CategoryName = "TenantName"
value = "@@{tenant_name}@@".strip()
description = "Tenant Onboarding category for %s"%value

base_url = 'https://{}:9440/api/nutanix/v3/categories'.format(PC_IP)
payload = {
            "name": CategoryName,
            "description": description,
#            "capabilities": {
#                "cardinality": 64
#            }
        }

api_url = base_url + '/' + CategoryName

r = requests.put(api_url, json=payload, 
                 auth=HTTPBasicAuth(pc_username, pc_password),
                 timeout=None, verify=False)
if not r.ok:
    print("PUT request failed", r.content)
    exit(1)

batch_url = "https://{}:9440/api/nutanix/v3/batch".format(PC_IP)

payload = {"action_on_failure":"CONTINUE",
                "execution_order":"NON_SEQUENTIAL",
                "api_request_list":[
                    {
                        "operation":"PUT",
                        "path_and_params":"/api/nutanix/v3/categories/{}/{}".format(CategoryName, value),
                        "body":{
                        "value":value,
                        "description":description
                        }
                    }
                    ],
                    "api_version":"3.0"}

r = requests.post(batch_url, json=payload, 
                  auth=HTTPBasicAuth(pc_username, pc_password),
                 timeout=None, verify=False)
if r.ok:
    print("Category created: {}".format(CategoryName))
    print("category_details={}".format(r.content))
else:
    print("Failed to create category - %s"%CategoryName)
    print(r.content)
