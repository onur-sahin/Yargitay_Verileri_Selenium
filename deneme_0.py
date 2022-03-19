from myErrorList import captcha_value_is_not_valid

def fnc(sayi):

   try:
      

      sonuc = 100/sayi
   except Exception as err:

         print("birinci hata alındı" + str(err))


   else:
      raise captcha_value_is_not_valid()
      return sonuc


try:
   print(fnc(10))

except BaseException as err:

   print("ikinci hata dönüşü: " + str(err))
