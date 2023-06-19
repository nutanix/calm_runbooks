# Runbook Variables

## **`APP Name (Required)`** 

  <details>
  <summary><b>Description</b></summary>
    The app name for a Nutanix blueprint would depend on the specific application or infrastructure being deployed using that blueprint. Nutanix blueprints are designed to deploy various types of infrastructures or application stacks, so the app name would reflect the purpose or characteristics of the deployed application or infrastructure.

    For example, if you are deploying a blueprint to create a web application stack, a suitable app name could be "Web Application Deployment" or "Web App Blueprint". If the blueprint is intended for a database cluster, an appropriate app name could be "Database Cluster Deployment" or "Database Blueprint".
  </details>  
    
  ### **Type:** _String_

  ### **Example:**
  ```
  Test_App
  ```

## **`Blueprint Name (Required)`**

  <details>
    <summary><b>Description</b></summary>
      In Nutanix, a blueprint refers to a predefined set of configurations and specifications that describe the infrastructure or application stack to be deployed on the Nutanix platform. It serves as a template or blueprint for creating and provisioning resources within a Nutanix environment.

      A Nutanix blueprint typically includes details such as virtual machine configurations, storage requirements, networking settings, security policies, and other parameters necessary to define the desired infrastructure or application stack. Blueprints help streamline and automate the deployment process, ensuring consistency and efficiency in creating and managing Nutanix resources.

      Nutanix blueprints can be created and customized through the Nutanix Prism web interface or using APIs and scripting tools. Administrators or users can define various blueprints based on their specific requirements, enabling them to quickly provision infrastructure or application stacks with consistent settings and configurations.

      Once a blueprint is defined, it can be used to create and deploy multiple instances of the specified infrastructure or application stack. This allows for efficient scaling, replication, and management of resources within the Nutanix environment.

      Overall, Nutanix blueprints play a crucial role in simplifying and accelerating the process of deploying and managing infrastructure and applications on the Nutanix platform, promoting agility, standardization, and automation.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  Test_BP
  ```

## **`Account Name (Required)`**

  <details>
    <summary><b>Description</b></summary>
    This variable represents the name of the Nutanix storage account used for provisioning and managing storage resources on the Nutanix cluster. Storage accounts provide a logical grouping of storage resources, such as containers and datastores, and are used to allocate and manage storage capacity for various applications and workloads. This variable is required for any operations that involve storage provisioning or management on the Nutanix cluster using the Prism Central management interface or APIs.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  NTNX_LOCAL_AZ
  ```

