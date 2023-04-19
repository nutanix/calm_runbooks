# Runbook Variables

## **`Management PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the username used to authenticate with the Managementt Prism Central management interface.
  </details>

  ### **Type:** _String_

  #### **Example:**

  ```
  admin
  ```

## **`Management PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the password used to authenticate with Prism Central.
  </details>

  ### **Type:** _String_
  ### **Example:**

  ```
  nutanix/4u
  ```

## **`Tenant Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the Name of the tenant. This ensures that all subsequent resources such as subnets, VPCs, projects, categories, and VPC tunnels are created under the correct tenant.
  </details>

  ### **Type:** _String_


  ### **Example:**

  ```
  MY_Tenant
  ```
  #### **Note:** All resources such as subnets,project,VPC etc.. are created under this teant using runbook will use tenant name as prefix while creating.

## **`Delete Existing setup (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the cleanup process for stale or existing resources such as project, VPC and tunnels, Subnets of "Tenant Name" as prefix.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  Yes
  ```

## **`Workload PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable specify the IP address of the Prism Central instance that should be used to onboard a tenant on the Workload Prism Central instance.
  </details>

  ### **Type:** _String_
  ### **Example:**
  ```
  Workload PC IP = 172.16.10.1
  ```

## **`Workload PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the Name of the username used to authenticate with the Workload Prism Central management interface 
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  admin
  ```

## **`Workload PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the password used to authenticate with the Workload Prism Central management interface 
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  Nutanix/4u
  ```

## **`Active Directory URL (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the URL address to the directory.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  ldap://10.10.10.66:389
  ```

## **`Active Directory Domain Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the domain name in DNS format.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  test.domain.com
  ```

## **`Active Directory Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the username used to authenticate with the Active Directory service.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  user@test.domain.com
  ```

## **`Active Directory Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the password used to authenticate with the Active Directory service. 
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  Test123
  ```

## **`Project Admin (Required)`**

  <details>
  <summary><b>Description</b></summary>
  A project admin of Nutanix who manages cloud objects belonging to a specific project. These cloud objects can include roles, virtual machines (VMs), applications, and marketplace items that are associated with the project.
  </details>

  ### **Type:** _String_


  ### **Example:**

  ```
  aduser@test.domain.com
  ```

## **`Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the Name of the Cluster.
  </details>
  
  ### **Type:** _String_

  ### **Example:**

  ```
  auto-pc-12345-6789
  ```

## **`Virtual Switch Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The name of the virtual switch.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vs0
  ```

## **`External VLAN ID (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The VLAN ID to be used for the virtual switch.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  110
  ```

## **`External Subnet IP with Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the External Subnet IP with Prefix
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.0/24
  ```

#### **`External Subnet IP Pool Range (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The IP address range for the external subnets.
  </details>
  
  ### **Type:** _String_


  ### **Example:**
  ```
  10.20.30.2-10.20.30.10
  ```

## **`External Subnet Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The gateway IP address for the external subnets.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.1
  ```

## **`External Subnet NAT (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable use to enable/disable NAT.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`Overlay Subnet IP With Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the Overlay Subnet IP address with network prefix.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.0/24
  ```

## **`Overlay Subnet Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The gateway IP address for the overlay subnets.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.1
  ```

## **`Account Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The name of Calm account.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  Multipc-account
  ```

## **`Quota : vCPUs (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Maximum amount of vCPUs that can be consumed by a project.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  10
  ```

## **`Quota : Memory in GB (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Maximum amount of Memory that can be consumed by a project.
  </details>
  
  ### **Type:** _Integer_

  ### **Example:**
  ```
  20
  ```

## **`Quota : Disk Size in GB (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Maximum amount of storage that can be consumed by a project.
  </details>

  ### **Type:** _Integer_

  ### **Example:**

  ```
  100
  ```

## **`Allow Project Collaboration (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Allow collaboration flag .
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`Create Project Environment with Default Values (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This option decides creating default Environment for project.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  Yes
  ```

## **`Environment operating system (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Operating System Type.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  Linux
  ```
  #### **Note:** if Create Project Environment with Default Values is selected as "Yes" user need to select proper environment operating system as mandatory.

## **`Image Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Name of Image which present on Prism Central or cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  Centos7HadoopMaster
  ```
  #### **Note:** if Create Project Environment with Default Values is selected as "Yes" user need to pass proper Image Name as mandatory variable.

## **`Guest Customization Script (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  script that needs executed when a new virtual machine is deployed .
  </details>

  ### **Type:** _Multi Line String_

  ### **Example:**

  ```
  Guest Customization Script = I2Nsb3VkLWNvbmZpZwp1c2VyczoKICAtIG5hbWU6IG51dGFuaXgKICAgIHNzaC1hdXRob3JpemVkLWtleXM6CiAgICAgIC0gc3NoLXJzYSBLRVkKICAgIHN1ZG86IFsnQUxMPShBTEwpIE5PUEFTU1dEOkFMTCddCiAgICBncm91cHM6IHN1ZG8KICAgIHNoZWxsOiAvYmluL2Jhc2gKCnBhY2thZ2VzOgogIC0gaHR0cGQ=
  ```
  #### **Note:** For Linux script should be ansible base64 encoded and for windows script should be in XML format.

## **`Environment Credential Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the username used to authenticate project enviornment resources.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  root
  ```

## **`Credential Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Authentication type ,could be SSH key-based or password .
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  KEY
  ```

## **`Password Or Key (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents password/key used to authenticate project enviornment resources.
  </details>

  ### **Type:** _Multi Line String_

  ### **Example:**
  ```
  test123
  ```
