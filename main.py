#from ossaudiodev import control_labels
from sqlite3 import Date
from download_data import download_data
from logger import setup_logging
import logging
import captcha
import datetime
import time

from my_tools import control_panel

setup_logging()

#captcha.create_img_folder()

start = datetime.datetime(2021, 12, 16)
end = datetime.datetime(2021, 12, 17)

year = 2021

restartCount = [0]

start_kararNo = -1
end_kararNo = 5

while(True):

   captcha.delete_all_images()

   status = download_data(year, restartCount, start_kararNo, end_kararNo)

   if(status == "q"):
      break

   elif(status == "finish"):

      print("{} : {} - {} Bütün kararlar indirildi".format(year, start_kararNo, end_kararNo))

      logging.warning("WARNING: {} : {} - {} PROGRAM BAŞARI İLE TÜM KARARLARI İNDİRDİ VE SONLANDI".format(year, start_kararNo, end_kararNo))

      logging.info("INFO: {} : {} - {} PROGRAM BAŞARI İLE TÜM KARARLARI İNDİRDİ VE SONLANDI".format(year, start_kararNo, end_kararNo))

      break

   elif(status == "restart"):
      restartCount[0] = 1
      continue

   else:
      continue






