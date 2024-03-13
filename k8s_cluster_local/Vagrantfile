Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"

  config.vm.define "k8s-controller-node1" do |master|
    master.vm.hostname = "k8s-controller-node1.cloud2solutions.net"
    master.vm.network "public_network"
    master.vm.provision "shell", path: "provision1.sh"
    master.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 2048]
      v.customize ["modifyvm", :id, "--name", "k8s-controller-node1"]
      v.customize ["modifyvm", :id, "--cpus", 2]   
    end
  end

  config.vm.define "k8s-worker-node1" do |worker1|
    worker1.vm.hostname = "k8s-worker-node1.cloud2solutions.net"
    worker1.vm.network "public_network"
    worker1.vm.provision "shell", path: "provision2.sh"
    worker1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 1024]
      v.customize ["modifyvm", :id, "--name", "k8s-worker-node1"]
      v.customize ["modifyvm", :id, "--cpus", 1] 
    end
  end

  config.vm.define "k8s-worker-node2" do |worker2|
    worker2.vm.hostname = "k8s-worker-node2.cloud2solutions.net"
    worker2.vm.network "public_network"
    worker2.vm.provision "shell", path: "provision3.sh"
    worker2.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 1024]
      v.customize ["modifyvm", :id, "--name", "k8s-worker-node2"]
      v.customize ["modifyvm", :id, "--cpus", 1] 
    end
  end
end