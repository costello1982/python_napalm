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

Test