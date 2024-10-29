import streamlit as st
import sqlite3
import pandas as pd
from func import addData, dataTable, pageButton, letMein

# เรียกใช้ letMein
letMein()
# หัวข้อ
st.title("Add New Record")
# เรียกใช้ pageButton
pageButton()

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect('tornado.db',check_same_thread=False)
cursor = conn.cursor()
conn.commit()

# อ่านข้อมูลจากฐานข้อมูล
dfMonth = pd.read_sql('SELECT month_num FROM month',conn)
dfSeason = pd.read_sql('SELECT tornado_season FROM tornadoSeason',conn)

# เรียกใช้ function เพื่อเพิ่มข้อมูลและแสดงตาราง
addData()
dataTable()

conn.close()