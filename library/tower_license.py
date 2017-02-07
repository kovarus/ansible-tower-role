#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import json
import tower_module_common as tower


def main():

    argument_spec = tower.tower_argument_spec()
    argument_spec.update(dict(
        license=dict(required=True, type='path')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    authtoken = tower.get_authtoken(module)

    user_license = get_license_file(license_file_path)

    tower_license = get_license(module, authtoken)

    if not tower_license:
        upload = 1
    else:
        upload = compare_license(user_license, tower_license)

    if upload:
        upload_status = upload_license(module, user_license, token)
        if upload_status != 200:
            module.fail_json(msg='license upload failed!')
        else:
            module.exit_json(changed=True)

    module.exit_json(changed=False)


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


if __name__ == '__main__':
    main()
