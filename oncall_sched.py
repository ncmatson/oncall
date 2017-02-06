from oc import *
from operator import itemgetter
import multiprocessing
import time
import json

def toCSV(filename, oncall):
    f = open(filename, 'w')
    f.write('date,ra oncall, weekend?\n')
    for night in oncall:
        if is_weekend(night[0]):
            f.write(night[0].isoformat() + ',' + night[1] + ',weekend\n')
        else:
            f.write(night[0].isoformat() + ',' + night[1] + ',weekday\n')

def excludeDayOfWeek(start, end, day):
    start = string_to_date(start)
    end = string_to_date(end)
    total_days  = (end - start).days + 1
    date_list = [start + datetime.timedelta(days=x) for x in range(0, total_days)]

    return [date.isoformat() for date in date_list if date.weekday() is day]

def writeStaff(staff, oncall):
    for person in staff:
        day_count = 0
        end_count = 0
        f = open('staff/'+person+'.csv', 'w')
        for night in oncall:
            if (night[1] is person):
                if is_weekend(night[0]):
                    end_count = end_count + 1
                    f.write(night[0].isoformat() + ',' + night[1] + ',weekend\n')
                else:
                    day_count = day_count + 1
                    f.write(night[0].isoformat() + ',' + night[1] + ',weekday\n')
        f.write('number of weeknights: ' + str(day_count) + '\n')
        f.write('number of weekends: ' + str(end_count) + '\n')

def convertExclude(ra_exclude, first_day):
    result = {}

    for person in ra_exclude:
        result[person] = []
        for date in ra_exclude[person]:
            result[person].append(calculate_offset(date, first_day))

    return result

def load(filename) :
    f = open(filename, 'r')

    return json.load(f)


def doIt():
    open('oncall.csv', 'w').close()
    data = load('oncall.json')

    first_day   = string_to_date(data['first_day'])
    last_day    = string_to_date(data['last_day'])
    total_days  = (last_day - first_day).days + 1

    staff       = data['staff']

    ra_exclude  = data['ra_exclude']
    ra_exclude  = convertExclude(ra_exclude, first_day)

    block_days  = calculate_block_days(data['block_days'], first_day)

    ra_doc = calculate_doc(staff, total_days, first_day, block_days)

    oncall = assign_on_call(ra_doc, first_day, total_days, dict(ra_exclude), block_days)

    print('assigned ', len(oncall), ' nights on call.')

    toCSV('oncall.csv', oncall)

    writeStaff(staff, oncall)

if __name__ == '__main__':
    count = 60
    # Start bar as a process
    print('writing on call...')
    while(count > 0):
        print('.', end='')
        p = multiprocessing.Process(target=doIt)
        p.start()

        p.join(1)

        if p.is_alive():
            p.terminate()
            p.join()
            count = count - 1
        else:
            print('done!')
            break
