from asyncio.windows_events import NULL
import logging
import os
from glob import glob
from selenium.webdriver.common.by import By
from image_compare import compare


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
         logging.warning("dosya zaten var dosya oluşturulmadı")
      else:
         os.mkdir(imgDir)
   
   except BaseException as err:
      logging.error('''create_img_folder() fonksiyonu çalışırken bir hata oluştu!!\n''' + err)
      return False
   
   else:
      logging.info("create_img_folder() fonksiyonu başarı ile çalıştı")
      return True



def delete_all_images():
   try:
      if os.path.exists(imgDir):
         for i in glob(pathAllImages):
            os.remove( i )
      
      else:
         os.mkdir(imgDir)
   
   except BaseException as err:
      logging.error('''delete_all_images() fonksiyonu çalışırken bir hata oluştu!!\n''' + err)
      return False
   
   else:
      logging.info("delete_all_images() fonksiyonu başarı ile çalıştı")
      return True



def did_img_refresh(driver):
   img1 = get_image_path(get_last_img_number())
   img2 = get_current_img()
   if compare(img1, img2):
      return False
   else:
      return True

def get_last_img_number():
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


def save_current_img(driver):
   imgName= str( get_last_img_number() + 1 )
   with open(imgDir + os.sep + imgName + '.png', 'wb') as file:
      file.write(driver.find_element(By.ID, 'aramaForm:cptImg').screenshot_as_png)

def get_current_img(driver):
   return driver.find_element(By.ID, 'aramaForm:cptImg').screenshot_as_png

def get_image_path(number):
   path = os.getcwd() + os.sep + folderName + os.sep + str(number) +'.png'
   if os.path.isfile(path):
      return path
   else:
      return NULL