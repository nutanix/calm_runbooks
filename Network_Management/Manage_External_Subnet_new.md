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

## **`Subnet Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
   This variable represents the name of the subnet that enables external connectivity for a Nutanix cluster. Its purpose is to assign external IP addresses to the virtual machines and networking resources such as load balancers within the cluster. The external subnet should have an adequate number of available IP addresses to handle the anticipated workload of the cluster. To ensure proper functionality of the cluster, it is crucial to keep the Nutanix.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  test_subnet
  ```

## **`Operation (Required)`**

  <details>
  <summary><b>Description</b></summary>
   The type of operation to perform on the external subnet in the Nutanix environment.

   This variable should be set to the type of operation to be performed on the external subnet in the Nutanix environment. The valid options for this variable are 'create', 'update', and 'delete'.

   - 'create': Use this option to create a new external subnet in the Nutanix environment.

   - 'update': Use this option to modify an existing external subnet in the Nutanix environment.

   - 'delete': Use this option to remove an existing external subnet from the Nutanix environment.

   The value of this variable determines which specific API call will be made to the Nutanix management platform, so it is important to ensure that the correct value is set based on the intended operation.

   Note that certain operations may require additional parameters or configuration options, depending on the specific resource being created, updated, or deleted. Be sure to consult the Nutanix documentation and API reference for more information on the requirements for each operation.

   Also, keep in mind that the external subnet is used to provide external connectivity to a Nutanix cluster, so any changes made to it can have an impact on the overall functionality of the cluster. It is important to follow best practices and test any changes in a non-production environment before making them in a production environment.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  create / update / delete
  ```

## **`VLAN ID (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The External Subnet VLAN ID refers to the VLAN ID associated with the external subnet in a Nutanix cluster. It is used to identify the external subnet within the network infrastructure and enable traffic to flow to and from the external network. The VLAN ID must be unique within the network infrastructure and configured appropriately to allow for communication between the external network and the Nutanix cluster. It is important to ensure that the External Subnet VLAN ID is correctly configured and maintained to avoid any disruption to network connectivity for the Nutanix cluster.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  10
  ```

## **`External VLAN UUID (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable should be set to the UUID of the VLAN that is associated with the external subnet in the Nutanix cluster. The UUID is used to uniquely identify the VLAN within the network infrastructure and enable traffic to flow to and from the external network.

  For 'create' operation, this variable is not required as Nutanix will create a new VLAN automatically.

  For 'update' and 'delete' operations, it is mandatory to specify the External Subnet VLAN UUID. This UUID can be obtained from the network infrastructure administrator or through network management tools.

  It is important to ensure that the External Subnet VLAN UUID is correctly configured and maintained to avoid any disruption to network connectivity for the Nutanix cluster.

  Note that this variable is typically used in conjunction with the External Subnet VLAN ID variable to configure external network connectivity for the Nutanix cluster.

  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  ec2c7ade-141d-4c19-a036-36c5bda31a73
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

## **`Enable NAT (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix External Subnet Enable NAT variable is used to specify whether or not Network Address Translation (NAT) is enabled on the external subnet of a Nutanix cluster.

  NAT is a technology used to map one IP address space into another by modifying network address information in the IP header of packets while they are in transit across a traffic routing device. In the context of a Nutanix cluster, enabling NAT on the external subnet allows virtual machines running on the cluster to communicate with external networks using IP addresses that are translated by the Nutanix cluster.

  The Nutanix External Subnet Enable NAT variable can be set to either "True" or "False" to enable or disable NAT on the external subnet, respectively. Enabling NAT can be useful in situations where there is a shortage of public IP addresses, or where security policies require that internal IP addresses are not exposed to the public internet.

  It is important to carefully consider the implications of enabling or disabling NAT on the external subnet of a Nutanix cluster. This variable should be configured according to the specific requirements of the environment and in line with best practices for networking and security.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  True / Fasle
  ```

## **`Network IP with Prefix (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Variable is used to specify the network IP address and prefix length for the external subnet of a Nutanix cluster.

  The network IP address and prefix length define the range of IP addresses that are available for use in the external subnet. The prefix length is a number that indicates the number of bits used for the network part of the IP address. For example, a prefix length of 24 indicates that the first 24 bits of the IP address are used for the network, leaving 8 bits for the host address.

  The Nutanix External Subnet Network IP with Prefix variable is typically set to an IP address and prefix length in the CIDR notation format, such as "192.168.0.0/24". This indicates that the network IP address is 192.168.0.0, and that the prefix length is 24 bits.

  It is important to ensure that the Nutanix External Subnet Network IP with Prefix variable is correctly configured to avoid any conflicts or issues with IP address allocation on the external subnet. The network IP address and prefix length should be chosen based on the size of the external subnet and the number of IP addresses required to support the expected workload of the Nutanix cluster..
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.40.0/24
  ```

## **`Gateway IP (Required)`**

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
  10.10.40.1
  ```

## **`IP Pool (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix External Subnet IP Pool variable is used to specify a range of IP addresses that can be assigned to virtual machines running in a Nutanix cluster.

  When a virtual machine is created, it can be assigned an IP address from the IP pool specified in this variable. The Nutanix cluster will then reserve the assigned IP address and ensure that it is not assigned to any other virtual machine.

  It is important to ensure that the Nutanix External Subnet IP Pool variable is correctly configured to avoid any conflicts or issues with IP address allocation on the external subnet. The IP pool should be large enough to support the expected workload of the Nutanix cluster, and should not overlap with any other IP address ranges in the environment.

  The Nutanix External Subnet IP Pool variable can be specified as a range of IP addresses in CIDR notation, such as "192.168.0.10-192.168.0.20" or "10.0.0.0/24". Alternatively, it can be specified as a list of individual IP addresses, such as "192.168.0.10, 192.168.0.11, 192.168.0.12".
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.40.2-10.10.40.10
  ```
## **`PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central Username variable is used to specify the username that is used to authenticate with the Nutanix Prism Central management interface.

  Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Username variable should be set to the username that has been granted access to the Prism Central management interface.

  It is important to ensure that the Nutanix Prism Central Username variable is correctly configured and kept up-to-date to ensure that the Nutanix clusters can be managed effectively. The username specified in this variable should have the appropriate level of permissions to perform the required management tasks in Prism Central.
  </details>
  #### **Type:** _String_

  #### **Example:**

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
  nutanix/4u
  ```

