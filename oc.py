import datetime, re, random
from collections import OrderedDict

# takes a properly formated string and returns a date object
#   (m)m/(d)d/yyyy
def string_to_date(input_date_string):
    input_date_list = re.split('-|/| ', input_date_string)
    return datetime.date(int(input_date_list[0]), int(input_date_list[1]), int(input_date_list[2]))

# returns a number representing the diference between the given date
#   and the first date
def calculate_offset(given_date_string, first_day):
    given_date = string_to_date(given_date_string)
    return (given_date - first_day).days

# returns 1 if the given date is a weekend (th, f, sa)
#   0 otherwise
def is_weekend(date):
    if 4 <= date.isoweekday() <= 6:
        return 1
    else: return 0

# counts the number of weekend days (th, f, sa) given a starting date
#   and a total number of days
def count_weekends(first_day, total_days, block_days):
    date_list = [first_day + datetime.timedelta(days=x) for x in range(0, total_days) if x not in block_days]

    return sum([is_weekend(day) for day in date_list])

def count_weekdays(first_day, total_days, block_days):
    date_list = [first_day + datetime.timedelta(days=x) for x in range(0, total_days) if x not in block_days]

    return len(date_list) - sum([is_weekend(day) for day in date_list])

def calculate_block_days(block_days, first_day):
    return [calculate_offset(day, first_day) for day in block_days]

# Calculate how many days each RA in staff should be on-call given the total number
#   of days, and total number of weekend days
def calculate_doc(staff, total_days, first_day, block_days):
    num_weekends = count_weekends(first_day, total_days, block_days)
    num_weekdays = count_weekdays(first_day, total_days, block_days)

    weekday_per = int(num_weekdays/len(staff))
    weekend_per = int(num_weekends/len(staff))

    weekday_remainder = num_weekdays % len(staff)
    weekend_remainder = num_weekends % len(staff)

    # {ra : [weekdays, weekends]}
    ra_doc = {k: [weekday_per, weekend_per] for k in staff}

    # If the number of days to assign is not divisible by the number of RAs,
    #   distribute the remaining number of days randomly to the staff.
    #   The max difference between any two RAs should be 1.
    def distribute_remainder(ra_doc, remainder, type_of_day):
        # RAs who have been given an extra day
        touched = []

        ra_doc_list = list(ra_doc.keys())
        l = len(ra_doc)

        while remainder > 0:
            while True:
                person = ra_doc_list[random.randint(0,l - 1)]
                if person not in touched:
                    touched.append(person)
                    ra_doc[person][type_of_day] = ra_doc[person][type_of_day] + 1
                    remainder = remainder - 1
                    break
        return ra_doc

    ra_doc = distribute_remainder(ra_doc, weekday_remainder, 0)
    ra_doc = distribute_remainder(ra_doc, weekend_remainder, 1)

    return ra_doc

# type_of_day is either 0 for weekday or 1 for weekend
def pick_person(ra_doc, ra_exclude, night, type_of_day):
    # make a list out of the on call dict
    ra_doc_list = list(ra_doc.keys())
    l = len(ra_doc.keys())
    while True:
        # pick a person to try to assign
        person = ra_doc_list[random.randint(0,l-1)]

        # if that person hasn't excluded that night and they have
        #   nights(including weekends) left...
        if night not in ra_exclude[person] and ra_doc[person][type_of_day] > 0:
            ra_doc[person][type_of_day] = ra_doc[person][type_of_day] - 1
            break
    return person

def assign_on_call(ra_doc, first_day, total_days, ra_exclude, block_days):
    oncall = []
    for night in range(total_days):
        if night in block_days:
            continue
        # create date object for the 'night'
        date = first_day + datetime.timedelta(days=night)

        # choose a person for the given night given what day of the week it is
        #   and the nights they have excluded
        person = pick_person(ra_doc, ra_exclude, night, is_weekend(date))

        # assign that person to be on-call
        oncall.append((date, person))
    return oncall
