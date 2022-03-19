from asyncio.windows_events import NULL
import logging
import os
from glob import glob
from selenium.webdriver.common.by import By
from image_compare import compare
from my_tools import control_panel


#import shutil #tüm bir dizi silmek için kullanılabilir

folderName = "captcha_images"

pathAllImages = os.getcwd() + os.sep + folderName + os.sep + "*.png"

imgDir = os.getcwd() + os.sep + folderName

def get_captcha_code():
   captcha_code =input()
   return captcha_code

def create_img_folder():
   try:
      if os.path.exists(imgDir):
         logging.warning("\ndosya zaten var dosya oluşturulmadı")
      else:
         os.mkdir(imgDir)
   
   except BaseException as err:
      logging.error('''\ncreate_img_folder() fonksiyonu çalışırken bir hata oluştu!!\n''' + str(err))
      return False
   
   else:
      logging.info("\ncreate_img_folder() fonksiyonu başarı ile çalıştı")
      return True



def delete_all_images():
   try:
      if os.path.exists(imgDir):
         for i in glob(pathAllImages):
            os.remove( i )
      
      else:
         os.mkdir(imgDir)
   
   except BaseException as err:
      logging.error('''\ndelete_all_images() fonksiyonu çalışırken bir hata oluştu!!\n''' + str(err))
      return False
   
   else:
      logging.info("\ndelete_all_images() fonksiyonu başarı ile çalıştı")
      return True



def did_img_refresh(driver):

   last_image_number =  get_last_img_number()

   

   if(last_image_number == 0):
      return True #yani şu an kayıtlı resim yok browser daki resmi kaydedecek

   img1 = get_image_path(last_image_number)

   img2 = get_current_img(driver)

   if(last_image_number == "restart" or img2 == "restart"):
      return "restart"

   elif(last_image_number == "quit" or img2 == "quit"):
      return "quit"

   if compare(img1, img2):
      return False

   else:
      return True


# Bu fonksiyon aynı zamanda captcha_image klasörü yoksa 
def get_last_img_number():

   error_count = 0

   while(True):

      try:

         imgNames = []

         if os.path.exists(imgDir):

            list = glob(pathAllImages)

            if list.__len__() == 0:
               return 0

            else:

               for path in list:
                  name = path.split(os.sep)
                  number = int( name[-1].split('.')[0] )
                  imgNames.append(number)

               return max(imgNames)
         else:
            create_img_folder()
            return 0

      except BaseException as err:

         logging.error("get_last_img_number() fonksiyonunda hata" + str(err))

         if(error_count >= 5):
            x = control_panel(str(err))

            if(x == "resume"):

               error_count = 0
               continue
            
            elif(x == "restart"):
               return "restart"
            
            elif(x == "quit"):
               return "quit"




         

         


def save_current_img(driver1):

   error_count = 0

   while(True):

      imgName= str( get_last_img_number() + 1 )

      try:
         with open(imgDir + os.sep + imgName + '.png', 'wb') as file:
            file.write(driver1.get_cptImg_we().screenshot_as_png)

      except BaseException as err:

         error_count += 0

         if(error_count == 5):

            logging.error("save_current_img() fonksiyonu dosyaya resmi kaydedemedi hata!: " + str(err))

            delete_all_images()

         elif(error_count >= 6):

            x = control_panel()

            if(x == "resume"):
               continue

            elif(x == "quit"):
               exit()

            else:
               print("save_current_img fonksiyonunda bu seçenekler kullanılamaz\n sadece resume ve quit:")


      else:
         return True


def get_current_img(driver1):

   error_count = 0

   while(True):
      
      try:
         return driver1.get_cptImg_we().screenshot_as_png

      except BaseException as err:

         error_count += 1

         logging.warning("get_current_img() fonksiyonu.screenshot_as_png de hata!: " + str(err) )



         if(error_count == 5):

            x = control_panel()

            if( x == "quit"):
               return "quit"

            elif(x == "resume"):
               error_count = 0
               continue

            elif(x == "restart"):
               return "restart"

      

def get_image_path(number):

   path = os.getcwd() + os.sep + folderName + os.sep + str(number) +'.png'

   if os.path.isfile(path):
      return path

   else:
      return NULL


   
