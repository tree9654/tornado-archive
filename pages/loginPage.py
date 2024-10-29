import streamlit as st
import sqlite3

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect('users.db')
c = conn.cursor()

# สร้างตาราง ถ้ายังไม่มีตาราง
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

# เพิ่ม user เข้าฐานข้อมูล
def add_user(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
    conn.commit()

# ตรวจการ login
def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

# Main
def main():
    # หัวข้อ
    st.title("Login to Website")

    # เริ่ม session state สำหรับตรวจสอบการ login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # ถ้า login อยู่แล้ว
    if st.session_state.logged_in:
        st.success(f"Welcome {st.session_state.username}!")
        st.switch_page("pages/HomePage.py")
        st.write("This is the main content of the web app. Only logged-in users can see this.")
    
    else:
        # สร้างกล่องกรอกข้อมูล
        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')

        # lihk ปุ่ม Login และ event
        if st.button("Login"):
            create_usertable()
            result = login_user(username, password)
            # กรอกถูก
            if result:
                st.success(f"Welcome {username}!")
                st.info("Click again to go to Home Page!")
                st.session_state.logged_in = True
                st.session_state.username = username
            # กรอกผิด
            else:
                st.warning("Invalid Username/Password")

        # ลงทะเบียน
        with st.expander("Sign Up"):
            new_user = st.text_input("New Username")
            new_password = st.text_input("New Password", type='password')

            if st.button("Sign Up"):
                create_usertable()
                add_user(new_user, new_password)
                st.success("You have successfully created a valid account")
                st.info("Go to Login Menu to login")

main()