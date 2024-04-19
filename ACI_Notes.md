# ACI Automation

### SSH to APIC 
```
apic1# bash
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8): No such file or directory
admin@apic1:~> show fabric membership
This command is being deprecated on APIC controller, please use NXOS-style equivalent command
clients:
serial-number  node-id  node-name  model        role   ip              decomissioned  supported-model
-------------  -------  ---------  -----------  -----  --------------  -------------  ---------------
TEP-1-104      101      spine-101  N9K-C9508    spine  10.0.128.65/32  no             yes
TEP-1-103      102      spine-102  N9K-C9508    spine  10.0.128.66/32  no             yes
TEP-1-101      201      leaf-201   N9K-C9396PX  leaf   10.0.128.64/32  no             yes
TEP-1-102      202      leaf-202   N9K-C9396PX  leaf   10.0.128.67/32  no             yes

apic1# fabric
101  102  201  202  leaf-201  leaf-202  spine-101  spine-102
apic1# fabric 201,202 show vpc

apic1# fabric 201,202 show vrf

apic1# bash
admin@apic1:~> attach leaf-202

```

For APIC API we will need to Enable Debug Info from the TOP cornder right gear ICON. Once that is enable you will be able to see the Current MO in the little bar on the bottom.
Ex: insieme.stromboli.model.def.fvTenant[uni/tn-Costello]

Once you Enable Debug Info you can go to https://<apic1>/visore.html#/
Class or DN or URL: fvTenant    then Run Query

- To Leak routes between Tenants you use the common Tennat.
- MGMT Tenant to manage the system, APIC want's to talk to vCenter it will use MGMT VRF. 
- INFRA Tenant is where the IS-IS is running and everything for the ACI infra. You don't want to touch this.

## ACI GUI Configuration
### Logical
 - Tenant, EPG, BD, Contract, etc.
### Physical
 - Actual Wire Connection
          - Physical Domain - Bare Metal Server (VLAN-10)
          - VMM Domain - Virtualized Server (VLAN-20-30; VLAN-40-50)
          - External Bridged Domains - L2 Switch (VLAN-80-90)
          - L3 Domain - L3 Router - (VLAN-60-70)
          - SAN Switch - Fibre Channel Domains (VSAN 101)
 

1. Create VLAN Pool: Fabric > Access Policies > Pools > VLAN > Right Click Create VLAN Pool  (CostelloTN_VlanPool)
                                - Vlan Range 10-300
                                - Static Allocation 
2. Create Physical and External Domains: Fabric > Access Policies > Physical and External Domains > Physical Domains > Right Click Create Physical Domain (CostelloTN_PhyDom)
                                - Select VLAN Pool Created at Step 1 CostelloTN_VlanPool
3. Create Attachable Access Entity Profiles (AAEP): Fabric > Access Policies > Policies > Global > Attachable Access Entity Profile > Right Click Create (CostelloTN_AAEProf)
                                - Click + to add attach the Domain that we created at the Step2 CostelloTN_PhyDom
                                - For the rest we let them like that for now. Next and Finish.
4. Create Interface Policy: Fabric > Access Policies > Policies > Interface
                                - Create CDP Interface, etc
                                - In my version they were some defaults that I will use where is already enable. I don't have to configure anything at this step. ACI 6.0(3d)
5. Create Interface Policy Group: Fabric > Access Policies > Interfaces > Leaf Interfaces > Policy Groups > Here we got 3 options:
                                5.1. Leaf Access Port (Access Port) > Right Click Create
                                    5.1.1. Name (servername-iDrac_IfPolGr)
                                    5.1.2. Attach Entity Profile Created at Step 3 CostelloTN_AAEProf
                                    5.1.3. Select CDP enable, LLDP enable, Link Level Policy 10G..., Submit
                                5.2. PC Interface (Port-Channel)
                                5.3. VPC Interface (For LACP between two Leaf Switches)
6. Create Interface Profile: Fabric > Access Policies > Interfaces > Profile > Right Click Create (Leaf201_IntProf)
                                - Interface Selector > Select all interfaces 1/1-36 and description will be MDC Leaf

https://www.youtube.com/watch?v=7-gsSFeuwE8



1. Configure VPC Domain: Fabric > Access Policies > Switch Policies > Policies > VPC Domain
1. Fabric > Access Policies > Quick Start > Configure an interface, PC, and VPC
   - Select the Leaf Switches and Ports
   - Create Leaf Access Port Policy Group, Name - AccessPort-PolicyGroup
                                                - CDP Interface Policy (Default system-cdp-enabled)
                                                - Link Level Policy (Default system-link-level-10G-auto)
                                                - LLDP Interface Policy (Default system-lldp-enabled)
   - Attachable Access Entity Profile > 