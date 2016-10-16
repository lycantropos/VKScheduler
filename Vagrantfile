# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "scheduler" do |scheduler|

    scheduler.vm.guest = :windows
    scheduler.vm.box = "designerror/windows-7"

    scheduler.vm.network "forwarded_port", guest: 32000, host: 32000

    scheduler.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "2048"]
      vb.customize ["modifyvm", :id, "--cpus", "1"]
      vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
      vb.customize ["modifyvm", :id, "--audio", "none"]
    end
  end
end
