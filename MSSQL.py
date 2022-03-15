from asyncio.windows_events import NULL
from datetime import date
import logging
import time
from Karar import Karar

import pandas as pd #veriyi düzenlemek için
import pyodbc       #MSSQL e bağlanmak için gerekli olam modül

class MSSQL:

   def __init__(self):
      
      self.serverName = "DESKTOP-KCCOUBH\SQLEXPRESS"
      self.databaseName = "yargitayKararlari"
      self.Trusted_Connection = "yes"

      self.conn = pyodbc.connect('Driver={SQL Server};'
                     'Server='   + self.serverName   + ';'
                     'Database=' + self.databaseName + ';'
                     'Trusted_Connection=' + self.Trusted_Connection + ';')

      self.cursor = self.conn.cursor()

      # sql_query = pd.read_sql_query('SELECT * FROM yargitayKararlari.dbo.tbl_karar', self.conn)

      # print(sql_query)
      # print(type(sql_query))

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
      result = self.cursor.execute("SELECT id_daire FROM yargitayKararlari.dbo.tbl_daire WHERE daire_ismi = ?", (daireName))
      try:
         result = result.fetchall()[0][0] #integer döner
      except:
         return NULL
      else:
         return result

   def isThereMahkemesi(self, mahkemesi):
      
      result = self.cursor.execute("SELECT id_mahkeme FROM yargitayKararlari.dbo.tbl_mahkemesi WHERE mahkeme_ismi = ? ", (mahkemesi))

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



