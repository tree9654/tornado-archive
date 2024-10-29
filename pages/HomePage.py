import streamlit as st
import sqlite3
import pandas as pd
from func import pageButton, letMein

# เรียกใช้ func letMein
letMein()
# หัวข้อ และ หัวข้อย่อย
st.title("Welcome to :tornado: Tornado Archive")
st.markdown("**By 65363759 นายภัทร ทานิล & 65364466 นายวิชภู ตันตราทร**")

# เรียกใช้ pageButton
pageButton()
