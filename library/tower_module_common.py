#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


def tower_argument_spec():
    argument_spec = url_argument_spec()
    argument_spec.update(dict(
        host=dict(required=True, type='str'),
        auth_file=dict(type='path'),
        url_username=dict(aliases=['tower_user'], type='str'),
        url_password=dict(aliases=['tower_password'], type='str', no_log=True),
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
