# Network Service Demo 
This demo shows how model driven programmability can offer even better experience to network engineers and network developers by leveraging network service models, rather than simply targeting device models.  

> In this context, a Network Service Model considers "the network" as a single item, rather than targeting individual devices that make it up.  

The network service in this demonstration is the creation and management of a VXLAN-EVPN fabric to offer multi-tenancy across a data center network.  

## Demo Preperation 
In order to run this demo you'll need to have installed Cisco NSO on your workstation.  You can download and find installation instructions for free up on [DevNet: NSO Getting Started](https://developer.cisco.com/docs/nso/#!getting-nso).  You will need to have either Linux or MacOS platforms to install NSO.  

> Note: The creation and value of "network services" can be done leveraging multiple tools, both open source and commercial.  Cisco NSO is used in this example as an example platform for network service based configuration management.  

There are two flavors for this demonstration, `dev` and `test`.  

For `dev` the network used to deploy the service to is a simulated set of devices that leverages `netsim`, a component of NSO and will run on your workstation.  

For `test` the network used is a virtualized network using Cisco VIRL.  If you have your own VIRL server available, you can use it.  However the demo was written and tested using the [DevNet Sandbox Multi-IOS Test Network](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology) and you are encouraged to reserve a free instance of this lab if you'd like to use the `test` variation. 

### Variation `dev` 
For this variation, the spine/leaf network is simulated through netsim.  This provides a management plane into the network for sending and managing device configurations, but no data or control plane will be available.  The steps to prepare and setup are: 

1. Setup and start a netsim network on your workstation 
1. Setup a local NSO instance on your workstation  (it will automatically link to netsim)

To simplify these steps `make dev` has been provided within the `Makefile` for this demo to prepare the full dev network.  Before running `make test`, be sure to have NSO properly installed.

At the end of `make dev` you should an output similar to this indicating the test network up up in VIRL and that NSO is connected to it.  

```
Here are your netsim node status.

ncs-netsim list for  /Users/hapresto/code/mdp_use_cases/network-services/netsim

name=spine1 netconf=12022 snmp=11022 ipc=5010 cli=10022 dir=/Users/hapresto/code/mdp_use_cases/network-services/netsim/spine1/spine1
name=spine2 netconf=12023 snmp=11023 ipc=5011 cli=10023 dir=/Users/hapresto/code/mdp_use_cases/network-services/netsim/spine2/spine2
name=leaf1 netconf=12024 snmp=11024 ipc=5012 cli=10024 dir=/Users/hapresto/code/mdp_use_cases/network-services/netsim/leaf1/leaf1
name=leaf2 netconf=12025 snmp=11025 ipc=5013 cli=10025 dir=/Users/hapresto/code/mdp_use_cases/network-services/netsim/leaf2/leaf2
name=leaf3 netconf=12026 snmp=11026 ipc=5014 cli=10026 dir=/Users/hapresto/code/mdp_use_cases/network-services/netsim/leaf3/leaf3
name=leaf4 netconf=12027 snmp=11027 ipc=5015 cli=10027 dir=/Users/hapresto/code/mdp_use_cases/network-services/netsim/leaf4/leaf4



Here is the device inventory in NSO.

NAME    ADDRESS    DESCRIPTION  NED ID    ADMIN STATE
-----------------------------------------------------
leaf1   127.0.0.1  -            cisco-nx  unlocked
leaf2   127.0.0.1  -            cisco-nx  unlocked
leaf3   127.0.0.1  -            cisco-nx  unlocked
leaf4   127.0.0.1  -            cisco-nx  unlocked
spine1  127.0.0.1  -            cisco-nx  unlocked
spine2  127.0.0.1  -            cisco-nx  unlocked
```

### Variation `test` 
For this variation, the spine/leaf network will be provided through a virtual network managed in Cisco VIRL.  The steps to prepare and setup are: 

