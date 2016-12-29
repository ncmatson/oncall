from oc import *
from operator import itemgetter

first_day   = string_to_date(input('whats the first day on call? '))
last_day    = string_to_date(input('whats the last day on call? '))
total_days  = (last_day - first_day).days + 1

staff = generate_ra_list()

ra_doc = calculate_doc(staff, total_days, count_weekends(first_day, total_days))

ra_exclude = {}
for person in staff:
    ra_exclude[person] = set_exclusion(person, first_day)

oncall = assign_on_call(ra_doc, first_day, total_days, dict(ra_exclude))

for night in oncall:
    if is_weekend(night[0]):
        print(night[0].isoformat() + '\t' + night[1] + '\tweekend')
    else:
        print(night[0].isoformat() + '\t' + night[1])
