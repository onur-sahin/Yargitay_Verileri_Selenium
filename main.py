from sqlite3 import Date
from download_data import download_data
from logger import setup_logging
import logging
import captcha
import datetime
import time

setup_logging()

captcha.create_img_folder()

start = datetime.datetime(2021, 12, 16)
end = datetime.datetime(2021, 12, 17)

year = 2021

while(True):

   status = download_data(year, start_esasNo=-1, end_kararNo=-1)

   if(status == "q"):
      break

   elif(status == "error"):
      break

   

time.sleep(120)



