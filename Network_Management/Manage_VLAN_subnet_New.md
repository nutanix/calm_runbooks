# Runbook Variables

## **`Subnet Name (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Subnet of VLAN type refers to a virtual local area network (VLAN) subnet that is created and managed within a Nutanix cluster. It allows multiple networks to coexist on the same physical network, and can be used to segregate traffic based on specific requirements, such as security or performance. The Nutanix VLAN Subnet Name variable is typically used to identify and manage this type of subnet.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  test_1234
  ```

## **`VLAN ID (Required)`**

  <details>
  <summary><b>Description</b></summary>
  A VLAN Subnet VLAN ID is a numerical identifier assigned to a virtual local area network (VLAN) subnet within a larger network. It is used to differentiate traffic on the network and enable better network management, particularly in larger environments where multiple VLANs are in use. In the context of Nutanix, the VLAN Subnet VLAN ID variable may be used to assign a unique ID to a VLAN subnet that is being managed within a Nutanix cluster.
  </details>

  ### **Type:** _Integer_

  #### **Example:**
  ```
  100
  ```

## **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
   The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.40.50.60
  ```

## **`Operation (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is used to determine the type of operation to perform on a Nutanix VLAN subnet. It should be set to 'create', 'update', or 'delete', depending on the desired action.

    'create': Use this option to create a new Nutanix VLAN subnet.
    'update': Use this option to modify an existing Nutanix VLAN subnet.
    'delete': Use this option to remove an existing Nutanix VLAN subnet.

    The value of this variable will determine the specific API call that will be made to the Nutanix management platform, so it is crucial to ensure that the correct value is set for the intended operation.

    Note that some operations may require additional parameters or configuration options, depending on the specific resource being created, updated, or deleted. Refer to the Nutanix documentation and API reference for more details on the requirements for each operation.

    It is important to note that Nutanix VLAN subnets play a crucial role in managing virtual networks within a Nutanix cluster. Therefore, any modifications made to these subnets can have an impact on the overall performance of the cluster. To avoid any potential issues, it is recommended to adhere to best practices and thoroughly test any changes in a non-production environment before deploying them in a production environment.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  create / update / delete
  ```

## **`Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Cluster Name variable is used to store the name of the Nutanix cluster being managed. It is a critical identifier for the cluster within the Nutanix environment and in external systems that interact with the cluster.

  The Nutanix cluster is a group of Nutanix nodes that work together to provide a scalable, highly available, and performant infrastructure for virtualized workloads. The cluster uses software-defined storage and hyperconverged infrastructure (HCI) technology to provide a distributed file system that aggregates the local storage of each node and presents it as a single shared pool of storage to the virtual machines running on the cluster.

  The Nutanix Cluster Name variable is typically used in conjunction with other Nutanix management variables, such as the Prism Central IP address, to manage the Nutanix cluster. It should be set to a unique and descriptive name that accurately reflects the purpose and function of the Nutanix cluster.

  Maintaining the Nutanix Cluster Name variable is crucial to ensure that the cluster remains identifiable and correctly configured. This helps to avoid any confusion with other clusters in the environment and ensures that the Nutanix cluster can be effectively managed and monitored.

  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  autopc-1278-55-t89
  ```

## **`Virtual Switch Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix VLAN Subnet Virtual Switch Name variable is used to store the name of the virtual switch associated with the VLAN subnet in the Nutanix environment. This virtual switch is used to provide connectivity between virtual machines and other resources within the Nutanix cluster.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  VS0
  ```

## **`VLAN UUID (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix VLAN Subnet VLAN UUID variable stores the unique identifier (UUID) of the VLAN associated with the subnet being managed in a Nutanix cluster. The VLAN UUID is used to uniquely identify the VLAN and associate it with the corresponding subnet. This variable is typically used in conjunction with other Nutanix management variables, such as the VLAN Subnet Name and Virtual Switch Name, to manage virtual networks within a Nutanix cluster. It is important to ensure that the correct VLAN UUID is set when creating, updating, or deleting a VLAN subnet to avoid any conflicts or unintended changes to the Nutanix environment.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  338aef43-5297-4923-8451-662cd56646f5
  ```

## **`Network IP With Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN network IP is used to identify and segment the network traffic within the Nutanix environment. It consists of the network IP address and the corresponding prefix.

  - Network IP: `10.0.0.0`
  - Prefix: `24`

  The network IP and prefix together define the range of IP addresses available within the Nutanix VLAN network. In this case, the network IP is `10.0.0.0` and the prefix length is `24`, which means that the network has `256` available IP addresses.

  Make sure to configure your Nutanix VLAN network devices and systems with the appropriate IP addresses and subnet masks based on the network IP and prefix specified above.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.0/24
  ```

## **`Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN network gateway IP is the IP address assigned to the default gateway within the VLAN network. It serves as the entry point for network traffic between the Nutanix cluster and external networks.

  - Gateway IP: `10.0.0.1`

  The gateway IP specified above, `10.0.0.1`, should be configured as the default gateway for devices within the Nutanix VLAN network. This ensures proper routing of network traffic to and from the Nutanix cluster.

  It is important to configure the network devices and systems within the Nutanix VLAN network to use the correct gateway IP address. This allows for seamless communication between the Nutanix infrastructure and other networks or devices.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.10.1
  ```

## **`IP Pools Range (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN network IP pools range defines the range of IP addresses available for assignment to virtual machines (VMs) and other network entities within the VLAN network. It helps in managing and allocating IP addresses efficiently.

  - Start IP: `10.0.0.10`
  - End IP: `10.0.0.50`

  The IP pools range specified above, from `10.0.0.10` to `10.0.0.50`, encompasses a total of `41` IP addresses. These addresses can be dynamically assigned to VMs and other network resources within the Nutanix VLAN network.

  When provisioning new VMs or allocating IP addresses for other network entities, ensure that the assigned IP addresses fall within this specified IP pools range. This helps prevent conflicts and ensures proper IP address management within the Nutanix environment.

  It is recommended to regularly monitor and update the IP pools range as per the network requirements to accommodate the growing needs of the Nutanix VLAN network.

  In the example above, the documentation provides an explanation of the Nutanix VLAN network IP pools range and its significance in IP address management. It specifies the start IP (10.0.0.10) and end IP (10.0.0.50) of the IP pools range, along with the total number of available addresses. The documentation also highlights the importance of assigning IP addresses within the specified range to prevent conflicts. The markdown formatting helps present the information in a clear and organized manner.

  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.10.10-10.10.10.20
  ```
## **`TFTP Server (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN TFTP server is used for network booting and firmware upgrades within the VLAN network. It allows for easy file transfer and deployment of operating system images, configuration files, and firmware updates to network devices.

  - TFTP Server IP: `10.0.0.100`
  - TFTP Server Port: `69`

  To utilize the Nutanix VLAN TFTP server, configure network devices or systems within the VLAN network to use the following TFTP server IP and port:

  - TFTP Server IP: `10.0.0.100`
  - TFTP Server Port: `69`

  Ensure that the TFTP server IP address and port are properly configured on the target devices to enable successful file transfers and network booting operations.

  Additionally, make sure that the necessary files, such as operating system images or firmware updates, are available on the TFTP server and accessible to the devices in the VLAN network.

  Note: TFTP is a lightweight file transfer protocol commonly used for network booting and firmware updates. It operates over UDP (User Datagram Protocol) and does not provide encryption or authentication. Exercise caution when using TFTP for transferring sensitive or critical files.

  In the above example, the documentation provides an explanation of the Nutanix VLAN TFTP server and its purpose in network booting and firmware upgrades. It specifies the TFTP server IP (10.0.0.100) and port (69) to be configured on the network devices within the VLAN network. The documentation also includes a note about the limitations of TFTP and the need for caution when transferring sensitive files. The markdown formatting helps present the information in a structured and readable format.

  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  tftp.server.com
  ```
## **`Boot File Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN boot file name specifies the file that network devices within the VLAN network should retrieve and execute during the boot process. It is used for network booting and provisioning operating systems or other bootable images.

  - Boot File Name: `pxelinux.0`

  To configure network devices for booting within the Nutanix VLAN network, ensure that the following boot file name is set:

  - Boot File Name: `pxelinux.0`

  The specified boot file name should be accessible on the designated TFTP server or boot server within the VLAN network. It contains the necessary instructions and configuration for network booting and subsequent system provisioning.

  Ensure that the boot file is correctly configured and available on the TFTP server, and that network devices are configured to request and retrieve the correct boot file during the boot process.

  Note: The boot file name may vary depending on the specific network boot infrastructure and configuration used within the Nutanix VLAN network.

  In the example above, the documentation provides an explanation of the Nutanix VLAN boot file name and its role in the network booting process. It specifies the boot file name (pxelinux.0) to be configured on network devices within the VLAN network. The documentation also includes a note about the potential variations in the boot file name based on specific network boot infrastructure. The markdown formatting helps present the information in a clear and structured manner.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  boot.test
  ```

## **`Domain Search List (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN subnet domain search list specifies the domain names that network devices within the VLAN subnet should search when resolving hostnames. It helps streamline DNS resolution and simplifies the process of accessing resources within the VLAN network.

  - Domain Search List: `example.com`, `internal.example.com`

  To configure network devices within the Nutanix VLAN subnet for DNS resolution, set the following domain search list:

  - Domain Search List:
    - `example.com`
    - `internal.example.com`

  The specified domain search list should be configured on the DNS settings of the network devices within the VLAN subnet. It allows these devices to search the specified domain names when attempting to resolve hostnames.

  Ensure that the domain names listed in the search list are valid and correspond to the appropriate DNS infrastructure within the Nutanix VLAN subnet.

  By configuring the domain search list, users and applications within the VLAN subnet can conveniently access resources using simplified hostnames without specifying the full domain name.

  Note: The actual domain names in the search list may vary based on your specific network configuration and requirements within the Nutanix VLAN subnet.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  domain.search.io
  ```
## **`Domain Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix VLAN subnet domain name is used to define the domain for the network devices within the VLAN subnet. It allows for logical grouping of devices and simplifies the management of DNS records and hostnames within the subnet.

  - Domain Name: `example.com`

  To configure the domain for network devices within the Nutanix VLAN subnet, set the following domain name:

  - Domain Name: `example.com`

  Ensure that the specified domain name accurately represents the intended domain for the VLAN subnet. This domain name will be used for DNS resolution and hostname assignment within the subnet.

  When configuring DNS settings for devices within the VLAN subnet, make sure to specify the domain name as `example.com` to ensure proper resolution of hostnames and seamless communication within the subnet.

  Note: The actual domain name may vary based on your specific network configuration and requirements within the Nutanix VLAN subnet.
 </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  test.domain.com
  ```

## **`DNS Servers IP (Required)`**

  <details>
  <summary><b>Description</b></summary>

  The Nutanix VLAN subnet DNS servers are responsible for resolving domain names to IP addresses within the VLAN subnet. They play a crucial role in enabling proper network communication and access to resources.

  - DNS Server 1: `10.0.0.1`
  - DNS Server 2: `10.0.0.2`

  To configure DNS settings for network devices within the Nutanix VLAN subnet, set the following DNS server IP addresses:

  - DNS Server 1: `10.0.0.1`
  - DNS Server 2: `10.0.0.2`

  Make sure to enter the correct IP addresses of the DNS servers provided by your network infrastructure. These DNS servers will handle the resolution of domain names and allow network devices within the VLAN subnet to access resources using hostnames.

  Verify that the DNS servers are operational and accessible from devices within the VLAN subnet to ensure reliable DNS resolution.

  Note: The actual IP addresses of the DNS servers may vary based on your specific network configuration and requirements within the Nutanix VLAN subnet.

</details>

  ### **Type:** _String_

  ### **Example:**
  ```
  8.8.8.6
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

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix
  ```
