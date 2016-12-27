from oc import *

first_day   = string_to_date(input('whats the first day on call? '))
last_day    = string_to_date(input('whats the last day on call? '))
total_days  = (last_day - first_day).days + 1

staff = generate_ra_list()

ra_doc = calculate_doc(staff, total_days)

ra_exclude = {}
for person in staff:
    ra_exclude[person] = set_exclusion(person, first_day)

oncall = assign_on_call(ra_doc, first_day, total_days, dict(ra_exclude))
