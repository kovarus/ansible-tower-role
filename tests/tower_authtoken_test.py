#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import json
import tower_module_common as tower


def main():

    argument_spec = tower.tower_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    authtoken = tower.get_authtoken(module)

    module.exit_json(changed=True, authtoken=authtoken)


if __name__ == '__main__':
    main()
