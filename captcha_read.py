from asyncio.windows_events import NULL
import logging
from captcha_solver import CaptchaSolver

from captcha_solver.error import (SolutionNotReady, SolutionTimeoutError,
                    ServiceTooBusy, InvalidServiceBackend)

from my_tools import check_ping, control_panel


def captcha_read(image_no):

   error_count = 0

   while(True):

      try:

         solver = CaptchaSolver('antigate', api_key='c8c5d34dcdfb5b93415f58b88a1e630c')
         raw_data = open("captcha_images/"+ str(image_no) + ".png",  'rb').read()
         result = solver.solve_captcha(raw_data, submiting_time=120)

         return result

      except SolutionTimeoutError as err:

         error_count += 1

         logging.error("\ncaptha_read() fonksiyonunda hata!:" + str(err))
         


      except InvalidServiceBackend as err:

         error_count += 1

         logging.error("\ncaptha_read() fonksiyonunda hata!:" + str(err))

      except BaseException as err:

         error_count += 1

         logging.error("\ncaptha_read() fonksiyonunda bilinmeyen bir hata!:" + str(err))


      finally:

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



            


