# Prepare your brand new bare metal server in packet.net

```
yum -y install docker
service docker start
yum -y install git
mkdir ~/docker
cd ~/docker
mkdir -p ./var/log
mkdir -p ./var/tmp
mkdir ~/docker/.ssh
ssh-keygen -t rsa -b 4096 -C "dev@nuage.io" -f ~/docker/.ssh/id_rsa -q -N ""
mkdir -p ~/docker/code
cd ~/docker/code
git clone https://github.com/p1nrojas/nuage-vns-inabox ~/docker/code/nuage-vns-inabox
echo "log_path = /var/log/ansible/ansible-vsc-in-a-box.log" >> ~/docker/code/nuage-vns-inabox/ansible.cfg
chown -R 1000:1000 ~/docker
```