1. Setup a local NSO instance on your workstation 
1. Start the VIRL network simulation 
1. Add the VIRL network into NSO

To simplify these steps `make test` has been provided within the `Makefile` for this demo to prepare the full test network.  Before running `make test`, be sure to have NSO properly installed, and be conencted to your DevNet Sandbox reservation via VPN.  

At the end of `make test` you should an output similar to this indicating the test network up up in VIRL and that NSO is connected to it.  

```
Here are your VIRL node status.

Here is a list of all the running nodes
╒═════════╤═════════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node    │ Type        │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞═════════╪═════════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ leaf1   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.161        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ leaf2   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.162        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ leaf3   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.163        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ leaf4   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.164        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ server1 │ server      │ ACTIVE  │ REACHABLE   │ ssh        │ 172.16.30.181        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ server2 │ server      │ ACTIVE  │ REACHABLE   │ ssh        │ 172.16.30.182        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ server3 │ server      │ ACTIVE  │ REACHABLE   │ ssh        │ 172.16.30.183        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ server4 │ server      │ ACTIVE  │ REACHABLE   │ ssh        │ 172.16.30.184        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ spine1  │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.171        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ spine2  │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.172        │ N/A                │
╘═════════╧═════════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛



Here is the device inventory in NSO.

NAME    ADDRESS        DESCRIPTION  NED ID    ADMIN STATE
---------------------------------------------------------
leaf1   172.16.30.161  -            cisco-nx  unlocked
leaf2   172.16.30.162  -            cisco-nx  unlocked
leaf3   172.16.30.163  -            cisco-nx  unlocked
leaf4   172.16.30.164  -            cisco-nx  unlocked
spine1  172.16.30.171  -            cisco-nx  unlocked
spine2  172.16.30.172  -            cisco-nx  unlocked
```

## Running the Demo
> Note: the following walkthrough provides the high level steps needed to run the demo, and provides some context and background on the technologies involved, however some background in VXLAN-EVPN Data Center design, is assumed.  

### How it looks without Network Services 
If you were to configure a VXLAN-EVPN fabric and tenants without a network service, you would do so by sending device based configuration out to all the spines and leafs in the topology.  This could be done through CLI configuration or using a programmatic interface like NETCONF or NX-API.  There are two high level steps involved in this... 

> Note, in this part of the demo we'll be looking at device CLI configurations for VXLAN-EVPN, but we will **not** be actually configuring the network with them.  

#### Step 1: Configuring the Fabric

Before you could add tenants, you need to configure the basic fabric and underlay.  Take a look at the sample CLI based configurations for setting up a fabric.  These are located in the [`device-model-exmaples/device-cli-example-fabric-setup.txt`](device-model-exmaples/device-cli-example-fabric-setup.txt) file in this repo.  You will find there are about 400 total lines of configuration needed across the 6 nodes in the fabric.  Much of this configuration is feature specific and repetitive. 

#### Step 2: Adding a Tenant to the Fabric 

Once the fabric is setup and functional, now you can add Tenants and their network segments to the fabric.  Again, this could be done using CLI or device interfaces.  Take a look at [`device-model-exmaples/device-cli-example-tenant-1-setup.txt`](device-model-exmaples/device-cli-example-tenant-1-setup.txt) for a basic Tenant initialization.  This tenant inludes 2 network segments, and a few ports on one of the leafs in the fabric.  Even for this small of a Tenant, there is a lot of device based configuration that needs to be generated.  

#### Step 2a: Adding a Network Segment to an Existing Tenant 

Let's suppose you wanted to add a new segment to an existing tenant.  Checkout the configuration needed to accomplish this task by looking at [`device-model-exmaples/device-cli-example-tenant-1-segment.txt`](device-model-exmaples/device-cli-example-tenant-1-segment.txt)

### Now a better way... Network Services. 

