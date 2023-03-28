# Runbook Variables
## **`prism central IP (Required)`** 

  #### **Type:** string
  
  <details>
  <summary>Description</summary>
 This variable represents the IP address or hostname of the Prism Central instance that will be used for the deployment. It is required for any operations that interact with Prism Central using API or CLI.
  
  </details>

  #### **Example:**

  ```
  10.0.0.1
  ```

## **`Management PC Username (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the username used to authenticate with the Managementt Prism Central management interface.
  </details>

  #### **Example:**

  ```
  admin
  ```

## **`Management PC Password (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the password used to authenticate with Prism Central.
  </details>

  #### **Example:**

  ```
  nutanix/4u
  ```

## **`Tenant Name (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the Name of the tenant. This ensures that all subsequent resources such as subnets, VPCs, projects, categories, and VPC tunnels are created under the correct tenant.
  </details>

  #### **Example:**

  ```
  MY_Tenant
  ```
  #### **Note:** All resources such as subnets,project,VPC etc.. are created under this teant using runbook will use tenant name as prefix while creating.

## **`Delete Existing setup (Optional)`**

  #### **Type:** string

  <details>
  <summary>Description</summary>
  This variable is used to specify the cleanup process for stale or existing resources such as project, VPC and tunnels, Subnets of "Tenant Name" as prefix.
  </details>

  #### **Example:**
  ```
  Yes
  ```

## **`Workload PC IP (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable specify the IP address of the Prism Central instance that should be used to onboard a tenant on the Workload Prism Central instance.
  </details>

  #### **Example:**
  ```
  Workload PC IP = 172.16.10.1
  ```

## **`Workload PC Username (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the Name of the username used to authenticate with the Workload Prism Central management interface 
  </details>

  #### **Example:**

  ```
  admin
  ```

## **`Workload PC Password (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the password used to authenticate with the Workload Prism Central management interface 
  </details>

  #### **Example:**

  ```
  Nutanix/4u
  ```

## **`Active Directory URL (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the URL address to the directory.
  </details>

  #### **Example:**

  ```
  ldap://10.10.10.66:389
  ```

## **`Active Directory Domain Name (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the domain name in DNS format.
  </details>

  #### **Example:**
  ```
  test.domain.com
  ```

## **`Active Directory Username (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the username used to authenticate with the Active Directory service.
  </details>

  #### **Example:**

  ```
  user@test.domain.com
  ```

## **`Active Directory Password (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the password used to authenticate with the Active Directory service. 
  </details>

  #### **Example:**

  ```
  Test123
  ```

## **`Project Admin (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  A project admin of Nutanix who manages cloud objects belonging to a specific project. These cloud objects can include roles, virtual machines (VMs), applications, and marketplace items that are associated with the project.
  </details>

  #### **Example:**

  ```
  aduser@test.domain.com
  ```

## **`Cluster Name (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the Name of the Cluster.
  </details>

  #### **Example:**

  ```
  auto-pc-12345-6789
  ```

## **`Virtual Switch Name (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The name of the virtual switch.
  </details>

  #### **Example:**
  ```
  vs0
  ```

## **`External VLAN ID (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The VLAN ID to be used for the virtual switch.
  </details>

  #### **Example:**
  ```
  110
  ```

## **`External Subnet IP with Prefix (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the External Subnet IP with Prefix
  </details>

  #### **Example:**
  ```
  10.20.30.0/24
  ```

#### **`External Subnet IP Pool Range (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The IP address range for the external subnets.
  </details>

  #### **Example:**
  ```
  10.20.30.2-10.20.30.10
  ```

## **`External Subnet Gateway IP (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The gateway IP address for the external subnets.
  </details>

  #### **Example:**
  ```
  10.20.30.1
  ```

## **`External Subnet NAT (Required)`**

  #### **Type:** Boolean
  <details>
  <summary>Description</summary>
  This variable use to enable/disable NAT.
  </details>

  #### **Example:**
  ```
  True
  ```

## **`Overlay Subnet IP With Prefix (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the Overlay Subnet IP address with network prefix.
  </details>

  #### **Example:**
  ```
  10.10.10.0/24
  ```

## **`Overlay Subnet Gateway IP (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The gateway IP address for the overlay subnets.
  </details>

  #### **Example:**
  ```
  10.10.10.1
  ```

## **`Account Name (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The name of Calm account.
  </details>

  #### **Example:**
  ```
  Multipc-account
  ```

## **`Quota : vCPUs (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The Maximum amount of vCPUs that can be consumed by a project.
  </details>

  #### **Example:**
  ```
  10
  ```

## **`Quota : Memory in GB (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The Maximum amount of Memory that can be consumed by a project.
  </details>

  #### **Example:**
  ```
  20
  ```

## **`Quota : Disk Size in GB (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The Maximum amount of storage that can be consumed by a project.
  </details>

  #### **Example:**

  ```
  100
  ```

## **`Allow Project Collaboration (Required)`**

  #### **Type:** Boolean
  <details>
  <summary>Description</summary>
  The Allow collaboration flag .
  </details>

  #### **Example:**
  ```
  admin
  ```

## **`Create Project Environment with Default Values (Required)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This option decides creating default Environment for project.
  </details>

  #### **Example:**
  ```
  Yes
  ```

## **`Environment operating system (Optional)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  Operating System Type.
  </details>

  #### **Example:**
  ```
  Linux
  ```
  #### **Note:** if Create Project Environment with Default Values is selected as "Yes" user need to select proper environment operating system as mandatory.

## **`Image Name (Optional)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  The Name of Image which present on Prism Central or cluster.
  </details>

  #### **Example:**

  ```
  Centos7HadoopMaster
  ```
  #### **Note:** if Create Project Environment with Default Values is selected as "Yes" user need to pass proper Image Name as mandatory variable.

## **`Guest Customization Script (Optional)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  script that needs executed when a new virtual machine is deployed .
  </details>

  #### **Example:**

  ```
  Guest Customization Script = I2Nsb3VkLWNvbmZpZwp1c2VyczoKICAtIG5hbWU6IG51dGFuaXgKICAgIHNzaC1hdXRob3JpemVkLWtleXM6CiAgICAgIC0gc3NoLXJzYSBLRVkKICAgIHN1ZG86IFsnQUxMPShBTEwpIE5PUEFTU1dEOkFMTCddCiAgICBncm91cHM6IHN1ZG8KICAgIHNoZWxsOiAvYmluL2Jhc2gKCnBhY2thZ2VzOgogIC0gaHR0cGQ=
  ```
  #### **Note:** For Linux script should be ansible base64 encoded and for windows script should be in XML format.

## **`Environment Credential Username (Optional)`**   (Required)-</span>

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents the username used to authenticate project enviornment resources.
  </details>

  #### **Example:**
  ```
  root
  ```

## **`Credential Type (Optional)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  Authentication type ,could be SSH key-based or password .
  </details>

  #### **Example:**
  ```
  KEY
  ```

## **`Password Or Key (Optional)`**

  #### **Type:** string
  <details>
  <summary>Description</summary>
  This variable represents password/key used to authenticate project enviornment resources.
  </details>

  #### **Example:**
  ```
  test123
  ```
