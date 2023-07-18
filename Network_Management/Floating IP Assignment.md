# Runbook Variables

## **`Floating IP Assignment Type (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  Floating IP assignment refers to a network configuration in which an IP address is not permanently tied to a specific device or network interface. Instead, the IP address can be dynamically assigned to different devices or interfaces as needed.
  </details>  
    
  ### **Type:** _String_

  ### **Example:**
  ```
  IP
  ```

## **`VM IP (Required)`**

  <details>
    <summary><b>Description</b></summary>
    When referring to a "VM IP," it typically means the IP address assigned to a specific virtual machine (VM). In a virtualized environment, each VM is typically allocated its own unique IP address, allowing it to communicate with other devices on the network
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
 10.20.40.36
  ```

## **`VPC Name (Required)`**

  <details>
    <summary><b>Description</b></summary>
    This variable represents the name of a Nutanix Virtual Private Cloud (VPC) and is used to identify and reference a specific VPC within a Nutanix environment.
    Nutanix VPC (Virtual Private Cloud) is a virtual network infrastructure provided by Nutanix for managing and organizing resources within a cloud environment. It is designed to create isolated network environments where virtual machines (VMs) and other resources can be deployed and interconnected securely.

    In Nutanix, a VPC allows users to define their own private network space with its own IP address range, subnets, and routing rules. It provides a logical abstraction of the network infrastructure, enabling users to create multiple VPCs within a Nutanix cluster and isolate resources based on different requirements, applications, or tenants.

    Key features and benefits of Nutanix VPC include:

      Network Isolation: VPCs enable logical network isolation, allowing different environments or tenants to operate independently within their own private network space.

      IP Address Management: Users can define their IP address range and subnets for each VPC, ensuring efficient IP address management and minimizing conflicts.

      Security and Segmentation: VPCs provide security controls, such as security groups, network access control lists (ACLs), and routing policies, to enforce access control and traffic segmentation between different VPCs or resources.

      Scalability and Flexibility: Nutanix VPCs can be easily scaled up or down based on resource requirements. They provide flexibility in terms of adding or removing subnets, updating IP address ranges, and adjusting network configurations.

      Connectivity Options: VPCs can be connected to other networks, such as on-premises data centers or external networks, using VPN (Virtual Private Network) or direct connectivity options, enabling hybrid cloud deployments.

    Nutanix VPCs play a vital role in managing and organizing the network infrastructure within Nutanix environments, enabling secure and isolated deployments of virtual resources.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  test_vpc
  ```

## **`External Subnet Name (Required)`**

  <details>
    <summary><b>Description</b></summary>
    This variable represents the name of the subnet that enables external connectivity for a Nutanix cluster. Its purpose is to assign external IP addresses to the virtual machines and networking resources such as load balancers within the cluster. The external subnet should have an adequate number of available IP addresses to handle the anticipated workload of the cluster. To ensure proper functionality of the cluster, it is crucial to keep the Nutanix.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  test_subnet
  ```

## **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
   The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.30
  ```

  ## **`Prism Central Password (Required)`**

  <details>
    <summary><b>Description</b></summary>
    The Nutanix Prism Central Password variable is used to store the password that is used to authenticate with the Nutanix Prism Central management interface.

    Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Password variable should be set to the password that corresponds to the username specified in the Nutanix Prism Central Username variable.

    It is important to ensure that the Nutanix Prism Central Password variable is kept secure and protected. The password should be stored in a secure manner, such as using a password manager or an encrypted file, and should not be shared with unauthorized individuals. Additionally, it is recommended to periodically change the password for security reasons.
   </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`Prism Central Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central Username variable is used to specify the username that is used to authenticate with the Nutanix Prism Central management interface.

  Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Username variable should be set to the username that has been granted access to the Prism Central management interface.

  It is important to ensure that the Nutanix Prism Central Username variable is correctly configured and kept up-to-date to ensure that the Nutanix clusters can be managed effectively. The username specified in this variable should have the appropriate level of permissions to perform the required management tasks in Prism Central.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  nutanix/4u
  ```


