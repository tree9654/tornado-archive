import streamlit as st
import sqlite3
import pandas as pd

# ตั้งค่ารูปแบบหน้าต่าง
st.set_page_config(page_title='Tornado',page_icon=':tornado:',layout='wide',initial_sidebar_state = 'collapsed')

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect('tornado.db',check_same_thread=False)
cursor = conn.cursor()
conn.commit()

# อ่านข้อมูลจากฐานข้อมูล โดยใช้ pandas
dfMonth = pd.read_sql('SELECT month_num FROM month',conn)
dfSeason = pd.read_sql('SELECT tornado_season FROM tornadoSeason',conn)

# ตั้งค่าหน้าต่างของ streamlit
loginPage = st.Page(
    page = "pages/loginPage.py",
    title = "Login",
    icon = "📝",
    default = True
)
HomePage = st.Page(
    page = "pages/HomePage.py",
    title = "Home",
    icon = "🏠"
    #default = True
)
addPage = st.Page(
    page = "pages/addPage.py",
    title = "Add New Record",
    icon = "➕"
)
deletePage = st.Page(
    page = "pages/deletePage.py",
    title = "Delete Record",
    icon = "➖"
)
updatePage = st.Page(
    page = "pages/updatePage.py",
    title = "Update Record",
    icon = "#️⃣"
)
dashPage = st.Page(
    page = "pages/dashPage.py",
    title = "DashBoard",
    icon = "📈"
)

# เพิ่ม logo ที่ sidebar จากไฟล์ assets
st.logo("assets/list.png",size = "large")

# run ตัวจัดการหน้าต่าง
pg = st.navigation(pages=[loginPage,HomePage,addPage,deletePage,updatePage,dashPage])
pg.run()




