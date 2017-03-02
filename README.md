##Caution! Use it under your own risk. Intended for PoCs and Labs

#Createyour SD-WAN in a box (Nuage VNS)

Hello there. Bored to create and recreate many times my lab for SD-WAN using Nuage VNS. I've created this playbook
Installing igateways, dns and ntp services, management and control planes in just one server with Centos7 KVM:
- Create a dns/ntp/dhcp instance.
- Nuage VSD ( management ) and a couple of VCSs (control).
- Util server to bootstrap your NSGs
- Stat to collect stats and apply Intelligence
- Two NSG-vs as head ends at the Datacenter
- Two independent NSG-vs as remote sites and a couple of clients behind

##Prepare your enviroment

Install docker and create an image as I show in the "Other otpion" at https://pinrojas.com/2017/02/07/ansible-docker-image-to-safely-run-my-playbooks-in-few-steps/

## Quick Start

### Step 1: Create Dummies/Bridges interfaces
Create your bridges and dummies interfaces if you plan to install this in one box. If you don't plan to use just one Box. Skip this step.
Check _bridges.yml for settings details.
_bridges.yml playbook will set your KVM server with the following:

1. Disable selinux
2. Enable forwarding
3. Disable NetworkManager and Firewall
4. Flush iptables and create NAT rules
5. Creat dummies and Bridges
6. Reboot KVM host

We'll create 5 bridges: core (as the datacenter), inet (internet), wan (as a WAN like a MPLS), branch1 and branch2.

### Step 2: Create KVM domains and install software SDN and more.

You had to be sure you will access all the servers from your ansble-host. Create routes if you need.
Check build.yml and nserver-deploy.yml vars previously to run the follow:

Now, from your container do the following

```
curl http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 > /tmp/centos7.qcow2
# Copy your vsd, nsg, util, stat  and vsc qcow2 images as follow: /tmp/vsd40r61.qcow2
# If you need those images ping me at pinrojas.com
ansible-playbook build.yml
./easy_way.sh
```

## Reverse

Use build-reset.yml to destroy your domains.

You can use either _bridges.yml (you have to uncomment _bridges-reset role and comment _bridges role into the file ) to reverse bridges and dummies; or _reset-all.yml to destroy all your KVM domains.

##Configuration

All the vars are in build.yml to create the server.
Check the vars before to proceed.

You can change things like:
1. domain (i.e. sdn40r61.lab )
2. hostnames ( the FQDN must be defined accordingly with the domain ), don't change the host part of the FQDN.
3. ip address, but no netmasks ( don't forget to check that on build.yml)
4. VSC system.ip
5. memory, vcpus and disk size where is defined. (Carefull with the minimal requirements)

Have fun!
