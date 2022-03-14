import pandas as pd
from Karar import Karar

from MSSQL import MSSQL

karar = Karar("w", "11/11/2021", 2021, 123, 2022, 124, "nn", "rrrrrrrrrrrrrrrrr")
mssql = MSSQL()

#print(mssql.isThereDaire("d"))
#print(mssql.insertDaire("rrrry"))
#print(mssql.isThereMahkemesi("rrrrx"))
print(mssql.save(karar))
# sql_query = pd.read_sql_query('SELECT * FROM yargitayKararlari.dbo.tbl_karar', mssql.conn)

# print(sql_query)
# print(type(sql_query))



