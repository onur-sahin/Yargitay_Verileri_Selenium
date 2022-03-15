
class Karar:

   def __init__(self):
      self.id = -1
      self.daire
      self.tarih
      self.kararYil
      self.kararNo
      self.esasYil
      self.esasNo
      self.mahkemesi
      self.metin

   def __init__(self, daire, tarih, kararYil, kararNo, esasYil, esasNo, mahkemesi, metin):
      self.id = -1
      self.daire = daire
      self.tarih = tarih
      self.kararYil = kararYil
      self.kararNo = kararNo
      self.esasYil = esasYil
      self.esasNo = esasNo
      self.mahkemesi = mahkemesi
      self.metin = metin


   def karar_print(self):
      print("id       = ", self.id, "\n",
            "daire    = ", self.daire, "\n",
            "tarih    = ", self.tarih, "\n",
            "kararYil = ", self.kararYil, "\n",
            "kararNo  = ", self.kararNo, "\n",
            "esasYil  = ", self.esasYil, "\n",
            "esasNo   = ", self.esasNo, "\n",
            "mahkemesi= ", self.mahkemesi, "\n",
            "metin    = ", self.metin, "\n",
            )