## **`Project Name for App Creation (Required)`**

  <details>
    <summary><b>Description</b></summary>
    In Nutanix, the term "Project Name" typically refers to the name given to a specific project or initiative for creating an application within the Nutanix environment. The project name represents a unique identifier or label for the application development project.

    The project name is chosen by the development team or project stakeholders and is used to track and manage the progress, resources, and activities related to the application creation process on the Nutanix platform.

    The specific Project Name would depend on the nature of the application being developed, the organization's naming conventions, and any relevant naming guidelines or standards in place.

    For example, if you are creating a project for developing a web application, a suitable Project Name could be "WebAppProject", "ProjectXYZ", or "AcmeWebApp". If the application is for a specific business domain or purpose, you could include that information in the Project Name, such as "RetailAppProject" or "FinanceApplicationProject".
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  Nutanix_project
  ```

## **`Create Protection Policy (Required)`**

  <details>
  <summary><b>Description</b></summary>
   This variable is a user-defined name given to a policy that determines how often and for how long backups or snapshots are taken of a specific object in the Nutanix cluster. This object can be a virtual machine, a container, or any other resource that requires protection against data loss. The policy can be configured with various options, such as backup frequency, retention period, backup schedule, compression, and encryption settings. This parameter is used to specify which protection policy to apply when creating or managing data protection policies for objects in the Nutanix cluster. The policy helps manage backup storage space, based on pre-defined recovery window goals.
  </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  Yes / No
  ```

  ## **`App Protection Policy Name (Required)`**

  <details>
    <summary><b>Description</b></summary>
      In Nutanix, an App Protection Policy refers to a set of rules and configurations designed to protect and safeguard applications running within the Nutanix environment. The primary goal of an App Protection Policy is to ensure the availability, integrity, and recoverability of critical applications and their associated data.

      The specific components and configurations of an App Protection Policy can vary based on the requirements of the application and the desired level of protection. Here are some common elements that may be included in an App Protection Policy:

      Backup Frequency: This specifies how often backups of the application and its associated data should be performed. It can be defined in terms of a schedule (e.g., daily, weekly) or specific time intervals.

      Retention Period: This determines how long the backups should be retained before they are considered no longer needed. The retention period is typically defined based on regulatory requirements, business needs, and recovery objectives.

      Recovery Point Objective (RPO): The RPO defines the maximum amount of acceptable data loss in the event of a failure or disaster. It specifies the point in time to which the application and data can be restored from the backup.

      Recovery Time Objective (RTO): The RTO specifies the maximum tolerable downtime for the application. It defines the target time for restoring the application and making it fully operational after a failure or disaster.

      Backup Storage Location: This indicates the location or target where the backups will be stored. It can be on-premises or in a cloud-based storage system, depending on the organization's data storage strategy.

      Testing and Validation: An App Protection Policy may include provisions for regular testing and validation of the backups to ensure their integrity and usability in the event of a restore operation.

      Encryption and Security: Security measures such as data encryption, access controls, and authentication mechanisms may be included in the App Protection Policy to protect the backups and prevent unauthorized access.

      Monitoring and Reporting: The policy may define monitoring and reporting requirements to ensure compliance with the protection policy and provide insights into the backup and recovery operations.

      It's important to tailor the App Protection Policy to the specific needs and criticality of the application. The policy should be regularly reviewed, updated, and tested to ensure its effectiveness and alignment with changing business requirements.
   </details>

  #### **Type:** _String_

  ### **Example:**
  ```
  Policy_Test_App
  ```

## **`Environment Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    Creating a project environment refers to the process of setting up an isolated environment for a specific project on the Nutanix cluster. This involves configuring resources such as virtual machines, networks, storage, and other services required for the project. The project environment can be customized based on the project requirements, and it can be created using the Nutanix management interface, such as Prism Central or using APIs. The process typically involves defining the project requirements, selecting the resources, configuring the settings, and deploying the project environment. The project environment can also be managed and monitored using the Nutanix management interface to ensure optimal performance and availability.

    This refers to the creation of a Calm environment within a Nutanix project, which allows for the deployment and management of applications and services. A Calm environment provides a platform for developing and publishing applications, and includes a range of tools and services for orchestration, automation, and monitoring. The creation of a Calm environment typically involves specifying the infrastructure resources required for the environment, such as virtual machines, networks, and storage, as well as the applications and services that will be deployed within the environment.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  Nutanix_project_Environment
  ```

## **`Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the name of the Nutanix cluster that will be used for the deployment. The cluster name is a unique identifier for a Nutanix cluster and is used for managing resources such as virtual machines, networks, storage, and user accounts. This variable is required for any operations that interact with the Nutanix cluster using API or CLI.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  cluster-012
  ```

## **`Subnet Name for APP VM (Required)`**

  <details>
  <summary><b>Description</b></summary>
    When protecting an application using Nutanix, the subnet name is not specifically tied to the backup and restore operations. The subnet name refers to the network subnet on which the application VMs or virtual resources are deployed within the Nutanix environment.

    The subnet name is typically chosen based on your organization's naming conventions or network segmentation strategy. It helps identify and differentiate the network segment associated with the application and its VMs. It is independent of the backup and restore operations but plays a role in providing connectivity and defining network boundaries for the application.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  Nutanix_project_Overlay_Subnet
  ```

## **`Image Name for APP Creation (Required)`**

  <details>
  <summary><b>Description</b></summary>
    When creating an image for application deployment in Nutanix, the image name typically represents the name or identifier assigned to the virtual machine (VM) image used to create instances of the application within the Nutanix environment.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  Centos7HadoopMaster.iso
  ```

## **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  10.10.20.30
  ```

## **`Prism Central UserName (Required)`**

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

  #### **Type:** _String_

  #### **Example:**
  ```
  nutanix/12
  ```
