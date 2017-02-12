#!/bin/bash
# Purpose: Run all playbooks at once
# Use with caution!
# Auhor: Mauricio Rojas / pinrojas.com

# Uncomment just in case you need to create bridges and dummy interfaces
# ansible-playbook _bridges.yml 

## Here we go!
echo "$(date) Here we go!"
# Start creating your servers
echo "$(date) Start creating your servers"
ansible-playbook -i hosts nuage-install.yml

# Configure your DNS, NTP and DHCP server
echo "$(date) checking nserver to come online..."


ssh-keygen -R 10.10.10.2

index=20
until [[ $index -lt  0 ]]
do
status=$(ssh -o BatchMode=yes -o ConnectTimeout=5 10.10.10.2 echo ok 2>&1)
if [[ $status == ok ]] || [[ $status == "Permission denied"* ]] || [[ $status == "Host key"* ]] ; then
  echo "$(date) auth ok: $status, do something"
  break
else
  echo "$(date) no access to 10.10.10.2 yet: $status. waiting a bit more..."
  let index-=1
  sleep 15
fi
done

if [[ $index -lt 0 ]] ; then
  echo "$(date) ERROR: Connection timeout to 10.10.10.2"
  exit 1
else
  ssh-keyscan -t rsa 10.10.10.2 | sed -e 's/#.*$//' | sed -e '/^$/d' >> ~/.ssh/known_hosts  # Adding nserver to known_hosts
fi 

echo "$(date) Configuring nserver"
ansible-playbook -i hosts nserver-deploy.yml

# Finish installation in  your VSD  server
ssh-keygen -R 10.10.10.10
ssh-keyscan -t rsa 10.10.10.10 | sed -e 's/#.*$//' | sed -e '/^$/d' >> ~/.ssh/known_hosts  # Adding vsd to known_hosts
echo "$(date) finishing installation of VSD"
ansible-playbook -i hosts nuage-deploy.yml 

echo "$(date) Listo! ahora juegue!" 
