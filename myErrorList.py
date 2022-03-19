__all__ = ('captcha_value_is_not_valid', 'captcha_refresh_is_error')

class captcha_value_is_not_valid(Exception):

   def __str__(self):
      return "captcha_value_is_not_valid"


class captcha_refresh_is_error(Exception):

   def __str__(self):
      return "captcha_refresh_is_error"