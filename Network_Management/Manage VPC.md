# Runbook Variables

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

  Nutanix VPCs play a vital role in managing and organizing the network infrastructure within Nutanix environments, enabling secure and isolated deployments of virtual resources..
  </details>  
    
  ### **Type:** _String_

  ### **Example:**
  ```
  test_vpc
  ```

## **`Operation (Required)`**

  <details>
    <summary><b>Description</b></summary>
    This variable is used to specify the type of operation to perform on a Nutanix VPC. It should be set to either 'create', 'update', or 'delete' to indicate the desired action.

    Options:

        create: Set this option to create a new VPC.
        update: Set this option to modify an existing VPC.
        delete: Set this option to remove an existing VPC.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  create / update / delete
  ```

## **`VPC UUID (Required)`**

  <details>
    <summary><b>Description</b></summary>
    The VPC UUID refers to the unique identifier assigned to a Virtual Private Cloud (VPC) within the Nutanix infrastructure. This UUID is a string of characters that serves as a globally unique identifier for the VPC.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  886fa64c-ec19-407d-91bf-d2a5f310dc19
  ```

## **`External Subnet UUID (Required)`**

  <details>
    <summary><b>Description</b></summary>
    The External Subnet UUID refers to the unique identifier assigned to an external subnet within the Nutanix infrastructure. This UUID is a string of characters that serves as a globally unique identifier for the external subnet.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  ec2c7ade-141d-4c19-a036-36c5bda31a73
  ```

## **`Externally Routable IP with prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Externally routable IP with prefix refers to an IP address range that can be used to route traffic to and from the internet or external networks. It is typically associated with a Virtual Private Cloud (VPC) to enable communication between the VPC and external entities.

  The externally routable IP with prefix consists of an IP address and a subnet prefix length, usually represented as CIDR notation (e.g., 192.168.0.0/24). The IP address range specified within the prefix is routable on the internet, allowing traffic to flow between the VPC and external networks.

  When configuring a Nutanix VPC, you can define an externally routable IP range to allocate to the VPC. This IP range will be used for assigning IP addresses to the resources within the VPC, such as virtual machines or containers, that require connectivity to external networks.

  The specific procedure for configuring the externally routable IP with prefix in Nutanix may vary depending on the Nutanix software version and management interface being used. It is typically done during the creation or configuration of the VPC, where you can specify the desired IP range and prefix length for external connectivity.

  By assigning an externally routable IP with prefix to a Nutanix VPC, you enable communication between resources within the VPC and external networks, allowing them to access the internet and interact with other external systems.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.0/24
  ```

  ## **`DNS Server (Required)`**

  <details>
    <summary><b>Description</b></summary>
    Virtual Private Cloud (VPC) can have its own DNS (Domain Name System) servers configured. These DNS servers are responsible for resolving domain names to IP addresses within the VPC.

    When setting up a Nutanix VPC, you have the option to configure DNS server IP addresses specific to the VPC. This allows the resources within the VPC to resolve domain names and access resources using hostnames.

    To configure DNS server settings for a Nutanix VPC, you would typically provide the IP addresses of the DNS servers during the VPC creation or configuration process. The exact procedure may vary depending on the Nutanix software version and management interface you are using.

    Once the DNS server IP addresses are configured for the VPC, the resources within the VPC can use these DNS servers for domain name resolution. This ensures that hostnames can be resolved to their corresponding IP addresses, enabling proper network communication and access to resources within the VPC.

    It's important to ensure that the DNS servers configured for the Nutanix VPC are operational and accessible from the VPC's resources. This can be verified by performing DNS resolution tests from within the VPC to ensure that domain names can be resolved correctly.

    Note that the actual DNS server IP addresses may vary based on your specific network configuration and requirements within the Nutanix VPC. It is recommended to consult your network infrastructure documentation or contact your network administrator to obtain the correct DNS server IP addresses for your environment.
   </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  dns.sys.com
  ```

## **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.20.30.40
  ```

## **`PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central Username variable is used to specify the username that is used to authenticate with the Nutanix Prism Central management interface.

  Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Username variable should be set to the username that has been granted access to the Prism Central management interface.

  It is important to ensure that the Nutanix Prism Central Username variable is correctly configured and kept up-to-date to ensure that the Nutanix clusters can be managed effectively. The username specified in this variable should have the appropriate level of permissions to perform the required management tasks in Prism Central.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central Password variable is used to store the password that is used to authenticate with the Nutanix Prism Central management interface.

  Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Password variable should be set to the password that corresponds to the username specified in the Nutanix Prism Central Username variable.

  It is important to ensure that the Nutanix Prism Central Password variable is kept secure and protected. The password should be stored in a secure manner, such as using a password manager or an encrypted file, and should not be shared with unauthorized individuals. Additionally, it is recommended to periodically change the password for security reasons.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  nutanix/12
  ```
