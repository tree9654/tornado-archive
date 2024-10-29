import streamlit as st
import sqlite3
import pandas as pd

#--------------------- ไฟล์เก็บ function ต่างๆ --------------------------

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect('tornado.db',check_same_thread=False)
cursor = conn.cursor()
#conn.commit()

# อ่านข้อมูลจากฐานข้อมูล โดยใช้ pandas
dfAll = pd.read_sql('SELECT * FROM tornado',conn)
dfYear = pd.read_sql('SELECT DISTINCT Year FROM tornado',conn)
dfMonth = pd.read_sql('SELECT month_num FROM month',conn)
dfSeason = pd.read_sql('SELECT tornado_season FROM tornadoSeason',conn)

# function เพิ่มข้อมูลเข้าฐานข้อมูล
def addData():
    # ป้าย
    st.markdown(":heavy_plus_sign: :green-background[**Add new record**]")
    
    # ช่องรับค่า input ต่างๆ
    year = st.number_input("Year (ค.ศ.)",min_value=1000, max_value=3000, value=None, placeholder="Type the year...")
    month = st.selectbox("Month", dfMonth, index=None, placeholder="Select the month..." )
    season = st.selectbox("Tornado Season (1 = before, 2 = early, 3 = mid, 4 = peak, 5 = end, 6 = after)", dfSeason, index=None, placeholder="Select number..." )
    killer = st.number_input("Killer Tornado in the month",min_value=0, max_value=1000)
    amount = st.number_input("Amount of Tornados in the month",min_value=0, max_value=2000)
    death = st.number_input("Death in the month",min_value=0, max_value=2000)

    # event เมื่อกดปุ่ม ADD
    if st.button("ADD"):
        cursor.execute('INSERT INTO tornado (Year, mouth_num, tornado_season, tornado_killer_count, tornado_amount, death_amount) VALUES (?, ?, ?, ?, ?, ?)', (year, month, season, killer, amount, death))
        conn.commit()
        st.success("Add new data successfully!")
#addData()

# function ลบข้อมูลออกจากฐานข้อมูล
def deleteData():
    # ป้าย
    st.markdown(":heavy_minus_sign: :red-background[**Delete record**]")
    
    # อ่านข้อมูลจากฐานข้อมูล
    dfDel = pd.read_sql('SELECT Year FROM tornado',conn)
    dfDel_year = dfDel
    dfDel_year['Year'] = dfDel['Year'].astype('int')
    max_year = dfDel_year["Year"].max()
    min_year = dfDel_year["Year"].min() 
    conn.commit()
    # ช่องรับค่า input ต่างๆ
    year_del = st.number_input("Year (ค.ศ.)",min_value=min_year, max_value=max_year, value=None, placeholder="Type the year...")
    month_del = st.selectbox("Month", dfMonth, index=None, placeholder="Select the month..." )

    # event เมื่อกดปุ่ม DELETE
    if st.button("DELETE"):
        cursor.execute('DELETE FROM tornado WHERE Year = ? AND mouth_num = ?', (year_del,month_del))
        conn.commit()
        st.success("Delete data successfully!")
#deleteData()

# function แก้ไขข้อมูลจากฐานข้อมูล
def updateData():
    # ป้าย
    st.markdown(":hash: :blue-background[**Update record**]")
    
    # อ่านข้อมูลจากฐานข้อมูล
    dfUp = pd.read_sql('SELECT Year FROM tornado',conn)
    dfUp_year = dfUp
    dfUp_year['Year'] = dfUp['Year'].astype('int')
    max_year = dfUp_year["Year"].max()
    min_year = dfUp_year["Year"].min()
    # ช่องรับค่า input ต่างๆ
    year_up = st.number_input("Year (ค.ศ.)",min_value=min_year, max_value=max_year, value=None, placeholder="Type the year...")
    month_up = st.selectbox("Month", dfMonth, index=None, placeholder="Select the month..." )
    new_season = st.selectbox("Tornado Season (1 = before, 2 = early, 3 = mid, 4 = peak, 5 = end, 6 = after)", dfSeason, index=None, placeholder="Select number..." )
    killer_up = st.number_input("Killer Tornado in the month",min_value=0, max_value=1000)
    amount_up = st.number_input("Amount of Tornados in the month",min_value=0, max_value=2000)
    death_up = st.number_input("Death in the month",min_value=0, max_value=2000)

    # event เมื่อกดปุ่ม UPDATE
    if st.button("UPDATE"):
        cursor.execute('UPDATE tornado SET tornado_season = ?, tornado_killer_count = ?, tornado_amount = ?, death_amount = ? WHERE Year = ? AND mouth_num = ?', (new_season, killer_up, amount_up, death_up, year_up, month_up))
        conn.commit()
        st.success("Update data successfully!")
