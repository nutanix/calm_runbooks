# script
import requests
from requests.auth import HTTPBasicAuth

PC_IP = "@@{PC_IP}@@"
pc_user = "@@{prism_central_username}@@"
pc_password = "@@{prism_central_passwd}@@"

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

def enable_leap(host_pc, pc_user, pc_password):
    url = _build_url(scheme="https",
                     resource_type="/services/disaster_recovery",
                     host=host_pc)
    data = requests.post(url, json={"state":"ENABLE"},
                        auth=HTTPBasicAuth(pc_user,pc_password),
                        timeout=None, verify=False)
    if data.status_code == 409:
        print("Leap is already enabled on %s"%host_pc)
    elif data.ok:
        print("Leap Enabled Successfully on %s"%host_pc)
    else:
        print("Failed to Enable Leap on %s"%host_pc)

params = @@{dr_account_items}@@
DR_PC = params['url']
DR_user = params['username']
DR_password = params['passwd']
enable_leap(host_pc=PC_IP, pc_user=pc_user, pc_password=pc_password)
enable_leap(host_pc=DR_PC, pc_user=DR_user, pc_password=DR_password)
