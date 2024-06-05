# Tenant Onboarding Runbook
The process of onboarding a new tenant is facilitated by the Service Provider using the Tenant onboarding runbook. The Service Provider executes this runbook from a Management cluster, which in turn creates all the required virtual resources on a Workload cluster for the tenant to run their applications. The workflow for the tenant onboarding process is illustrated below.

![image](https://github.com/ideadevice/calm_runbooks/assets/97866756/b1300b17-8b14-45d9-8fb2-e979c59bda3b)

![Tenant Onboarding](/images/tenant_onboarding.png)

# Tenant Onboarding Runbooks for different CALM versions:
Use tenant onboarding runbook from this table as per your management cluster calm version.
| Calm Version       | Link           
| ------------------ |:-------------:|
| v3.7.2.1             |[Tenant Onboarding](https://github.com/nutanix/calm_runbooks/tree/release/calm-3.7.2.1/Tenant_onboarding)|
| v3.8.0           |[Tenant Onboarding](https://github.com/nutanix/calm_runbooks/tree/release/calm-3.8.0/Tenant_onboarding) |

# Runbook Variables

## **`Management PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the IP address or hostname of the Nutanix Prism Central management interface. The Prism Central instance acts as a centralized management interface for multiple Nutanix clusters, allowing administrators to manage and monitor workloads across different clusters from a single interface. This variable is required.
  </details>

  ### **Type:** _String_
  ### **Example:**
  ```
  10.44.46.56
  ```

## **`Management PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the username used for authentication with the Nutanix Prism Central management interface. The management username is required for performing administrative tasks on the Nutanix cluster through the Prism Central management interface. It allows access to features such as health monitoring, capacity planning, resource management, and user management.

  Nutanix Prism Central is a web-based management interface that allows administrators to manage and monitor multiple Nutanix clusters from a single interface. It provides a unified management experience across multiple Nutanix clusters and enables centralized management of virtualization, storage, and network resources.

  The Nutanix Prism Central management interface provides various features such as health monitoring, capacity planning, resource management, and user management. It also allows administrators to create and manage virtual machines, configure storage policies, and set up data protection policies.

  To access the Prism Central management interface, you need to have valid credentials, which typically include a username and password. Once logged in, you can perform various administrative tasks, such as creating and managing Nutanix clusters, configuring network and storage resources, and monitoring the health and performance of your Nutanix infrastructure.

  </details>

  ### **Type:** _String_

  #### **Example:**

  ```
  admin
  ```

## **`Management PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the password used for authentication with the Nutanix Prism Central management interface. The management password is required for performing administrative tasks on the Nutanix cluster through the Prism Central management interface. It is used in combination with the management username to authenticate and access features such as health monitoring, capacity planning, resource management, and user management.
  </details>

  ### **Type:** _String_
  ### **Example:**

  ```
  nutanix/4u
  ```

## **`Tenant Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable may be provided as input to specify the name of the tenant or organization associated with the Nutanix cluster. The tenant name can be used to organize multiple Nutanix clusters by assigning them to specific tenants or organizations. This can be useful for large enterprises or service providers that manage multiple Nutanix clusters for different departments or customers. If not provided, the default tenant name will be used.
  </details>

  ### **Type:** _String_


  ### **Example:**

  ```
  MY_Tenant
  ```
  #### **Note:** When using a runbook to create resources like subnets, projects, and VPCs, they will be created under a specific tenant. The tenant name will be used as a prefix during creation to organize the resources accordingly.

## **`Delete Existing setup (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The purpose of this variable is to define the cleanup process for obsolete or pre-existing resources such as projects, VPCs, tunnels, and subnets that have a "Tenant Name" prefix.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  No
  ```

## **`Workload PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the IP address or hostname of the Nutanix Prism Central instance that will be used for workload management. The Prism Central instance acts as a centralized management interface for multiple Nutanix clusters, allowing administrators to manage and monitor workloads across different clusters from a single interface. This variable is required for any operations that involve workload management through Prism Central, such as creating or managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  ### **Type:** _String_
  ### **Example:**
  ```
  172.16.10.1
  ```

## **`Workload PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the username used for authentication with the Nutanix Prism Central instance for workload management. The management username is required for performing administrative tasks related to workload management on the Nutanix clusters through the Prism Central management interface. Once authenticated, administrators can create and manage virtual machines, configure storage policies, and set up data protection policies for their workloads.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  admin
  ```

## **`Workload PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the password used for authentication with the Nutanix Prism Central instance for workload management. The management password is required for performing administrative tasks related to workload management on the Nutanix clusters through the Prism Central management interface. It is used in combination with the management username to authenticate and access features such as creating and managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  Nutanix/4u
  ```

## **`Active Directory URL (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the URL of the Active Directory (AD) server that will be used for user authentication and authorization on the Nutanix cluster. AD is a directory service used in Windows-based environments to store and organize information about users, computers, and other resources on a network. This variable is required for any operations that require user authentication and authorization on the Nutanix cluster using AD, such as creating and managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  ldap://10.10.10.66:389
  ```

## **`Active Directory Domain Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the name of the Active Directory (AD) domain that will be used for user authentication and authorization on the Nutanix cluster. AD is a directory service used in Windows-based environments to store and organize information about users, computers, and other resources on a network. This variable is required for any operations that require user authentication and authorization on the Nutanix cluster using AD, such as creating and managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  test.domain.com
  ```

## **`Active Directory Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the username used for authentication with the Nutanix cluster using the Active Directory (AD) server. The username is used in combination with the password to authenticate and authorize users to access shared drives, printers, and other network resources that are secured by AD. This variable is required for any operations that require user authentication and authorization on the Nutanix cluster using AD, such as creating and managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  user@test.domain.com
  ```

## **`Active Directory Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is necessary to set the password for the Nutanix AD service account used for user authentication and authorization on the Nutanix cluster. AD is a directory service that stores and organizes information about users, computers, and resources on a network in Windows-based environments. This variable is mandatory for any operations that need user authentication and authorization on the Nutanix cluster through AD, such as creating and managing virtual machines, setting up data protection policies, and configuring storage policies.
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  Test123
  ```

## **`Project Admin (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the username of the Nutanix project administrator who has permissions to create, manage and delete projects on the Nutanix cluster. A project administrator is responsible for managing resources such as virtual machines, networks, storage, and user accounts that are assigned to a project. This variable is mandatory for any operations that require creating, managing or deleting projects on the Nutanix cluster using APIs or CLI.
  </details>

  ### **Type:** _String_


  ### **Example:**

  ```
  aduser@test.domain.com
  ```

## **`Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the name of the Nutanix cluster that will be used for the deployment. The cluster name is a unique identifier for a Nutanix cluster and is used for managing resources such as virtual machines, networks, storage, and user accounts. This variable is required for any operations that interact with the Nutanix cluster using API or CLI.
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  auto-pc-12345-6789
  ```

## **`Virtual Switch Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the name of the virtual switch on the Nutanix cluster that will be used for networking operations. A virtual switch is a software-based network switch that connects virtual machines to each other and to the physical network. This variable is required for any operations that involve configuring or managing virtual networks on the Nutanix cluster using API or CLI.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vs0
  ```

## **`External VLAN ID (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the VLAN ID for the external network connection on the Nutanix cluster. VLAN (Virtual Local Area Network) is a technology that enables multiple networks to share a single physical network infrastructure. If you have an external network connection, you can use this variable to specify the VLAN ID to be used for communication with the external network. This variable is optional and only required if you have an external network connection configured on the Nutanix cluster.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  110
  ```

## **`External Subnet IP with Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the IP address and prefix length for the external subnet on the Nutanix cluster. The IP address and prefix length together define the range of IP addresses that can be used for the external network connection. This variable is optional and only required if you have an external network connection configured on the Nutanix cluster and need to specify the IP address and prefix for the external subnet.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.0/24
  ```

#### **`External Subnet IP Pool Range (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the IP address pool range for the external subnet on the Nutanix cluster. The IP address pool range defines the range of IP addresses that can be used for the external network connection. This variable is optional and only required if you have an external network connection configured on the Nutanix cluster and need to specify the IP address pool range for the external subnet.
  </details>

  ### **Type:** _String_


  ### **Example:**
  ```
  10.20.30.2-10.20.30.10
  ```

## **`External Subnet Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the IP address of the default gateway for the external subnet on the Nutanix cluster. The default gateway is the IP address of the router that connects the external subnet to other networks. This variable is optional and only required if you have an external network connection configured on the Nutanix cluster and need to specify the IP address of the default gateway for the external subnet.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.1
  ```

## **`External Subnet NAT (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the NAT IP address for the external subnet on the Nutanix cluster. Network Address Translation (NAT) is used to map one IP address space into another by modifying network address information in the IP header of packets while they are in transit across a traffic routing device. This variable is optional and only required if you have an external network connection configured on the Nutanix cluster and need to specify the NAT IP address for the external subnet.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`Overlay Subnet IP With Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the IP address and prefix length for the overlay subnet on the Nutanix cluster. The overlay subnet is used for virtualized workloads and is isolated from the external networks. The IP address and prefix length together define the range of IP addresses available for use within the overlay subnet. This variable is required for configuring the overlay subnet on the Nutanix cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.0/24
  ```

## **`Overlay Subnet Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the IP address of the gateway for the overlay network subnet used for communication between virtual machines within the Nutanix cluster. The overlay network is a software-defined network that provides a virtual network layer on top of the physical network infrastructure. The gateway IP address is used as the default gateway for the virtual machines within the overlay network. This variable is required for any operations that involve configuring or managing the overlay network on the Nutanix cluster, such as creating virtual machines, configuring network security policies, and setting up load balancing
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.1
  ```

## **`Account Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the name of the Nutanix storage account used for provisioning and managing storage resources on the Nutanix cluster. Storage accounts provide a logical grouping of storage resources, such as containers and datastores, and are used to allocate and manage storage capacity for various applications and workloads. This variable is required for any operations that involve storage provisioning or management on the Nutanix cluster using the Prism Central management interface or APIs.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  Multipc-account
  ```

## **`Quota : vCPUs (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the maximum number of virtual CPUs (vCPUs) that can be allocated to a project on the Nutanix cluster. It is a required input parameter for creating a project and setting resource limits on it. The vCPU quota determines the number of virtual processors that can be used by virtual machines (VMs) running within the project. Exceeding the vCPU quota may result in performance degradation or VMs failing to power on.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  10
  ```

## **`Quota : Memory in GB (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the maximum amount of memory in gigabytes that can be consumed by virtual machines running in a Nutanix project. The memory quota is a limit set on the amount of memory that can be allocated to virtual machines, and it ensures that the project does not exceed its resource allocation. This quota can be adjusted as needed to optimize resource usage and meet changing workload demands.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  20
  ```

## **`Quota : Disk Size in GB (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the disk size quota in GB for a Nutanix project. A project is a logical container for a group of related entities and resources, and disk size quota refers to the maximum disk space that can be used by virtual machines created within the project. This variable is required for any operation that involves creating virtual machines within the project, as the virtual machines will consume disk space as they are created and run. It is important to ensure that the disk size quota is set appropriately to prevent overconsumption of disk space and to ensure that sufficient resources are available for other projects and applications.
  </details>

  ### **Type:** _Integer_

  ### **Example:**

  ```
  100
  ```

## **`Allow Project Collaboration (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Allow Project Collaboration" feature in Nutanix allows multiple projects to collaborate and share resources within a single Nutanix cluster. When this feature is enabled, users can be added to multiple projects and can access resources such as virtual machines, networks, and storage across all projects. This can improve resource utilization and reduce management overhead in environments where multiple teams or business units share a common infrastructure.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`Create Project Environment with Default Values (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Creating a project environment refers to the process of setting up an isolated environment for a specific project on the Nutanix cluster. This involves configuring resources such as virtual machines, networks, storage, and other services required for the project. The project environment can be customized based on the project requirements, and it can be created using the Nutanix management interface, such as Prism Central or using APIs. The process typically involves defining the project requirements, selecting the resources, configuring the settings, and deploying the project environment. The project environment can also be managed and monitored using the Nutanix management interface to ensure optimal performance and availability.

  This refers to the creation of a Calm environment within a Nutanix project, which allows for the deployment and management of applications and services. A Calm environment provides a platform for developing and publishing applications, and includes a range of tools and services for orchestration, automation, and monitoring. The creation of a Calm environment typically involves specifying the infrastructure resources required for the environment, such as virtual machines, networks, and storage, as well as the applications and services that will be deployed within the environment.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  Yes
  ```

## **`Environment operating system (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix project environment operating system refers to the type of operating system that will be installed on the virtual machines within the project. It is usually specified during the creation of a project environment and can be set to a variety of operating systems, including Windows, Linux, and others. This specification is important because it affects the applications and workloads that can be run within the project, as well as the security features and management tools that will be available.
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
  This variable specifies the name of the Nutanix image that will be used to create a new VM or update an existing one. An image is a pre-configured and optimized template that contains the operating system, applications, and other necessary components for a particular workload. The image name must be unique within the Nutanix cluster and match the name of an existing image in the image repository. Providing a valid image name is required for any operation that involves creating, updating, or managing VMs in Nutanix, such as launching a new VM or modifying its configuration.
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
  Nutanix Guest Customization Script is a script that can be used to automate the configuration of virtual machines running on the Nutanix AHV hypervisor. This script can be used to install software, configure settings, and perform other tasks on the virtual machine. The script can be written in any scripting language that is supported by the guest operating system, such as PowerShell or Bash, and can be executed during the virtual machine provisioning process. This variable should be provided as input to specify the path to the guest customization script that should be executed on the virtual machine during provisioning.
  </details>

  ### **Type:** _Multi Line String_

  ### **Example:**

  ```
  Guest Customization Script = I2Nsb3VkLWNvbmZpZwp1c2VyczoKICAtIG5hbWU6IG51dGFuaXgKICAgIHNzaC1hdXRob3JpemVkLWtleXM6CiAgICAgIC0gc3NoLXJzYSBLRVkKICAgIHN1ZG86IFsnQUxMPShBTEwpIE5PUEFTU1dEOkFMTCddCiAgICBncm91cHM6IHN1ZG8KICAgIHNoZWxsOiAvYmluL2Jhc2gKCnBhY2thZ2VzOgogIC0gaHR0cGQ=
  ```
  #### **Note:** The customization script for Linux environments should be encoded in Ansible Base64 format, while for Windows environments, the script should be in XML format.

## **`Environment Credential Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable refers to the username that is required to authenticate and access the environment in the Nutanix project. This credential is used for various purposes, such as deploying and configuring applications, managing virtual machines, and performing other operations within the project environment. It is important to provide a valid and secure username to ensure proper access control and security measures within the Nutanix project.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  root
  ```

## **`Credential Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable refers to the type of credential used to authenticate and authorize access to resources in the Nutanix environment. There are various types of credentials supported by Nutanix, such as username and password, SSH key, certificate, and more. The credential type may vary based on the type of resource being accessed and the security requirements of the organization. The credential type can be specified as input when creating or configuring resources in the Nutanix environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  KEY
  ```

## **`Password Or Key (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to indicate the authentication method required to access the target machine during deployment. It is a mandatory input when deploying an application or service to a Nutanix cluster, and the user must provide the value while executing the deployment task. When using a password for authentication, the value must be provided as plain text, while an SSH key should be provided in PEM format. The actual value entered will be determined by the specific deployment criteria and security guidelines in place.
  </details>

  ### **Type:** _Multi Line String_

  ### **Example:**
  ```
  test123
  ```
