# Runbook Variables

## **`Operation (Required)`** 

  <details>
  <summary><b>Description</b></summary>
    This variable determines whether to create or delete Nutanix policy-based routing
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  CREATE / DELETE
  ```

## **`Priority of route (Required)`**

  <details>
  <summary><b>Description</b></summary>
    In Nutanix policy-based routing, the priority of a route refers to the order in which routes are evaluated and applied based on their defined priorities. The route with the highest priority is processed first, followed by routes with lower priorities.
  </details>

  ### **Type:** _Integer_

  #### **Example:**
  ```
  12
  ```

## **`Protocol Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
    In Nutanix, the protocol type in policy-based VPC routing refers to the specific network protocol that is used for routing traffic between different virtual private clouds (VPCs) or subnets. The protocol type determines the type of traffic that is allowed or restricted based on the defined policies.

    Common protocol types used in Nutanix policy-based VPC routing include:

      TCP (Transmission Control Protocol): TCP is a connection-oriented protocol that provides reliable and ordered delivery of data packets. It is commonly used for applications that require reliable and error-free data transmission, such as web browsing, email, and file transfer.

      UDP (User Datagram Protocol): UDP is a connectionless protocol that provides a lightweight and fast method of transmitting data packets. It is often used for real-time streaming, multimedia applications, and DNS (Domain Name System) lookups.

      ICMP (Internet Control Message Protocol): ICMP is a protocol used for diagnostic and control purposes in IP networks. It includes functions such as echo requests and replies (ping) and error reporting. ICMP is commonly used for network troubleshooting and monitoring.

      Other protocols: Nutanix policy-based VPC routing may also support other protocols such as ICMPv6 (ICMP for IPv6), IGMP (Internet Group Management Protocol) for multicast traffic, or specific application-layer protocols based on your network requirements.

    By specifying the protocol type in policy-based VPC routing, you can define rules and policies that govern the routing of traffic based on the specific protocol being used. This allows you to control and optimize the flow of network traffic within your Nutanix environment based on your application and security requirements.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  TCP / UDP / ALL / ICMP / PROTOCOL_NUMBER
  ```

## **`Protocol Number (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix VPC static routing, the protocol number refers to the numerical identifier assigned to different network protocols. These protocol numbers are used to identify and differentiate various protocols when configuring static routes.

  These protocol numbers are defined by the Internet Assigned Numbers Authority (IANA) and are widely used to identify different network protocols.

  When configuring static routes in Nutanix, you may need to specify the appropriate protocol number based on the protocol being used. This ensures that the routing table correctly identifies and handles the traffic associated with that protocol.

  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  0
  ```

## **`ICMP Protocol Parameter Type (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix VPC policy-based routing, the ICMP (Internet Control Message Protocol) Protocol Parameter Type refers to the specific type of ICMP message being used. ICMP is a protocol used for diagnostic and control purposes in IP networks. It includes various types of messages that serve different functions, such as error reporting, network troubleshooting, and network congestion control.

  The ICMP Protocol Parameter Types in Nutanix VPC policy-based routing are the same as those used in standard ICMP. Here are some commonly used ICMP Protocol Parameter Types in Nutanix VPC policy-based routing:

    Type 0: Echo Reply
    Type 3: Destination Unreachable
    Type 8: Echo Request
    Type 11: Time Exceeded
    Type 12: Parameter Problem

  These ICMP Protocol Parameter Types help classify and handle different types of ICMP messages within Nutanix VPC policy-based routing. By configuring policies based on the specific ICMP message types, you can control the routing behavior and apply actions accordingly.

  When defining policy-based routing rules in Nutanix VPC, it's important to consider the ICMP Protocol Parameter Types that are relevant to your network requirements. This allows you to create rules and actions that effectively manage ICMP traffic and meet your specific routing needs.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  12
  ```

## **`ICMP Protocol Parameter Code (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    The ICMP (Internet Control Message Protocol) Protocol Parameter Code refers to the specific code associated with an ICMP message type. ICMP messages are used for various purposes in network communication, such as error reporting, troubleshooting, and network management.

    The ICMP Protocol Parameter Codes in Nutanix policy-based routing are the same as those used in standard ICMP.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  12
  ```

## **`Source Port Range List (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    In Nutanix VPC policy-based routing, the Source Port Range List refers to a list of source port ranges used for defining policies and routing decisions based on the source port of network traffic.

    When configuring policy-based routing rules in Nutanix VPC, you can specify a range of source ports or multiple source port ranges to define the criteria for routing decisions. Each entry in the Source Port Range List typically consists of a starting port number and an ending port number, indicating the range of source ports to be matched.

    For example, a Source Port Range List entry may look like this:

    Range 1: Start Port 1024, End Port 2048
    Range 2: Start Port 5000, End Port 6000

    These ranges can be used to match incoming traffic based on the source port number. If the source port of a packet falls within any of the defined ranges, the corresponding routing action associated with that range will be applied.

    By configuring the Source Port Range List in Nutanix VPC policy-based routing, you have granular control over routing decisions based on the source ports of network traffic. This allows you to define specific policies and actions based on the source port ranges, helping you manage and route traffic according to your network requirements.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  21-56
  ```

## **`Destination Port Range List(Optional)`**

  <details>
  <summary><b>Description</b></summary>
    VPC policy-based routing, the Destination Port Range List refers to a list of destination port ranges used for defining policies and routing decisions based on the destination port of network traffic.

    When configuring policy-based routing rules in Nutanix VPC, you can specify a range of destination ports or multiple destination port ranges to define the criteria for routing decisions. Each entry in the Destination Port Range List typically consists of a starting port number and an ending port number, indicating the range of destination ports to be matched.

    For example, a Destination Port Range List entry may look like this:

      Range 1: Start Port 80, End Port 443
      Range 2: Start Port 8080, End Port 8090

    These ranges can be used to match incoming traffic based on the destination port number. If the destination port of a packet falls within any of the defined ranges, the corresponding routing action associated with that range will be applied.

    By configuring the Destination Port Range List in Nutanix VPC policy-based routing, you have granular control over routing decisions based on the destination ports of network traffic. This allows you to define specific policies and actions based on the destination port ranges, helping you manage and route traffic according to your network requirements.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  30-40
  ```

## **`Source Address Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
    VPC policy-based routing, the Source Address Type can be categorized into three options: External, All, and Custom.

      External: This option refers to external or public IP addresses. It allows you to define routing policies based on traffic originating from external sources, such as the internet or other external networks. Using the External source address type, you can apply specific routing rules to handle traffic coming from outside of your VPC.

      All: This option represents all possible source IP addresses. When you choose the All source address type, it means that the routing policies will be applied to all source IP addresses within your VPC, regardless of their specific ranges or subnets. This can be useful when you want the policy to be applied universally to all traffic within your VPC.

      Custom: This option allows you to specify a custom source address or a range of source addresses for policy-based routing. You can define specific IP addresses, subnet ranges (CIDR notation), or address groups as the source address criteria. Custom source address type gives you flexibility in defining granular routing policies based on specific source addresses or address ranges that suit your network requirements.

    By selecting the appropriate Source Address Type in Nutanix VPC policy-based routing, you can define the scope of your routing policies and specify the sources from which the policies should be applied. Whether you want to target external sources, all sources within your VPC, or specific custom-defined sources, the Source Address Type provides the flexibility to tailor your routing rules accordingly.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  INTERNET / ALL / CUSTOM
  ```

## **`Source IP Prefix (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  policy-based routing, the Source IP Prefix refers to the specific IP address prefix or subnet range used to define the source IP addresses for routing policies.

  When configuring policy-based routing rules, you can specify a source IP prefix that represents a range of IP addresses or a subnet in CIDR notation. This allows you to define the source addresses from which the routing policy should be applied.

  For example, if you define the Source IP Prefix as "192.168.0.0/24", it means that the routing policy will be applied to all IP addresses within the subnet range of 192.168.0.0 to 192.168.0.255. This allows you to target a specific range of source IP addresses for routing decisions.

  By specifying the Source IP Prefix in Nutanix policy-based routing, you can control which source IP addresses should be subject to the routing policy. This allows you to define routing rules based on specific subnets or IP address ranges, providing granular control over the flow of network traffic based on its source.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.40.2/24
  ```
## **`Destination Address Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Destination Address Type can be categorized into three options: All, Custom, and External.

    All: This option represents all possible destination IP addresses. When you choose the All destination address type, it means that the routing policies will be applied to all destination IP addresses, regardless of their specific ranges or subnets. This can be useful when you want the policy to be applied universally to all traffic regardless of its destination.

    Custom: This option allows you to specify a custom destination address or a range of destination addresses for policy-based routing. You can define specific IP addresses, subnet ranges (CIDR notation), or address groups as the destination address criteria. Custom destination address type gives you flexibility in defining granular routing policies based on specific destination addresses or address ranges that suit your network requirements.

    External: This option refers to external or public IP addresses. It allows you to define routing policies based on traffic destined for external sources, such as the internet or other external networks. Using the External destination address type, you can apply specific routing rules to handle traffic going outside of your network.

  By selecting the appropriate Destination Address Type in Nutanix policy-based routing, you can define the scope of your routing policies and specify the destinations to which the policies should be applied. Whether you want to target all destinations, custom-defined destinations, or external destinations, the Destination Address Type provides the flexibility to tailor your routing rules accordingly.
  </details>
  
  #### **Type:** _String_

  #### **Example:**

  ```
  INTERNET / ALL / CUSTOM
  ```
## **`Destination IP with Prefix (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix VPC policy-based routing, the Destination IP with Prefix refers to the specific IP address prefix or subnet range used to define the destination IP addresses for routing policies.

  When configuring policy-based routing rules, you can specify a destination IP prefix that represents a range of IP addresses or a subnet in CIDR notation. This allows you to define the destination addresses to which the routing policy should be applied.

  For example, if you define the Destination IP with Prefix as "10.0.0.0/24", it means that the routing policy will be applied to all IP addresses within the subnet range of 10.0.0.0 to 10.0.0.255. This allows you to target a specific range of destination IP addresses for routing decisions.

  By specifying the Destination IP with Prefix in Nutanix VPC policy-based routing, you can control which destination IP addresses should be subject to the routing policy. This allows you to define routing rules based on specific subnets or IP address ranges, providing granular control over the flow of network traffic based on its destination.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.40.0/24
  ```

## **`Action (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix VPC static routing, the Action refers to the action taken for the matched static route. There are typically three types of actions that can be associated with a static route:

    PERMIT: When the action is set to PERMIT, it means that the matched traffic is allowed or permitted to proceed. This action allows the traffic to follow the configured static route and reach its intended destination.

    DENY: When the action is set to DENY, it means that the matched traffic is explicitly denied or blocked from proceeding. This action is used to prevent specific traffic from following the configured static route, effectively blocking access to the destination.

    REROUTE: When the action is set to REROUTE, it means that the matched traffic is redirected or rerouted to a different next hop or destination. This action is useful when you want to redirect traffic from the original static route to an alternative path or destination.

  By selecting the appropriate action in Nutanix VPC static routing, you can control the behavior of the matched traffic. Whether you want to permit the traffic to follow the static route, deny the traffic to block access, or reroute the traffic to an alternative path, the action associated with the static route allows you to define the desired behavior for the traffic flow.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  PERMIT / DENY / REROUTE
  ```

## **`VPC Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The VPC name in Nutanix VPC static routing refers to the name or identifier of the Virtual Private Cloud (VPC) in which the static routing configuration is being applied.

  A VPC is a virtual network infrastructure that allows you to create and manage your own isolated network within a cloud environment. It provides the foundation for organizing and managing resources, including virtual machines, subnets, and routing configurations.

  When configuring static routes in Nutanix VPC, you associate the static routes with a specific VPC by specifying the VPC name. This ensures that the static routes are applied within the context of the designated VPC.

  By providing the VPC name in Nutanix VPC static routing, you can define the scope of the routing configuration and ensure that the static routes are applied to the correct VPC within your cloud environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  test_vpc
  ```

## **`Bi-Directional (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix policy-based routing, the term "Bi-Directional" refers to the capability of routing traffic in both directions, allowing communication between source and destination devices in both outbound and inbound directions.

  When policy-based routing is configured to be bi-directional, it means that routing decisions and policies are applied to traffic flowing in both the outbound and inbound directions. This allows you to control and shape network traffic not only when it originates from your network (outbound) but also when it is destined for your network (inbound).

  By enabling bi-directional policy-based routing, you can implement advanced routing policies and traffic management techniques that consider the characteristics and requirements of traffic in both directions. This can be useful in scenarios where you want to apply specific routing rules, perform traffic shaping, or enforce security measures for bidirectional communication between different network segments or across different networks.

  Enabling bi-directional policy-based routing provides a more comprehensive and flexible approach to managing network traffic and ensuring that routing policies are applied to traffic in both the outbound and inbound directions as required by your network environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True / False
  ```

## **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
   The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix/4u
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
  nutanix/4u
  ```

## **`Prism Central Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central Password variable is used to store the password that is used to authenticate with the Nutanix Prism Central management interface.

  Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Password variable should be set to the password that corresponds to the username specified in the Nutanix Prism Central Username variable.

  It is important to ensure that the Nutanix Prism Central Password variable is kept secure and protected. The password should be stored in a secure manner, such as using a password manager or an encrypted file, and should not be shared with unauthorized individuals. Additionally, it is recommended to periodically change the password for security reasons.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```
