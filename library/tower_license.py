#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


def main():
    argument_spec = url_argument_spec()
    argument_spec.update(dict(
        host=dict(required=True, type='str'),
        auth_file=dict(type='path'),
        url_username=dict(aliases=['tower_user'], type='str'),
        url_password=dict(aliases=['tower_password'], type='str', no_log=True),
        license=dict(required=True, type='path')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    host = module.params['host']
    license_file_path = module.params['license']
    tower_config_url = "https://{0}/api/v1/config/".format(host)

    user_license = get_license_file(license_file_path)

    tower_config = get_config(module, tower_config_url)
    tower_license = tower_config['license_info']

    if not tower_license:
        upload = 1
    else:
        upload = compare_license(user_license, tower_license)

    if upload:
        upload_status = upload_license(module, user_license, tower_config_url)
        if upload_status != 200:
            module.fail_json(msg='license upload failed!')
        else:
            module.exit_json(changed=True)

    module.exit_json(changed=False)


def upload_license(module, ul, url):
    headers = {}
    headers['Content-Type'] = 'application/json'
    ul_json = json.dumps(ul)
    resp, info = fetch_url(module, url, data=ul_json, headers=headers,
                           method='POST')
    output = resp.read()

    return info['status']


def compare_license(ul, tl):
    compare_list = ['company_name', 'contact_email', 'contact_name',
                    'hostname', 'instance_count', 'license_date',
                    'license_key', 'license_type', 'subscription_name',
                    'trial']

    for param in compare_list:
        if ul[param] != tl[param]:
            return 1
            break

    return 0


def get_license_file(path):

    with open(path) as license_data:
        d = json.load(license_data)
        return d


def get_config(module, url):

    resp, info = fetch_url(module, url)
    content = json.loads(resp.read())

    return content


if __name__ == '__main__':
    main()
