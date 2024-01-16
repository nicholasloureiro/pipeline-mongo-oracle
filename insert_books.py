import cx_Oracle
import pandas as pd
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Get database credentials from environment variables
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
service = os.getenv('DB_SERVICE')

dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)


cursor = conn.cursor()

df_books = pd.read_csv('/home/nicholas10/DE_ALURA/data/table_books.csv')

cursor.execute(""" 
DECLARE 
  tbl_count NUMBER; 
BEGIN  
  SELECT COUNT(*) INTO tbl_count FROM user_tables WHERE table_name = 'BOOKS';   
  IF tbl_count = 0 THEN 
    EXECUTE IMMEDIATE 'CREATE TABLE BOOKS (
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

data = [tuple(row) for i, row in df_books.iterrows()]

print(data)

cursor.executemany("INSERT INTO BOOKS VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)", data)

conn.commit()