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

      self.detayli_arama_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.ID, "aramaForm:detayliAramaLabel")
         )
      )
      
      self.detayli_arama_we.click()
      
      self.captcha_input_we = self.driver.find_element(By.ID, "aramaForm:guvenlikKodu")

      self.cptImg_we = self.driver.find_element(By.ID, "aramaForm:cptImg")

      self.karar_yili_we = self.driver.find_element(By.ID, "aramaForm:karaYilInput")

      self.tarih_bas_we = self.driver.find_element(By.ID, "aramaForm:ilkTarih_input")

      self.tarih_son_we = self.driver.find_element(By.ID, "aramaForm:sonTarih_input")

      self.search_we = self.driver.find_element(By.ID, "aramaForm:detayliAraCommandButton")



   def get_detayli_arama_we(self):
      self.detayli_arama_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.ID, "aramaForm:detayliAramaLabel")
         )
      )
      return self.detayli_arama_we

   def get_captcha_input_we(self):
      self.captcha_input_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.ID, "aramaForm:guvenlikKodu")
         )
      )
      return self.captcha_input_we

   def get_cptImg_we(self):
      self.cptImg_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.ID, "aramaForm:cptImg")
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


