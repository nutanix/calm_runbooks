# Runbook Variables

## **`Operation (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  The "Operation" refers to the action you want to perform on a static route, such as updating or deleting it.

    Update: When the operation is set to "Update", it means you want to modify the configuration of an existing static route. This could involve changing the next hop IP address, modifying the destination IP range, adjusting the metric or priority, or making any other necessary changes to the static route configuration.

    Delete: When the operation is set to "Delete", it means you want to remove or delete an existing static route from the routing table. This action removes the entry for the static route, effectively stopping the traffic from being routed according to that specific route.

  By selecting the appropriate operation in Nutanix static routing, you can control the actions performed on the static routes. Whether you need to update the configuration of a static route to reflect changes in your network environment or delete a static route that is no longer needed, the operation allows you to manage the routing table effectively and ensure proper network connectivity.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  UPDATE / DELETE
  ```

## **`VPC Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The VPC Name refers to the name or identifier of the Virtual Private Cloud (VPC) in which the static routing configuration is being applied.

  A VPC is a virtual network infrastructure that allows you to create and manage your own isolated network within a cloud environment. It provides the foundation for organizing and managing resources, including virtual machines, subnets, and routing configurations.

  When configuring static routes in Nutanix, you associate the static routes with a specific VPC by specifying the VPC Name. This ensures that the static routes are applied within the context of the designated VPC.

  By providing the VPC Name in Nutanix static routing, you can define the scope of the routing configuration and ensure that the static routes are applied to the correct VPC within your cloud environment. This allows you to establish routing between different subnets or networks within the specified VPC, enabling seamless communication between resources in your network infrastructure
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  test_vpc
  ```

## **`IP with Prefix [ Destination ] (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The IP with Prefix [Destination] refers to the specific IP address prefix or subnet range that is used to define the destination IP addresses for the static route.

  When configuring a static route, you can specify an IP address prefix or a subnet range (in CIDR notation) that represents the destination network or destination IP addresses for the route. This allows you to define the target network or specific range of destination IP addresses to which the static route should be applied.

  For example, if you define the IP with Prefix [Destination] as "192.168.0.0/24", it means that the static route is targeting the subnet range from 192.168.0.0 to 192.168.0.255. This indicates that any traffic with a destination IP address within this range should follow the configured static route.

  By specifying the IP with Prefix [Destination] in Nutanix static routing, you can control the flow of network traffic based on the destination IP address. This allows you to direct traffic to specific destination networks or IP address ranges, ensuring that it reaches the intended destination through the defined static route.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.0/24
  ```

## **`External Subnet Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix static routing, the External Subnet Name refers to the name or identifier of the external subnet that is used in the static routing configuration.

  An external subnet typically represents a subnet or network segment that is outside of your Nutanix infrastructure. It could be a subnet in a different cloud provider's network, a remote on-premises network, or any other external network that you need to establish connectivity with.

  When configuring static routing in Nutanix, you may specify the External Subnet Name to identify the specific subnet or network segment that the static route is targeting for communication. This helps in defining the routing path and establishing connectivity between your Nutanix infrastructure and the external subnet.

  By providing the External Subnet Name in Nutanix static routing, you can ensure that the static routes are correctly associated with the desired external subnet, allowing traffic to flow between your Nutanix environment and the specified external network segment.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  test_external
  ```

## **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
   The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.

  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.40
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
  nutanix
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
  admin
  ```
