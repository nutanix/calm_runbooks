# script
import requests
from requests.auth import HTTPBasicAuth

tenant = @@{UID}@@
CategoryName = @@{tenant_name}@@
description = "Tenant Onboarding category for VM"
value = tenant['tenant_uuid']

base_url = 'https://{}:9440/api/nutanix/v3/categories'.format(@@{PC_IP}@@)
payload = {
            "name": CategoryName,
            "description": description,
            "capabilities": {
                "cardinality": 64
            }
        }

api_url = base_url + '/' + CategoryName

r = requests.put(api_url, json=payload, 
                 auth=HTTPBasicAuth(@@{prism_central_username}@@,
                                    @@{prism_central_passwd}@@),
                 timeout=None, verify=False)
if not r.ok:
    print("PUT request failed", r.content)
    exit(1)

batch_url = "https://{}:9440/api/nutanix/v3/batch".format(@@{PC_IP}@@)

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
                  auth=HTTPBasicAuth(@@{prism_central_username}@@,
                                     @@{prism_central_passwd}@@),
                 timeout=None, verify=False)
if r.ok:
    print("Category created: {}".format(CategoryName))
    print("category_details={}".format(r.content))
else:
    print("Failed to create category - %s"%CategoryName)
    print(r.content)
