# Runbook Variables

This runbook can create, update or delete overlay subnet.

## **`Management PC IP (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  Provide Management PC or CALM VM IP. This will be used for updating project with newly created overlay subnet if specified in `Add Subnet to Project` option.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  admin
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

  ### **Example:**
  ```
  admin
  ```

## **`Management PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the password used for authentication with the Nutanix Prism Central management interface. The management password is required for performing administrative tasks on the Nutanix cluster through the Prism Central management interface. It is used in combination with the management username to authenticate and access features such as health monitoring, capacity planning, resource management, and user management.
  </details>

  ### **Type:** _Integer_

  #### **Example:**
  ```
  nutanix123
  ```

## **`Subnet Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The overlay subnet name represents the name assigned to a specific overlay subnet within the Nutanix environment. It provides a unique identifier for the overlay subnet.

  The Nutanix overlay subnet is a virtual network created within the Nutanix environment that allows for seamless communication between virtual machines (VMs) and other network entities. It operates as an overlay on top of the physical network infrastructure, providing a secure and isolated network environment.

  The overlay subnet enables VMs to communicate with each other regardless of their physical location or the underlying network infrastructure. It abstracts the underlying network details and provides a virtualized network space for VMs to interact.

  The Nutanix overlay subnet utilizes various technologies, such as VXLAN (Virtual Extensible LAN), to encapsulate and tunnel network traffic between VMs. This enables VMs to communicate as if they were on the same local network, even if they are distributed across different physical hosts or datacenters.

  By using overlay networks, Nutanix allows for flexible deployment and scaling of VMs without being constrained by physical network limitations. It simplifies network management and provides the foundation for building highly available and resilient virtualized infrastructures.

  The overlay subnet also incorporates network security features, such as micro-segmentation and network policies, to enforce access controls and protect against unauthorized access. These security measures help isolate and protect individual VMs and ensure the integrity of the overlay network.

  Overall, the Nutanix overlay subnet plays a crucial role in enabling efficient and secure communication among VMs within the Nutanix environment, providing a flexible and scalable network infrastructure for virtualized workloads.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  Test_overlay_subnet
  ```

## **`Operation (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is used to determine the type of operation to perform on a Nutanix overlay subnet. It should be set to 'create', 'update', or 'delete', depending on the desired action.

    'create': Use this option to create a new Nutanix overlay subnet.
    'update': Use this option to modify an existing Nutanix overlay subnet.
    'delete': Use this option to remove an existing Nutanix overlay subnet.

    Setting the correct value for this variable is crucial as it determines the specific API call to be made to the Nutanix management platform.

    Please note that certain operations may require additional parameters or configuration options, depending on the specific resource being created, updated, or deleted. Refer to the Nutanix documentation and API reference for detailed requirements of each operation.

    It is important to understand that Nutanix overlay subnets play a vital role in managing virtual networks within a Nutanix cluster. Therefore, any modifications made to these subnets can significantly impact the overall cluster performance. To mitigate any potential issues, it is highly recommended to follow best practices and thoroughly test any changes in a non-production environment before deploying them in a production environment.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  create / update / delete
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

  #### **Type:** _String_

  ### **Example:**
  ```
  test_vpc
  ```

## **`Network IP with Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In a Nutanix overlay subnet, the network IP with prefix refers to the IP address range allocated to the subnet, along with the associated subnet mask or prefix length. The network IP represents the base address of the subnet, while the prefix indicates the number of bits used to define the subnet.

  For example, if the network IP is 192.168.0.0 and the prefix is /24, it means that the subnet includes IP addresses ranging from 192.168.0.0 to 192.168.0.255, with a subnet mask of 255.255.255.0.

  The prefix length is represented as the number of consecutive bits set to 1 in the subnet mask. In the example above, /24 indicates that the first 24 bits of the IP address are used to identify the network portion, while the remaining 8 bits are available for host addresses.

  The network IP with prefix is essential for defining the address space and subnet boundaries within a Nutanix overlay subnet. It helps in determining the range of available IP addresses and configuring the appropriate network settings for virtual machines, routing, and connectivity within the subnet.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.0/24
  ```

## **`Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In a subnet overlay network, a gateway IP refers to the IP address assigned to the gateway device within the overlay network. The gateway acts as an intermediary between the overlay network and external networks or other subnets.

  The specific IP address of the gateway depends on the configuration of the overlay network. Typically, the gateway IP address is chosen from within the range of IP addresses assigned to the subnet. It serves as the default gateway for devices within the subnet to communicate with devices outside the subnet or in other subnets.

  For example, let's say you have an overlay network with a subnet using the IP address range 192.168.0.0/24. The gateway IP address might be assigned as 192.168.0.1. This means that any device within the subnet would use 192.168.0.1 as the gateway IP to send traffic outside the subnet.

  It's important to note that the specific configuration of a subnet overlay network, including the choice of gateway IP, can vary depending on the network infrastructure and the technology being used for overlay networking, such as Virtual Extensible LAN (VXLAN) or Generic Routing Encapsulation (GRE)..
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.10.1
  ```

## **`IP Pools (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, an overlay subnet IP pool is a range of IP addresses used for overlay networking within the Nutanix environment. These IP addresses are assigned to virtual machines (VMs) and services running on the Nutanix cluster.

  The overlay subnet IP pools in Nutanix are typically managed by the Acropolis Distributed Network Encryption (ADNE) feature, which provides network encryption and segmentation capabilities. ADNE uses VXLAN (Virtual Extensible LAN) technology to create overlay networks.

  To configure overlay subnet IP pools in Nutanix, you would typically follow these steps:

    Access the Nutanix Prism Central web interface.
    Navigate to the Networking section and locate the ADNE settings.
    Create a new overlay subnet IP pool or modify an existing one.
    Specify the IP address range for the pool, ensuring it does not overlap with other networks or subnets in your environment.
    Define any additional settings or options, such as the subnet mask, gateway IP, DNS servers, etc.
    Save the configuration.

  Once the overlay subnet IP pool is configured, Nutanix will automatically allocate IP addresses from the pool to the virtual machines and services as they are created within the Nutanix cluster. This allows for seamless communication and networking between the VMs and services, while maintaining security and isolation through the overlay network.

  It's important to note that the exact steps and terminology may vary depending on the specific version of Nutanix software you are using. It's recommended to consult the official Nutanix documentation or contact Nutanix support for detailed instructions based on your environment.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.2-10.10.10.30
  ```

## **`DNS Servers List (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix overlay subnet DNS servers are the DNS servers that are configured specifically for the overlay network subnet in a Nutanix environment. These DNS servers are responsible for resolving domain names to IP addresses within the overlay subnet.

  The exact configuration and IP addresses of the Nutanix overlay subnet DNS servers may vary depending on your specific Nutanix deployment and network setup. To determine the DNS servers configured for the overlay subnet in your Nutanix environment, you can refer to your network configuration or consult your Nutanix administrator or network team.

  Typically, the Nutanix overlay subnet DNS servers are set to the IP addresses of the DNS servers provided by your network infrastructure or DNS service provider. These DNS servers enable proper name resolution within the overlay subnet, allowing network resources to be accessed using hostnames.

  It's important to ensure that the Nutanix overlay subnet DNS servers are properly configured and operational to facilitate smooth network communication and access to resources within the overlay network.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  server.dns.com
  ```

## **`Domain Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Domain names are typically associated with DNS (Domain Name System) and are used to translate human-readable domain names (such as example.com) into IP addresses. While the Nutanix overlay subnet may utilize DNS servers for name resolution, the subnet itself does not have a dedicated domain name.

  The domain name configuration within the Nutanix environment would typically be managed at a higher level, such as the DNS configuration for the overall network or within specific virtual machines or services running on the Nutanix platform.

  If you require a domain name for resources within the Nutanix overlay subnet, you would need to configure the appropriate DNS settings and assign domain names to individual virtual machines or services within that subnet.

  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  test.com
  ```
## **`Domain Search List (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The domain search list is a configuration setting used by DNS resolvers to search for domain names when a hostname is entered without a fully qualified domain name (FQDN). It allows the resolver to append domain suffixes to the hostname and attempt to resolve the name using different domain names.

  The domain search list is typically configured at the client level or within the DNS resolver settings of the operating system or network infrastructure. It is not directly tied to the Nutanix overlay subnet itself.

  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  8.8.8.8
  ```
## **`Boot File Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The boot file name is usually specific to the operating system or boot loader being used and is typically configured within the DHCP server settings. It specifies the file name or path that the client should retrieve from a TFTP server to start the boot process.

  In a Nutanix environment, the configuration of boot file names would typically be handled at the DHCP server level or within the virtual machine configurations themselves. The Nutanix overlay subnet would not have a specific boot file name associated with it as it is a networking construct rather than a boot configuration.

  If you are looking to configure boot file names for virtual machines or services within your Nutanix environment, you would need to configure the appropriate DHCP server settings or virtual machine configurations as per your specific requirements.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  boot.test
  ```

## **`TFTP Server (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The configuration and setup of a TFTP server in a Nutanix environment would be similar to setting up a TFTP server in any other network environment. This would typically involve installing TFTP server software on a separate server or device, configuring the server to serve the desired files, and ensuring proper network connectivity and access.

  Once the TFTP server is set up, you can configure the appropriate network boot settings or firmware update procedures within your Nutanix environment to utilize the TFTP server as needed.

  Please note that the specific steps for setting up a TFTP server may vary depending on your network infrastructure, operating system, and specific requirements. It's recommended to consult the documentation of your chosen TFTP server software and consider best practices for secure and reliable file transfers within your network environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  tftp.server.com
  ```
## **`Add Subnet to Project (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable defines whether the subnet should be added to the project or not.
 </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  Yes / No
  ```

## **`Project Name (Optional)`**

  <details>
  <summary><b>Description</b></summary>

    In Nutanix, a project refers to a logical grouping or container that allows you to organize and manage various resources within your Nutanix environment. Projects provide a way to isolate and allocate resources, such as virtual machines, networks, storage, and policies, for specific teams, departments, or applications.

    Make sure VPC is added to the project specified here.

    Here are some key characteristics and functionalities of a Nutanix project:

    Resource segregation: Projects enable you to segregate resources within your Nutanix environment, providing dedicated spaces for different teams or projects. This segregation helps in better resource management, control, and isolation.

    Access control: Projects allow you to define access control policies, granting specific permissions to users or groups for managing and accessing resources within the project. This helps enforce security and restrict unauthorized access to resources.

    Resource allocation: With projects, you can allocate specific resources to a project, ensuring that the resources are dedicated and available for the intended purpose. This includes allocating CPU, memory, storage, and networking resources.

    Quotas and limits: Projects support setting quotas and limits on resource usage. You can define limits on the amount of CPU, memory, and storage that a project can consume, ensuring fair resource distribution and preventing resource hogging.

    Policy enforcement: Projects enable the enforcement of policies specific to the project's requirements. This includes policies related to networking, security, compliance, and governance.

    Reporting and monitoring: Nutanix provides reporting and monitoring capabilities at the project level, allowing you to track resource usage, performance metrics, and health status of resources within a project.

    Projects in Nutanix offer a structured and controlled approach to managing and organizing resources, promoting efficient resource utilization, better security, and simplified administration within your Nutanix environment.

</details>

  ### **Type:** _String_

  ### **Example:**
  ```
  test_project
  ```

## **`Workload PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the IP address or hostname of the Nutanix Prism Central instance that will be used for workload management. The Prism Central instance acts as a centralized management interface for multiple Nutanix clusters, allowing administrators to manage and monitor workloads across different clusters from a single interface. This variable is required for any operations that involve workload management through Prism Central, such as creating or managing virtual machines, configuring storage policies, and setting up data protection policies.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.6
  ```

## **`Workload PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be provided as input to specify the username used for authentication with the Nutanix Prism Central instance for workload management. The management username is required for performing administrative tasks related to workload management on the Nutanix clusters through the Prism Central management interface. Once authenticated, administrators can create and manage virtual machines, configure storage policies, and set up data protection policies for their workloads.
  </details>

  ### **Type:** _String_

  ### **Example:**
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
  nutanix
  ```
