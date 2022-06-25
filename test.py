# ####################### Standard Libraries #####################################
# import os
# from selenium.webdriver.common.by import By
import datetime as dt
################################# My Libraries #################################

date = "May 10, 2022"
try:
    date = dt.datetime.strptime(date, '%b. %d, %Y').date()
    print(date)
except ValueError:
    try:
        date = dt.datetime.strptime(date, '%B %d, %Y').date()
        print(date)
    except Exception as e:
        print(e)
# date = "2022-06-10"
# date = dt.datetime.strptime(date, '%Y-%m-%d').date()

# today = dt.datetime.today().date()
# print(date < today)