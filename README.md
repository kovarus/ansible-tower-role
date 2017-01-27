tower
=========

This role installs Ansible Tower.

Requirements
------------

A license file is needed prior to using and the license path is passed as a variable.

For the test.yml file to be used, a license.json file needs to be placed in the tests directory.

Role Variables
--------------
`license_file_path`
- default: blank
- description: This is a mandatory variable that specifies the path to the license file to be uploaded to Tower after installation.

`tower_version`
- default: 3.0.3
- description: This specifies the version of tower to be installed.

`admin_password`
- default: "password"
- description: This specifies the administrator password for Tower

`redis_password`
- default: "password"
- description: This specifies the password for the Redis cache

`postgres_password`
- default: "password"
- description: This specifies the password for the PostgreSQL database

`install_cli`
- default: True
- description: This specifies whether or not to install and configure the ansible-tower-cli pip package.

Dependencies
------------

None

Example Playbook
----------------

```json
---
- name: tower
  hosts: localhost
  roles:
    - role: tower
      license_file_path: license.json
```
License
-------

MIT

Author Information
------------------

Taylor Owen (towen@kovarus.com)

