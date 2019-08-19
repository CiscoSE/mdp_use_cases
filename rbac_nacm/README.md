# Network Configuration Access Control Demo

This demo shows how model driven programmability can be extended outside of service turn up. There are significant benefits to leveraging model driven programmability into traditional help desk/operational work flows provided there is a method for providing Role Based Access Control (RBAC). 

RFC 6536 provides a frame work for providing RBAC by restricting access to specific NETCONF actions (get, get-config, edit-config, etc.), data stores (running, candidate, etc.) or specific YANG modules. Buy default only users with PRIV15 are granted access to interact with the device through NETCONF/YANG. 

In this demo we will simulate a typical help desk function where a junior operations engineer has access to retrieve configuration and operational details from a device for troubleshooting but they must escalate to a senior engineer to provide the 'fix'.

## Demo Prepration

The network topology for this demo was built using Cisco VIRL a network simulation platform. If you do not have your own VIRL server available you the demo was written and tested using [DevNet Sandbox Multi-IOS Test Network](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology) and you are encouraged to reserve a free instance of this lab. 

Before starting the lab update the ```srv_env.template``` file with the IP address, username and password used to access your instance of VIRL and source the file. Once complete start the VIRL instance with ```virl up```

There is a python script in the code directory that is used to generate pseudo network traffic. Before starting the demo run the ```0_nacm_traffic.py``` script in a background terminal. The username and password is ```cisco/cisco```.

## Running the Demo

### The Scenario ###

A user has opened up a ticket stating that they are unable to access a resource at 172.16.11.1. The ticket was routed a new help desk engineer and they are tasked with triaging the issue. Once they identify the problem they need to escalate the issue to a senior engineer to apply the appropriate configuration change. 

## Step 1 - Implementing Role Based Access Control in a Model Driven World

As stated previously, by default, only users authorized at privilege level 15 are able to interact with NETCONF/YANG. A users privilege level can be assigned statically through a locally defined user account or it can be returned as part of a TACACS authentication. For the purpose of our demo there are two users

**Bryan** - a junior help desk engineer who only has read access to 
network devices

```
username - bryan
password - cisco
```

**Hank** - a senior escalation contact who has full read/write access to the network

```
username - hank
password - cisco
```

In order to implement our NACM policy we will use a crafted NETCONF payload to configure the access restrictions. After running the code our policy will look like this:

- Junior engineers will be assigned PRIV02 access.
	- Deny edit operation
	- Allow get operation
	- Full access to all YANG modules
- Senior engineers will be assigned PRIV15 access
	- Allow edit operation
	- Allow get operation
	- Full access to all YANG modules.

Let's run the code and define our policy for PRIV02 users. 

```
python 1_nacm_policy.py
```

Supply the IP address for the device core1 and the username password combination for our senior engineer (hank/cisco) and then re run the code for the device core2.

Now that we have our policy in place let's walk through a model driven troubleshooting.

### The Scenario ###

A user has opened up a ticket stating that they are unable to access a resource at 172.16.11.1. The ticket was routed a new help desk engineer and they are tasked with triaging the issue. Once they identify the problem they need to escalate the issue to a senior engineer to apply the appropriate configuration change.

## Step 2 - Verifying the Configuration

In this step we will use a pre-defined script to retrieve the ACL configuration of a device in path. While we are focusing on retrieving details for what amounts to a single show command the power of using model driven programmability in a "real" environment is having this part of a larger script designed to retrieve details for multiple functions on a platform.

With that let's run our script using the account details of our PRIV02 level user ```bryan/cisco```

```
python 2_nacm_get_acl.py
```

The Output:

```
Access-List Name: IMPACT
 For ACE: 100
  Protocol: ospf
   Action: permit

 For ACE: 200
  Protocol: ip
   Destination Network: 172.16.0.0
   Destination Wildcard Mask: 0.0.255.255
   Action: deny

 For ACE: 300
  Protocol: ip
   Destination Network: 10.255.255.0
   Destination Wildcard Mask: 0.0.0.255
   Action: permit

 For ACE: 1000
  Protocol: ip
   Action: deny

```

The script returns a short summary of the currently configured access-list. Our operator can now quickly scan through the list and see that ACE number 30 is likely denying our user from getting access to the host 172.16.11.

