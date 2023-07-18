# Runbook Variables

## **`Protection Policy Name (Required)`** 

  <details>
  <summary><b>Description</b></summary>
   This variable is a user-defined name given to a policy that determines how often and for how long backups or snapshots are taken of a specific object in the Nutanix cluster. This object can be a virtual machine, a container, or any other resource that requires protection against data loss. The policy can be configured with various options, such as backup frequency, retention period, backup schedule, compression, and encryption settings. This parameter is used to specify which protection policy to apply when creating or managing data protection policies for objects in the Nutanix cluster. The policy helps manage backup storage space, based on pre-defined recovery window goals.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  policy123
  ```

## **`Recovery Plan Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
   This variable refers to a user-defined name given to a recovery plan that specifies the steps required to recover a particular object or service in the event of a disaster or system failure. The recovery plan can be set up with various options, such as the order in which services or virtual machines should be recovered, the specific recovery point to use, and the notification settings for administrators. The Nutanix Recovery Plan Name is used as a parameter to specify which recovery plan to apply when recovering objects or services in the Nutanix cluster.

   In other words, a recovery plan is a set of predefined steps and procedures that must be followed to restore normal service in case of a disaster. It specifies the steps that need to be taken to recover data and services after an unexpected event such as a power outage, hardware failure, or a natural disaster. The Nutanix Recovery Plan Name parameter is used to identify the specific recovery plan that should be applied during a disaster recovery scenario.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  Recoveryplan123
  ```

## **`Custom RPO Interval for Replication in Hours (Required)`**

  <details>
  <summary><b>Description</b></summary>
   The "Nutanix Custom RPO Interval for Replication in Hours" parameter refers to the Recovery Point Objective (RPO) interval for replication of data between Nutanix clusters. The RPO interval determines how frequently the replicated data is synchronized between the source and target clusters. A smaller RPO interval means that the data is synchronized more frequently, resulting in less data loss in case of a disaster. This parameter allows the user to define a custom RPO interval in hours that suits their specific requirements and recovery goals. The value of this parameter should be chosen based on factors such as the criticality of the data, the frequency of changes, and the available network bandwidth for replication.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  4
  ```

