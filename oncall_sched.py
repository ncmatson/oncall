from oc import *
from operator import itemgetter

def toCSV(filename, oncall):
    f = open(filename, 'w')
    f.write('date,ra oncall, weekend?\n')
    for night in oncall:
        if is_weekend(night[0]):
            f.write(night[0].isoformat() + ',' + night[1] + ',weekend\n')
        else:
            f.write(night[0].isoformat() + ',' + night[1] + ',weekday\n')


first_day   = string_to_date(input('whats the first day on call? '))
last_day    = string_to_date(input('whats the last day on call? '))
total_days  = (last_day - first_day).days + 1

staff = generate_ra_list()

ra_doc = calculate_doc(staff, total_days, count_weekends(first_day, total_days))

ra_exclude = {}
for person in staff:
    ra_exclude[person] = set_exclusion(person, first_day)

oncall = assign_on_call(ra_doc, first_day, total_days, dict(ra_exclude))

toCSV('oncall.csv', oncall)
