# vi:ft=ruby:

Vagrant.configure("2") do |config|
    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "precise32"

    # cache packages installed on provisioned VMs
    # https://github.com/fgrehm/vagrant-cachier
    config.cache.auto_detect = true
    config.cache.scope = :machine
    config.cache.enable :apt
    # probably not too helpful to cache ruby gems, but why not
    config.cache.enable :gem
    # no pip cache support... yet
    # https://github.com/fgrehm/vagrant-cachier/issues/18

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    config.vm.network :private_network, ip: "192.168.50.4"

    ## For masterless, mount your file roots file root
    config.vm.synced_folder "salt/roots/", "/srv/"

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8089" will access port 80 on the guest machine.
    config.vm.network :forwarded_port, guest: 80, host: 8089

    ## Set your salt configs here
    # https://github.com/saltstack/salty-vagrant
    config.vm.provision :salt do |salt|
        ## Minion config is set to ``file_client: local`` for masterless
        salt.minion_config = "salt/minion"

        ## Installs our example formula in "salt/roots/salt"
        salt.run_highstate = true
    end
end
# salt-call --local state.highstate -l debug
# http://www.barrymorrison.com/2013/Mar/11/deploying-django-with-salt-stack/
# https://github.com/brutasse/states
# https://github.com/illumin-us-r3v0lution/django-saltstack/blob/master/salt/postgresql/init.sls
# https://github.com/uggedal/states
# https://github.com/kwo/salt-states

