import datetime, re, random
from collections import defaultdict

def generate_ra_list():
    ra_list = []
    print('enter your staff')
    while True:
        ra = input()
        if ra == 'done':
            break;
        ra_list.append(ra)
    return ra_list

def string_to_date(input_date_string):
    input_date_list = re.split('-|/| ', input_date_string)
    return datetime.date(int(input_date_list[2]), int(input_date_list[0]), int(input_date_list[1]))

def calculate_offset(input_date_string, first_day):
    input_date = string_to_date(input_date_string)
    return (input_date - first_day).days

def set_exclusion(person, first_day):
    exclude = []
    print("what days can %s not be oncall?" % person)
    day = input()
    while day != 'done':
        exclusion = calculate_offset(day, first_day)
        exclude.append(exclusion)
        day = input()
    return exclude

def distribute_remainder(ra_doc, remainder):
    touched = []
    ra_doc_list = list(ra_doc.keys())
    l = len(ra_doc)
    while remainder > 0:
        while True:
            person = ra_doc_list[random.randint(0,l - 1)]
            if person not in touched:
                break
        touched.append(person)
        ra_doc[person] = ra_doc[person] + 1
        remainder = remainder - 1
    return ra_doc

def calculate_doc(ra_doc, total_days):
    oncall_per = int(total_days/len(ra_doc))
    remainder = total_days % len(ra_doc)

    ra_doc = {k : v + oncall_per for k, v in ra_doc.items()}
    ra_doc = distribute_remainder(ra_doc, remainder)

    return ra_doc

def pick_person(ra_doc, ra_exclude, night):
    ra_doc_list = list(ra_doc.keys())
    l = len(ra_doc.keys())
    while True:
        person = ra_doc_list[random.randint(0,l-1)]
        if night not in ra_exclude[person] and ra_doc[person] > 0:
            ra_doc[person] = ra_doc[person] - 1
            break
    return person

def assign_on_call(ras, total_days, ra_exclude):
    nights = [None] * total_days
    oncall = []
    for i, night in enumerate(nights):
        while True:
            person = pick_person(ras, ra_exclude, i)
            if i not in ra_exclude[person]:
                break;
        oncall.append(person)
    return oncall