The goal of the first part of the demo is to show the current state without network services, and how complicated and potentially error prone it can be managing the network device by device, but also keeping track of such large configurations... let's see how network services changes things.  

> Note, now comes the good part.. we'll be actually configuring the network using NSO and network services.  

#### Step 0: Making sure there isn't any fabric yet configured 

1. Connect to the Cisco NSO CLI by running the command 

    ```
    ncs_cli -C -u admin

    # Output
    admin connected from 127.0.0.1 using console on HAPRESTO-M-Q0Y6
    admin@svc_demo#
    ```

1. Look at the configuration on `spine1`. Look through the configuration and notice that there is no evpn config... even the features aren't enabled yet.  

    ```
    devices device spine1 live-status exec show running-config

    # Partial Output 
    result

    !Command: show running-config
    !Running configuration last done at: Thu Aug 15 03:50:30 2019
    !Time: Thu Aug 15 04:33:41 2019

    version 9.3(1) Bios:version
    hostname spine1
    vdc spine1 id 1
    limit-resource vlan minimum 16 maximum 4094
    limit-resource vrf minimum 2 maximum 4096
    limit-resource port-channel minimum 0 maximum 511
    limit-resource u4route-mem minimum 96 maximum 96
    limit-resource u6route-mem minimum 24 maximum 24
    limit-resource m4route-mem minimum 58 maximum 58
    limit-resource m6route-mem minimum 8 maximum 8

    feature telnet
    feature nxapi
    feature ospf
    feature bgp
    .
    .
    ```

1. Repeat for `leaf1`

    ```
    devices device leaf1 live-status exec show running-config
    ```

1. Feel free to check the other network devices... 

1. Exit out of NSO with `exit` to return to your terminal. 

#### Step 1: Configuring the Fabric 

1. Before we deploy the fabric, let's look at the model definition we'll be using.  For this install `pyang` if you don't already have it installed.  

    ```
    pip install pyang
    ```

1. The YANG models for the service are available at `packages/vxlan-evpn/src/yang/`.  Let's use `pyang` to explore the `vxlan-fabric.yang` model. 
    * Notice how the model focuses on the aspects of the fabric that are specific to the deployment.  A name, different pools, and the physical topology.  Configuration specifics for the devices are all part of the templates and code that make up the service definition.  

    ```
    pyang -f tree packages/vxlan-evpn/src/yang/vxlan-fabric.yang

    # Output 
    module: vxlan-fabric
    +--rw vxlan-fabric* [name]
        +--rw name             string
        +--rw pim-pool         inet:ipv4-prefix
        +--rw loopback-pool    inet:ipv4-prefix
        +--rw interior-pool    inet:ipv4-prefix
        +--rw ssm-range?       inet:ipv4-prefix
        +--rw group-range?     inet:ipv4-prefix
        +--rw as-number?       uint16
        +--rw spines* [device]
        |  +--rw device         -> /ncs:devices/device/name
        |  +--rw connections* [leaf]
        |     +--rw leaf         -> ../../../leaves/device
        |     +--rw interface?   string
        +--rw leaves* [device]
            +--rw device         -> /ncs:devices/device/name
            +--rw connections* [spine]
            +--rw spine        -> ../../../spines/device
            +--rw interface?   string
    ```

1. Now let's use the model to configure the fabric.  
1. Jump back into NSO and enter config mode. 

    ```
    ncs_cli -C -u admin
    config 
    ```

1. Enter this configuration to setup the fabric.  

    ```
    vxlan-fabric fabric1
    pim-pool      100.2.1.0/24
    loopback-pool 10.2.1.0/24
    interior-pool 172.16.0.0/16

    spines spine1
    connections leaf1 interface 1/1
    connections leaf2 interface 1/2
    connections leaf3 interface 1/3
    connections leaf4 interface 1/4

    spines spine2
    connections leaf1 interface 1/1
    connections leaf2 interface 1/2
    connections leaf3 interface 1/3
    connections leaf4 interface 1/4

    leaves leaf1 
    connections spine1 interface 1/1
    connections spine2 interface 1/2

    leaves leaf2
    connections spine1 interface 1/1
    connections spine2 interface 1/2

    leaves leaf3 
    connections spine1 interface 1/1
    connections spine2 interface 1/2

    leaves leaf4 
    connections spine1 interface 1/1
    connections spine2 interface 1/2
    ```

