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

```

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
7. Create Switch Policy Group: Fabric > Access Policies > Switches > Leaf Switches > Policy Group > Right Click Create (CostelloTN_SW_PGr) I don't see this created in Prod.
8. Create Switch Profile: Fabric > Access Policies > Switches > Leaf Switches > Profile > Right Click Create (Leaf101_Pro)
                                - Leaf Selector > Name: 101 > Blocks: 101 > Policy Group: CostelloTN_SW_PGr (We created this at step 7)
                                - Step 2 > Associations > Leaf201_IntProf (Created at Step 6)
9. 


```

```
1. Create VLAN Pool: Fabric > Access Policies > Pools > VLAN > Right Click Create VLAN Pool  (CostelloTN_VlanPool)
                                - Allocation Mode: Static Allocation
                                - Click + Encap Blocks to add the VLAN Range    
                                            - Ex: Vlan Range 10-300
                                            - Static Allocation
2. Create Physical and External Domains: Fabric > Access Policies > Physical and External Domains > Physical Domains > Right Click Create Physical Domain (CostelloTN_PhyDom)
                                - Select VLAN Pool Created at Step 1 CostelloTN_VlanPool
3. Create Attachable Access Entity Profiles (AAEP): Fabric > Access Policies > Policies > Global > Attachable Access Entity Profile > Right Click Create (CostelloTN_AAEProf)
                                - Click + to add attach the Domain that we created at the Step2 CostelloTN_PhyDom
                                - For the rest we let them like that for now. Next and Finish.
4. Create Interface Policy: Fabric > Access Policies > Policies > Interface 
                                - Create CDP Interface, etc
                                - In my version they were some defaults that I will use where is already enable. I don't have to configure anything at this step. ACI 6.0(3d)
5. Create Interface Profile: Fabric > Access Policies > Interfaces > Leaf Interfaces > Profile > Right Click Create (Leaf101_IntProf), then Submit without adding Interface Selectors.
                                - Now we create Leaf Interface Profiles, objects that will be created only once and will represent the Interfaces of each Leaf. Later when you would need a new port configured on ACI, you will just add Interface Selector inside one of the Leafs Interface Profiles.
6. Create Access Interface Policy Group: Fabric > Access Policies > Interfaces > Leaf Interfaces > Policy Groups > Here we got 3 options:
                                5.1. Leaf Access Port (Access Port) > Right Click Create
                                    5.1.1. Name (servername-iDrac_IfPolGr), Description - Server port description usually.
                                    5.1.2. Attach Entity Profile Created at Step 3 CostelloTN_AAEProf
                                    5.1.3. Select CDP enable, LLDP enable, Link Level Policy 10G..., Submit
                                5.2. PC Interface (Port-Channel)
                                5.3. VPC Interface (For LACP between two Leaf Switches)
                                - Policy Group will be configured once for each type of single port configuration and once for each vPC configuration, because vPC config needs its own ID so it cannot be reused. Note that the most important think that you need to configure is the AAEP in the end because without it all other config done here will simply not be pushed to the Leaf. Most important is CDP-Enable, LLDP-Enable, 10G or 1Ginterface...
7. Create VPC Domain: This can be created once you create your ACI fabric or after. When you configuring vPC interface teaming you first need to have vPC domain configured which is done for each two pair of vPC Leafs: Fabric > Access Policies > Policies > Switch > Virtual Port Channel Default.
8. Create VPC Interface with LACP Policy Group: Fabric > Access Policies > Interfaces > Leaf Interfaces > Policy Groups > VPC Interface 
                                8.1 VPC Interface Right Click Create, Name (servername-db_vPC)
                                8.2 Description each server port.
                                8.3 Attached Entity Profile. Attach the AAEP created at step 3.
                                8.4 CDP-Enable, LACP-Enable, Link-10G
                                8.5 Port Channel Policy - system-lacp-active
9. Create Leaf Switch Profile: Now we are ready to create Switch Selector, objects that will be created only once and which will represent Leafs and will be a placeholder for Leaf Interface configuration. I created one of them for each of the first Leafs and one for first vPC Leaf pair. Added into them Leaf ID and Interface Selector Profile created above.
                                9.1 Fabric > Access Policies > Switches > Leaf Switches > Profiles > Right Click Create
                                9.2 Name: Leaf101_Prof
                                9.3 Leaf Selector +: Leaf Name Leaf101; Blocks 101; Policy group Empty.
                                9.4 Associations: Interface Selector Profiles > Leaf101_IntProf created at step 5.
10. Configure our first Leaf Trunk Interface: Now we are all set to configure our first Leaf port as a 10G optical port with CDP on and LLDP on. We just enter the Leaf Interface profile of Leaf-101 and add the port 1 configuration with 1/1 selector and 10G access port Interface Policy Group. After that, the port will become active as soon we map the first EPG to it.
                                10.1 Fabric > Access Policies > Interfaces > Leaf Interfaces > Profiles > Leaf101_IntProf that was already created at step 5.
                                10.2 Interface Selector + : Create Access Port Selector; Name Port1; Interface ID's 1/1
                                                    - Interface Policy Group servername-iDrac_IfPolGr created at step 6.
                                                    - In order to get the configuration pushed from APIC to the port, we still have a lot to do. We need to create ACI Application Policy which will define the port to EPG Membership and define the VLANs that are allowed to cross that trunk port.



```


https://www.youtube.com/watch?v=7-gsSFeuwE8



1. Configure VPC Domain: Fabric > Access Policies > Switch Policies > Policies > VPC Domain
1. Fabric > Access Policies > Quick Start > Configure an interface, PC, and VPC
   - Select the Leaf Switches and Ports
   - Create Leaf Access Port Policy Group, Name - AccessPort-PolicyGroup
                                                - CDP Interface Policy (Default system-cdp-enabled)
                                                - Link Level Policy (Default system-link-level-10G-auto)
                                                - LLDP Interface Policy (Default system-lldp-enabled)
   - Attachable Access Entity Profile > 