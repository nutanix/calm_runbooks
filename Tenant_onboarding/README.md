# Runbook Variables
## **`prism central IP (Required)`** 

  #### **Type:** string
  
  <details>
  <summary>\**Description\**</summary>
 This variable represents the IP address or hostname of the Prism Central instance that will be used for the deployment. It is required for any operations that interact with Prism Central using API or CLI.
  
</details>

  #### **Description:**

  This variable represents the IP address or hostname of the Prism Central instance that will be used for the deployment. It is required for any operations that interact with Prism Central using API or CLI.

  #### **Example:**

  ```
  prism_central_ip = 10.0.0.1
  ```
 
 ## **`prism central username (Required)`** 

  #### **Type:** string

  #### **Description:**

  This variable represents the IP address or hostname of the Prism Central instance that will be used for the deployment. It is required for any operations that interact with Prism Central using API or CLI.

  #### **Example:**

  ```
  prism central username = admin
  ```

* **`Management PC Username`**   (Required)-username used to authenticate with the Prism Central management interface.</span>

  **Type:** string

  **Example:**

  ```
  Management PC Username = admin
  ```

* **`Management PC Password`**   (Required)-This variable represents the password used to authenticate with Prism Central.</span>

  **Type:** string

  **Example:**

  ```
  Management PC Password = password
  ```

* **`Tenant Name`**   (Required)-name of the tenant. This ensures that all subsequent resources such as subnets, VPCs, projects, categories, and VPC tunnels are created under the correct tenant..</span>

  **Type:** string

  **Example:**

  ```
  Tenant Name = MY_Tenant
  ```
  **Note:** All resources such as subnets,project,VPC etc.. are created under this teant using runbook will use tenant name as prefix while creating.

* **`Delete Existing setup`**   (Optional)-used to specify the cleanup process for stale or existing resources such as project, VPC and tunnels, Subnets of "Tenant Name" as prefix.</span>

  **Type:** string

  **Example:**

  ```
  Delete Existing setup = Yes
  ```

* **`Workload PC IP`**   (Required)-specify the IP address of the Prism Central instance that should be used to onboard a tenant on the Workload Prism Central instance.</span>

  **Type:** string

  **Example:**

  ```
  Workload PC IP = 172.16.10.1
  ```

* **`Workload PC Username`**   (Required)-username used to authenticate with the Workload Prism Central management interface.</span>

  **Type:** string

  **Example:**

  ```
  Workload PC Username = admin
  ```

* **`Workload PC Password`**   (Required)-username used to authenticate with the Workload Prism Central management interface.</span>

  **Type:** string

  **Example:**

  ```
  Workload PC Password = Nutanix/4u
  ```

* **`Active Directory URL`**   (Required)-URL address to the directory.</span>

  **Type:** string

  **Example:**

  ```
  Active Directory URL =  ldap://10.10.10.66:389
  ```

* **`Active Directory Domain Name`**   (Required)-domain name in DNS format.</span>

  **Type:** string

  **Example:**

  ```
  Active Directory Domain Name = test.domain.com
  ```

* **`Active Directory Username`**   (Required)-username used to authenticate with the Active Directory service.</span>

  **Type:** string

  **Example:**

  ```
  Active Directory Username = user@test.domain.com
  ```

* **`Active Directory Password`**   (Required)- password used to authenticate with the Active Directory service.</span>

  **Type:** string

  **Example:**

  ```
  Active Directory Password = Test123
  ```

* **`Project Admin`**   (Required)-A project admin of Nutanix who manages cloud objects belonging to a specific project. These cloud objects can include roles, virtual machines (VMs), applications, and marketplace items that are associated with the project.</span>

  **Type:** string

  **Example:**

  ```
  Project Admin = aduser@test.domain.com
  ```

* **`Cluster Name`**   (Required)-Name of the Cluster.</span>

  **Type:** string

  **Example:**

  ```
  Cluster Name = auto-pc-12345-6789
  ```

* **`Virtual Switch Name`**   (Required)- The name of the virtual switch.</span>

  **Type:** string

  **Example:**

  ```
  Virtual Switch Name = vs0
  ```

* **`External VLAN ID`**   (Required)-The VLAN ID to be used for the virtual switch.</span>

  **Type:** string

  **Example:**

  ```
  External VLAN ID = 110
  ```

