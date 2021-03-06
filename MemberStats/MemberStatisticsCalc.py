#!/usr/bin/env python

from datetime import datetime, date, timedelta
from MemberStats.MemberSiteAPI import Session


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

        if date < expiration_date and date >= creation_date:
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


def get_membership_dist(members):

    nbr_students = 0
    nbr_working = 0
    nbr_senior = 0
    nbr_unknown = 0

    for member in members:
        if member['member_type'] == 'student':
            nbr_students += 1
        elif member['member_type'] == 'working':
            nbr_working += 1
        elif member['member_type'] == 'senior':
            nbr_senior += 1
        else:
            nbr_unknown += 1

    return {'student': nbr_students, 'working': nbr_working,
            'senior': nbr_senior, 'unknown': nbr_unknown}


# Get all new members that signed up a given year
def get_new_members_during_year(members, year, extract=True):
    return get_new_members(members, datetime(year, 1, 1), datetime(year, 12, 31), extract=True)


def get_members_local_group(members, local_group):
    in_local_group = []
    for member in members:
        if local_group.lower() in member['location'].lower():
            in_local_group.append(member)

    return in_local_group


if __name__ == "__main__":
    ses = Session(verbose=True)

    ses.login()
    all_members = ses.get_all_members()
    nbr_curr_members, curr_members = members_at_date(all_members, datetime.today(), extract=True)

    nbr_members = len(all_members)

    genders = get_gender_dist(curr_members)

    males = genders['male']
    females = genders['female']
    unknown_gender = genders['unknown']

    member_types = get_membership_dist(curr_members)

    students = member_types['student']
    working = member_types['working']
    seniors = member_types['senior']
    unknown_types = member_types['unknown']

    print('\n# General Statistics')
    print('Number of members in register: {}'.format(nbr_members))
    print('Number of current members: {}'.format(nbr_curr_members))

    print('\n# Current Gender Distribution')
    print('Male:    {:>4}, {:>5.1f}%'
          .format(males, males/nbr_curr_members*100))
    print('Female:  {:>4}, {:>5.1f}%'
          .format(females, females/nbr_curr_members*100))
    print('Unknown: {:>4}, {:>5.1f}%'
          .format(unknown_gender, unknown_gender/nbr_curr_members*100))

    print('\n# Current Membership Distribution')
    print('Student: {:>4}, {:>5.1f}%'
          .format(students, students/nbr_curr_members*100))
    print('Working: {:>4}, {:>5.1f}%'
          .format(working, working/nbr_curr_members*100))
    print('Senior:  {:>4}, {:>5.1f}%'
          .format(seniors, seniors/nbr_curr_members*100))
    print('Unknown: {:>4}, {:>5.1f}%'
          .format(unknown_types, unknown_types/nbr_curr_members*100))

    print('\n# Membership history')
    for year in range(2010,datetime.today().year + 1):
        print('Members {}: {}'
              .format(year, members_at_date(all_members, datetime(year, 12, 31))))

    nbr_new, new_members = get_new_members(all_members, datetime(2017,1,1), extract=True)

    print('\n# Changes in members')
    # This date shouldn't be hardcoded
    print('New members last year: {}'
          .format(get_new_members(all_members, datetime(datetime.today().year - 1,1,1))))
    print('New members this year: {}'
          .format(get_new_members(all_members, datetime(datetime.today().year,1,1))))


    # Quarterly breakdown
    print('\n# Quarterly breakdown for {}'.format(date.today().year - 1))
    print('Q1: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year - 1,  3, 31))))
    print('Q2: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year - 1,  6, 30))))
    print('Q3: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year - 1,  9, 30))))
    print('Q4: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year - 1, 12, 31))))

    print('\n# Quarterly breakdown for {}'.format(date.today().year))
    print('Q1: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year,  3, 31))))
    print('Q2: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year,  6, 30))))
    print('Q3: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year,  9, 30))))
    print('Q4: {:>4}'.format(members_at_date(all_members, datetime(datetime.today().year, 12, 31))))

    # Breakdown on local group level from last year
    year = 2019
    print('\n# Local group breakdown for {}, new members'.format(year))
    locations = ['luleå', 'uppsala', 
                 'karlstad', 'stockholm', 
                 'göteborg', 'malmö', 
                 'lund', 'linköping',
                 'helsingborg', 'örebro']

    new_mems_last_year, new_members_last_year = get_new_members_during_year(all_members, year, extract=True)
    for location in locations:
        local_members = get_members_local_group(new_members_last_year, location)
        mem_dist = get_membership_dist(local_members)
        print('\n## {}'.format(location.capitalize()))
        print('Students: {:>4}, {:5.1f}%'.format(mem_dist['student'], mem_dist['student']/new_mems_last_year*100))
        print('Working:  {:>4}, {:5.1f}%'.format(mem_dist['working'], mem_dist['working']/new_mems_last_year*100))
        print('Seniors:  {:>4}, {:5.1f}%'.format(mem_dist['senior'],  mem_dist['senior']/new_mems_last_year*100))
        print('Unknowns: {:>4}, {:5.1f}%'.format(mem_dist['unknown'], mem_dist['unknown']/new_mems_last_year*100))
