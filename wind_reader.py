'''
This program uses the hourly climate data from Cedar Creek Ecosystem
Science Reserve, Experiment 080. The data is publically available at
https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-cdr.382.10

We are interested in the max wind speed during the week around September 20
(9/17 - 9/23) each year. The program computes the average max wind speed
during this week, over all years with complete wind speed data.
'''

from collections import defaultdict
speeds_by_year = defaultdict(list) # defaults to empty list instead of KeyError

file_name = "e080_Hourly climate data.txt"
for line in open(file_name):
    entries = line.split('\t')
    date = entries[0]
    speed = entries[7]
    if date in ['Date', '"Date"']: continue # skip column headings
    if speed in [' ', ' . ']: continue # skip missing speeds 
    month, day, year = date.split('/')
    month = int(month)
    day = int(day)
    year = int(year)
    speed = float(speed)

    # select for dates near September 20:
    if month != 9: continue
    if not (17 <= day <= 23): continue
    
    speeds_by_year[year].append(speed)

max_speeds = []

for speeds in speeds_by_year.values():
    length = len(speeds)
    zeros = sum(s == 0 for s in speeds)
    # select only years with all 7*24 = 168 hourly measuments present,
    # and no more than 100 zeros. (some zeros are normal, but very long
    # streaks of only zeros indicate a sensor problem)
    if length == 168 and zeros < 100:
        max_speeds.append(max(speeds))

print("years with complete data:", len(max_speeds))
print("average max wind speed:", sum(max_speeds)/len(max_speeds))
