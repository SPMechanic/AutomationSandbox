Latest LEMP Stack Installation on Ubuntu Server using Ansible
--------

[LEMP Installation Tutorial] - This step by step tutorial explains the installation and configuration of LEMP Stack on Ubuntu 14.04 server.

### To use this Role:

Edit the `site.yml` file, mentioned this role:

```yaml
---
- hosts: server
  become: yes
  gather_facts: yes
  roles:
    - LEMP
``` 
After that edit the `defaults/main.yml` file:

> Change the `mysql_port` & `mysql_bind_address` if you are using non-standard/modified setting. 
>
> Edit the `mysql_root_pass` for MySQL root password.
>
> Give the maximum nginx connections and server_name as well (default is 1024 connections and localhost as server_name)

After Editing the file, it will look like this:
```yaml
---
 mysql_port: 3306 #Default is 3306, please change it if you are using non-standard
 mysql_bind_address: "127.0.0.1" #Change it to "0.0.0.0",if you want to listen everywhere
 mysql_root_pass: mypassword #MySQL Root Password
 connections: 1024 #Nginx Connection
 server_name: localhost #Nginx server_name, change it to your website e.g: rbgeek.com
```

Then run this command:

```
ansible-playbook -i hosts -u <server username/login> site.yml
```

[LEMP Installation Tutorial]:https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-14-04
