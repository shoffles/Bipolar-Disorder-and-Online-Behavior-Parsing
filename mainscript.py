import MboxParser as Mbox
import mailbox
import time
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.gridspec as gridspec
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


#Test
# Keywords to flag for




if __name__ == '__main__':

    try:
        print('Select a file')
        file_path = askopenfilename()
        print(file_path)
    except IOError:
        print('Could not load file')


    try:
        print("Please select output file location")
        output_path = askdirectory()
        print(output_path)
    except IOError:
        print("Could not specify path")

    # Checks if output files exist. If existing, gives option to overwrite or append new data
    try:
        if os.path.getsize(output_path+"/FlaggedEmails.txt") != 0 or os.path.getsize(output_path+"/NormalEmails.txt") != 0:
            answer = input('Output files have data. Overwrite? (y/n): ')
            if answer == 'y':
                answer = input('Are you sure? (y/n): ')
                if answer == 'y':
                    file = open(output_path+"/FlaggedEmails.txt", 'w', encoding='utf-8')
                    file.close()
                    file = open(output_path+"/NormalEmails.txt", 'w', encoding='utf-8')
                    file.close()
                    print('Files wiped')
                else:
                    print('Files kept, new data will be appended')
            else:
                print('Files kept, new data will be appended')
    except IOError:
        print('Output files not found, ignoring...')

    start_time = time.time()
    print('Running...')

    data_list = []
    emails = mailbox.mbox(file_path)
    for email in emails:
        parsed = Mbox.Email(email)
        if parsed.flag:
            file = open(output_path+"/FlaggedEmails.txt", 'a', encoding='utf-8')
            file.write(parsed.to_string())
            file.close()
        else:
            file = open(output_path+"/NormalEmails.txt", 'a', encoding='utf-8')
            file.write(parsed.to_string())
            file.close()

        data_list.append(parsed.to_dict())

    elapsed_time = time.time() - start_time
    print('Parsing Complete')
    print(elapsed_time)






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
    mindate = pd.Timestamp('2018-01-01 00:00:00-05:00')
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
