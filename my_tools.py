from asyncio.windows_events import NULL
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
   
   print("date:" + x_day+'/'+x_month+'/'+x_year)

   return x_day+'/'+x_month+'/'+x_year


def get_yil(no):
   return no[0:4]

def get_no(no):
   return no[5:]

def get_mahkemesi(metin):

   array1 = str.lower("mahkemesi")

   array_lower = [i for i in metin]
   array_upper = array_lower
   
   for i in enumerate(array_lower):
      
      if(i[1] == "<"):
         array_lower[i[0]] = " " + array_lower[i[0]]
         array_upper[i[0]] = " " + array_upper[i[0]]

      if(i[1] == ">"):
         array_lower[i[0]] = array_lower[i[0]] + " "
         array_upper[i[0]] = array_upper[i[0]] + " "

      # if(i[1] == "'"):
      #    array_lower[i[0]] = " "

      # if(i[1] == "\""):
      #    array_lower[i[0]] = " "

      # if(i[1] == "\\"):
      #    array_lower[i[0]] = " "

      if(i[1] == "I"):
         array_lower[i[0]] = "ı"

      if(i[1] == "İ"):
         array_lower[i[0]] = "i"


   array_lower = "".join(map(str, array_lower) )
   array_upper = "".join(map(str, array_upper) )

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

      if(i != "<br>"):
         mahkemesi.append(i)
      else:
         return " ".join(mahkemesi)
