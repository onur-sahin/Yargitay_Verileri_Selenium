from asyncio.windows_events import NULL
import logging
import time
from pythonping import ping
import winsound
from threading import Thread
from copy import deepcopy

import datetime
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

from numpy import compare_chararrays
import numpy

def get_str_date(x_date):
   x_day = x_date.day
   x_month = x_date.month
   x_year = str(x_date.year)

   if(x_day < 10):
      x_day = '0'+str(x_day)
   else:
      x_day = str(x_day)

   if(x_month < 10):
      x_month = '0' + str(x_month)
   else:
      x_month = str(x_month)
   
   #print("date:" + x_day+'/'+x_month+'/'+x_year)

   return x_day+'/'+x_month+'/'+x_year


def get_yil(no):
   return no[0:4]

def get_no(no):
   return no[5:]

def get_mahkemesi(metin):

   array1 = str.lower("mahkemesi")

   array_lower = [i for i in metin]


   array_upper = deepcopy(array_lower) 
   
   for i in enumerate(array_lower):
      
      if(i[1] == "<"):
         array_lower[i[0]] = " " + array_lower[i[0]]
         array_upper[i[0]] = " " + array_upper[i[0]]

      if(i[1] == ">"):
         array_lower[i[0]] = array_lower[i[0]] + " "
         array_upper[i[0]] = array_upper[i[0]] + " "

      if(i[1] == '\t'):
         array_lower[i[0]] = " " + array_lower[i[0]] + " "
         array_upper[i[0]] = " " + array_upper[i[0]] + " "

      if(i[1] == "I"):
         array_lower[i[0]] = "ı"

      if(i[1] == "İ"):
         array_lower[i[0]] = "i"

      # if(i[1] == "'"):
      #    array_lower[i[0]] = " "

      # if(i[1] == "\""):
      #    array_lower[i[0]] = " "

      # if(i[1] == "\\"):
      #    array_lower[i[0]] = " "


   array_lower = "".join(array_lower)
   array_upper = "".join(array_upper)

   array_lower = str.lower(array_lower)

   list_lower = array_lower.split(" ")
   list_upper = array_upper.split(" ")


  
   bool_array = compare_chararrays(array1, list_lower , "==", True )

   true_index_array = numpy.where(bool_array == True)

   first_index = -1

   try:
      first_index = true_index_array[0][0]
   except:
      return NULL
   
   mahkemesi = []

   for i in list_upper[first_index+1:]:

      if (len(i) != 0):
         if(i[0] == ":"):
            i = i[1:]

      if (len(i) != 0):
         if(i[0] == '\t'):
            i = i[1:]

      if(i != "<br>"):
         mahkemesi.append(i)

      else:
         mahkemesi = " ".join(mahkemesi)
         print("bura1" + mahkemesi + "\n")
         return mahkemesi






def control_panel( hata=""):

   x = [-1]

   if(len(hata) != 0):
      print(hata)

   while(True):

      

      if(x[0] == -1):
         print("\n sessize almak için 's' tuşuna basınız:")

      thread_warning = Thread(target = warning, args = (x, 1000, ) )
      therad_input_x = Thread(target = input_x, args=(x, ) )
      thread_warning.start()
      therad_input_x.start()

      while(thread_warning.is_alive()):
         pass

      break
      


   while(True):
      
      print('''seçiniz:
               evaluate :e
               resume   :r
               restart  :restart
               quit     :q''')

      x[0] = input()

      if(x[0] == "e"):
         print("input your codes:\n")
         code = input()
         eval(code)

      elif(x[0] == "r"):
         return "resume"

      elif(x[0] == "q"):
         return "quit"

      elif(x[0] == "restart"):
         return "restart"
      
      else:
         print("Geçerli Seçim Yapınız!:")
         continue

def ping_cite():

   response_list = ping('212.175.130.131', size=40, count=10)

   if(response_list.packet_loss < 0.5):
      return True
   else:
      return False


def check_ping():

   sleep_time = [15, 15, 15, 15, 30, 30, 60, 60, 60, 60, 60, 60, 60, 60]

   i = 0
   count = 0

   while(True):

      count += 0
      
      logging.warning("ping atma problemi yaşanıyor " + str(count) + ". ping denemesi yapılıyor")
      
      result = ping_cite()

      if(result == True):
         return True

      else:
         time.sleep(sleep_time[i])
         i += 1
      

      if( i == sleep_time.__len__() ):

         logging.error("internet problemi")
         
         x = control_panel()

         if( x == 'resume'):
            i = 0
            count = 0
            continue

         elif(x == "quit"):
            return "quit"

         elif( x == "restart"):
            return "restart"            





   




#########################################################
def warning( x, seconds=1000, duration=2000):

   i = seconds
   
   while( i >= 0 ):
      if(x[0] != "s"):
         frequency = 2500  # Set Frequency To 2500 Hertz
         # Set Duration To 1000 ms == 1 second
         winsound.Beep(frequency, duration)
         i -= 1
      else:
         break


def input_x( x ):

   while(True):
      if(x[0] == "s" or x[0] == "S"):

         break
      else:
         x[0] = input()



def convert_all_uppercase(metin):

   list = [i for i in metin]

   for i in enumerate(list):

      if(len(i[1]) == 0):
         continue

      elif( i[1] == "i"):
         list[i[0]] = "İ"

      elif( i[1] == "ı"):
         list[i[0]] = "I"

      else:
         list[i[0]] = str.capitalize(i[1])
      

   return "".join(list)


def   convert_all_lowercase(metin):
   list = [i for i in metin]

   for i in enumerate(list):

      if(len(i[1]) == 0):
         continue

      elif( i[1] == "İ"):
         list[i[0]] = "i"

      elif( i[1] == "I"):
         list[i[0]] = "ı"

      else:
         list[i[0]] = str.lower(i[1])
      

   return "".join(list)


def   convert_title(metin):
   list_1 = [i for i in metin]

   for i in enumerate(list_1):

      if(len(i[1]) == 0):
         continue

      if(i[1] =='\t' ):
         list_1[i[0]] = " " + '\t' + " "

   list = "".join(list_1)

   list = list.split(" ")

   for i in enumerate(list):

      if(len(i[1]) == 0):
         continue

      elif( i[1][0] == "i"):
         list[i[0]] = "İ" + list[i[0]][1:]

      elif( i[1][0] == "ı"):
         list[i[0]] = "I" + list[i[0]][1:]

      else:
         list[i[0]] = str.upper(list[i[0]][0]) + list[i[0]][1:]
      

   return " ".join(list) 