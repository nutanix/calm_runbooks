sleep(2)
import requests
from requests.auth import HTTPBasicAuth

tenant = "@@{tenant_name}@@".strip()
management_cluster_info = {
    "username": "@@{management_pc_username}@@".strip(),
    "password": "@@{management_pc_password}@@".strip(),
    "ip": "@@{management_pc_ip}@@".strip()
}
workload_cluster_info = {
    "username": "@@{prism_central_username}@@".strip(),
    "password": "@@{prism_central_passwd}@@".strip(),
    "ip": "@@{PC_IP}@@".strip()
}

vpc_name = "{}_VPC".format(tenant)
external_subnet_name = "{}_External_Subnet".format(tenant)
overlay_subnet_name = "{}_Overlay_Subnet".format(tenant)
project_name = "{}_project".format(tenant)
tunnel_name = "@@{tenant_name}@@"+"_VPC_Tunnel"

def _build_url(scheme, resource_type, host, **params):
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

def _get_tunnel_uuid(tunnel_name, host):
    tunnel_state = ["CONNECTING","NOT_VALIDATED" ]
    url = _build_url(scheme="https",resource_type="/tunnels/list",host=host.get("ip"))
    data = requests.post(url, json={"kind": "tunnel","filter":"name==%s"%tunnel_name},
                         auth=HTTPBasicAuth(host.get("username"),
                                            host.get("password")),
                                            timeout=None,
                                            verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s does not exist"%(tunnel_name))
        elif data.json()['metadata']['total_matches'] > 1:
            print("There are more than one tunnel with name - %s"%(tunnel_name))
            print("Please delete it manually before executing runbook.")
            exit(1)
        elif data.json()['entities'][0]['status']['state'] in tunnel_state:
            print("tunnel is in NOT_VALIDATED,Please delete it manually before executing runbook.")
            exit(1)
        else:
            tunnel_uuid = data.json()['entities'][0]['status']['resources']['uuid']
            return tunnel_uuid
    else:
        print("Error while fetching tunnel details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)

def _get_network_group_uuid(tunnel_name, host):
    url = _build_url(scheme="https",resource_type="/network_groups/list",host=host.get("ip"))
    data = requests.post(url, json={"kind": "network_group","filter":"name==%s"%tunnel_name},
                         auth=HTTPBasicAuth(host.get("username"),
                                            host.get("password")),
                         timeout=None, verify=False)
    if data.ok:
        if data.json()['metadata']['total_matches'] == 0:
            print("%s does not exist"%(tunnel_name))
        else:
            group_uuid = data.json()['entities'][0]['status']['resources']['uuid']
            return group_uuid
    else:
        print("Error while fetching network group details :- ",data.json().get('message_list',
                                     data.json().get('error_detail', data.json())))
        exit(1)


def delete_tunnel(tunnel_name, host):
    print("Fetching tunnel details:{}".format(tunnel_name))
    tunnel_name = tunnel_name.strip()
    _group_uuid = _get_network_group_uuid(tunnel_name, host)
    _tunnel_uuid = _get_tunnel_uuid(tunnel_name, host)
    if _group_uuid:
        url = _build_url(scheme="https",resource_type="network_groups/{}/tunnels/{}".format(_group_uuid, _tunnel_uuid),
                         host = host.get("ip"), username=host.get("username"), password=host.get("password"))
        data = requests.delete(url, auth=HTTPBasicAuth(host.get("username"), host.get("password")),
                               timeout=None, verify=False)

        print("deleting tunnel with name %s"%tunnel_name)
    else:
        print("Info : %s tunnel not present on Management PC"%(tunnel_name))

def get_entity_uuid(resource_type, name, host, filter=None):
    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    if not filter:
        filter = "name=={0}".format(name)
    payload = {"filter": filter}
    url = _build_url(scheme="https",resource_type="/{0}/list".format(resource_type), host=ip)
    data = requests.post(url, json=payload,
                        auth=HTTPBasicAuth(username, password),verify=False)
    if data.ok:
        if data.json().get("metadata", {}).get("total_matches", 0) > 0:
            for entity in data.json().get("entities", []):
                return entity.get('metadata', {}).get('uuid'), None
        else:
            return None, "{0} with name {1} not found".format(resource_type, name)
    else:
        msg = "Failed to fetch {0} details. ".format(name) + data.json()
        return None, msg

def delete_vpc(vpc_name, host):
    print("Fetching %s VPC information..."%vpc_name)
    vpc_name = vpc_name.strip()
    uuid, err = get_entity_uuid("vpcs", vpc_name, host)
    if err:
        print("Info : %s VPC not present on %s. "%(vpc_name, host.get("ip")), err)
        return

    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    url = _build_url(scheme="https", resource_type="/vpcs/%s"%uuid, host=ip)
    data = requests.delete(url, auth=HTTPBasicAuth(username, password),
                            timeout=None, verify=False)
    wait_for_completion(data, username, password, ip)
    print("%s VPC deleted successfully."%vpc_name)

def delete_subnet(subnet_name, host):
    print("Fetching %s subnet information..."%subnet_name)
    subnet_name = subnet_name.strip()
    uuid, err = get_entity_uuid("subnets", subnet_name, host)
    if err:
        print("Info : %s Subnet not present on %s. "%(subnet_name, host.get("ip")), err)
        return

    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    url = _build_url(scheme="https", resource_type="/subnets/%s"%uuid, host=ip)
    data = requests.delete(url, auth=HTTPBasicAuth(username, password),
                            timeout=None, verify=False)
    wait_for_completion(data, username, password, ip)
    print("%s Subnet deleted successfully."%vpc_name)


def delete_project(project_name, host):
    print("Deleting project %s"%project_name)
    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    project_name = project_name.strip()
    _uuid, err = get_entity_uuid("projects", project_name, host)
    if err:
        print("Info : %s Project not present on %s. "%(project_name, host.get("ip")), err)
        exit(1)
    url = _build_url(scheme="https", host=ip,resource_type="/projects/%s"%_uuid)
    data = requests.delete(url, auth=HTTPBasicAuth(username,
                                                   password),
                           timeout=None, verify=False)
    wait_for_completion(data, username, password, ip)
    print("%s Project deleted successfully."%project_name)

def delete_app_protection_policies(project_name, host):
    print("Fetching app protection policies information...")
    project_uuid, err = get_entity_uuid("projects", project_name, host)
    if err:
        print("Info : %s Project not present on %s. "%(project_name, host.get("ip")), err)
        exit(1)
    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    url = "https://{0}:9440/api/calm/v3.0/app_protection_policies/list".format(ip)
    data = requests.post(url, json={"filter":"project_reference==%s"%project_uuid,"length":20},
                         auth=HTTPBasicAuth(username,
                                            password),
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
        url = "https://{0}:9440/api/calm/v3.0/app_protection_policies/{1}".format(ip, _uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(username,
                                                       password),
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


def fetch_entities_uuid_associated_to_project(resource_type, project_name, host):
    uuids = []
    limit = 20
    offset = 0
    auth = HTTPBasicAuth(host.get("username"), host.get("password"))
    while(True):
        url = _build_url(scheme="https", host=host.get("ip"),resource_type="/%s/list"%resource_type)
        data = requests.post(url, json={"length": limit, "offset": offset},
                             auth=auth,
                             timeout=None, verify=False)
        if data.ok:
            if len(data.json().get("entities", [])) > 0:
                for _entity in data.json()["entities"]:
                    if _entity["metadata"]["project_reference"]["name"] == project_name:
                        uuids.append(_entity["metadata"]["uuid"])
            else:
                break
        else:
            print("Failed fetching {0} for project {1}:".format(resource_type, project_name), data.json())
            exit(1)
        offset += limit
    return uuids

def delete_applications(project_name, host):
    print("Fetching applications information...")
    project_name = project_name.strip()
    uuids = fetch_entities_uuid_associated_to_project("apps", project_name, host)
    if not uuids:
        print("No applications associated to project with name %s"%project_name)
        return
    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    for _uuid in uuids:
        url = _build_url(scheme="https", host=ip,resource_type="/apps/%s"%_uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(username,
                                                       password),
                               timeout=None, verify=False)
        task_uuid = data.json()["status"]["ergon_task_uuid"]
        wait_for_completion(data, username, password, ip, task_uuid)
    print("Applications deleted successfully.")

def delete_blueprints(project_name, host):
    print("Fetching blueprints information...")
    project_name = project_name.strip()
    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    uuids = fetch_entities_uuid_associated_to_project("blueprints", project_name, host)
    if not uuids:
        print("No applications associated to project with name %s"%project_name)
        return
    for _uuid in uuids:
        url = _build_url(scheme="https", host=ip,resource_type="/blueprints/%s"%_uuid)
        data = requests.delete(url, auth=HTTPBasicAuth(username,
                                                       password),
                               timeout=None, verify=False)
        if not data.ok:
            print("Failed to delete blueprints", data.json())
            exit(1)

    print("Blueprints deleted successfully.")

def delete_project_environment(project_name, host):
    print("Fetching project environments information...")
    project_name = project_name.strip()
    ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")
    url = _build_url(scheme="https", host=ip,resource_type="/environments/list")
    data = requests.post(url, json={"kind":"environment"},
                         auth=HTTPBasicAuth(username,
                                            password),
                           timeout=None, verify=False)
    uuid_list = []
    if data.ok:
        if data.json()["metadata"].get("total_matches") > 0:
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
        url = _build_url(scheme="https", host=ip,resource_type="/environments/%s"%_uuid)
        data = requests.delete(url,auth=HTTPBasicAuth(username,
                                                  password),
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
            if responce.json().get('status', None) in ['DELETE_PENDING', 'RUNNING', 'QUEUED']:
                state = 'DELETE_PENDING'
                sleep(5)
            elif responce.json().get('status', None) == 'FAILED':
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
        # clear entities from management cluster
        delete_applications(project_name, host=management_cluster_info)
        delete_blueprints(project_name, host=management_cluster_info)
        delete_app_protection_policies(project_name, host=management_cluster_info)
        delete_tunnel(tunnel_name, host=management_cluster_info)
        delete_project_environment(project_name, host=management_cluster_info)
        delete_project(project_name, host=management_cluster_info)

        # clear entities from workload cluster
        delete_subnet(overlay_subnet_name, host=workload_cluster_info)
        delete_vpc(vpc_name, host=workload_cluster_info)
        delete_subnet(external_subnet_name, host=workload_cluster_info)
    except Exception as e:
      raise e
else:
    try:
        # clear entities from management cluster
        delete_tunnel(tunnel_name, host=management_cluster_info)

        # clear entities from workload cluster
        delete_subnet(overlay_subnet_name, host=workload_cluster_info)
        delete_vpc(vpc_name, host=workload_cluster_info)
        delete_subnet(external_subnet_name, host=workload_cluster_info)
    except Exception as e:
      raise e