* **`External Subnet IP with Prefix`**   (Required)-username used to authenticate with the Prism Central management interface.</span>

  **Type:** string

  **Example:**

  ```
  External Subnet IP with Prefix = 10.20.30.0/24
  ```

* **`External Subnet IP Pool Range`**   (Required)-The IP address range for the external subnets.</span>

  **Type:** string

  **Example:**

  ```
  External Subnet IP Pool Range = 10.20.30.2-10.20.30.10
  ```

* **`External Subnet Gateway IP`**   (Required)-The gateway IP address for the external subnets.</span>

  **Type:** string

  **Example:**

  ```
  External Subnet Gateway IP = 10.20.30.1
  ```

* **`External Subnet NAT`**   (Required)- use to enable/disable NAT .</span>

  **Type:** Boolean

  **Example:**

  ```
  External Subnet NAT = True
  ```

* **`Overlay Subnet IP With Prefix`**   (Required)-Overlay Subnet IP address with network prefix.</span>

  **Type:** string

  **Example:**

  ```
  Overlay Subnet IP With Prefix = 10.10.10.0/24
  ```

* **`Overlay Subnet Gateway IP`**   (Required)-The gateway IP address for the overlay subnets.</span>

  **Type:** string

  **Example:**

  ```
  Overlay Subnet Gateway IP = 10.10.10.1
  ```

* **`Account Name`**   (Required)-The name of Calm account.</span>

  **Type:** string

  **Example:**

  ```
  Account Name = Multipc-account
  ```

* **`Quota : vCPUs`**   (Required)-The Maximum amount of vCPUs that can be consumed by a project.</span>

  **Type:** string

  **Example:**

  ```
  Quota : vCPUs = 10
  ```

* **`Quota : Memory in GB`**   (Required)-The Maximum amount of Memory that can be consumed by a project.</span>

  **Type:** string

  **Example:**

  ```
  Quota : Memory in GB = 20
  ```

* **`Quota : Disk Size in GB`**   (Required)-The Maximum amount of storage that can be consumed by a project.</span>

  **Type:** string

  **Example:**

  ```
  Quota : Disk Size in GB = 100
  ```

* **`Allow Project Collaboration`**   (Required)-The Allow collaboration flag .</span>

  **Type:** Boolean

  **Example:**

  ```
  Allow Project Collaboration = admin
  ```

* **`Create Project Environment with Default Values`**   (Required)-This option decides creating default Environment for project.</span>

  **Type:** string

  **Example:**

  ```
  Create Project Environment with Default Values = Yes
  ```

* **`Environment operating system`**   (Optional)-Operating System Type.</span>

  **Type:** string

  **Example:**

  ```
  Environment operating system = Linux
  ```
  **Note:** if Create Project Environment with Default Values is selected as "Yes" user need to 
  select proper environment operating system

* **`Image Name`**   (Required)-The Name of Image which present on Prism Central or cluster.</span>

  **Type:** string

  **Example:**

  ```
  Image Name = Centos7HadoopMaster
  ```
  **Note:** if Create Project Environment with Default Values is selected as "Yes" user need to 
  pass proper Image Name.

* **`Guest Customization Script`**   (Optional)- script that needs executed when a new virtual machine is deployed .</span>

  **Type:** string

  **Example:**

  ```
  Guest Customization Script = I2Nsb3VkLWNvbmZpZwp1c2VyczoKICAtIG5hbWU6IG51dGFuaXgKICAgIHNzaC1hdXRob3JpemVkLWtleXM6CiAgICAgIC0gc3NoLXJzYSBLRVkKICAgIHN1ZG86IFsnQUxMPShBTEwpIE5PUEFTU1dEOkFMTCddCiAgICBncm91cHM6IHN1ZG8KICAgIHNoZWxsOiAvYmluL2Jhc2gKCnBhY2thZ2VzOgogIC0gaHR0cGQ=
  ```
  **Note:** For Linux script should be ansible base64 encoded and for windows script should be in XML format.

* **`Environment Credential Username`**   (Required)-username used to authenticate project enviornment resources.</span>

  **Type:** string

  **Example:**

  ```
  Environment Credential Username = root
  ```

* **`Credential Type`**   (Required)- Authentication type ,could be SSH key-based or password .</span>

  **Type:** string

  **Example:**

  ```
  Credential Type = KEY
  ```

* **`Password Or Key`**   (Required)-password/key used to authenticate project enviornment resources.</span>

  **Type:** string

  **Example:**

  ```
  Password Or Key = test123
  ```
