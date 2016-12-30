from oc import *
from operator import itemgetter
import json

def toCSV(filename, oncall):
    f = open(filename, 'w')
    f.write('date,ra oncall, weekend?\n')
    for night in oncall:
        if is_weekend(night[0]):
            f.write(night[0].isoformat() + ',' + night[1] + ',weekend\n')
        else:
            f.write(night[0].isoformat() + ',' + night[1] + ',weekday\n')

def load(filename) :
    f = open(filename, 'r')

    return json.load(f)

data = load('oncall.json')

first_day   = string_to_date(data['first_day'])
last_day    = string_to_date(data['last_day'])
total_days  = (last_day - first_day).days + 1

staff       = data['staff']

ra_exclude  = data['ra_exclude']

block_days  = calculate_block_days(data['block_days'], first_day)

ra_doc = calculate_doc(staff, total_days, first_day, block_days)

oncall = assign_on_call(ra_doc, first_day, total_days, dict(ra_exclude), block_days)

toCSV('oncall.csv', oncall)
