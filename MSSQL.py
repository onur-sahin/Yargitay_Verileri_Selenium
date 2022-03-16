from asyncio.windows_events import NULL
from datetime import date
from distutils.log import error
import logging
from posixpath import curdir
import time
from Karar import Karar

import pandas as pd #veriyi düzenlemek için
import pyodbc#MSSQL e bağlanmak için gerekli olam modül

from my_tools import control_panel, convert_all_uppercase, convert_title  


class MSSQL:

   def __init__(self):
      
      self.serverName = "DESKTOP-KCCOUBH\SQLEXPRESS"
      self.databaseName = "yargitayKararlari"
      self.Trusted_Connection = "yes"

      # sql_query = pd.read_sql_query('SELECT * FROM yargitayKararlari.dbo.tbl_karar', self.conn)

      # print(sql_query)
      # print(type(sql_query))

   def mssql_close(self):

      try:
         self.cursor.close()
      except:
         pass

      try:
         self.conn.close()
      except:
         pass


   def mssql_connect(self):

      error_count = 0

      while(True):

         try:

            self.conn = pyodbc.connect('Driver={SQL Server};'
                           'Server='   + self.serverName   + ';'
                           'Database=' + self.databaseName + ';'
                           'Trusted_Connection=' + self.Trusted_Connection + ';')

            self.cursor = self.conn.cursor()

         except BaseException as err:

            logging.warning("mssql'e bağlantıda hata" + str(error_count) + ". defa bağlanmaya çalışılıyor:" + str(err))
            
            time.sleep(5)
            
            error_count += 1
            
            logging.error("mssql 'bağlantıda hata!: " + str(err))

            if(error_count == 5):

               x = control_panel()

               if(x == "quit"):
                  return "quit"

               elif(x == "resume"):
                  error_count = 0
                  continue

         else:

            return True
         

   def last_karar(self, year):

      error_count = 0

      while(True):

         query_text = 'SELECT TOP 1 *  FROM tbl_karar WHERE karar_yil={} ORDER BY karar_no DESC'.format(year)

         try:
            result = self.cursor.execute( query_text )

         except BaseException as err:

            logging.warning("mssql last_karar() fonksiyonunda hata!" + str(error_count) + ". deneme: " + str(err) )

            error_count += 1

            time.sleep(5)

            if(error_count == 5):

               logging.error("last_karar(self) fonksiyonunda hata!: " + str(err))

               self.mssql_close()

               mssql_connection_status = self.mssql_connect()

               if( mssql_connection_status == True):
                  continue

               elif(mssql_connection_status == "quit"):
                  return "quit"

            elif(error_count == 6):

               x = control_panel()

               if(x == "resume"):
                  
                  error_count = 0
                  continue

               elif(x == "quit"):
                  return "quit"


         else:

            if ( result.rowcount == 0 ) :
               return NULL

            return result.__next__()[5] #karar no sütunu


   def save(self, karar):
      self.karar = karar

      id_daire = self.isThereDaire( karar.daire)

      if(id_daire == NULL):
         id_daire = self.insertDaire(karar.daire)

      id_mahkeme = self.isThereMahkemesi(karar.mahkemesi)

      if(id_mahkeme == NULL):
         id_mahkeme = self.insertMahkeme(karar.mahkemesi)
      
      if(id_daire != NULL and id_mahkeme != NULL):

         sonuc = self.isThereKarar(karar)

         if(sonuc != NULL):
            logging.warning("kayıtlı bir karar kaydedilmeye çalışıldı")
            return True

         karar.esasYil = int(karar.esasYil)
         karar.esasNo  = int(karar.esasNo)
         karar.kararYil= int(karar.kararYil)
         karar.kararNo = int(karar.kararNo)

         karar.tarih   = time.strptime (karar.tarih, '%d.%m.%Y')
         k_tarih_str   = str(karar.tarih.tm_year) + "." +str(karar.tarih.tm_mon) + "." + str(karar.tarih.tm_mday)

         sonuc = self.cursor.execute('''INSERT INTO yargitayKararlari.dbo.tbl_karar
                                             (daire,
                                             esas_yil,
                                             esas_no,
                                             karar_yil,
                                             karar_no,
                                             tarih,
                                             mahkemesi,
                                             metin
                                             ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                             (id_daire,
                                             karar.esasYil,
                                             karar.esasNo,
                                             karar.kararYil,
                                             karar.kararNo,
                                             k_tarih_str,
                                             id_mahkeme,
                                             karar.metin
                                             )        )

         self.conn.commit()
         time.sleep(1)

         return True
      else:
         return False

   def isThereDaire(self, daireName):
      try:
         result = self.cursor.execute("SELECT id_daire FROM yargitayKararlari.dbo.tbl_daire WHERE daire_ismi = ?", (  convert_title(daireName)   )   )
      except BaseException as err:
         logging.error("isThereDaire() fonksiyonu mssql query hatası!:" + str(err))

         ##################################x
         #buraya hata ile ilgili kurtarma yazılacak


      try:
         result = result.fetchall()[0][0] #integer döner
      except:
         return NULL
      else:
         return result

   def isThereMahkemesi(self, mahkemesi):

      result = self.cursor.execute("SELECT id_mahkeme FROM yargitayKararlari.dbo.tbl_mahkemesi WHERE mahkeme_ismi = ? ", (convert_all_uppercase(mahkemesi)))

      try:
         result = result.fetchall()[0][0] #integer döner
      except:
         return NULL
      else:
         return result

   def isThereKarar(self, karar):
      result = self.cursor.execute(
         '''SELECT id FROM yargitayKararlari.dbo.tbl_karar WHERE
            daire = ? and esas_yil = ? and esas_no = ? and karar_yil = ? and karar_no = ?''',
            (self.isThereDaire(karar.daire), karar.esasYil, karar.esasNo, karar.kararYil, karar.kararNo))
      try:
         result = result.fetchall()[0][0] #integer döner
      except:
         return NULL
      else:
         return result


   def insertDaire(self, daireName):

      if(self.isThereDaire(daireName) != NULL):
         return NULL

      result = self.cursor.execute("INSERT INTO yargitayKararlari.dbo.tbl_daire(daire_ismi) VALUES(?);", (daireName) )
      self.conn.commit()
      time.sleep(1)

      result = self.isThereDaire(daireName)
      if(result == NULL):
         return NULL
      else:
         return result

   def insertMahkeme(self, mahkemeName):

      if(self.isThereMahkemesi(mahkemeName) != NULL):
         logging.warning("varolan bri mahkeme kaydedilmeye çalışıldı")
         return NULL
         
      result = self.cursor.execute("INSERT INTO yargitayKararlari.dbo.tbl_mahkemesi(mahkeme_ismi) VALUES(?);", (mahkemeName) )
      self.conn.commit()
      time.sleep(1)

      result = self.isThereMahkemesi(mahkemeName)

      if(result == NULL):
         return NULL
      else:
         return result



