#!/usr/bin/env python

from datetime import datetime, timedelta
from MemberSiteAPI import Session

def members_at_date(members, date=datetime.today()):
    
    nbr_members = 0

    for member in members:
        if member['created_at'] == None or member['expiration_date'] == None:
            continue
        creation_date = datetime.strptime(member['created_at'], 
                                          "%Y-%m-%dT%H:%M:%S.%fZ")
        expiration_date = datetime.strptime(member['expiration_date'], 
                                          "%Y-%m-%dT%H:%M:%S.%fZ")

        if date < expiration_date and date > creation_date:
            nbr_members += 1

    return nbr_members

def get_gender_dist(members):

    nbr_male = 0
    nbr_female = 0
    nbr_unknown = 0

    for member in members:
        if member['gender'] == 'male':
            nbr_male += 1
        elif member['gender'] == 'female':
            nbr_female += 1
        else:
            nbr_unknown += 1

    return {'male': nbr_male, 'female': nbr_female, 'unknown': nbr_unknown}

ses = Session()

ses.login()
members = ses.get_all_members()

nbr_members = len(members)

genders = get_gender_dist(members)

males = genders['male']
females = genders['female']
unknowns = genders['unknown']

current_members = members_at_date(members)

print('Number of members in register: {}'.format(len(members)))

print('# Gender distrobution')
print('Male: {}'.format(males))
print('Female: {}'.format(females))
print('Unknown: {}'.format(unknowns))

print('Current number of members: {}'.format(current_members))
for year in range(2010,2019):
    print('Members {}: {}'
          .format(year, members_at_date(members, datetime(year, 12, 31))))
