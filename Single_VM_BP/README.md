# Runbook Variables

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

  ### **Type:** _String_

  #### **Example:**
  ```
  nutanix/4u
  ```

## **`APP Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The app name for a Nutanix blueprint would depend on the specific application or infrastructure being deployed using that blueprint. Nutanix blueprints are designed to deploy various types of infrastructures or application stacks, so the app name would reflect the purpose or characteristics of the deployed application or infrastructure.

    For example, if you are deploying a blueprint to create a web application stack, a suitable app name could be "Web Application Deployment" or "Web App Blueprint". If the blueprint is intended for a database cluster, an appropriate app name could be "Database Cluster Deployment" or "Database Blueprint".
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  app_name
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

  ### **Example:**
  ```
  bp_name
  ```

## **`Project Name for App Creation (Required)`**

  <details>
  <summary><b>Description</b></summary>
    In Nutanix, the term "Project Name" typically refers to the name given to a specific project or initiative for creating an application within the Nutanix environment. The project name represents a unique identifier or label for the application development project.

    The project name is chosen by the development team or project stakeholders and is used to track and manage the progress, resources, and activities related to the application creation process on the Nutanix platform.

    The specific Project Name would depend on the nature of the application being developed, the organization's naming conventions, and any relevant naming guidelines or standards in place.

    For example, if you are creating a project for developing a web application, a suitable Project Name could be "WebAppProject", "ProjectXYZ", or "AcmeWebApp". If the application is for a specific business domain or purpose, you could include that information in the Project Name, such as "RetailAppProject" or "FinanceApplicationProject".
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix_project
  ```

## **`Account Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable represents the name of the Nutanix storage account used for provisioning and managing storage resources on the Nutanix cluster. Storage accounts provide a logical grouping of storage resources, such as containers and datastores, and are used to allocate and manage storage capacity for various applications and workloads. This variable is required for any operations that involve storage provisioning or management on the Nutanix cluster using the Prism Central management interface or APIs.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutnx_local
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
  nutanix_project_env
  ```

## **`Tenant Category for APP VM (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, when assigning a category name to an application VM, you can assign categories to your application VMs using a feature called "VM Custom Tags." This allows you to categorize and organize your VMs based on different criteria, such as application type, department, or environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  {"TenantName":"nutanix"}
  ```

## **`Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable is used to specify the name of the Nutanix cluster that will be used for the deployment. The cluster name is a unique identifier for a Nutanix cluster and is used for managing resources such as virtual machines, networks, storage, and user accounts. This variable is required for any operations that interact with the Nutanix cluster using API or CLI.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  PHX-POC092
  ```

## **`App VM OS Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The "OS Type" of an application VM refers to the operating system installed on that VM. Nutanix does not have a built-in feature to automatically detect or determine the OS type of a VM. Instead, the OS type is typically manually specified during the VM creation process or can be identified based on the information provided by the user.

  When creating an application VM in Nutanix, you would typically select the desired operating system from a list of supported OS options. This selection can be made based on the specific OS distribution and version that you intend to install on the VM.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  Linux / Windows
  ```
## **`Image Name for APP Creation (Required)`**

  <details>
  <summary><b>Description</b></summary>
    When creating an image for application deployment in Nutanix, the image name typically represents the name or identifier assigned to the virtual machine (VM) image used to create instances of the application within the Nutanix environment.
    </details>
  
  #### **Type:** _String_

  #### **Example:**

  ```
  wordpress-db
  ```
## **`App VM Memory in GB (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, when creating an application VM, you can specify the amount of memory (RAM) allocated to the VM in gigabytes (GB). The memory allocation determines the available RAM resources for the VM to run applications and perform its tasks.
  It's important to consider the requirements of your applications and workloads when determining the appropriate amount of memory to allocate to your VMs. Insufficient memory can result in performance issues, while excessive memory allocation can lead to resource wastage.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  PHX-POC100
  ```

## **`Number of App VM vCPUs (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, the number of virtual CPUs (vCPUs) allocated to an application VM determines the computing resources available to the VM for executing tasks and running applications. The specific number of vCPUs assigned to an app VM can vary based on the requirements of the workload and the capabilities of the underlying hardware and hypervisor.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  2
  ```

## **`Subnet Name for APP VM (Required)`**

  <details>
  <summary><b>Description</b></summary>
    The subnet name is not specifically tied to the backup and restore operations. The subnet name refers to the network subnet on which the application VMs or virtual resources are deployed within the Nutanix environment.

    The subnet name is typically chosen based on your organization's naming conventions or network segmentation strategy. It helps identify and differentiate the network segment associated with the application and its VMs. It is independent of the backup and restore operations but plays a role in providing connectivity and defining network boundaries for the application.
  </details>
  
  ### **Type:** _String_

  ### **Example:**
  ```
  subnet_name
  ```

## **`Custom IP for VM (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, you can assign a custom IP address to a virtual machine (VM) by leveraging the network configuration options available in your environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.12.19
  ```

## **`App Credential User (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The management of application credentials and users is typically handled within the operating system and applications themselves. Nutanix provides various tools and features to manage the VMs and the underlying infrastructure, but it does not directly manage the application-level user credentials.

  To manage application credentials and users within a VM running on Nutanix, you would typically follow the standard practices specific to the operating system and applications installed on the VM. This may involve creating user accounts, setting passwords, configuring access controls, and managing authentication within the operating system and the applications themselves.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  root
  ```

## **`App Credential Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The management of application credentials and users is typically handled within the operating system and applications themselves. Nutanix provides various tools and features to manage the VMs and the underlying infrastructure, but it does not directly manage the application-level user credentials.

  To manage application credentials and users within a VM running on Nutanix, you would typically follow the standard practices specific to the operating system and applications installed on the VM. This may involve creating user accounts, setting passwords, configuring access controls, and managing authentication within the operating system and the applications themselves.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix/4u
  ```

#### **`PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>
  
  ### **Type:** _Integer_

  ### **Example:**
  ```
  10.10.10.12
  ```

## **`Project User Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The variable username refers to the username associated with a project user in Nutanix. This variable is used to represent the specific username that you choose for a project user account within your Nutanix environment.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  admin
  ```

## **`Project User Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The variable password refers to the password associated with a project user in Nutanix. This variable is used to represent the specific password that you choose for a project user account within your Nutanix environment.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix/4u
  ```