1. Now `commit` the configuration to apply this service to the network and exit out of configuration mode.  

    ```
    commit
    end 
    ```

1. Now look at the configuration on `spine1` and `leaf1` again.  You should now see the fabric configuration has been pushed out.  
    > Note: It may take up to 2 minutes for the configurations to be fully pushed out to the devices.  

    ```
    devices device spine1 live-status exec show running-config
    devices device leaf1 live-status exec show running-config
    ```

1. Network Services can also include actions, such as verifications.  Let's use the `verify` action to see if the fabric is healthy.  
    * **NOTE: If you are running with `dev` and netsim, the output from `verify` will show `NOT READY` because netsim doesn't actually build a control plane for OSPF/BGP.**

    ```
    vxlan-fabric fabric1 verify 

    # Output 
    result Spine spine1, OSPF status: 4/4, BGP STATUS: 4/4 - READY
    Spine spine2, OSPF status: 4/4, BGP STATUS: 4/4 - READY
    Leaf leaf1, OSPF status: 2/2, BGP STATUS: 2/2 - READY
    Leaf leaf2, OSPF status: 2/2, BGP STATUS: 2/2 - READY
    Leaf leaf3, OSPF status: 2/2, BGP STATUS: 2/2 - READY
    Leaf leaf4, OSPF status: 2/2, BGP STATUS: 2/2 - READY
    SUMMMARY: BGP AND OSPF OK

    ready true
    ```

1. Exit out of nso with `exit`. 

#### Step 2: Adding a Tenant to the Fabric 
Setting up the fabric was super easy... let's checkout the tenant.  

1. Like with the fabric, let's start by looking at the yang model for the tenant.  Notice how the `fabric` leaf is a reference to the `fabric` service, and similar with the `leaf` under `connections`.

    ```
    pyang -f tree packages/vxlan-evpn/src/yang/vxlan-tenant.yang

    # Output
    module: vxlan-tenant
    +--rw vxlan-tenant* [name]
        +--rw name        string
        +--rw fabric      -> /vxlan-fabric:vxlan-fabric/name
        +--rw segments* [name]
            +--rw name            string
            +--ro vni-id?         uint32
            +--ro vlan-id?        uint32
            +--rw network         inet:ipv4-prefix
            +--rw suppress-arp?   boolean
            +--rw connection* [leaf iface]
            +--rw leaf     -> /vxlan-fabric:vxlan-fabric[vxlan-fabric:name=current()/../../../fabric]/leaves/device
            +--rw iface    string
            +--rw mode?    enumeration
    ```

1. Let's setup that simple `Tenant-1`.  

    ```
    # Log into NSO again and jump into config mode
    ncs_cli -C -u admin
    config 

    # Send the tenant configuration 
    vxlan-tenant Tenant-1
    fabric fabric1

    segments Seg1
    network      10.0.11.0/24
    suppress-arp false
    connection leaf1 1/3
    connection leaf1 1/4

    segments Seg2
    network      10.0.12.0/24
    suppress-arp false
    connection leaf1 1/3

    # Commit the change and exit from config mode 
    commit 
    end
    ```

1. Now look at the configuration on `leaf1` again.  You should now see the tenant specific configuration
    > Note: As this tenant only has connections on leaf1, only that leaf will be configured.  
    > Note: It may take up to 2 minutes for the configurations to be fully pushed out to the devices.  

    ```
    devices device leaf1 live-status exec show running-config
    ```

