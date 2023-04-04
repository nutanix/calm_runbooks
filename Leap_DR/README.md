# Runbook Variables
## **`Protection Policy Name (Required)`** 

  <details>
  <summary><b>Description</b></summary>
  The name of a protection policy.
  A protection policy is the central mechanism for controlling management of backup storage space, based on pre-defined recovery window goals.
  </details>
  
  
  ### **Type:** _String_ 


  ### **Example:**

  ```
  policy123
  ```

## **`Recovery Plan Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The name of a Recovery plan.
  A recovery plan is a set of procedures and guidelines that outline the steps to be taken to restore a system or data to its normal operational state in the event of a disaster or disruption. In the context of backup and restore, a recovery plan is developed to ensure that data can be recovered and restored in a timely and efficient manner following a data loss event.
  </details>

  ### **Type:** _String_

  #### **Example:**

  ```
  Recoveryplan123
  ```

## **`Custom RPO Interval for Replication in Hours (Required)`**

  <details>
  <summary><b>Description</b></summary>
  Replication time frequencey to replicate VM snapshots from source to destination. Default Value is 1hr.
  The RPO is a measure of the amount of data that can be lost in the event of a disaster or disruption. For example, an RPO of 1 hour means that data loss can be tolerated up to 1 hour before the next backup or replication point.
  </details>

  ### **Type:** _Integer_

  ### **Example:**

  ```
  4
  ```

## **`Local Schedule (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents Local RPO schedule to keep snapshots of VM locally.
  </details>

  ### **Type:** _String_


  ### **Example:**

  ```
  True
  ```

## **`Custom RPO Interval for Local Snapshot in Hours (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents RPO interval.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  10
  ```
  ### **Note:** Default Value is 1, Should be >= 1 when Local Schedule is enabled

## **`Retention on Primary and Remote (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the maximum of Number of snapshots can keep in system.
  The maximum number of snapshots that can be retained for a specific backup or replication job. A snapshot is a point-in-time copy of data that captures the state of the system or application at a particular moment. Snapshots are commonly used for data protection and disaster recovery purposes.
  </details>

  ### **Type:** _Integer_

  ### **Example:**
  ```
  5
  ```

## **`Protection Start Time (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents start protecting VMs after certain time provided.
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
  This variable represents Production Calm Account Name. 
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  PHX-POC092
  ```

## **`Primary PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the Primary prism central IP.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  10.10.10.40
  ```

## **`Primary PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents primary Prism central username.
  </details>

  #### **Type:** _String_

  #### **Example:**
  ```
  admin
  ```

## **`Primary PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the password used to authenticate with Primary prism central.
  </details>

  #### **Type:** _String_

  #### **Example:**

  ```
  nutanix/4u
  ```

## **`DR Account Cluster Name (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents Cluster name whre VMs going to recovered. This cluster should be present in provided Calm Account.
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  PHX-POC100
  ```

## **`DR PC IP (Required)`**

  <details>
  <summary><b>Description</b></summary>
    This variable represents secondary prism central IP.
  </details>

  ### **Type:** _String_


  ### **Example:**

  ```
  10.20.30.40
  ```

## **`DR PC Username (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the username of secondary prism central.
  </details>
  
  ### **Type:** _String_

  ### **Example:**

  ```
  admin
  ```

## **`DR PC Password (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the password of secondary prism central.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  nutanix/4u
  ```

## **`VM Category for Protection Policy and Recovery Plan (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents categories to which the vms got tagged.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  {"TenantName": "Tmp"}
  ```

## **`Recovery Plan Network Type (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents the recovery plan network type.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  stretched 
  or 
  non-stretched
  ```

#### **`Stage Delay [ In Seconds ] (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The variable represents the delay between stages / boot order for recovery plan.
  </details>
  
  ### **Type:** _Integer_


  ### **Example:**
  ```
  10
  ```

## **`Enable Boot Script (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The variable represents whether enable boot script or not .
  User can provide boot script to each VM. Whenever recovery plan executes this boot script will run on those VMs which have boot scripts available on below path :- for Linux - production --> /usr/local/sbin/production_vm_recovery Linux - Test --> /usr/local/sbin/test_vm_recovery, and for Windows - Production --> (Relative to Nutanix directory in Program Files)/scripts/production/vm_recovery.bat Windows - Test --> (Relative to Nutanix directory in Program Files)/scripts/test/vm_recovery.bat
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`Primary Network Name - Production Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents to production Primary subnet network name.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlan10
  ```

## **`Primary Network Name - Test Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents to production test subnet network name.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlan11
  ```

## **`DR Network Name - Production Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents to Secondary side Primary subnet network name.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlandr10
  ```

## **`DR Network Name - Test Subnet (Required)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents to Secondary side test subnet network name.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  vlandr11
  ```

## **`Enable Static IP Mapping (Required)`**

  <details>
  <summary><b>Description</b></summary>
  The Variable represnts enabling static IP mapping or not.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  True
  ```

## **`VM Name (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The varibles represents vms names for which static ip mapping should be done after recovery.
  </details>
  
  ### **Type:** _string_

  ### **Example:**
  ```
  vm1,vm2
  ```

## **`Primary Network Prod Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The variable represents static ips.
  </details>

  ### **Type:** _String_

  ### **Example:**

  ```
  10.10.10.20,10.20.20.40
  ```

## **`Primary Network Test Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  The variable represents test network static Ips.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```

## **`DR Network Prod Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represnts DR network static IPs.
  </details>

  ### **Type:** _String_

  #### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```

## **`DR Network Test Static IP (Optional)`**

  <details>
  <summary><b>Description</b></summary>
  This variable represents test static IPs.
  </details>

  ### **Type:** _String_

  ### **Example:**
  ```
  10.10.10.20,10.20.20.40
  ```

