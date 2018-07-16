#Vagrant Multi-Machine Environment
This is a vagrant configuration for having multi-machine, multi-node vagrant environment, which also creates the local user and sets the authorized key.

##Usage
To use multi-machine environment, there is no need to configure the Vagrantfile, all you have to do is add required machines to the **machine-config.yml**. Here is a snippet from the yaml file, in case if you need a new machine you just need to add a new item in the yaml file. If you like to have more than one machine you can set the nodes variable, as you can see in the example of riak configuration.

```
---
  - name: "vagrant"
    url:  "http://files.vagrantup.com/precise64.box"
    ip:    192.168.50.150


  - name: "postgresql"
    url:  "http://files.vagrantup.com/precise64.box"
    ip:    192.168.60.150

  - name: "riak"
    url:  "http://files.vagrantup.com/precise64.box"
    ip:    192.168.70.150
    nodes: 3
    memory: 1024
    cpu: 2 

```


##Provisioning & Controlling Machines
If you would like to provision all the machines in the **machine-config.yml**:

```
vagrant up
```

If you would like to provision only certain hosts, you can use regular expression, and vagrant will launch any host that is matching. The following command will launch all vagrant instances. 

```
vagrant up '/vagrant[1-9]/'
```

If you would like to provision only certain node:

```
vagrant up vagrant1
```

Same procedures applies for halting and destroying

```
vagrant halt '/vagrant[1-9]/'
vagrant destroy '/vagrant[1-9]/'
```


#License
MIT License.
