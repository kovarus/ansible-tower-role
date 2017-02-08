#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


def tower_argument_spec():
    argument_spec = url_argument_spec()
    argument_spec.update(dict(
        host=dict(required=True, type='str'),
        url_username=dict(aliases=['tower_user'], type='str'),
        url_password=dict(aliases=['tower_password'], type='str', no_log=True),
        license=dict(type='path')
    ))

    return argument_spec


def get_authtoken(module):
    host = module.params['host']
    user = module.params['url_username']
    password = module.params['url_password']

    headers = {}
    headers['Content-Type'] = 'application/json'

    data = {}
    data['username'] = user
    data['password'] = password
    json_data = json.dumps(data)

    url = "https://{0}/api/v1/authtoken/".format(host)

    resp, info = fetch_url(module, url, method='POST', data=json_data,
                           headers=headers)
    content = json.loads(resp.read())

    return content['token']


def upload_license(module, ul, token):
    host = module.params['host']
    url = "https://{0}/api/v1/config/".format(host)

    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = "Token {0}".format(token)

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


def get_license(module, token):
    host = module.params['host']
    url = "https://{0}/api/v1/config/".format(host)

    headers = {}
    headers['Authorization'] = "Token {0}".format(token)

    resp, info = fetch_url(module, url, headers=headers)
    content = json.loads(resp.read())

    return content['license_info']


def tower_license(module, token):
    license_path = module.params['license']
    user_license = get_license_file(license_path)

    tower_license = get_license(module, token)

    if not tower_license:
        upload = 1
    else:
        upload = compare_license(user_license, tower_license)

    if upload:
        upload_status = upload_license(module, user_license, token)
        if upload_status != 200:
            return 'license upload failed', 'failed'
        else:
            return 'license upload succeeded', 'changed'

    return 'no license change', 'unchanged'


def main():

    argument_spec = tower_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    authtoken = get_authtoken(module)

    output = {}

    if module.params['license']:
        license_msg, license_status = tower_license(module, authtoken)
        output['tower_license'] = {}
        output['tower_license']['msg'] = license_msg
        output['tower_license']['status'] = license_status

    failed = {}
    changed = {}

    for element in output:
        if output[element]['status'] == 'failed':
            failed[element] = output[element]['msg']

    for element in output:
        if output[element]['status'] == 'changed':
            changed[element] = output[element]['msg']

    if failed:
        module.fail_json(msg=failed)

    if changed:
        module.exit_json(changed=True, msg=changed)

    module.exit_json(changed=False)


if __name__ == '__main__':
    main()
