import datetime

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