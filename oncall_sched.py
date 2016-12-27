import datetime, calendar, re, itertools, random
from collections import defaultdict


def string_to_date(input_date_string):
    input_date_list = re.split('-|/| ', input_date_string)
    return datetime.date(int(input_date_list[2]), int(input_date_list[0]), int(input_date_list[1]))

def calculate_offset(input_date_string, first_day):
    input_date = string_to_date(input_date_string)
    return (input_date - first_day).days

def set_exclusion(person, ra_exclude, first_day):
    print("what days can %s not be oncall?" % person)
    day = input()
    while day != 'done':
        exclusion = calculate_offset(day, first_day)
        ra_exclude[person].append(exclusion)
        day = input()

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


ra_doc = {'cameron':0, 'samiat':0, "aabid":0, 'hannah':0, 'amanda':0, 'holt':0, 'ryan':0, 'alex':0}
ra_exclude = defaultdict(list)

first_day = string_to_date(input('whats the first day on call? '))
last_day = string_to_date(input('whats the last day on call? '))

total_days = (last_day - first_day).days
print(total_days)

ra_doc = calculate_doc(ra_doc, total_days)

for person in ra_doc:
    set_exclusion(person, ra_exclude, first_day)

oncall = assign_on_call(ra_doc, total_days, ra_exclude)
print(oncall)
