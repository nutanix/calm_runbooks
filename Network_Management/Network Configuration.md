# Runbook Variables

## **`PC IP (Required)`** 

  <details>
  <summary><b>Description</b></summary>
   The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.40
  ```

## **`Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix Cluster Name variable is used to store the name of the Nutanix cluster being managed. It is a critical identifier for the cluster within the Nutanix environment and in external systems that interact with the cluster.

    The Nutanix cluster is a group of Nutanix nodes that work together to provide a scalable, highly available, and performant infrastructure for virtualized workloads. The cluster uses software-defined storage and hyperconverged infrastructure (HCI) technology to provide a distributed file system that aggregates the local storage of each node and presents it as a single shared pool of storage to the virtual machines running on the cluster.

    The Nutanix Cluster Name variable is typically used in conjunction with other Nutanix management variables, such as the Prism Central IP address, to manage the Nutanix cluster. It should be set to a unique and descriptive name that accurately reflects the purpose and function of the Nutanix cluster.

    Maintaining the Nutanix Cluster Name variable is crucial to ensure that the cluster remains identifiable and correctly configured. This helps to avoid any confusion with other clusters in the environment and ensures that the Nutanix cluster can be effectively managed and monitored.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  autopc-xy-123
  ```

## **`Virtual Switch Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix VLAN Subnet Virtual Switch Name variable is used to store the name of the virtual switch associated with the VLAN subnet in the Nutanix environment. This virtual switch is used to provide connectivity between virtual machines and other resources within the Nutanix cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vs0
  ```

## **`Create External Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable determines whether an external subnet should be created or not.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True / False
  ```

## **`External Subnet Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
   This variable represents the name of the subnet that enables external connectivity for a Nutanix cluster. Its purpose is to assign external IP addresses to the virtual machines and networking resources such as load balancers within the cluster. The external subnet should have an adequate number of available IP addresses to handle the anticipated workload of the cluster. To ensure proper functionality of the cluster, it is crucial to keep the Nutanix.

  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  ext_subnet
  ```

## **`External VLAN ID (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The External Subnet VLAN ID refers to the VLAN ID associated with the external subnet in a Nutanix cluster. It is used to identify the external subnet within the network infrastructure and enable traffic to flow to and from the external network. The VLAN ID must be unique within the network infrastructure and configured appropriately to allow for communication between the external network and the Nutanix cluster. It is important to ensure that the External Subnet VLAN ID is correctly configured and maintained to avoid any disruption to network connectivity for the Nutanix cluster.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  12
  ```

## **`External Subnet IP with Prefix (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The Variable is used to specify the network IP address and prefix length for the external subnet of a Nutanix cluster.

  The network IP address and prefix length define the range of IP addresses that are available for use in the external subnet. The prefix length is a number that indicates the number of bits used for the network part of the IP address. For example, a prefix length of 24 indicates that the first 24 bits of the IP address are used for the network, leaving 8 bits for the host address.

  The Nutanix External Subnet Network IP with Prefix variable is typically set to an IP address and prefix length in the CIDR notation format, such as "192.168.0.0/24". This indicates that the network IP address is 192.168.0.0, and that the prefix length is 24 bits.

  It is important to ensure that the Nutanix External Subnet Network IP with Prefix variable is correctly configured to avoid any conflicts or issues with IP address allocation on the external subnet. The network IP address and prefix length should be chosen based on the size of the external subnet and the number of IP addresses required to support the expected workload of the Nutanix cluster.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.20.30.0/24
  ```

## **`External Subnet IP Pool Range (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The External Subnet IP Pool Range variable is used to specify a range of IP addresses that can be assigned to virtual machines running in a Nutanix cluster.

  When a virtual machine is created, it can be assigned an IP address from the IP pool specified in this variable. The Nutanix cluster will then reserve the assigned IP address and ensure that it is not assigned to any other virtual machine.

  It is important to ensure that the External Subnet IP Pool Range variable is correctly configured to avoid any conflicts or issues with IP address allocation on the external subnet. The IP pool should be large enough to support the expected workload of the Nutanix cluster, and should not overlap with any other IP address ranges in the environment.

  The External Subnet IP Pool Range variable can be specified as a range of IP addresses in CIDR notation, such as "192.168.0.10-192.168.0.20" or "10.0.0.0/24". Alternatively, it can be specified as a list of individual IP addresses, such as "192.168.0.10, 192.168.0.11, 192.168.0.12".
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.2-10.20.30.10
  ```

## **`External Subnet Gateway IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix External Subnet Gateway IP variable is used to specify the IP address of the default gateway for the external subnet of a Nutanix cluster.

  The default gateway is the IP address of the router that is used to connect the external subnet to other networks, such as the internet. The Nutanix External Subnet Gateway IP variable is typically set to the IP address of the router that is connected to the external subnet.

  It is important to ensure that the Nutanix External Subnet Gateway IP variable is correctly configured to ensure that traffic can be routed to and from the external subnet. The IP address specified in this variable should be reachable from the external subnet and should be valid for the network configuration of the external subnet.

  If the Nutanix cluster is configured to use multiple external subnets, each subnet should have its own gateway IP address specified in this variable.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.20.30.1
  ```

## **`External Subnet NAT (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The External Subnet NAT variable is used to specify whether or not Network Address Translation (NAT) is enabled on the external subnet of a Nutanix cluster.

  NAT is a technology used to map one IP address space into another by modifying network address information in the IP header of packets while they are in transit across a traffic routing device. In the context of a Nutanix cluster, enabling NAT on the external subnet allows virtual machines running on the cluster to communicate with external networks using IP addresses that are translated by the Nutanix cluster.

  The External Subnet NAT variable can be set to either "True" or "False" to enable or disable NAT on the external subnet, respectively. Enabling NAT can be useful in situations where there is a shortage of public IP addresses, or where security policies require that internal IP addresses are not exposed to the public internet.

  It is important to carefully consider the implications of enabling or disabling NAT on the external subnet of a Nutanix cluster. This variable should be configured according to the specific requirements of the environment and in line with best practices for networking and security.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  True / False
  ```
## **`Create VPC (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable determines whether a VPC should be created or not.
  </details>
  
  #### **Type:** _String_

  #### **Example:**

  ```
  True / False
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
## **`Create Overlay Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable indicates whether an overlay subnet should be created or not.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True / False
  ```

## **`Overlay Subnet Name (Required)`**

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
  test_overlay
  ```

## **`Overlay Subnet IP With Prefix (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  In a Nutanix overlay subnet, the network IP with prefix refers to the IP address range allocated to the subnet, along with the associated subnet mask or prefix length. The network IP represents the base address of the subnet, while the prefix indicates the number of bits used to define the subnet.

  For example, if the network IP is 192.168.0.0 and the prefix is /24, it means that the subnet includes IP addresses ranging from 192.168.0.0 to 192.168.0.255, with a subnet mask of 255.255.255.0.

  The prefix length is represented as the number of consecutive bits set to 1 in the subnet mask. In the example above, /24 indicates that the first 24 bits of the IP address are used to identify the network portion, while the remaining 8 bits are available for host addresses.

  The network IP with prefix is essential for defining the address space and subnet boundaries within a Nutanix overlay subnet. It helps in determining the range of available IP addresses and configuring the appropriate network settings for virtual machines, routing, and connectivity within the subnet.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.20.0/24
  ```

## **`Overlay Subnet Gateway IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In a subnet overlay network, a gateway IP refers to the IP address assigned to the gateway device within the overlay network. The gateway acts as an intermediary between the overlay network and external networks or other subnets.

  The specific IP address of the gateway depends on the configuration of the overlay network. Typically, the gateway IP address is chosen from within the range of IP addresses assigned to the subnet. It serves as the default gateway for devices within the subnet to communicate with devices outside the subnet or in other subnets.

  For example, let's say you have an overlay network with a subnet using the IP address range 192.168.0.0/24. The gateway IP address might be assigned as 192.168.0.1. This means that any device within the subnet would use 192.168.0.1 as the gateway IP to send traffic outside the subnet.

  It's important to note that the specific configuration of a subnet overlay network, including the choice of gateway IP, can vary depending on the network infrastructure and the technology being used for overlay networking, such as Virtual Extensible LAN (VXLAN) or Generic Routing Encapsulation (GRE).
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.1
  ```

## **`Prism Central Username (Required)`**

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

## **`Prism Central Password (Required)`**

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
