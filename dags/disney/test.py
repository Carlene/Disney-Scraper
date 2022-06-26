# ####################### Standard Libraries #####################################
import pandas as pd
import numpy as np
from datetime import datetime as dt, timedelta
################################# My Libraries #################################
from run import create_csv

file_string = "raw_2022-06-24_disney.csv"
print(create_csv(file_string)) # cleaned pull

# df2 = pd.DataFrame(np.array([["A", "B", None], ["J", "K", None], ["O", "P", None], [None, None, None]]),
#                    columns=[1, 2, 3])
# df2[3] = df2[3].str.lower()
# print(df2)