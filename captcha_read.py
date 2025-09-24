from asyncio.windows_events import NULL
import logging
from captcha_solver import CaptchaSolver

from captcha_solver.error import (SolutionNotReady, SolutionTimeoutError,
                    ServiceTooBusy, InvalidServiceBackend)

from myErrorList import captcha_value_is_not_valid

from my_tools import check_ping, control_panel


def captcha_read(image_no, driver):

   error_count = 0

   while(True):

      try:
         # https://anti-captcha.com
         solver = CaptchaSolver('antigate', api_key='c8c5d34dcdfb5b93415f58b88a1e630c')
         # This usage is outdated and needs to be updated. (https://anti-captcha.com)
         raw_data = open("captcha_images/"+ str(image_no) + ".png",  'rb').read()
         result = solver.solve_captcha(raw_data, submiting_time=120)

         if(str(result).__len__() != 5):
            logging.warning("geri dönen captcha değeri 5 karakter değil")
            raise captcha_value_is_not_valid()

         else:
            return result

      except captcha_value_is_not_valid as err:

         error_count += 1

         if(error_count == 2):

            refresh_captcha = driver.refresh_captcha()

            if(refresh_captcha == "restart"):
               return "restart"

            elif(refresh_captcha == "quit"):
               return "quit"

            elif(refresh_captcha == True):
               continue

         elif(error_count >=3 ):

            x = control_panel()

            if( x == "quit"):
               return "quit"

            elif(x == "restart"):
               return "restart"
               
            elif(x == "resume"):
               error_count == 0
               continue
            
         else:
            continue
       
         

      except SolutionTimeoutError as err:

         error_count += 1

         logging.error("\ncaptha_read() fonksiyonunda hata!:" + str(err))

         if(error_count == 5):

            check_ping()
            continue

         elif(error_count == 6):
            return "restart"

         elif(error_count >= 7):
            x = control_panel()

            if( x == "quit"):
               return "quit"
               
            elif(x == "resume"):
               error_count == 0
               continue
         


      except InvalidServiceBackend as err:

         error_count += 1

         logging.error("\ncaptha_read() fonksiyonunda hata!:" + str(err))

         if(error_count == 5):

            check_ping()
            continue

         elif(error_count == 6):
            return "restart"

         elif(error_count >= 7):
            x = control_panel()

            if( x == "quit"):
               return "quit"
               
            elif(x == "resume"):
               error_count == 0
               continue

      except BaseException as err:

         error_count += 1

         logging.error("\ncaptha_read() fonksiyonunda bilinmeyen bir hata!:" + str(err))

         if(error_count == 5):

            check_ping()
            continue

         elif(error_count == 6):
            return "restart"

         elif(error_count >= 7):
            x = control_panel()

            if( x == "quit"):
               return "quit"
               
            elif(x == "resume"):
               error_count == 0
               continue
         


