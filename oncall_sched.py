from oc import *


staff = generate_ra_list()
ra_doc = dict(zip(staff, [0]*len(staff)))

# ra_exclude = defaultdict(list)
ra_exclude = {}

first_day = string_to_date(input('whats the first day on call? '))
last_day = string_to_date(input('whats the last day on call? '))

total_days = (last_day - first_day).days + 1
print(total_days)

ra_doc = calculate_doc(ra_doc, total_days)

for person in ra_doc:
    ra_exclude[person] = set_exclusion(person, first_day)

print(ra_exclude)

oncall = assign_on_call(ra_doc, total_days, dict(ra_exclude))
print(oncall)
