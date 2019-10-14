#!/usr/bin/env python3
 
from MemberSiteAPI import Session
from pprint import pprint
from datetime import date


ses = Session(verbose=True)
ses.login()
members = ses.get_active_members()

filename = 'active_member_emails_{}.txt'.format(date.today())

with open(filename,'w') as f:
    for member in members:
        f.write(member['email'] + '\n')