Feel free to investigate the code to see how the NETCONF filter was defined.

## Step 3 - Real Time Monitoring with Model Driven Programmability

Before escalating our ticket up to the Senior engineer our help desk engineer would like to check for incrementing hits on the ACE counter for sequence number 200. We are now moving away from an all purpose script to requiring something custom to retrieve details on what is may be a device specific configuration. In this case we will leverage a python script using a Jinja template that prompts the operator to provide inputs on specifically what details they need.

Before we run our code let's look at the code specifically the portion for that reads in the Jinja Template

```
cat 3_nacm_get_seq.py
```

Of note:

```
# Read in Jinja template
with open("nacm_get_seq.j2") as f:
    template_in = Template(f.read())

# Render Jinja template with variables
filter = template_in.render(acl_name=device["acl"], ace_number=device["seq"])
```

And now let's look at what's included in that template:

```
<filter>
  <access-lists xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl-oper">
    <access-list>
      <access-control-list-name>{{ acl_name }}</access-control-list-name>
      <access-list-entries>
        <access-list-entry>
          <rule-name>{{ ace_number }}</rule-name>
        </access-list-entry>
      </access-list-entries>
    </access-list>
  </access-lists>
</filter>
```

As we can see from the template our operator will need to provide the ACL name and the specific SEQ number that they want to monitor. Let's run the code and see what happens.


```
python 3_nacm_get_seq.py
```

If we let our script run we should see incrementing hits on our ACL sequence number 200. With that piece of information our junior ops engineer is confident that the access-list needs to be updated.

## Step 4 - Updating the Access List

Our junior help desk engineer is very happy he's identified the issue on the network and like any good engineer he doesn't want to hand off the issue to a peer. He wants to see this issue through to resolution. He knows that all the provisioning scripts are available in a git repository so he's determined to push the fix out.

For our configuration script the change details are stored in a YAML file. Our help desk engineer updated the YAML and he's ready to deploy the change. Let's take a look at what the change will look like:

```
---

- acl:
  name: IMPACT
  aces:
    - seq: 125
      action: permit
      protocol: ip
      src_prefix: any
      src_wildcard:
      dst_prefix: 172.16.11.1
      dst_wildcard: 0.0.0.255
```

Feeling fairly confident in his change let's go a head and run the code:


```
python 4_nacm_edit_acl.py
```

The change is denied by the network device as our PRIV02 level help desk user does not have the appropriate level of access. The code should return:

```
There was an error (access-denied) with your transaction.
```

Our help desk engineer now escalates the ticket to a senior engineer. The senior engineer can now run the change that Bryan queued up:

```
python 4_nacm_edit_acl.py
Device IP Address?
172.16.30.198
Operator Username?
hank 
Operator Password?

NETCONF RPC OK: True
```

As any good senior engineer should do Hank runs through some verification scripts to ensure his change had the desired effect.

```
(venv) $ python 2_nacm_get_acl.py 
Device IP Address?
172.16.30.198
Operator Username?
hank
Operator Password?

Access-List Name: IMPACT
 For ACE: 100
  Protocol: ospf
   Action: permit

 For ACE: 125
  Protocol: ip
   Destination Network: 172.16.11.1
   Destination Wildcard Mask: 0.0.0.255
   Action: permit

 For ACE: 200
  Protocol: ip
   Destination Network: 172.16.0.0
   Destination Wildcard Mask: 0.0.255.255
   Action: deny

 For ACE: 300
  Protocol: ip
   Destination Network: 10.255.255.0
   Destination Wildcard Mask: 0.0.0.255
   Action: permit

 For ACE: 1000
  Protocol: ip
   Action: deny

(venv) $ python 3_nacm_get_seq.py 
Device IP Address?
172.16.30.198
ACL Name?
IMPACT
ACE SEQ Number?
125
Operator Username?
hank
Operator Password?

 For SEQ number: 125 the number of ACE matches is: 34
 For SEQ number: 125 the number of ACE matches is: 34
 For SEQ number: 125 the number of ACE matches is: 39
 For SEQ number: 125 the number of ACE matches is: 44
 For SEQ number: 125 the number of ACE matches is: 49
```

### Cleaning UP the Demo

When you are done with the demo you can issue a ```virl down``` to stop the simulation.