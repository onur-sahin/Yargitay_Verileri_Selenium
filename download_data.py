from asyncio.windows_events import NULL
from lib2to3.pgen2 import driver
import logging
import click
from numpy import compare_chararrays
from selenium.webdriver.common.keys import Keys
from myErrorList import captcha_refresh_is_error
import captcha
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from captcha_read import captcha_read
from my_tools import check_ping, control_panel, convert_title, get_mahkemesi, get_no, get_str_date, get_yil


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
from Karar import Karar

from MSSQL import MSSQL


from Driver import Driver



def download_data(year, restartCount, start_kararNo=-1, end_kararNo=-1, ):


   url1= "https://karararama.yargitay.gov.tr/YargitayBilgiBankasiIstemciWeb/"

   mssql = MSSQL(restartCount)

   driver1 = Driver(url1, restartCount)


   while(True):

      #check_ping()

      if( mssql.mssql_test() == False):

         mssql.mssql_close()
         
         mssql_connection_status = mssql.mssql_connect()

         if( mssql_connection_status == "quit" ):
            return "quit"

         elif( mssql_connection_status == "restart"):

            driver1.browser_quit()
            return "restart"

         else:
            pass

      else:
         pass
      

      
      driver1.connect_driver()

      # if(driver1.isActive == False):

      #    driver1.driver_close()

      #    driver_connection_status = driver1.connect_driver()

      #    if( driver_connection_status == "quit" ):
      #       return "quit"

      #    elif(driver_connection_status == True):
      #       pass

      #    elif(driver_connection_status == "restart"):
      #       return "restart"
      #  else:

      #    driver_connection_status = driver1.connect_driver()

      #    if( driver_connection_status == "quit" ):
      #       return "quit"

      #    elif(driver_connection_status == True):
      #       pass

      #    elif(driver_connection_status == "restart"):
      #       return "restart"


      last_karar = mssql.last_karar(year)

      if(last_karar == "quit"):
         return "quit"

      elif(last_karar == "restart"):

         driver1.browser_quit()
         return "restart"

      else:      #diğer durumlarda geçerli bir last_karar numarası gelmiştir
         pass

      if( start_kararNo > end_kararNo ):

         logging.error("başlangıç karar numarası bitişi karar numarasından büyük olamaz, programdan çıkılıyor")
         return "quit"
      
      if(start_kararNo == -1):

         if(end_kararNo >= last_karar):
            ilk_karar_no_input = last_karar

         else:
           return "finish"

      elif(start_kararNo >= 0):

         if(start_kararNo >= last_karar):
            ilk_karar_no_input = start_kararNo

         else:
            ilk_karar_no_input = last_karar

      else:

         logging.error("KARAR NUMARASI BAŞLANGIÇ değerinde HATA! -1 den küçük olamaz programdan çıkılıyor")

         return "quit"



      action = ActionChains(driver1.driver, 250)

      is_img_refresh = captcha.did_img_refresh(driver1)

      if(is_img_refresh == "restart"):
         driver1.browser_quit()
         return "restart"
      elif(is_img_refresh == "quit"):
         return "quit"

      error_count = 0

      try: # 1. try except

         if( is_img_refresh == True ):

            captcha.save_current_img(driver1)

         driver1.get_detayli_arama_we().location_once_scrolled_into_view
         time.sleep(0.1)

         driver1.get_detayli_arama_we().click()
         time.sleep(0.1)


         driver1.get_captcha_input_we().location_once_scrolled_into_view
         time.sleep(0.1)
         
        

         captcha_code = captcha_read(str(captcha.get_last_img_number()), driver1)

         if( captcha_code == "quit"):
            return "quit"

         elif(captcha_code == "restart"):
            raise captcha_refresh_is_error
         
         action.send_keys_to_element(driver1.get_captcha_input_we(), captcha_code)

         action.perform()


         driver1.get_karar_yili_we().location_once_scrolled_into_view

     
         driver1.get_karar_yili_we().send_keys(str(year))

         # driver1.get_tarih_bas_we().location_once_scrolled_into_view
        
         # driver1.get_tarih_bas_we().send_keys(get_str_date(start_date))
         

         # driver1.get_tarih_son_we().location_once_scrolled_into_view
         # time.sleep(1)
         # driver1.get_tarih_son_we().send_keys(get_str_date(end_date))


         driver1.get_radio_button_karar_we()[0].location_once_scrolled_into_view
         driver1.get_radio_button_karar_we()[0].click()

         driver1.get_son_karar_no_input_we().location_once_scrolled_into_view

         try:
            WebDriverWait(driver1.driver, 10).until(
               EC.element_to_be_clickable(
                  (By.CSS_SELECTOR, "input[id='aramaForm:ilkKararNoInput']")
               )
            )
         except Exception as err:
            logging.error("ilk karar numarasını girerken hata!: " + str(err))
            driver1.browser_quit()
            return "restart"
         
         time.sleep(1)

         driver1.get_ilk_karar_no_input_we().send_keys( str(ilk_karar_no_input) )
         time.sleep(0.1)


         driver1.get_radio_button_karar_we()[1].location_once_scrolled_into_view
         time.sleep(0.1)
         driver1.get_radio_button_karar_we()[1].click()
         time.sleep(0.1)


         try:
            WebDriverWait(driver1.driver, 10).until(
               EC.element_to_be_clickable(
                  (By.CSS_SELECTOR, "input[id='aramaForm:sonKararNoInput']")
               )
            ).send_keys( str(end_kararNo) )

            time.sleep(0.1)

         except Exception as err:
            logging.error("son karar numarasını girerken hata!: " + str(err))
            driver1.browser_quit()
            return "restart"


         driver1.get_search_we().location_once_scrolled_into_view
         time.sleep(0.1)
         

         driver1.get_search_we().send_keys(Keys.RETURN)
         time.sleep(1)

         

      except Exception as err:

         error_count += 1

         logging.error( "download_data() 1. try except hata!: " + str(err) )

         if(restartCount[0] == 1 and error_count == 5):

            logging.error("1. try except hata!: " + str(err))

            x = control_panel(str(err))

            if(x == "resume"):

               error_count = 0
               driver1.browser_quit()
               continue
            
            elif(x == "restart"):
               
               driver1.browser_quit()
               return "restart"
            
            elif(x == "quit"):
               return "quit"

         elif(restartCount[0] == 0 and error_count == 5):
            driver1.browser_quit()
            return "restart"

         else:
            driver1.browser_quit()
            continue


      try:
         result_sonucTable = driver1.is_there_sonucTable_head()

      except Exception as err:

         error_count += 1

         logging.warning( "\nis_there_sonucTable_head() hata!:{}".format(err) )

         message = driver1.is_there_message()

         if(message == NULL):

            logging.error("is_there_sonucTable_head() fonksiyonu içerisinde is_there_message() fonksiyonundan geriye mesaj web elementinin olmadığı hatası alındı.")

            if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):
                  driver1.browser_quit()
                  continue
               
               elif(x == "restart"):
                  driver1.browser_quit()
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"

            driver1.browser_quit()
            return "restart"
            
         elif(message == "message could not be read"):

            logging.error( "(2. try except) mesaj kutusu var ancak mesaj okunamadı, hata!" + str(err)  )

            if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):
                  driver1.browser_quit()
                  continue
               
               elif(x == "restart"):
                  driver1.browser_quit()
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"

            driver1.browser_quit()
            return "restart"

         elif(convert_title(message) == "Sonuç Bulunamadı!"):

            if( restartCount[0] == 1):

               x = control_panel( str(err) )

               if(x == "resume"):
                  driver1.browser_quit()
                  continue
               
               elif(x == "restart"):
                  driver1.browser_quit()
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"
            
            driver1.browser_quit()
            return "restart"

         elif(convert_title(message) == "Güvenlik Kodunu Kontrol Ediniz!"):
            return "restart"

         else:

            if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):

                  driver1.browser_quit()
                  continue
               
               elif(x == "restart"):
                  driver1.browser_quit()
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"


            else:
               driver1.browser_quit()
               return "restart"



      try:

         if( driver1.click_to_last_tab() == False):
            raise Exception("3. try da click_to_last_tab() hata alındı")
         
         time.sleep(1)

         


      except Exception as err:

         logging.error("(3. try except) hata" + str(err))

         if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):
                  driver1.browser_quit()
                  continue
               
               elif(x == "restart"):
                  driver1.browser_quit()
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"

         driver1.browser_quit()
         return "restart"


      while(True):

         try:
            count_element = driver1.driver.execute_script("return document.getElementById(\"aramaForm:sonucTable_data\").childElementCount")
         except:
            pass
         
         for i in range (0, 5):

            try:
               row_elements = driver1.driver.execute_script("return document.getElementById(\"aramaForm:sonucTable_data\").childNodes")

               break

            except BaseException as err:
               logging.error("row_elements script execute edilmedi" + str(err))

               if(i == 4):
                  return "restart"

         list = []

         for web_element in row_elements:
            list.append(    int(  web_element.get_attribute("data-ri")  )    )

         list.sort()



         for i in range(list[0], list[-1]+1 ):


            data_ri = driver1.get_data_ri_we(i).find_elements(By.CSS_SELECTOR, "td[role='gridcell']")

            sira     = data_ri[0].text
            daire    = data_ri[1].text

            esas     = data_ri[2].text
            esasNo   = get_no(esas)
            esasYil  = get_yil(esas)
            
            karar    = data_ri[3].text
            kararNo  = get_no(karar)
            kararYil = get_yil(karar)
            k_tarih  = data_ri[4].text

            
            
            data_ri_click_result = driver1.data_ri_click(i)
            
            if(data_ri_click_result == False):

               logging.error(str(i) + ". satıra tıklanamadı!")

               if( restartCount[0] == 1):

                  while (True):

                     x = control_panel( str(err) )

                     if(x == "resume"):
                        print("for döngüsü içersinde resume seçeneği seçilemez!!")
                        continue
                     
                     elif(x == "restart"):
                        driver1.browser_quit()
                        return "restart"
                     
                     elif(x == "quit"):
                        return "quit"

               driver1.browser_quit()
               return "restart"

            
            
            try:
               icerik = driver1.copy_karar_icerik_panel()
            except BaseException as err:

               logging.error("data_ri_click("+str(i)+") tıklama başarılı ancak kopyalama başarısız\n" + str(err))

               if( restartCount[0] == 1):

                  while (True):

                     x = control_panel( str(err) )

                     if(x == "resume"):
                        print("for döngüsü içersinde resume seçeneği seçilemez!!")
                        continue
                     
                     elif(x == "restart"):
                        driver1.browser_quit()
                        return "restart"
                     
                     elif(x == "quit"):
                        return "quit"

               driver1.browser_quit()
               return "restart"

            else:

               metin = icerik.get_attribute("innerHTML")

               mahkemesi = get_mahkemesi(metin)
               
               karar = Karar(daire, k_tarih, kararYil, kararNo, esasYil, esasNo, mahkemesi, metin)

               karar.karar_print(False)

               save_status = mssql.save(karar)

               if(save_status == False):

                  if( restartCount[0] == 1):

                     while (True):

                        x = control_panel( str(err) )

                        if(x == "resume"):
                           print("for döngüsü içersinde resume seçeneği seçilemez!!")
                           continue
                        
                        elif(x == "restart"):
                           driver1.browser_quit()
                           return "restart"
                        
                        elif(x == "quit"):
                           return "quit"

                  driver1.browser_quit()
                  return "restart"



               restartCount[0] = 0  #Eğer bir restart sonrası bir belge başarı
                                    #ile kaydedilebilirse restartCount sıfırlandı
            



         

         click_to_previous_tab_result = driver1.click_to_previous_tab()

            

         if( click_to_previous_tab_result == "finish"):
            return "finish"

         elif(click_to_previous_tab_result == True):
            pass

         elif(click_to_previous_tab_result == "restart"):
            driver1.browser_quit()
            return "restart"





