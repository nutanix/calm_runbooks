# Runbook Variables

## **`Recovery Plan Name (Required)`** 

  <details>
  <summary><b>Description</b></summary>
   This variable refers to a user-defined name given to a recovery plan that specifies the steps required to recover a particular object or service in the event of a disaster or system failure. The recovery plan can be set up with various options, such as the order in which services or virtual machines should be recovered, the specific recovery point to use, and the notification settings for administrators. The Nutanix Recovery Plan Name is used as a parameter to specify which recovery plan to apply when recovering objects or services in the Nutanix cluster.

   In other words, a recovery plan is a set of predefined steps and procedures that must be followed to restore normal service in case of a disaster. It specifies the steps that need to be taken to recover data and services after an unexpected event such as a power outage, hardware failure, or a natural disaster. The Nutanix Recovery Plan Name parameter is used to identify the specific recovery plan that should be applied during a disaster recovery scenario.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  Test_recovery
  ```

## **`Availability Zone of Entity  Failing Over From (Required)`**

  <details>
  <summary><b>Description</b></summary>
    Availability Zones (AZs) play a crucial role in disaster recovery strategies for cloud-based systems. An Availability Zone is essentially a data center or a cluster of data centers within a specific geographic region. Each Availability Zone is designed to be isolated from failures in other zones and has its own power, cooling, networking, and physical security measures in place.
    
    The primary objective of a disaster recovery solution is to ensure that critical business systems and data can be recovered in the event of a disaster or major disruption. This recovery can involve:

    Replicating data: The entity's data is replicated from the primary environment to the secondary environment, which may span multiple Availability Zones or regions. This replication can occur in near real-time to minimize data loss in the event of a failure.

    Activating failover: When a disaster occurs or the primary environment becomes unavailable, the entity is failed over to the secondary environment. This involves redirecting traffic, activating standby resources, and ensuring that the necessary infrastructure and services are available in the secondary environment.

    Testing and validation: Regular testing of the disaster recovery plan is crucial to ensure its effectiveness. This may involve conducting planned failover exercises to simulate a disaster scenario and validate the failover process, including the activation of the entity in the secondary environment across different Availability Zones.

    It's important to note that the specific process of failing over from one entity to another using a disaster recovery solution can vary depending on the cloud service provider, the architecture of the application or infrastructure, and the specific requirements of the organization.

    In summary, when implementing disaster recovery, an entity is typically failed over from its primary environment to a secondary environment that spans multiple Availability Zones. The failover process involves replicating data, activating failover mechanisms, and conducting regular testing to ensure the effectiveness of the disaster recovery solution.

  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  LOCAL_AZ
  ```

## **`Availability Zone of Entity  Failing Over To (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The variable you are referring to is commonly known as a "failover zone" or "failover target." A failover zone is an alternative Availability Zone where applications can be redirected or switched to in the event of a failure or outage in the primary zone.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  DR_AZ
  ```

## **`Prism Central IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.20.30
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
  The Nutanix Prism Central Username variable is used to specify the username that is used to authenticate with the Nutanix Prism Central management interface.

  Prism Central is a web-based management interface that provides a centralized view of multiple Nutanix clusters. The Nutanix Prism Central Username variable should be set to the username that has been granted access to the Prism Central management interface.

  It is important to ensure that the Nutanix Prism Central Username variable is correctly configured and kept up-to-date to ensure that the Nutanix clusters can be managed effectively. The username specified in this variable should have the appropriate level of permissions to perform the required management tasks in Prism Central.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```
