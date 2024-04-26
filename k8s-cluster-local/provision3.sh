#!/bin/bash
sudo su

echo "Adicionando IP static"
sudo cat <<EOT > /etc/netplan/50-vagrant.yaml
---
network:
  version: 2
  renderer: networkd
  ethernets:
    eth1:
      dhcp4: false
      addresses: [192.168.3.52/24]
      gateway4: 192.168.3.1
      nameservers:
              addresses: [192.168.3.1]
EOT

netplan apply

echo "....................."
sleep 15

echo "Validando IP static"
ip a

echo "192.168.3.50 k8s-controller-node1.cloud2solutions.net k8s-controller-node1" | sudo tee -a /etc/hosts
echo "192.168.3.51 k8s-worker-node1.cloud2solutions.net k8s-worker-node1" | sudo tee -a /etc/hosts
echo "192.168.3.52 k8s-worker-node2.cloud2solutions.net k8s-worker-node2" | sudo tee -a /etc/hosts