#### Step 2a: Adding a Network Segment to an Existing Tenant 
With Tenant-1 configured in the network, it's easy to add a third segment to it.  

1. Jump back into config mode. 

    ```
    config
    ```

1. Add `Seg3` to the existing tenant.  

    ```
    vxlan-tenant Tenant-1

    segments Seg3
    network      10.0.13.0/24
    suppress-arp false
    connection leaf1 1/4
    ```

1. Finish by committing it to the system.  

    ```
    commit
    ```

#### Bonus 1: A More Complicated Tenant 
Tenant-1 was pretty simple.. it only existed on 1 leaf, and had very basic connections.  Here's a configuration for a more complex tenant.  This one is on all the leafs, and has both trunk and and access style connections. 

```
vxlan-tenant Demo-Tenant
fabric fabric1

segments production01
network      10.0.1.0/24
suppress-arp false
connection leaf1 1/11
connection leaf2 1/11
connection leaf3 1/11
connection leaf4 1/11
connection leaf1 1/12 mode access
connection leaf2 1/12 mode access

segments production02
network      10.0.2.0/24
suppress-arp false
connection leaf1 1/11
connection leaf2 1/11
connection leaf3 1/11
connection leaf4 1/11
connection leaf3 1/12 mode access
connection leaf4 1/12 mode access

segments production03
network      10.0.3.0/24
suppress-arp false
connection leaf1 1/11
connection leaf2 1/11
connection leaf3 1/11
connection leaf4 1/11
connection leaf1 1/13 mode access
connection leaf2 1/13 mode access
connection leaf3 1/13 mode access
connection leaf4 1/13 mode access
```

#### Bonus 2: What about when a Tenant Goes Away... 
If configuring new things in the network is complicated... un-configuring things is a step above in complications.  It's hard to track what parts of the configuration relate to some specific feature... this results in the removal of configuration somethign that is often avoided, or not done at all... stranding bits of configuration all over the network.  Network Services package up and track the changes related to an instance of a service, so removing the configuration is super simply.  Let's see it in action!  

1. If you arne't, jump into NSO cli and config mode.  
1. Remove the configuration for `Tenant-1`. *Don't commit it yet.*  

    ```
    no vxlan-tenant Tenant-1
    ```

1. Let's see what will be removed by doing a dry-run of the commit.  We include `outformat native` to see the raw CLI configuration being sent to the device. 

    ```
    commit dry-run outformat native

    # Output 
    native {
        device {
            name leaf1
            data router bgp 65001
                no vrf Tenant-1
                !
                no vlan 10-13
                evpn
                no vni 10001 l2
                no vni 10002 l2
                no vni 10003 l2
                !
                no interface Vlan10
                no interface Vlan11
                no interface Vlan12
                no interface Vlan13
                vrf context Tenant-1
                address-family ipv4 unicast
                no route-target both auto evpn
                exit
                no address-family ipv4 unicast
                no vni 10000
                no rd  auto
                exit
                no vrf context Tenant-1
                interface nve1
                no member vni 10000 associate-vrf
                no member vni 10001
                no member vni 10002
                no member vni 10003
                !
                interface Ethernet1/3
                switchport trunk allowed vlan remove 11-12
                no switchport trunk allowed vlan
                no switchport mode
                exit
                interface Ethernet1/4
                switchport trunk allowed vlan remove 11,13
                no switchport trunk allowed vlan
                no switchport mode
                exit
        }
    }
    ```

1. Now we can run the actual `commit` to remove the configuration from the network, freeing up the interfaces and resource to be used again.  

    ```
    commit
    ```

## Cleaning Up the Demo 
When you are done with the demo, you can run `make clean` to destroy the VIRL and/or netsim networks, as well as clear out the local NSO installation we've been using.  

```
make clean
```

> Note: you might see some errors from the `make clean` command related to attempts to tear down the network for which ever instance you did **not** use.  They can be ignored.  
