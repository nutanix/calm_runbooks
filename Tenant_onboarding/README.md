
| Variable Display Name           | Variable Actual Name        | Type       | Description |
| :-----------------------------  | :-------------------------- | :--------- | :------------- |
| Tenant Name                     |  tenant_name                | Mandatory  | Name of Tenant. It will be used to create Subnets, VPC, Project , Category, VPC_Tunnel.  |
| Delete Existing setup           |  delete_existing            | Mandatory  | If "yes" It will delete existing project, VPC, Subnets of "Tenant Name" if tenant name is same.  |
| PC IP                           |  PC_IP                      | Mandatory  | Prism Central IP address on which Tenant needs to be onboard.  |
| IDP Name                        |  idp_name                   | Mandatory  | Identity provider's Name. User Can provide any name.  |
| IDP Metadata                    |  idp_metadata               | Mandatory  | Identity Provider's metadata in XML format.  |
| Admin User for Project          |  project_admin_user         | Mandatory  | Username to add user in tenant's project as Admin.  |
| Cluster Name                    |  cluster_name               | Mandatory  | Cluster name for Tenant.  |
| Virtual Switch Name             |  virtual_switch             | Mandatory  | Virtual Switch name for External Subnet.  |
| External VLAN ID                | external_vlan_id            | Mandatory  | External subnet VLAN ID should be Unique.  |
| External Subnet IP with Prefix  | external_subnet_ip          | Mandatory  | External Subnet IP address with network prefix, IE : 10.20.30.0/24  |
| External Subnet IP Pool Range   | external_subnet_ip_pool     | Mandatory  | IP Pool range for external subnet, IE : 10.20.30.2-10.20.30.10  |
| External Subnet Gateway IP      | external_subnet_gateway_ip  | Mandatory  | Gateway IP of External Subnet should be within the range of network IP.   |
| External Subnet NAT             | external_subnet_nat         | Mandatory  | NAT protocol, True will Enable it, False will Disable it.  |
| Overlay Subnet IP With Prefix   | overlay_subnet_ip           | Mandatory  | Overlay Subnet IP address with network prefix, IE : 10.20.30.0/24. Default IP Pool range is used of 50 IP's. IE : 10.20.30.2-10.20.30.52.  |
| Overlay Subnet Gateway IP       | overlay_subnet_gateway_ip   | Mandatory  | Gateway IP of Overlay Subnet should be within the range of Overlay network IP.   |
| PC Account Name for Project     | account_name                | Mandatory  | Calm Account Name for project.  |
| Quota : Project Memory in GB    | project_memory              | Mandatory  | Mamory in GB for project resources. User can pass 0 if not needed.   |
| Quota : Project VCPUs           | project_vcpu                | Mandatory  | VCPUs for project resources. User can pass 0 if not needed.   |
| Quota : Project Disk Size in GB | project_disk_size           | Mandatory  | Disk size in GB for project resources. User can pass 0 if not needed.   |
| Allow Collaboration             | allow_collaboration         | Mandatory  | True will enable allow collaboration between project users, False will disable it.  |
| Create Project Environment with Default Values| create_environment | Mandatory  | "yes" will create environment with default values, User need to pass operating system, image name, and guest customization script to create default environment.  |
| Environment operating system    | environment_os              | Mandatory  | Choose from Linux ar Windows.  |
| Image Name                      | image_name                  | Mandatory  | Depending upon "Environment operating system" User needs to pass correct image which is present on Prism Central and given Cluster.  |
| Guest Customization Script      | guest_customization_script  | Mandatory  | Depending upon "Environment operating system" User needs to pass correct script. For Linux script should be ansible base64 encoded and for windows script should be in XML format.  |
| Environment Credential Username | credential_username         | Mandatory  | Credentials required for environment creation. Give any name to credentials. If not creating environment pass NA.  |
| Credential Type                 | credential_type             | Mandatory   | choose from PASSWORD or KEY. Depending on this selection need to enter Password or Key in "Password Or Key" parameter.  |
| Password Or Key                 | password_or_key             | Mandatory  | Provide password or ssh key. Pass NA if not creating environment with default values.  |
| Prism Central UserName          | prism_central_username      | Mandatory  | Prism Central Username.  |
| Prism Central Password          | prism_central_passwd        | Mandatory  | Prism Central Password.  |
