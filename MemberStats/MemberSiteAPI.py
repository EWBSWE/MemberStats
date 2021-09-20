#!/usr/bin/env python3

import os
import http.client 
import getpass
import json
from pprint import pprint
from datetime import datetime


EWB_MEMBER_BASE_URL = 'member.ewb-swe.org'

class EWBServerException(Exception):
    
    def __init__(self, message):
        self.message = message



# Creates a session with the server. The session is then used to communicate with the server.
class Session():

    def __init__(self, save_token_to_file=True, verbose=False):
        self.token = None

        self.save_token_to_file = save_token_to_file
        self.verbose = verbose


    def manual_login(self):
        usr_email = input('Email: ')
        usr_pwd = getpass.getpass()

        cred_json = '{{"email":"{}","password":"{}"}}'.format(usr_email, usr_pwd)
        self.login_with_credentials(cred_json)


    def login_with_credentials(self, cred_json):
        data =  bytes(cred_json, 'utf-8')

        headers = {"Accept": "application/json, text/plain, */*",
                "Content-Length": str(len(data)),
                "Content-Type": "application/json;charset=UTF-8"}

        conn = http.client.HTTPSConnection(EWB_MEMBER_BASE_URL)
        conn.request('POST', '/auth/local', body=data, headers=headers)

        resp = conn.getresponse()

        if resp.status != 200:
            print('Could not connect! Login failed!')
            print('Server response:')
            print(resp.status, resp.reason)
            raise EWBServerException(f"ERROR: Server responded with status code '{resp.status}' and reason'{resp.reason}'")
        elif self.verbose:
            print('Login successful!')
        
        json_resp = json.loads(resp.read())
        self.token = json_resp['token']

        if self.verbose:
            print("Received token: %s" % (self.token))

        # Save token to file so we don't have to login every single time
        if self.save_token_to_file:
            with open('.token','w') as token_file:
                token_file.write(self.token)


    def login(self):
        print("Checking for token...")
        if not self.check_for_token():
            print("Reverting to manual login")
            self.manual_login()


    def get_all_members(self, filename=None):

        self.check_for_token()

        headers = {"Accept": "application/json, text/plain, */*",
                   "Content-Type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer " + self.token,
                   "Cookie": 'token=%22' + self.token + '%22'}

        conn = http.client.HTTPSConnection(EWB_MEMBER_BASE_URL)
        conn.request('GET', '/api/members', headers=headers)

        resp = conn.getresponse()

        if resp.status != 200:
            print('Could not get members!')
            print('Server response:')
            print(resp.status, resp.reason)
        elif self.verbose:
            print('Members successfully fetched!')

        if filename:
            with open(filename, 'w') as out_file:
                out_file.write(resp.read())

        return json.loads(resp.read())

    def get_active_members(self, filename=None):
        self.check_for_token()

        all_members = self.get_all_members()

        active_members = []

        for member in all_members:
            if member['created_at'] == None or member['expiration_date'] == None:
                continue
            creation_date = datetime.strptime(member['created_at'], 
                                            "%Y-%m-%dT%H:%M:%S.%fZ")
            expiration_date = datetime.strptime(member['expiration_date'], 
                                            "%Y-%m-%dT%H:%M:%S.%fZ")

            if datetime.today() < expiration_date and datetime.today() >= creation_date:
                active_members.append(member)

        if filename:
            with open(filename, 'w') as out_file:
                out_file.write(active_members)

        return active_members

    def check_for_token(self, func=None, *args):
        if not self.token:

            if '.token' in os.listdir():
                with open('.token','r') as token_file:
                    self.token = token_file.read()
                    # Test token to see if it is still valid
                    if self.try_token():
                        #if func:
                        #    func(args)
                        return True
                    else:
                        print('Token has expired or is no longer valid, please login again!')
                        #self.login()
                        #if func:
                        #    func(args)
                        return False
            else:
                print('No token found, please login before using API!')
                return False
                #self.login()
                #if func:
                #    func(args)

    def try_token(self):
        success = False

        headers = {"Accept": "application/json, text/plain, */*",
                   "Content-Type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer " + self.token,
                   "Cookie": 'token=%22' + self.token + '%22'}

        conn = http.client.HTTPSConnection(EWB_MEMBER_BASE_URL)
        conn.request('HEAD', '/api/members', headers=headers)

        resp = conn.getresponse()

        if resp.status != 200:
            print('Token verification failed!')
            print('Server response:')
            print(resp.status, resp.reason)
        else:
            if self.verbose:
                print('Token verification success!')
                #print('Server response:')
                #print(resp.status, resp.reason)
                #print(resp.read())
            success = True

        return success