#updateData()

# function แสดงตารางฐานข้อมูล
def dataTable():

    # อ่านข้อมูลจากฐานข้อมูล
    df1 = pd.read_sql("SELECT tornado.Year,month.month_name AS Month,tornado.tornado_season AS TornadoSeason,tornado.tornado_killer_count AS TornadoKiller,tornado.tornado_amount AS TornadoAmount,tornado.death_amount AS DeathCount FROM tornado LEFT JOIN month ON tornado.mouth_num = month.month_num", conn)#GROUP BY tornado.Year
    df2 = pd.read_sql("SELECT COUNT(*) AS Records FROM tornado",conn)
    record = df2.iloc[0,0]
    conn.commit()

    # สร้าง column ในการจัดการข้อมูล
    col1, col2 = st.columns(2)
    with col1:
        # ตารางแสดงฐานข้อมูล
        st.dataframe(df1.sort_values(by=['Year']),hide_index=True)
    with col2:
        # widget แสดงจำนวนข้อมูลทั้งหมด
        st.metric("Record Amount",value=record,delta=None, delta_color="normal")

# function ปุ่มเปลี่ยนหน้าต่าง
def pageButton():
    # สร้าง column ในการจัดการปุ่ม และลิ้งค์ไปอีกหน้าต่าง
    col01, col02, col03, col04, col05, col06 = st.columns(6)
    with col01:
        st.page_link("pages/HomePage.py", label="**Home**", icon="🏠")
    with col02:
        st.page_link("pages/addPage.py", label="**Add new record**", icon="➕")
    with col03:
        st.page_link("pages/deletePage.py", label="**Delete record**", icon="➖")
    with col04:
        st.page_link("pages/updatePage.py", label="**Update record**", icon="#️⃣")
    with col05:
        st.page_link("pages/dashPage.py", label="**Dashbroad**", icon="📈")
    with col06:
        # event เมื่อกดปุ่ม Log out
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.switch_page("pages/loginPage.py")

# function กันไม่ให้คนที่ยังไม่ได้ login เข้าสู่เว็บไซต์
def letMein():
    if not st.session_state.logged_in:
        st.switch_page("pages/loginPage.py")



# def metricChart():
#     cursor.execute('SELECT SUM(tornado_killer_count), SUM(tornado_amount), SUM(death_amount), MAX(Year) FROM tornado')
#     sum_killer, sum_amount, sum_death, max_year = cursor.fetchone()
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric("Killer Tornado",value=sum_killer,delta=None, delta_color="normal")
#     with col2:
#         st.metric("Tornado Amount",value=sum_amount,delta=None, delta_color="normal")
#     with col3:
#         st.metric("Death",value=sum_death,delta=None, delta_color="normal")
#     with col4:
#         st.metric("Latest Year",value=max_year,delta=None, delta_color="normal")

# def barChart():

#     dfB = pd.read_sql("SELECT tornado.Year,month.month_name AS Month,tornado.tornado_season AS TornadoSeason,tornado.tornado_killer_count AS TornadoKiller,tornado.tornado_amount AS TornadoAmount,tornado.death_amount AS DeathCount FROM tornado LEFT JOIN month ON tornado.mouth_num = month.month_num",conn)
    
#     #colA, colB, colC= st.columns([1,1,1])

#     st.subheader("Killer Tornado Chart")
#     st.bar_chart(dfB, x = "Year", y = "TornadoKiller", y_label = "Killer Tornado Count", color = "Month")
    
#     st.subheader("Tornado Amount Chart")
#     st.bar_chart(dfB, x = "Year", y = "TornadoAmount", y_label = "Tornado Amount", color = "Month")
    
#     st.subheader("Death Chart")
#     st.bar_chart(dfB, x = "Year", y = "DeathCount", y_label = "Death Count", color = "Month")

# def lineChart():
    # st.subheader("Line Chart")
    # dfL = pd.read_sql("SELECT tornado_killer_count, tornado_amount, death_amount FROM tornado",conn)
    # st.line_chart(dfL)