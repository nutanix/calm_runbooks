# Runbook Variables

## **`PC IP (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  The Nutanix Prism Central IP is the network address or IP address of the Nutanix Prism Central management platform. It is the location where you can access the central management console for managing Nutanix clusters, including virtualization, storage, and networking resources. You can use this IP address to connect to the Prism Central instance from a web browser or through API calls to automate management tasks. It is important to keep the Nutanix Prism Central IP secure, as it provides access to the management platform and the Nutanix clusters it manages.
  </details>  
  
  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.12
  ```

## **`Project Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
    In Nutanix, the term "Project Name" typically refers to the name given to a specific project or initiative for creating an application within the Nutanix environment. The project name represents a unique identifier or label for the application development project.

    The project name is chosen by the development team or project stakeholders and is used to track and manage the progress, resources, and activities related to the application creation process on the Nutanix platform.

    The specific Project Name would depend on the nature of the application being developed, the organization's naming conventions, and any relevant naming guidelines or standards in place.

    For example, if you are creating a project for developing a web application, a suitable Project Name could be "WebAppProject", "ProjectXYZ", or "AcmeWebApp". If the application is for a specific business domain or purpose, you could include that information in the Project Name, such as "RetailAppProject" or "FinanceApplicationProject".
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  Nutanix_project
  ```

## **`Authentication Type [ Used in Project ] (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, the authentication type used for project user accounts depends on the specific authentication mechanisms and settings configured within the environment. Nutanix supports multiple authentication types that can be used for project users. Here are some common authentication types used in Nutanix:

  Local Authentication: Nutanix Prism provides a built-in local authentication mechanism where project users can be created and authenticated directly within the Nutanix cluster. With local authentication, user accounts and passwords are managed within the Nutanix environment itself.

  Active Directory (AD) Authentication: Nutanix also supports integrating with an external Active Directory (AD) domain for user authentication. This allows project users to authenticate using their AD credentials, providing a centralized and unified authentication mechanism.

  Lightweight Directory Access Protocol (LDAP) Authentication: Nutanix can also be configured to use LDAP servers for project user authentication. LDAP authentication enables authentication against a directory service that follows the LDAP protocol, such as Microsoft Active Directory or OpenLDAP.

  Security Assertion Markup Language (SAML) Authentication: SAML authentication enables integration with identity providers (IdPs) that support the SAML protocol. Project users can authenticate using their credentials from the configured IdP, which can be an external SAML-based identity provider.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  AD / IDP
  ```

## **`IDP Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable refers to the name of an Identity Provider in the context of authentication and user management. This variable is used to represent the specific name or identifier associated with the IdP used for authentication in your system.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  ad_name
  ```

## **`Active Directory Domain Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Active Directory (AD) Domain Name refers to the fully qualified domain name (FQDN) of an Active Directory domain in a Windows environment. It is the unique name that identifies the specific Active Directory domain within a network.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  test.domain.com
  ```

## **`operation (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The variable operation is commonly used to represent the type of operation being performed on user accounts, such as adding, updating, or deleting users. This variable helps determine the specific action to be taken when managing user accounts within a system.
  Possible values:
  - 'add': Adding a new user.
  - 'update': Updating an existing user.
  - 'delete': Deleting an existing user.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  add_user / update / delete_user
  ```

## **`Admin Users (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Project Admin Users are specific user accounts with administrative privileges that are associated with a particular project or tenant within the Nutanix environment. These users have elevated permissions within the scope of the assigned project and can perform administrative tasks related to that specific project.

  Project Admin Users have control over the resources and settings within their assigned project. They can manage virtual machines, storage, networking, and other aspects of the project infrastructure. They also have the ability to configure user roles and permissions for other users within the project.

  Here are some key points about Nutanix Project Admin Users:

  Scope: Project Admin Users have administrative privileges limited to the specific project or tenant they are associated with. Their administrative actions and settings affect only the resources within that project.

  Project-Level Control: Project Admin Users can create, modify, and delete resources within their project, such as virtual machines, storage containers, and network configurations.

  User Management: Project Admin Users have the authority to manage user accounts and assign roles and permissions to other users within their project. They can control the level of access and actions that other users can perform within the project.

  Collaboration: Project Admin Users can collaborate with other users within the project, sharing resources, configuring access controls, and working together to achieve project goals.

  The exact configuration and management of Project Admin Users may vary depending on the version of Nutanix software being used and the specific setup of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information on how to manage and configure Project Admin Users within your specific Nutanix cluster.

</details>

  #### **Type:** _String_

  #### **Example:**
  ```
  admin@test.domain.com
  ```

## **`Developer Users (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Developer Users are user accounts with specific permissions and access rights tailored towards development and application-related tasks. These users are typically assigned roles and privileges that allow them to create, deploy, and manage applications within the Nutanix environment.

  Developer Users in Nutanix may have the following characteristics:

  Application Deployment: Developer Users have the ability to deploy applications within the Nutanix infrastructure. They can create and manage virtual machines, containers, and other resources required for application deployment.

  Resource Management: Developer Users can manage the resources allocated to their applications, including storage, networking, and compute resources. They can scale their applications based on demand and optimize resource utilization.

  Application Configuration: Developer Users have the necessary privileges to configure application-specific settings, such as network configurations, load balancing, security policies, and integration with other services.

  Monitoring and Troubleshooting: Developer Users can monitor the performance and health of their applications, leveraging Nutanix monitoring and logging features. They can identify issues, troubleshoot application-related problems, and take appropriate actions to ensure smooth operation.

  Collaboration: Developer Users can collaborate with other team members, including system administrators, network administrators, and other developers, to coordinate application deployments, troubleshoot issues, and share resources and knowledge.

  The specific roles, permissions, and capabilities of Developer Users can be customized based on the organization's requirements and security policies. Nutanix provides role-based access control (RBAC) mechanisms to define and manage user roles with granular permissions.

  It's important to note that the exact user roles, permissions, and capabilities may vary depending on the version of Nutanix software being used and the specific configuration of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information about Developer Users and their roles within your Nutanix cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  developer@test.domain.com
  ```

## **`Consumer Users (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Consumer Users refer to user accounts that have limited access and permissions within the Nutanix environment. These users are typically granted access to specific resources or services based on their role or business needs. Consumer Users are not typically involved in the administration or management of the Nutanix infrastructure but rather consume the services provided by the system.

  Here are some key points about Consumer Users in Nutanix:

  Limited Access: Consumer Users have restricted access to the Nutanix infrastructure and are only granted access to the resources or services that are necessary for their specific role or requirements.

  Resource Consumption: Consumer Users primarily consume the services and resources provided by Nutanix, such as virtual machines, applications, or data stored within the environment. They may interact with these resources through web interfaces, APIs, or other designated access points.

  Role-Based Access: The permissions and access rights of Consumer Users are typically defined through role-based access control (RBAC). This means that their level of access and the specific actions they can perform are determined by their assigned role or user profile.

  Self-Service Provisioning: In some cases, Consumer Users may have the ability to self-provision or request specific resources within predefined limits. This enables them to initiate the creation of virtual machines or other resources without the direct involvement of administrators.

  User Experience: Nutanix provides user-friendly interfaces and tools to enhance the user experience for Consumer Users. This includes self-service portals, dashboards, and simplified workflows tailored to their specific needs.

  It's important to note that the specific roles, permissions, and capabilities of Consumer Users can be customized based on the organization's requirements and security policies. The exact configuration and management of Consumer Users may vary depending on the version of Nutanix software being used and the specific setup of your Nutanix environment.

  For detailed information on configuring and managing Consumer Users within your Nutanix cluster, it's recommended to refer to the Nutanix documentation or consult with your system administrator.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  consumer@test.domain.com
  ```

## **`Operator Users (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Operator Users are user accounts with specific permissions and access rights that are focused on managing and operating the Nutanix infrastructure. These users are responsible for performing day-to-day administrative tasks, monitoring system health, and ensuring the smooth operation of the Nutanix cluster.

  Here are some key points about Operator Users in Nutanix:

  Infrastructure Management: Operator Users have the necessary privileges to manage and operate the Nutanix infrastructure. They can perform tasks such as configuring storage, managing networking, monitoring cluster health, and ensuring high availability.

  Cluster Monitoring: Operator Users are responsible for monitoring the performance and health of the Nutanix cluster. They have access to monitoring tools and interfaces to track system metrics, analyze performance trends, and identify potential issues.

  Troubleshooting and Maintenance: Operator Users have the ability to troubleshoot and resolve issues related to the Nutanix infrastructure. They can investigate system alerts, perform diagnostics, and initiate maintenance tasks to ensure optimal system performance.

  Resource Allocation and Optimization: Operator Users can manage the allocation and optimization of resources within the Nutanix cluster. They can monitor resource utilization, identify bottlenecks, and make adjustments to ensure efficient resource utilization across the infrastructure.

  Collaboration with Administrators: Operator Users work closely with administrators, system engineers, and other team members to coordinate infrastructure management activities. They collaborate on tasks such as capacity planning, performance optimization, and infrastructure upgrades.

  The specific roles, permissions, and capabilities of Operator Users can be customized based on the organization's requirements and security policies. Nutanix provides role-based access control (RBAC) mechanisms to define and manage user roles with granular permissions.

  It's important to note that the exact user roles, permissions, and capabilities may vary depending on the version of Nutanix software being used and the specific configuration of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information about Operator Users and their roles within your Nutanix cluster.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  operator@test.domain.com
  ```
## **`Admin Groups (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Project Admin Groups are groups of users with administrative privileges that are associated with a specific project or tenant within the Nutanix environment. These groups provide a convenient way to manage and assign administrative roles and permissions to multiple users within a project.

  Here are some key points about Project Admin Groups in Nutanix:

  Scope: Project Admin Groups have administrative privileges limited to the specific project or tenant they are associated with. The users in these groups have administrative control over the resources and settings within their assigned project.

  Role-Based Access Control: Nutanix uses role-based access control (RBAC) to define and manage user roles and permissions. Project Admin Groups are typically assigned a specific administrative role within the project, which determines their access rights and privileges.

  Group Management: Project Admin Groups can be created, modified, and deleted within the Nutanix environment. System administrators or users with appropriate permissions can manage the membership of these groups, adding or removing users as needed.

  Role Assignment: Once a Project Admin Group is created, the desired administrative role can be assigned to the group. This role determines the level of access and the specific actions that the users within the group can perform within the project.

  Collaboration: Project Admin Groups enable effective collaboration among project administrators. By assigning users to these groups, administrators can easily share responsibilities, coordinate administrative tasks, and ensure consistent access control and permissions management.

  It's important to note that the exact configuration and management of Project Admin Groups may vary depending on the version of Nutanix software being used and the specific setup of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information on how to create, manage, and assign roles to Project Admin Groups within your specific Nutanix cluster.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  admingroup@test.domain.com
  ```
## **`Developer Groups (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Developer Groups are groups of users that are created and managed to facilitate collaboration and access control for developers within the Nutanix environment. These groups are specifically designed to group developers together and provide them with the necessary permissions and resources to carry out their development tasks effectively.

  Here are some key points about Developer Groups in Nutanix:

  Collaboration and Teamwork: Developer Groups allow developers to be organized and collaborate more efficiently. By grouping developers together, it becomes easier to assign permissions, share resources, and coordinate development efforts within the Nutanix environment.

  Role-Based Access Control: Nutanix utilizes role-based access control (RBAC) to define and manage user roles and permissions. Developer Groups are typically assigned specific roles or permissions tailored to the needs of developers. These roles determine the level of access and the actions that developers can perform within the Nutanix environment.

  Resource Allocation: Developer Groups can be granted access to specific resources and services within the Nutanix infrastructure. This includes virtual machines, containers, storage, and other resources necessary for development purposes. The resources allocated to Developer Groups can be customized based on the requirements of the development team.

  Simplified Access Management: Instead of individually managing permissions for each developer, Developer Groups allow for easier management of access control. Permissions can be assigned or revoked at the group level, ensuring consistent access across the group members.

  Project-specific Groups: Developer Groups can be created and associated with specific projects or development initiatives. This allows developers to work within the context of their projects, focusing on their specific development tasks while collaborating with other team members.

  It's important to note that the exact configuration and management of Developer Groups may vary depending on the version of Nutanix software being used and the specific setup of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information on how to create, manage, and assign roles to Developer Groups within your specific Nutanix cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  developergroup@test.domain.com
  ```

## **`Operator Groups (Required)`**

  <details>
  <summary><b>Description</b></summary>
    In Nutanix, Operator Groups are groups of users that are created and managed to facilitate collaboration and access control for operators within the Nutanix environment. These groups are specifically designed to group operators together and provide them with the necessary permissions and resources to carry out their operational tasks effectively.

    Here are some key points about Operator Groups in Nutanix:

    Collaboration and Teamwork: Operator Groups allow operators to be organized and collaborate more efficiently. By grouping operators together, it becomes easier to assign permissions, share resources, and coordinate operational tasks within the Nutanix environment.

    Role-Based Access Control: Nutanix utilizes role-based access control (RBAC) to define and manage user roles and permissions. Operator Groups are typically assigned specific roles or permissions tailored to the needs of operators. These roles determine the level of access and the actions that operators can perform within the Nutanix environment.

    Infrastructure Management: Operator Groups are granted permissions to manage and operate the Nutanix infrastructure. This includes tasks such as configuring storage, managing networking, monitoring cluster health, and ensuring high availability.

    Resource Allocation: Operator Groups can be granted access to specific resources and services within the Nutanix infrastructure. This may include managing virtual machines, storage containers, and other resources necessary for operational tasks. The resources allocated to Operator Groups can be customized based on the requirements of the operational team.

    Simplified Access Management: Instead of individually managing permissions for each operator, Operator Groups allow for easier management of access control. Permissions can be assigned or revoked at the group level, ensuring consistent access across the group members.

    It's important to note that the exact configuration and management of Operator Groups may vary depending on the version of Nutanix software being used and the specific setup of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information on how to create, manage, and assign roles to Operator Groups within your specific Nutanix cluster.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  operatorgroup@test.domain.com
  ```

## **`Consumer Groups (Required)`**

  <details>
  <summary><b>Description</b></summary>
  In Nutanix, Consumer Groups are groups of users that are created and managed to facilitate collaboration and access control for consumers within the Nutanix environment. These groups are specifically designed to group consumers together and provide them with the necessary permissions and resources to consume services and resources effectively.

  Here are some key points about Consumer Groups in Nutanix:

  Collaboration and Teamwork: Consumer Groups allow consumers to be organized and collaborate more efficiently. By grouping consumers together, it becomes easier to assign permissions, share resources, and coordinate consumption of services within the Nutanix environment.

  Role-Based Access Control: Nutanix utilizes role-based access control (RBAC) to define and manage user roles and permissions. Consumer Groups are typically assigned specific roles or permissions tailored to the needs of consumers. These roles determine the level of access and the actions that consumers can perform within the Nutanix environment.

  Resource Consumption: Consumer Groups are granted permissions to consume services and resources within the Nutanix infrastructure. This includes accessing virtual machines, applications, data, and other resources necessary for their specific requirements. The resources allocated to Consumer Groups can be customized based on the consumption needs of the consumer group.

  Simplified Access Management: Instead of individually managing permissions for each consumer, Consumer Groups allow for easier management of access control. Permissions can be assigned or revoked at the group level, ensuring consistent access across the group members.

  Project-specific Groups: Consumer Groups can be created and associated with specific projects or initiatives. This allows consumers to work within the context of their projects, focusing on their specific consumption requirements while collaborating with other team members.

  It's important to note that the exact configuration and management of Consumer Groups may vary depending on the version of Nutanix software being used and the specific setup of your Nutanix environment. It's recommended to refer to the Nutanix documentation or consult with your system administrator for detailed information on how to create, manage, and assign roles to Consumer Groups within your specific Nutanix cluster.
  </details>
  
  ### **Type:** _String_

  ### **Example:**
  ```
  consumergroup@test.domain.com
  ```

## **`Project User Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Project Admin User Username in Nutanix refers to the username or login name associated with a user account that has administrative privileges within a specific project or tenant. This username is used to authenticate and identify the user when performing administrative tasks and managing resources within the project.

  The Project Admin User Username is typically unique to each administrator and is chosen during the user account creation process. It is used in combination with a corresponding password or other authentication credentials to authenticate the user and grant them administrative access to the resources and services within the Nutanix project.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  user1
  ```

## **`Project User Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Project Admin User password in Nutanix refers to the password associated with a user account that has administrative privileges within a specific project or tenant. This password is used to authenticate and identify the user when performing administrative tasks and managing resources within the project.

  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix/4u
  ```
