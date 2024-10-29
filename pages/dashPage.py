import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from func import pageButton , letMein, dataTable #,filters

# เรียกใช้ letMein
letMein()
# หัวข้อ
st.title("DashBoard")
# เรียกใช้ pageButton
pageButton()

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect('tornado.db',check_same_thread=False)
cursor = conn.cursor()
conn.commit()

# อ่านข้อมูลจากฐานข้อมูลมาเตรียมไว้ใช้
dfAll = pd.read_sql("SELECT tornado.Year,month.month_name AS Month,tornado.tornado_season AS TornadoSeason,tornado.tornado_killer_count AS TornadoKiller,tornado.tornado_amount AS TornadoAmount,tornado.death_amount AS DeathCount FROM tornado LEFT JOIN month ON tornado.mouth_num = month.month_num",conn)
dfYear = pd.read_sql('SELECT DISTINCT Year FROM tornado',conn)
dfMonthN = pd.read_sql('SELECT month_name FROM month',conn)
dfSeason = pd.read_sql('SELECT tornado_season FROM tornadoSeason',conn)

# สร้าง filters แบบหลายตัว
year_filt = st.multiselect("Select the Year", options = dfYear, default = dfYear)
month_filt = st.multiselect("Select the month", options = dfMonthN, default = dfMonthN)
season_filt = st.multiselect("Select the season", options = dfSeason, default = dfSeason)
df_select = dfAll.query(
    "Year == @year_filt & Month == @month_filt & TornadoSeason == @season_filt" 
)

# ทำ Drill-Down
drill_level = st.selectbox("**Select drill level**", ('Year','Month'))

def drill_down_data(level):
    if level == 'Year':
        return df_select.groupby('Year').agg({'TornadoKiller': 'sum', 'TornadoAmount':'sum','DeathCount':'sum'}).reset_index()
    elif level == 'Month':
        return df_select.sort_values(by=['Year'])
   
# แสดงข้อมูลตารางตามระดับที่ผู้ใช้เลือก
drilled_data = drill_down_data(drill_level)
st.write(f"Drill Level: {drill_level}")
st.dataframe(drilled_data,hide_index=True)

# MetricChart()
sum_killer = df_select['TornadoKiller'].sum()
sum_amount = df_select['TornadoAmount'].sum()
sum_death = df_select['DeathCount'].sum()
dfmax = df_select
dfmax['Year'] = dfmax['Year'].astype('int')
max_year = dfmax['Year'].max()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Killer Tornado",value=sum_killer,delta=None, delta_color="normal")
with col2:
    st.metric("Tornado Amount",value=sum_amount,delta=None, delta_color="normal")
with col3:
    st.metric("Death",value=sum_death,delta=None, delta_color="normal")
with col4:
    st.metric("Latest Year",value=max_year,delta=None, delta_color="normal")


# TOP 5
colA, colB, colC = st.columns(3)
with colA:
    st.markdown(":orange[**TOP 5**] :blue-background[Killer Tornado]")
    dfKill = dfAll[['Year','Month','TornadoSeason','TornadoKiller']].sort_values(by='TornadoKiller',ascending=False)
    st.dataframe(dfKill.head(5),hide_index=True)
with colB:
    st.markdown(":orange[**TOP 5**] :green-background[Tornado Amount]")
    dfAmo = dfAll[['Year','Month','TornadoSeason','TornadoAmount']].sort_values(by='TornadoAmount',ascending=False)
    st.dataframe(dfAmo.head(5),hide_index=True)
with colC:
    st.markdown(":orange[**TOP 5**] :red-background[Death Count]")
    dfDeath = dfAll[['Year','Month','TornadoSeason','DeathCount']].sort_values(by='DeathCount',ascending=False)
    st.dataframe(dfDeath.head(5),hide_index=True)

# Bar Chart
st.subheader("Killer Tornado Chart")
st.bar_chart(df_select, x = "Year", y = "TornadoKiller", y_label = "Killer Tornado Count", color = "Month" ,stack=False) #"Month"
    
st.subheader("Tornado Amount Chart")
st.bar_chart(df_select, x = "Year", y = "TornadoAmount", y_label = "Tornado Amount", color = "Month",stack=False)
    
st.subheader("Death Chart")
st.bar_chart(df_select, x = "Year", y = "DeathCount", y_label = "Death Count", color = "Month",stack=False)

# Line Chart
st.subheader("Line Chart")
dfL = pd.read_sql("SELECT tornado_killer_count, tornado_amount, death_amount FROM tornado",conn)
st.line_chart(dfL)
