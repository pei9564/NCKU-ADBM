import pyodbc
import pandas as pd


DRIVER = 'ODBC Driver 17 for SQL Server'
SERVER = 'LAPTOP-V7M8IDF4'
DATABASE = 'AMDB'
UID = 'sa'
PWD = 'test1234'

business_db = pd.read_csv('business_table.csv', encoding='utf-8').head(100)
disposal_db = pd.read_csv('disposal_table.csv', encoding='utf-8').head(100)
law_db = pd.read_csv('law_table.csv', encoding='utf-8').head(100)

connection_string = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD}'
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# 逐筆新增資料至事業table
for index, row in business_db.iterrows():
    business_id = row['事業id']
    business = row['事業']
    cursor.execute("INSERT INTO 事業 (事業id, 事業) VALUES (?, ?)", business_id, business)
    connection.commit()

# 逐筆新增資料至法規table
# for index, row in law_db.iterrows():
#     law_id = row['法規id']
#     law = row['法規']
#     law_type = row['法規類別']
#     cursor.execute("INSERT INTO 法條 (法條id, 法規法條, 類別) VALUES (?, ?, ?)", law_id, law, law_type)
#     connection.commit()

# 逐筆新增資料至處分table
# for index, row in disposal_db.iterrows():
#     disposal_id = row['處分id']
#     # print('處分id', type(disposal_id))
#     business_id = row['事業id']
#     # print('事業id',type(business_id))
#     law_id = row['法規id']
#     # print(type(law_id))
#     disposal_amount = int(row['處分金額'])
#     # print(type(disposal_amount))
#     disposal_date = row['處分日期']
#     # print(type(disposal_date))
#     disposal_content = str(row['處分內容'])
#     # print(disposal_content)
#     cursor.execute("INSERT INTO 處分 (處分id, 事業id, 法條id, 處分金額, 處分日期, 處分內容) VALUES (?, ?, ?, ?, ?, ?)", disposal_id, business_id, law_id, disposal_amount, disposal_date, disposal_content)
#     connection.commit()

# 關閉 cursor 和連接
cursor.close()
connection.close()
