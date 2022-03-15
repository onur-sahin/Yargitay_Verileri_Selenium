from asyncio.windows_events import NULL
from lib2to3.pgen2 import driver
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager

import time

class Driver:

   

   def __init__(self, url):
      self.url = url

      self.driver = webdriver.Firefox(
         service=Service(
            GeckoDriverManager().install()
         )
      )

      self.driver.get(url)
      
      # self.detayli_arama_we = WebDriverWait(self.driver, 10).until(
      #    EC.presence_of_element_located(
      #       (By.ID, "aramaForm:detayliAramaLabel")
      #    )
      # )
      
      # self.detayli_arama_we.click()
      
      # self.captcha_input_we = self.driver.find_element(By.ID, "aramaForm:guvenlikKodu")

      # self.cptImg_we = self.driver.find_element(By.ID, "aramaForm:cptImg")

      # self.karar_yili_we = self.driver.find_element(By.ID, "aramaForm:karaYilInput")

      # self.tarih_bas_we = self.driver.find_element(By.ID, "aramaForm:ilkTarih_input")

      # self.tarih_son_we = self.driver.find_element(By.ID, "aramaForm:sonTarih_input")

      # self.search_we = self.driver.find_element(By.ID, "aramaForm:detayliAraCommandButton")

   def get_we(self, type, str, element, element_type):

      if(type == "CLASS_NAME"):
         self.get_we = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CLASS_NAME, str)
            )
         )

         

      if(type == "CSS_SELECTOR"):
         self.get_we = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, element+"["+element_type+"*='"+str+"']")
            )
         )
      
      
      
      return self.get_we

   
   def get_logo(self):
      
      self.get_logo = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "img[class='img-responsive logo']")
         )
      )
      return self.get_logo



   def get_detayli_arama_we(self):
      # self.detayli_arama_we = WebDriverWait(self.driver, 10).until(
      #    EC.presence_of_element_located(
      #       (By.ID, "aramaForm:detayliAramaLabel")
      #    )
      # )
      self.detayli_arama_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span[id='aramaForm:detayliAramaLabel'")
         )
      )
      return self.detayli_arama_we

   def get_captcha_input_we(self):
      self.captcha_input_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:guvenlikKodu']")
         )
      )
      return self.captcha_input_we

   def get_cptImg_we(self):
      self.cptImg_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "img[id='aramaForm:cptImg']")
         )
      )
      return self.cptImg_we

   def get_karar_yili_we(self):
      self.karar_yili_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:karaYilInput']")
         )
      )
      return self.karar_yili_we

   def get_tarih_bas_we(self):
      self.tarih_bas_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:ilkTarih_input']")
         )
      )
      return self.tarih_bas_we

   def get_tarih_son_we(self):
      self.tarih_son_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:sonTarih_input']")
         )
      )
      return self.tarih_son_we

   def get_search_we(self):
      self.search_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[id='aramaForm:detayliAraCommandButton']")
         )
      )
      return self.search_we
      
   def is_there_sonucTable_head(self):
      result = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "thead[id='aramaForm:sonucTable_head']")
         )
      )
      return result

   def get_data_ri_we(self, no):
      self.get_data_ri_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "tr[data-ri='" + str(no) + "']")
         )
      )
      return self.get_data_ri_we

   def get_data_ri_count(self):
      self.get_data_ri_count = WebDriverWait(self.driver, 10).until(
         EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "tr[data-ri*=''")
         ).count()
      )
      return self.get_data_ri_count

   def get_data_ri_button_we(self, no):
      self.get_data_ri_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[onclick='PrimeFaces.ab({s:\"aramaForm:sonucTable:0:rowbtn\",p:\"aramaForm:sonucTable:0:rowbtn\",u:\"aramaForm:karakIcerikPanel\",onst:function(cfg){disableScroll();;}});return false;']")
         )
      )
      return self.get_data_ri_button_we
      
      #.find_element(By.CSS_SELECTOR, "span[class='ui-button-icon-left ui-icon ui-c ui-icon-search']")

      #"button[id='aramaForm:sonucTable:" + str(no) + ":rowbtn'"

   def data_ri_click(self, no):
      try:
         self.driver.execute_script("document.getElementById(\"aramaForm:sonucTable:" + str(no) + ":rowbtn\").click();")
      except:
         logging.error("data_ri_click()" + str(no) +". satirinda hata")
         return False
      else:
         return True


   def get_karar_icerik_panel_we(self):

      try:
         self.get_karar_icerik_panel_we = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "div[id='aramaForm:karakIcerikPanel']")
            )
         )
      except:
         logging.error("get_karar_icerik_panel_we() fonksiyonunda hata!")
         return NULL
      else:
         return self.get_karar_icerik_panel_we


   def copy_karar_icerik_panel(self):
      try:
         #self.copy_karar_icerik_panel = self.driver.execute_script("")
         self.copy_karar_icerik_panel = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "p[align='justify']")
            )
         )

      except:
         logging.error("copy_karar_icerik_panel() fonksiyonunda hata")
         return NULL

      else:
         return self.copy_karar_icerik_panel



