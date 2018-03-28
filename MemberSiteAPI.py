#!/usr/bin/env python

import http.client 
import getpass
import json
from pprint import pprint

verbose = False

class Session():

    def __init__(self):
        self.token = None

    def login(self):
        usr_email = input('Email: ')
        usr_pwd = getpass.getpass()

        data_str = '{{"email":"{}","password":"{}"}}'.format(usr_email, usr_pwd)
        data =  bytes(data_str, 'utf-8')

        headers = {"Accept": "application/json, text/plain, */*",
                "Content-Length": str(len(data)),
                "Content-Type": "application/json;charset=UTF-8"}

        conn = http.client.HTTPSConnection("blimedlem.ingenjorerutangranser.se")
        conn.request('POST', '/auth/local', body=data, headers=headers)

        resp = conn.getresponse()

        if resp.status is not 200:
            print('Could not connect! Login failed!')
            print('Server response:')
            print(resp.status, resp.reason)
        elif verbose:
            print('Login successful!')

        json_resp = json.loads(resp.read())
        self.token = json_resp['token']

    def get_all_members(self):

        self.check_token()

        headers = {"Accept": "application/json, text/plain, */*",
                   "Content-Type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer " + self.token,
                   "Cookie": 'token=%22' + self.token + '%22'}

        conn = http.client.HTTPSConnection("blimedlem.ingenjorerutangranser.se")
        conn.request('GET', '/api/members', headers=headers)

        resp = conn.getresponse()

        if resp.status is not 200:
            print('Could not get members!')
            print('Server response:')
            print(resp.status, resp.reason)
        elif verbose:
            print('Members successfully fetched!')

        return json.loads(resp.read())

    def check_token(self):
        if not self.token:
            print('No token found, please login before using API!')
            self.login()
