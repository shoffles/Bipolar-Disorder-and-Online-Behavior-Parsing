import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.gridspec as gridspec
import mailbox
import MboxParser as Mbox



mbox_filepath = 'C:\\Mail\\BigFile.mbox'

emails = mailbox.mbox(mbox_filepath)
