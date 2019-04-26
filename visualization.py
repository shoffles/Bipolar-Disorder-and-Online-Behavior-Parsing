import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.gridspec as gridspec
import mailbox
import MboxParser as Mbox
import os
import tkinter as tk
from tkinter.filedialog import *
from datetime import timedelta, datetime, date


def try_parse_date(d):
    try:
        ts = pd.Timestamp(d)
        if ts.tz is None:
            ts = ts.tz_localize('UTC')
        return ts.tz_convert('UTC')
    except:
        return np.nan


data_list = []

try:
    print('Select a file')
    file_path = askopenfilename()
    print(file_path)
except IOError:
    print('Could not load file')



with open(file_path, 'r', encoding='utf-8') as f:

    temp_dict = dict()
    for line in f.readlines():
        if "Word Count" in line:
            temp_dict['word count'] = line[12:len(line)-2]

        if "Character Count" in line:
            temp_dict['character count'] = line[17:len(line)-2]

        if  "Subject" in line:
            temp_dict['subject'] = line[9:len(line)-2]

        if "Sender" in line:
            temp_dict['sender'] = line[8:len(line)-2]

        if "Receiver" in line:
            temp_dict['receiver'] = line[10:len(line)-2]

        if "Time" in line:
            temp_dict['time'] = line[6:len(line)-1]

        if "Sentiment" in line:
            temp_dict['sentiment'] = line[11:len(line)-2]

        if "Body" in line:
            temp_dict['body'] = line[6:len(line)-2]

        if len(temp_dict) == 8:
            data_list.append(temp_dict)
            temp_dict = dict()



    #Visualization start
df = pd.DataFrame(data_list)
df['timestamp'] = df.time.map(try_parse_date)
df['hour'] = df.timestamp.map(lambda x: x.hour)

print(df)

freq = 'W' # could also be 'W' (week) or 'D' (day)
df = df.set_index('timestamp', drop=False)
df.index = df.index.to_period(freq)

#mindate = df.timestamp.min()

#Sets the start date of Jan 1 2016
mindate = pd.Timestamp('2017-01-01 00:00:00-05:00')
maxdate = df.timestamp.max()
pr = pd.period_range(mindate, maxdate, freq=freq)
hm = pd.DataFrame(np.zeros([len(pr), 24]) , index=pr)

for period in pr:
    if period in df.index:
        hm.ix[period] = df.ix[[period]].hour.value_counts()
        hm.fillna(0, inplace=True)



### Set up figure
fig = plt.figure(figsize=(12,8))
gs = gridspec.GridSpec(2, 2, height_ratios=[4,1], width_ratios=[20,1],)
gs.update(wspace=0.05)


ax = plt.subplot(gs[0])
x = dates.date2num([p.start_time for p in pr])
t = [datetime(2000, 1, 1, h, 0, 0) for h in range(24)]
t.append(datetime(2000, 1, 2, 0, 0, 0))
y = dates.date2num(t)
cm = plt.get_cmap('Oranges')
plt.pcolor(x, y, hm.transpose().as_matrix(), cmap=cm)

### Now format our axes to be human-readable
ax.xaxis.set_major_formatter(dates.DateFormatter('%b %Y'))
ax.yaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
ax.set_yticks(t[::2])
ax.set_xticks(x[::12])
ax.set_xlim([x[0], x[-1]])
ax.set_ylim([t[0], t[-1]])
ax.tick_params(axis='x', pad=14, length=10, direction='inout')

### pcolor makes it sooo easy to add a color bar!
plt.colorbar(cax=plt.subplot(gs[1]))

plt.show()
