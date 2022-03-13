from sqlite3 import Date
from download_data import download_data
from logger import setup_logging
import logging
import captcha
import datetime
import time



setup_logging()

captcha.create_img_folder()

start = datetime.datetime(2021, 12, 11)
end = datetime.datetime(2021, 12, 17)

download_data(start, end)

time.sleep(120)



