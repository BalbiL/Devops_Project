Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  
  # Configurer une IP privée
  config.vm.network "private_network", ip: "192.168.56.10"
  
  # Configurer le dossier partagé
  config.vm.synced_folder ".", "/vagrant"

  # Provisionnement avec Ansible
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "provision/playbook.yml"
  end
end
