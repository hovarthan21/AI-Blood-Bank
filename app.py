import streamlit as st
import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_URI = os.getenv("SQLALCHEMY_DATABASE_URI")  
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


if DB_URI.startswith("sqlite:///"):
    DB_PATH = DB_URI.replace("sqlite:///", "")
else:
    st.error("❌ Only SQLite DB is supported in this version.")
    st.stop()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    blood_type TEXT,
                    city TEXT,
                    phone TEXT
                )''')
    conn.commit()
    conn.close()

def add_donor(name, age, blood_type, city, phone):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO donors (name, age, blood_type, city, phone) VALUES (?, ?, ?, ?, ?)",
              (name, age, blood_type.upper(), city.title(), phone))
    conn.commit()
    conn.close()

def search_donors(city="", blood_type=""):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT name, age, blood_type, city, phone FROM donors WHERE 1=1"
    params = []
    if city:
        query += " AND LOWER(city) LIKE ?"
        params.append(f"%{city.lower()}%")
    if blood_type:
        query += " AND blood_type LIKE ?"
        params.append(f"%{blood_type.upper()}%")
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def send_email(to_email, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(EMAIL_USER, to_email, email_message)
        server.quit()
        st.success(f"📩 Email sent to {to_email}")
    except Exception as e:
        st.error(f"Email error: {e}")

init_db()


st.set_page_config(page_title="AI Blood Bank", page_icon="🩸", layout="wide")
menu = st.sidebar.radio("📍 Navigation", ["Register as Donor", "Search Donors"])


st.markdown(
    """
    <h1 style='text-align: center; font-size: 50px; color: #d62828; margin-bottom: 0;'>
        🩸 AI Blood Bank
    </h1>
    """,
    unsafe_allow_html=True
)


if menu == "Register as Donor":
    st.markdown(
        """
        <h3 style='text-align: center; color: gray; margin-top: 5px;'>
             Register as a Blood Donor
        </h3>
        <hr style='margin-top: 10px; margin-bottom: 20px;'>
        """,
        unsafe_allow_html=True
)
elif menu == "Search Donors":
    st.markdown(
        """
        <h3 style='text-align: center; color: gray; margin-top: 5px;'>
            🔍 Search for Blood Donors
        </h3>
        <hr style='margin-top: 10px; margin-bottom: 20px;'>
        """,
        unsafe_allow_html=True
    )

if menu == "Register as Donor":
    with st.form("register_form"):
          name = st.text_input("Full Name")
          age = st.number_input("Age", min_value=18, max_value=65, step=1)
          blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
          city = st.text_input("City")
          phone = st.text_input("Phone Number")
          submit = st.form_submit_button("Register")

    if submit:
        if name and city and phone:
            add_donor(name, age, blood_type, city, phone)
            st.success(f"✅ {name} registered successfully as a donor!")
        else:
            st.error("⚠️ Please fill all required fields.")


elif menu == "Search Donors":
    st.markdown('<p class="big-title">🔍 Search for Blood Donors</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        search_city = st.text_input("Enter City Name")
    with col2:
        search_blood = st.text_input("Enter Blood Type (e.g., A+, O-)")

    if st.button("Search"):
        results = search_donors(search_city, search_blood)
        if not results.empty:
            st.success(f"Found {len(results)} matching donors.")
            st.dataframe(results, use_container_width=True)

            with st.expander("📧 Send Email to All Found Donors"):
                subject = st.text_input("Email Subject")
                message = st.text_area("Email Message")
                if st.button("Send Email"):
                    for _, donor in results.iterrows():
                        send_email(donor['email'], subject, message)
        else:
            st.warning("No donors found matching your criteria.")

