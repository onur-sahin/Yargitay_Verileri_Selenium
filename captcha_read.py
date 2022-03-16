from asyncio.windows_events import NULL
import logging
from captcha_solver import CaptchaSolver

from captcha_solver.error import (SolutionNotReady, SolutionTimeoutError,
                    ServiceTooBusy, InvalidServiceBackend)


def captcha_read(image_no):

   try:

      solver = CaptchaSolver('antigate', api_key='c8c5d34dcdfb5b93415f58b88a1e630c')
      raw_data = open("captcha_images/"+ str(image_no) + ".png",  'rb').read()
      result = solver.solve_captcha(raw_data, submiting_time=120)

      return result

   except SolutionTimeoutError as err:
      logging.error("\ncaptha_read() fonksiyonunda hata!:" + str(err))
      return NULL

   except InvalidServiceBackend as err:
      logging.error("\ncaptha_read() fonksiyonunda hata!:" + str(err))
      return NULL

   except BaseException as err:
      logging.error("\ncaptha_read() fonksiyonunda bilinmeyen bir hata!:" + str(err))
      return NULL


