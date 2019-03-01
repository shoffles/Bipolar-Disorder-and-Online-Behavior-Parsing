import MboxParser as Mbox
import mailbox
import time
import os

# Keywords to flag for
KEY_WORDS = ('Amazon', 'Walmart', 'Target', 'BestBuy', 'Ebay', 'Etsy', 'Alixpress', 'Costco', 'Kohls', 'Sears',
             'Zappos', 'shopping', 'online shopping', 'online store', 'sales', 'store', 'receipt', 'order',
             'credit card', 'debit card', 'shipping', 'gamble', 'casino', 'gambling')

# Illegal Characters for file creation
ILLEGAL_CHARACTERS = ('/', ':', '*', '?', '<', '>', '|', '\\', ' ', '"', '-', '\\n')

# Select path for mbox file here
mbox_filepath = 'C:\\Mail\\BigFile.mbox'

# Set flagged output path here
flagged_path = 'FlaggedEmails.txt'

# Set normal output path here
normal_path = 'NormalEmails.txt'


if __name__ == '__main__':

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

    start_time = time.time()
    print('Running...')

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
        print(parsed.to_string())

    elapsed_time = time.time() - start_time
    print('Complete')
    print(elapsed_time)
