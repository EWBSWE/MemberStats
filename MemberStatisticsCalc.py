#!/usr/bin/env python

from datetime import datetime, timedelta
from MemberSiteAPI import Session

def members_at_date(members, date=datetime.today(), extract=False):
    
    nbr_members = 0
    mbrs = []

    for member in members:
        if member['created_at'] == None or member['expiration_date'] == None:
            continue
        creation_date = datetime.strptime(member['created_at'], 
                                          "%Y-%m-%dT%H:%M:%S.%fZ")
        expiration_date = datetime.strptime(member['expiration_date'], 
                                          "%Y-%m-%dT%H:%M:%S.%fZ")

        if date < expiration_date and date > creation_date:
            nbr_members += 1
            if extract:
                mbrs.append(member)
    if extract:
        return (nbr_members, mbrs)
    else:
        return nbr_members

def get_new_members(members, start_date, end_date=datetime.today(), extract=False):
    nbr_new_members = 0

    new_members = []

    for member in members:
        if member['created_at'] == None or member['expiration_date'] == None:
            continue

        creation_date = datetime.strptime(member['created_at'], 
                                          "%Y-%m-%dT%H:%M:%S.%fZ")

        if creation_date <= end_date and creation_date >= start_date:
            nbr_new_members += 1
            if extract:
                new_members.append(member)

    if extract:
        return (nbr_new_members, new_members)
    else:
        return nbr_new_members

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
all_members = ses.get_all_members()
nbr_curr_members, curr_members = members_at_date(all_members, datetime(2017,12,31), extract=True)

nbr_members = len(all_members)

genders = get_gender_dist(curr_members)

males = genders['male']
females = genders['female']
unknowns = genders['unknown']

print('Number of members in register: {}'.format(nbr_members))
print('Number of current members: {}'.format(nbr_curr_members))

print('# Current Gender distrobution')
print('Male: {}, {:.1f}%'.format(males, males/nbr_curr_members*100))
print('Female: {}, {:.1f}%'.format(females, females/nbr_curr_members*100))
print('Unknown: {},{:.1f}%'.format(unknowns, unknowns/nbr_curr_members*100))

print('# Membership history')
for year in range(2010,2019):
    print('Members {}: {}'
          .format(year, members_at_date(all_members, datetime(year, 12, 31))))

nbr_new, new_members = get_new_members(all_members, datetime(2017,1,1), extract=True)

print('New members this year: {}'
      .format(get_new_members(all_members, datetime(2018,1,1))))
