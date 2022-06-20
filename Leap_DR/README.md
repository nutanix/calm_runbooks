
| Variable_Display_Name    | Variable_Actual_Name        | Type       | Description |
| :---------------------  | :-------------------------- | :--------- | :---------- |
| Protection Policy Name | protection_policy_name  | Mandatory  | Name of protection policy.  |
| Recovery Plan Name  | recovery_plan_name  | Mandatory  | Name of Recovery plan.  |
| Custom RPO Interval for Replication in Hours  | custom_rpo_interval_replication  | Mandatory  | Replication time frequencey to replicate VM snapshots from source to destination. Default Value is 1.   |
| Local Schedule  | local_schedule  | Mandatory  | Local RPO schedule to keep snapshots of VM locally.  |
| Custom RPO Interval for Local Snapshot in Hours  | custom_rpo_interval_local  | Mandatory  | Default Value is 1, Should be >= 1 for "Local Schedule = True".  |
| Number of Snapshot Retention   | number_of_snapshot_retention  | Mandatory  | How many snapshots should be retained. It will retain number of latest snapshots.  |
| Policy Schedule Time From Now  | policy_schedule_time  | Mandatory  | Can schedule policy / start protecting VMs after certain time provided.  |
| Primary Account Name  | primary_account_name  | Mandatory  | Name of Calm Account at Production PC. I.E. :- NTNX_LOCAL_AZ.  |
| Primary Account Cluster Name  | primary_account_cluster  | Mandatory  | Cluster name for policy and recovery plan schedule. This cluster should be present in provided Calm Account.  |
| DR Account Name  | dr_account_name  | Mandatory  | This Runbook will create Calm Account of DR PC on production PC with this provided name.  |
| DR Account Cluster Name  | dr_account_cluster  | Mandatory  | Cluster name for policy and recovery plan schedule. This cluster should be present at DR PC.  |
| DR PC IP  | dr_account_url  | Mandatory  | DR Prism Central IP address.  |
| DR PC Username  | dr_account_username  | Mandatory  | DR Prism Central username.  |
| DR PC Password  | dr_account_password  | Mandatory  | DR Prism Central Password.  |
| VM Category for Protection Policy and Recovery Plan  | vm_category  | Mandatory  | It will protect VMs depending upon categories. You will need to provide category names in json format.  |
| Recovery Plan Network Type  | recovery_network_type  | Mandatory  | Need to choose from two type : stretched, non-stretched.  |
| Stage Delay [ In Seconds ]  | stage_delay  | Mandatory  | Delay between stages / boot order for recovery plan.  |
| Enable Boot Script   | enable_boot_script  | Mandatory  | User can provide boot script to each VM. Whenever recovery plan executes this boot script will run on those VMs which have boot scripts available on below path :- for Linux - production --> /usr/local/sbin/production_vm_recovery   Linux - Test --> /usr/local/sbin/test_vm_recovery,  and for Windows - Production --> (Relative to Nutanix directory in Program Files)/scripts/production/vm_recovery.bat Windows - Test --> (Relative to Nutanix directory in Program Files)/scripts/test/vm_recovery.bat  |
| Primary Network Name - Production Subnet  | primary_network_prod_name  | Mandatory  | Primary subnet name at production PC for recovery plan.  |
| Primary Network Gateway IP with Prefix - Production  | primary_network_prod  | Mandatory  | Gateway IP with network prefix of "Primary Network Name - Production Subnet" for recovery plan.  |
| Primary Network Name - Test Subnet  | primary_network_test_name  | Mandatory  | Test subnet name at production PC for recovery plan.  |
| Primary Network Gateway IP with Prefix - Test Subnet  | primary_network_test  | Mandatory  | Gateway IP with network prefix of "Primary Network Name - Test Subnet" for recovery plan.  |
| DR Network Name - Production Subnet  | dr_network_prod_name  | Mandatory  | Primary subnet name at DR PC for recovery plan. VM will be recoverd at DR site on this network for actual disaster.  |
| Recovery Network Gateway IP with Prefix - Production Subnet  | dr_network_prod  | Mandatory  | Gateway IP with network prefix of "Recovery Network Name - Production Subnet" for recovery plan.  |
| DR Network Name - Test Subnet  | dr_network_test_name  | Mandatory  | Test subnet name at DR PC for recovery plan. VM will be recoverd at DR site on this network while testing disaster.  |
| Recovery Network Gateway IP with Prefix - Test Subnet  | dr_network_test  | Mandatory  | Gateway IP with network prefix of "Recovery Network Name - Test Subnet" for recovery plan.  |
| Enable Static IP Mapping   | static_ip_mapping  | Mandatory  | User can assign static IP's to VMs at production / Recovery networks. If user need to provide static IP mapping to any of the VM choose True.  |
| VM Name Primary Network Test Static IP  | vm_name primary_network_test_static_ip | Mandatory  | Default Value is "NA". User Can provide multiple VM Names qama separated. IE. :- VM1, VM2. Also user needs to provide Number of static IP's of VM. Default Value is "NA". User Need to provide test IP at Production site for Number of VM's in  "VM Name" qama separated. IE. :- 10.1.1.3, 10.1.1.6. First IP will gets map to first VM1 and second IP will get maps to VM2 and likewise.  |
| Primary Network Prod Static IP [ Should be present VM IP ]  | primary_network_prod_static_ip | Mandatory  | Default Value is "NA". User Need to provide Current IP of VM at Production site for Number of VM's in  "VM Name" qama separated. IE. :- 10.1.1.3, 10.1.1.6. First IP will gets map to first VM1 and second IP will get maps to VM2 and likewise.  |
| DR Network Prod Static IP  | dr_network_prod_static_ip  | Mandatory  | Default Value is "NA". User Need to provide DR Production Network IP  for Number of VM's in  "VM Name" qama separated. IE. :- 10.1.1.3, 10.1.1.6. First IP will gets map to first VM1 and second IP will get maps to VM2 and likewise.  |
| DR Network Test Static IP  | dr_network_test_static_ip  | Mandatory  | Default Value is "NA". User Need to provide DR Test Network IP  for Number of VM's in  "VM Name" qama separated. IE. :- 10.1.1.3, 10.1.1.6. First IP will gets map to first VM1 and second IP will get maps to VM2 and likewise.  |
| PC IP  | PC_IP  | Mandatory  | Production Prism Central IP address.  |
| Prism Central Password  | prism_central_passwd  | Mandatory  | Production Prism Central Password.  |
| Prism Central UserName  | prism_central_username  | Mandatory  | Production Prism Central Username.  |