## **`Local Schedule (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the schedule for taking local backups or snapshots of a specified object, such as a virtual machine or container, within a Nutanix cluster. The local schedule includes settings such as the frequency of backups or snapshots, the time of day when the backups or snapshots will be taken, and any additional options such as retention policies or data compression settings. The "Local RPO" setting in the schedule specifies the Recovery Point Objective, which is the maximum amount of data loss that is acceptable in the event of a disaster or outage. This schedule is used to keep snapshots of the VM locally, allowing for quick recovery in case of data loss or corruption.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`Custom RPO Interval for Local Snapshot in Hours (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is used to define the custom RPO (Recovery Point Objective) interval in hours for local snapshots of virtual machines in a Nutanix cluster. RPO is the amount of data that an organization is willing to lose in the event of a disaster or data loss. The custom RPO interval determines how frequently local snapshots should be taken for the specified virtual machines, ensuring that the data is protected and the RPO objective is met. The Nutanix local snapshots feature allows organizations to take and store local snapshots of virtual machines that can be used to restore data in case of any data loss events. The custom RPO interval can be set based on the organization's data protection and recovery objectives.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  10
  ```
  ### **Note:** The default value for this parameter is set to 1, and it should be greater than or equal to 1 when the local schedule is enabled. 

## **`Retention on Primary and Remote (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix retention on primary and remote refers to the duration for which backup data is kept on the primary and remote sites. In a Nutanix cluster, backups can be stored locally on the primary site or remotely on a secondary site or cloud. The retention period for each backup copy determines how long the backup data will be kept and available for restore operations.

    The retention period can be set as a fixed number of days or based on the number of available snapshots. The retention on primary and remote can be set differently depending on the organization's data protection and compliance requirements. Organizations should consider factors such as data growth rate, storage capacity, backup frequency, and restore objectives when setting the retention period for their backup data.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  5
  ```

## **`Protection Start Time (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix snapshot protection start time parameter refers to the time at which the initial snapshot for the protected object will be taken. This parameter can be set to start immediately or scheduled to start at a specific time. If scheduled, the protection start time can be set according to the organization's requirements for data protection and recovery objectives. The start time can be specified using a 24-hour clock format and must be set to a time that is in the future. It is important to ensure that the protection start time is set appropriately to avoid any gaps in data protection or recovery.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  Immediate 
  or 
  <xx>h:<yy>m (13:10)
  ```

## **`Primary Account Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix Primary Account Cluster Name parameter refers to the name of the primary Nutanix cluster that is used for disaster recovery and backup purposes. This cluster serves as the primary destination for backups and replication of data to ensure business continuity in case of any disaster or data loss event. The primary account cluster name is an essential parameter that must be specified when configuring data protection policies, disaster recovery plans, and backup schedules for virtual machines and other objects in the Nutanix cluster. It is important to ensure that the primary account cluster is configured correctly and is capable of supporting the required data protection and recovery objectives for the environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  PHX-POC092
  ```

## **`Primary PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Primary Prism Central IP parameter for backup and disaster recovery refers to the IP address of the primary Prism Central instance that will be used for managing backup and disaster recovery operations in a Nutanix cluster. The primary Prism Central instance serves as the central point of control for data protection policies, disaster recovery plans, and other management tasks related to backup and recovery. This parameter is used to specify the IP address of the primary instance, which allows the backup and disaster recovery tools to connect to the instance and perform the necessary operations, such as creating and managing data protection policies, replicating data to remote sites, and recovering data in case of a disaster.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.10.40
  ```

## **`Primary PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the username of the account that will be used to authenticate with the primary Prism Central instance in a Nutanix cluster during disaster recovery operations. This account must have sufficient privileges to perform the required disaster recovery tasks, such as restoring data from backups or initiating failover operations to a remote site. The username is typically an administrative account that is created specifically for disaster recovery purposes and is separate from the regular user accounts used for day-to-day operations in the Nutanix cluster. The Primary Prism Central Username for Disaster Recovery parameter is used by the deployment tool to authenticate with the primary instance during disaster recovery operations.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  admin
  ```
## **`Primary PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the username used to authenticate with the primary Prism Central instance in a Nutanix cluster for disaster recovery and backup purposes. Prism Central is a centralized management interface that provides a unified view of multiple Nutanix clusters, allowing administrators to manage and monitor their infrastructure from a single pane of glass. The primary Prism Central instance is the main instance that is used for managing and monitoring the Nutanix cluster, and it serves as the central point of control for data protection policies, disaster recovery, and other management tasks. The primary side Prism Central username parameter is used to specify the username of the account used to authenticate with the primary instance, which allows the deployment tool to connect to the instance and perform management tasks as needed."
   </details>
  
  #### **Type:** _String_

  #### **Example:**

  ```
  nutanix/4u
  ```
## **`DR Account Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the name of the Nutanix cluster that is designated as the Disaster Recovery (DR) site. In a Nutanix environment, organizations can set up a secondary cluster at a separate physical location to serve as a DR site, which can be used for data protection and disaster recovery purposes. The DR Account Cluster Name parameter is used to specify the name of the DR cluster, which allows the deployment tool to connect to the DR site and perform management tasks as needed.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  PHX-POC100
  ```

## **`DR PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Prism Central IP parameter refers to the IP address of the disaster recovery (DR) Prism Central instance in a Nutanix cluster. In the event of a disaster or outage, the DR instance can be used to failover critical workloads and data to a secondary site, ensuring business continuity and minimizing downtime. The DR Prism Central instance is typically located at a secondary site and is configured to replicate data from the primary site on a regular basis, allowing for quick and seamless failover in the event of an outage. The disaster recovery Prism Central IP parameter is used to specify the IP address of the DR instance, which allows the deployment tool to connect to the instance and perform management tasks related to disaster recovery.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.20.30.40
  ```

## **`DR PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the username used to authenticate with the disaster recovery Prism Central instance in a Nutanix cluster. This username is typically associated with an account that has administrative privileges, allowing the deployment tool to perform management tasks as needed on the disaster recovery site.
  </details>
  
  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`DR PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the password used to authenticate with the disaster recovery Prism Central instance in a Nutanix cluster. This password is used in conjunction with the associated username to authenticate and gain access to the disaster recovery site for management tasks, data protection policies, and other administrative functions. It is important to ensure that this password is securely managed and kept confidential to maintain the security and integrity of the Nutanix cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix/4u
  ```

## **`VM Category for Protection Policy and Recovery Plan (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix VM Category for Protection Policy and Recovery Plan parameter refers to a category or group of virtual machines within a Nutanix cluster that share a common set of data protection and recovery requirements. The category is defined by the administrator based on factors such as the criticality of the virtual machines, the type of data they contain, and the recovery objectives for the organization.

    Protection policies are applied to VM categories to define the data protection requirements for the virtual machines in the category. These policies typically include settings such as the frequency of backups, retention policies, and any specific backup options such as compression or encryption.

    Recovery plans are also associated with VM categories, and they define the recovery objectives and procedures for the virtual machines in the category in case of a disaster or data loss event. The recovery plan typically includes steps for restoring the virtual machines from backups, testing the recovery process, and verifying the recoverability of the data.

    By categorizing virtual machines based on their data protection and recovery requirements, administrators can easily manage and apply consistent policies and procedures to ensure that critical data is protected and recoverable in case of any data loss events.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  {"TenantName": "Tmp"}
  ```

## **`Recovery Plan Network Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix Recovery Plan Network Type parameter refers to the type of network used for replication between the primary and recovery sites in a disaster recovery scenario. There are two options for this parameter: stretched and non-stretched.

    Stretched: In a stretched network, the primary and recovery sites are in the same Layer 2 network domain, which allows for seamless failover and failback operations. This network type is typically used when the primary and recovery sites are in close proximity to each other.

    Non-stretched: In a non-stretched network, the primary and recovery sites are in separate Layer 2 network domains, which requires additional configuration for replication and failover. This network type is typically used when the primary and recovery sites are geographically separated and cannot be in the same Layer 2 network domain.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  stretched (or) non-stretched
  ```

#### **`Stage Delay [ In Seconds ] (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The variable refers to the amount of time that is added to the recovery plan execution time for each stage in the plan. The stage delay can be used to introduce a delay between stages of the recovery plan, allowing administrators to verify that each stage has completed successfully before proceeding to the next stage. This delay can be used to ensure that each stage has completed successfully and to provide time for any necessary troubleshooting or remediation. The stage delay parameter can be configured according to the organization's recovery objectives and requirements for disaster recovery.
  </details>
  
  ### **Type:** _Integer_

  ### **Example:**
  ```
  10
  ```

## **`Enable Boot Script (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix disaster recovery Enable Boot Script parameter is a boolean variable that specifies whether or not to enable the execution of a boot script during the disaster recovery process. A boot script is a script that is executed when a virtual machine is started up, and it can be used to automate various tasks, such as installing software or configuring the operating system. Enabling the boot script during the disaster recovery process can help to ensure that the virtual machine is configured correctly and that it is ready to run the necessary applications and services after the recovery process is complete. If the parameter is set to true, the boot script will be executed during the recovery process. If it is set to false, the boot script will not be executed.
    The Nutanix cluster has the following boot scripts available for virtual machine recovery:
    For Linux:

        Production: /usr/local/sbin/production_vm_recovery
        Test: /usr/local/sbin/test_vm_recovery

    For Windows:

        Production: (Relative to Nutanix directory in Program Files)/scripts/production/vm_recovery.bat
        Test: (Relative to Nutanix directory in Program Files)/scripts/test/vm_recovery.bat

    The specific location of the Nutanix directory may vary depending on the installation configuration. These boot scripts can be used to automate the recovery process for virtual machines during disaster recovery scenarios.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`Primary Network Name - Production Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the name of the primary network used for production workloads in a Nutanix cluster. This parameter is used to identify the network that is used by virtual machines running production workloads, such as web servers, databases, and other critical applications. By specifying the name of the primary network, administrators can ensure that data protection and disaster recovery policies are applied to the correct network and workloads. The primary network is typically configured to provide high-speed connectivity and low latency for production workloads, and it may be segregated from other networks used for backup or management purposes.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlan10
  ```

## **`Primary Network Name - Test Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the name of the network that is associated with the test subnet in a Nutanix cluster. The test subnet is a separate network segment that is used for testing and development purposes, and it is typically isolated from the production network to prevent any interference or impact on live systems. The primary network name parameter is used to specify the name of the test subnet network, which allows the deployment tool to configure network settings and policies as needed.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlan11
  ```

## **`DR Network Name - Production Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the name of the production subnet in the disaster recovery (DR) site of a Nutanix cluster. The DR site is a secondary site where data and applications can be replicated and recovered in case of a disaster or disruption at the primary site. The production subnet is the network segment in the DR site where the recovered virtual machines (VMs) will be deployed and run after a failover. The DR Network Name - Production Subnet parameter is used to specify the name of this subnet, which is needed for configuring the network settings of the recovered VMs and ensuring they are properly connected to the network in the DR site.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlandr10
  ```

## **`DR Network Name - Test Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable refers to the name of the test subnet in the disaster recovery site of a Nutanix cluster. This parameter is used in the recovery plan to specify the network configuration for the test environment. The test subnet is a separate network segment that is used for testing purposes and is isolated from the production environment. It allows organizations to test their disaster recovery procedures without impacting their production environment. By specifying the DR Network Name - Test Subnet parameter, administrators can configure the network settings for the test environment to ensure that it is properly connected and can communicate with the necessary resources.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlandr11
  ```

## **`Enable Static IP Mapping (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Variable refers to a feature that enables administrators to map the IP addresses of protected virtual machines in the primary site to specific IP addresses in the disaster recovery site. This feature is useful when the IP addresses of virtual machines in the primary site are different from the IP addresses in the disaster recovery site, which can cause issues with connectivity and application functionality after a failover event.

    When this parameter is enabled, administrators can create static IP mappings for protected virtual machines in the primary site, which will be used to assign specific IP addresses to the virtual machines in the disaster recovery site during a failover event. This ensures that applications and services continue to function as expected after a failover, even if the IP addresses of the virtual machines have changed.

    It's important to note that the Enable Static IP Mapping feature is optional and may not be required in all scenarios. If the IP addresses of virtual machines in the primary and disaster recovery sites are the same, this feature may not be necessary.

 </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`VM Name (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    To enable static IP mapping for a VM in Nutanix, you need to provide the name of the VM for which you want to enable the static IP mapping in the list of VMs.
  </details>
  
  ### **Type:** _string_

  ### **Example:**
  ```
  vm1,vm2
  ```

## **`Primary Network Prod Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is used to specify a static IP address for a protected VM in the primary site's production network in Nutanix. When disaster recovery is activated and the VM is failed over to the secondary site, the static IP mapping ensures that the VM retains the same IP address, making it easier to manage and access. By setting this variable, you can ensure that the protected VM will have a consistent IP address across both the primary and secondary sites, even if the network configurations are different.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```

## **`Primary Network Test Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is used to specify a static IP address for a protected VM in the primary site's test network. In Nutanix, test networks are typically used for non-production workloads or for testing purposes. By specifying a static IP address for a protected VM in the test network, you can ensure that the VM retains the same IP address even after a failover event. This is particularly useful for applications that are dependent on specific IP addresses.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```

## **`DR Network Prod Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is utilized to define a fixed IP address for a protected VM in the production network of the disaster recovery (DR) site. It helps to ensure that the network configurations remain consistent during failover events, allowing the protected VMs to be accessed and communicate with other resources in the network. In addition, the VMs will be recovered with these defined IPs after the failover.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```

## **`DR Network Test Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
    This variable is used to set a static IP address for a protected virtual machine in the test network of the disaster recovery (DR) site. This ensures that the virtual machines maintain consistent network configurations during failover events and are able to communicate with other resources in the network. Additionally, it enables the virtual machines to be recovered with the pre-defined IPs after the failover.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```
