# Runbook Variables

## **`Management PC Username (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the username used for authentication with the Nutanix Prism Central management interface. The management username is required for performing administrative tasks on the Nutanix cluster through the Prism Central management interface. It allows access to features such as health monitoring, capacity planning, resource management, and user management.

  Nutanix Prism Central is a web-based management interface that allows administrators to manage and monitor multiple Nutanix clusters from a single interface. It provides a unified management experience across multiple Nutanix clusters and enables centralized management of virtualization, storage, and network resources.

  The Nutanix Prism Central management interface provides various features such as health monitoring, capacity planning, resource management, and user management. It also allows administrators to create and manage virtual machines, configure storage policies, and set up data protection policies.

  To access the Prism Central management interface, you need to have valid credentials, which typically include a username and password. Once logged in, you can perform various administrative tasks, such as creating and managing Nutanix clusters, configuring network and storage resources, and monitoring the health and performance of your Nutanix infrastructure.

  </details>  
    
  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`Management PC Password (Required)`**

  <details>
    <summary><b>Description</b></summary>
    This variable should be provided as input to specify the password used for authentication with the Nutanix Prism Central management interface. The management password is required for performing administrative tasks on the Nutanix cluster through the Prism Central management interface. It is used in combination with the management username to authenticate and access features such as health monitoring, capacity planning, resource management, and user management.
  </details>

  ### **Type:** _String_

  #### **Example:**
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
  nutanix_tenant
  ```

## **`Delete only network configuration (Required)`**

  <details>
  <summary><b>Description</b></summary>
    If the user provides the input as True, the program should check if the subnets and VPC are not being used in the project. If they are not being used, the program should proceed to delete the subnets and VPC.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  True / False
  ```

## **`Workload PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the IP address or hostname of the Nutanix Prism Central instance that will be used for workload management. The Prism Central instance acts as a centralized management interface for multiple Nutanix clusters, allowing administrators to manage and monitor workloads across different clusters from a single interface. This variable is required for any operations that involve workload management through Prism Central, such as creating or managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.40
  ```

  ## **`Workload PC Username (Required)`**

  <details>
    <summary><b>Description</b></summary>
  This variable should be provided as input to specify the username used for authentication with the Nutanix Prism Central instance for workload management. The management username is required for performing administrative tasks related to workload management on the Nutanix clusters through the Prism Central management interface. Once authenticated, administrators can create and manage virtual machines, configure storage policies, and set up data protection policies for their workloads.
   </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`Workload PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the password used for authentication with the Nutanix Prism Central instance for workload management. The management password is required for performing administrative tasks related to workload management on the Nutanix clusters through the Prism Central management interface. It is used in combination with the management username to authenticate and access features such as creating and managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  nutanix/4u
  ```
