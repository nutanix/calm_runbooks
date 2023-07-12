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

## **`Account Name of Entity Failing Over From (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Nutanix Account Name refers to the name of the entity or organization that is failing over from one environment to another within the Nutanix infrastructure. It typically represents the account or organization associated with the source environment that is being transitioned or failed over to a target environment.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  LOCAL_AZ
  ```

## **`Account Name of Entity Failing Over To (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The Account Name of the entity failing over to a Nutanix environment represents the name of the target account or organization that is receiving the failover or migration from another environment. In the context of Nutanix, this typically refers to the account or organization associated with the destination or target Nutanix environment.

    The specific Account Name will depend on the configuration and setup of the Nutanix deployment in the target environment. It could be the name of a company, department, or any other entity that owns and manages the Nutanix infrastructure in that specific environment.
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
  admin
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
  nutanix/4u
  ```
