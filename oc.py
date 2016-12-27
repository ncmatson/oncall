import datetime, re, random
from collections import defaultdict

#TODO:  update ra_doc to include weekend count
#TODO:  incorporate weekend into assign on call
#TODO:  include holidays
#

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

def count_weekends(first_day, total_days):
    date_list = [first_day + datetime.timedelta(days=x) for x in range(0, total_days)]

    def is_weekend(date):
        if 4 <= date.isoweekday() <= 6:
            return 1
        else: return 0

    return sum([is_weekend(day) for day in date_list])

def distribute_remainder(ra_doc, remainder, type_of_day):
    touched = []
    ra_doc_list = list(ra_doc.keys())
    l = len(ra_doc)
    while remainder > 0:
        while True:
            person = ra_doc_list[random.randint(0,l - 1)]
            if person not in touched:
                break
        touched.append(person)
        ra_doc[person][type_of_day] = ra_doc[person][type_of_day] + 1
        remainder = remainder - 1
    return ra_doc

def calculate_doc(staff, total_days, num_weekends):
    num_weekdays = total_days - num_weekends
    weekday_per = int(num_weekdays/len(staff))
    weekend_per = int(num_weekends/len(staff))

    weekday_remainder = num_weekdays % len(staff)
    weekend_remainder = num_weekends % len(staff)

    ra_doc = {k : [weekday_per, weekend_per] for k in staff}
    ra_doc = distribute_remainder(ra_doc, weekday_remainder, 0)
    ra_doc = distribute_remainder(ra_doc, weekend_remainder, 1)

    return ra_doc

def set_exclusion(person, first_day):
    exclude = []
    print("what days can %s not be oncall?" % person)
    day = input()
    while day != 'done':
        exclusion = calculate_offset(day, first_day)
        exclude.append(exclusion)
        day = input()
    return exclude

def pick_person(ra_doc, ra_exclude, night):
    ra_doc_list = list(ra_doc.keys())
    l = len(ra_doc.keys())
    while True:
        person = ra_doc_list[random.randint(0,l-1)]
        if night not in ra_exclude[person] and ra_doc[person] > 0:
            ra_doc[person] = ra_doc[person] - 1
            break
    return person

def assign_on_call(ra_doc, first_day, total_days, ra_exclude):
    oncall = {}
    for night in range(total_days):
        date = first_day + datetime.timedelta(days=night)
        while True:
            person = pick_person(ra_doc, ra_exclude, night)
            if night not in ra_exclude[person]:
                break;
        oncall[date] = person
    return oncall
