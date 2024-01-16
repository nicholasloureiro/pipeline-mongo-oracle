import os

import cx_Oracle
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
service = os.getenv('DB_SERVICE')

dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)

cursor = conn.cursor()

df_products = pd.read_csv('/home/nicholas10/DE_ALURA/data/table_products.csv')

cursor.execute(""" 
DECLARE 
  tbl_count NUMBER; 
BEGIN  
  SELECT COUNT(*) INTO tbl_count FROM user_tables WHERE table_name = 'PRODUCTS';   
  IF tbl_count = 0 THEN 
    EXECUTE IMMEDIATE 'CREATE TABLE PRODUCTS (
   numrow INT,
   id VARCHAR(100) PRIMARY KEY,
   Product VARCHAR(100),
   Category VARCHAR(100),
   Price FLOAT,
   Freight FLOAT,
   Buy_date VARCHAR(100),
   Salesperson VARCHAR(100),
   City VARCHAR(100),
   Sales_rating INT,
   Pay_method VARCHAR(100),
   Installment_quantity INT,
   latitude FLOAT,
   longitude FLOAT
    )';               
  END IF; 
END;

""")

data = [tuple(row) for i, row in df_products.iterrows()]

print(data)

cursor.executemany("INSERT INTO PRODUCTS VALUES (:0,:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)", data)

conn.commit()