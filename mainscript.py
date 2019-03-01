import MboxParser as Mbox
import mailbox
import time
import os
import pandas as pd
import numpy as np


# Keywords to flag for
KEY_WORDS = ('Amazon', 'Walmart', 'Target', 'BestBuy', 'Ebay', 'Etsy', 'Alixpress', 'Costco', 'Kohls', 'Sears',
             'Zappos', 'shopping', 'online shopping', 'online store', 'sales', 'store', 'receipt', 'order',
             'credit card', 'debit card', 'shipping', 'gamble', 'casino', 'gambling')

# Illegal Characters for file creation
ILLEGAL_CHARACTERS = ('/', ':', '*', '?', '<', '>', '|', '\\', ' ', '"', '-', '\\n')

# Select path for mbox file here
mbox_filepath = 'C:\\Mail\\BigFile.mbox'

# Set flagged output path here
flagged_path = 'C:\\Users\\Thomas\\Documents\\Programming\\WHI Lab\\Outputs\\FlaggedEmails.txt'

# Set normal output path here
normal_path = 'C:\\Users\\Thomas\\Documents\\Programming\\WHI Lab\\Outputs\\NormalEmails.txt'



if __name__ == '__main__':

    # Checks if output files exist. If existing, gives option to overwrite or append
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

    df = pd.DataFrame(data_list)
    print(df)
