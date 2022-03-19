from asyncio.windows_events import NULL
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager

import time

from my_tools import check_ping, control_panel

class Driver:

   def __init__(self, url, restartCount):

      self.url = url
      self.restartCount = restartCount



   def connect_driver(self):

      error_count = 0

      while(True):

         try:

            self.driver = webdriver.Firefox(
               service=Service(
                  GeckoDriverManager().install()
               )
            )

            browser = self.driver.get(self.url)

         except BaseException as err:

            error_count += 1

            self.browser_quit()
            
            logging.warning("driver'a bağlantıda hata!: " + str(error_count) + ". defadır bağlanmaya çalışılıyor" + str(err) )

            time.sleep(5)
            

            if(error_count == 5):

               ping_status = check_ping()


               if(ping_status == "quit"):
                  return "quit"

               elif(ping_status == "restart"):
                  return "restart"

               #elif( ping_status == "resume"): böyle bir sonuç gelemez

               elif(ping_status == True): #Eğer ki ping başarılı ise bir kez daha driver'a
                  continue                #bağlanılmaya çalışılacak. Bu denemede de hata
                                          #olursa aşağıdaki elif yapısına girecek
            elif(error_count >= 6):

               x = control_panel( str(err) )

               if(x == "quit"):
                  return "quit"

               elif(x == "resume"):
                  error_count = 0
                  continue

               elif(x == "restart"):
                  return "restart"

               

         else: #try except 'in else 'i 
            return True


   def driver_close(self):
      try:
         self.driver.close()
      except:
         pass

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

   
   # def get_logo(self):
      
   #    self.get_logo = WebDriverWait(self.driver, 10).until(
   #       EC.presence_of_element_located(
   #          (By.CSS_SELECTOR, "img[class='img-responsive logo']")
   #       )
   #    )
   #    return self.get_logo

   
   

   def get_detayli_arama_we(self):

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

      try:
         self.cptImg_we = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "img[id='aramaForm:cptImg']")
            )
         )

         return self.cptImg_we

      except BaseException as err:

         logging.warning("get_cptImg_we() fonksiyonunda hata!: " + str(err) )

         check_ping()

 


        


   def get_karar_yili_we(self):
      self.karar_yili_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:karaYilInput']")
         )
      )
      return self.karar_yili_we


   def get_ilk_karar_no_input_we(self):
      
      self.get_ilk_karar_no_input_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:ilkKararNoInput']")
         )
      )
      return self.get_ilk_karar_no_input_we

   def get_son_karar_no_input_we(self):

      self.get_son_karar_no_input_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:sonKararNoInput']")
         )
      )
      return self.get_son_karar_no_input_we

   def get_ilk_esas_no_input_we(self):

      self.get_ilk_esas_no_input_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[id='aramaForm:ilkEsasNoInput']")
         )
      )
      return self.get_ilk_esas_no_input_we


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
            (By.CSS_SELECTOR, "tr[data-ri*='']")
         ).count()
      )
      return self.get_data_ri_count

   def get_data_ri_min_and_max(self, driver1):

      list = []
      try:

         self.get_data_ri_min_and_max = WebDriverWait(driver1.driver, 60).until(
            EC.presence_of_all_elements_located(
               (By.CSS_SELECTOR, "tr[data-ri*='']")
            )
         )

      except BaseException as err:
         print(err)

      # self.get_data_ri_min_and_max = self.driver.execute_script("return document.getElementsByClassName('ui-widget-content normalrow')")

      print(self.get_data_ri_min_and_max.getAttribute("innerHTML"))

      for web_element in self.get_data_ri_min_and_max:
         list.append(    int(  web_element.getAttribute("data-ri")  )    )

      list.sort()

      return [ list.__getitem__(0), list.pop() ]

   def get_data_ri_button_we(self, no):
      self.get_data_ri_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[onclick='PrimeFaces.ab({s:\"aramaForm:sonucTable:0:rowbtn\",p:\"aramaForm:sonucTable:0:rowbtn\",u:\"aramaForm:karakIcerikPanel\",onst:function(cfg){disableScroll();;}});return false;']")
         )
      )
      return self.get_data_ri_button_we
      
      #.find_element(By.CSS_SELECTOR, "span[class='ui-button-icon-left ui-icon ui-c ui-icon-search']")

      #"button[id='aramaForm:sonucTable:" + str(no) + ":rowbtn'"


   # def get_radio_button_karar_we(self):

   #    self.radio_button_karar_we = WebDriverWait(self.driver, 10).until(
   #       EC.presence_of_element_located(
   #          (By.CSS_SELECTOR, "table[id='aramaForm:siralamaKriteri']")
   #       )
   #    )

   #    return self.radio_button_karar_we

   def get_radio_button_karar_we(self):

      self.radio_button_karar_we = WebDriverWait(self.driver, 10).until(
         EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[class*='ui-radiobutton-box ui-widget ui-corner-all']")
         )
      )

      return self.radio_button_karar_we



   def click_to_last_tab(self):

      i = 0

      while(i <= 5):

         try:
            self.click_to_last_tab = WebDriverWait(self.driver, 10).until(
               EC.presence_of_element_located(
                  (By.CSS_SELECTOR, "a[class='ui-paginator-last ui-state-default ui-corner-all']")
               )
            )

            time.sleep(0.1)

            self.click_to_last_tab.click()

            time.sleep(0.1)

            WebDriverWait(self.driver, 10).until(
               EC.presence_of_element_located(
                  (By.CSS_SELECTOR, "a[class='ui-paginator-last ui-state-default ui-corner-all ui-state-disabled']")
               )
            )

            return True

         except :
            if(i == 5):
               return False

   def is_there_previous_tab(self):

      try:

         self.is_there_previous_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "a[class='ui-paginator-prev ui-state-default ui-corner-all ui-state-disabled']")
            )
         )

         return False

      except :

         return True

   def click_to_previous_tab(self):

      try:
         self.is_there_sonucTable_head()
      except Exception as err:
         logging.error("click_to_previous_tab de is_there_sonuc_table_head de hata" + str(err))

         return "restart"

      try:

         if(self.is_there_previous_tab() == False):
            return "finish"

         self.click_to_previous_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "a[class='ui-paginator-prev ui-state-default ui-corner-all']")
            )
         )

         self.click_to_previous_tab.click()

         self.is_there_sonucTable_head()


         return True

      except :

         return "restart"


   def data_ri_click(self, no):
      try:
         self.driver.execute_script("document.getElementById(\"aramaForm:sonucTable:" + str(no) + ":rowbtn\").click();")
         time.sleep(1)
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

   def is_there_message(self):

      try:
         result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "div[id='aramaForm:messages']")
            )
         )
      except:
         return NULL

      else:
         try:
            result_message = WebDriverWait(self.driver, 10).until(
               EC.presence_of_element_located(
                  (By.CSS_SELECTOR, "span[class='ui-messages-info-summary']")
               )
            )
         except:
            logging.error("div[id='aramaForm:messages' elementi var ve içeriği: {}".format(result.text))

            return "message could not be read"
         
         else:
            return result_message.text





   def copy_karar_icerik_panel(self):

         #self.copy_karar_icerik_panel = self.driver.execute_script("")
         self.copy_karar_icerik_panel = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "p[align='justify']")
            )
         )
         
         return self.copy_karar_icerik_panel



   def browser_quit(self):
      try:
         self.driver.quit()
      except:
         pass


   def refresh_captcha():
      pass

