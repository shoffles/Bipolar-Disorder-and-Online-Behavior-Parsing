import MboxParser as Mbox
import mailbox
import time
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.gridspec as gridspec
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
KEY_WORDS = ('Amazon', 'Walmart', 'Target', 'BestBuy', 'Ebay', 'Etsy', 'Alixpress', 'Costco', 'Kohls', 'Sears',
             'Zappos', 'shopping', 'online shopping', 'online store', 'sales', 'store', 'receipt', 'order',
             'credit card', 'debit card', 'shipping', 'gamble', 'casino', 'gambling')

# Illegal Characters for file creation, not in use
ILLEGAL_CHARACTERS = ('/', ':', '*', '?', '<', '>', '|', '\\', ' ', '"', '-', '\\n')

# Select path for mbox file here
mbox_filepath = 'C:\\Users\\Thomas\\Documents\\Programming\\WHI Lab\\Mbox\\SmallFile.mbox'

# Set flagged output path here
flagged_path = 'C:\\Users\\Thomas\\Documents\\Programming\\WHI Lab\\Outputs\\FlaggedEmails.txt'

# Set normal output path here
normal_path = 'C:\\Users\\Thomas\\Documents\\Programming\\WHI Lab\\Outputs\\NormalEmails.txt'


if __name__ == '__main__':

    # Checks if output files exist. If existing, gives option to overwrite or append new data
    try:
        if os.path.getsize(flagged_path) != 0 or os.path.getsize(normal_path) != 0:
            answer = input('Output files have data. Overwrite? (y/n): ')
            if answer == 'y':
                answer = input('Are you sure? (y/n): ')
                if answer == 'y':
                    file = open(flagged_path, 'w', encoding='utf-8')
                    file.close()
                    file = open(normal_path, 'w', encoding='utf-8')
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
    emails = mailbox.mbox(mbox_filepath)
    for email in emails:
        flagged = []
        parsed = Mbox.Email(email)
        for word in KEY_WORDS:
            if word in parsed.subject:
                flagged.append(word)
                parsed.flag = True
        if len(flagged) != 0:
            file = open(flagged_path, 'a', encoding='utf-8')
            file.write("Flagged Words: {}\n".format(flagged))
            file.write(parsed.to_string())
            file.close()
        else:
            file = open(normal_path, 'a', encoding='utf-8')
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
    mindate = pd.Timestamp('2015-01-01 00:00:00-05:00')
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
