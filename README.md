##Caution! Use it under your own risk. Intended for PoCs and Labs

#Create a Nuage VCS in a KVM Box

Hello there. Bored to create and recreate many times a dns/ntp/dhcp and Nuage VSP ( SDN controller ) servers for my demos. I've created this playbook
It would create a libvirt VMs and set bind, ntp and dhcp up in one of the servers. And Nuage VSD ( management ) and a couple of VCSs (control).

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

### Step 2: Create KVM domains and install software SDN and more.

You had to be sure you will access all the servers from your ansble-host. Create routes if you need.
Check build.yml and nserver-deploy.yml vars previously to run the follow:

```
git clone https://github.com/p1nrojas/vcs-in-a-box
cd vsc-in-a-box
curl http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 > /tmp/centos7.qcow2
# Copy your vsd and vsc qcow2 images to /tmp/vsc40r61.qcow2 and /tmp/vsd40r61.qcow2
# If you need those images ping me at pinrojas.com
ansible-playbook build.yml
./easy_way.sh
```

## Reverse

You can use either _bridges.yml (you have to uncomment _bridges-reset role and comment _bridges role into the file ) to reverse bridges and dummies; or _reset-all.yml to destroy allyour KVM domains.

##Configuration

All the vars are in build.yml to create the server. And use nserver-deploy.yml for the services.
Check the vars before to proceed.

You can change things like:
1. domain (i.e. sdn40r61.lab )
2. hostnames ( the FQDN must be defined accordingly with the domain )
3. ip address and netmasks ( don't forget to check that on build.yml and nserver-deploy.yml )
4. Images paths
5. VSC system.ip
6. memory, vcpus and disk size where is defined.

Have fun!
