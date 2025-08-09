## 🩸 AI Blood Bank
### A Smart Platform to Connect Blood Donors with People in Need

AI Blood Bank is a cloud-ready, Python-based application built using Streamlit and SQLite.
It allows donor registration, real-time search by city & blood type, and automated email alerts to matching donors — helping save lives faster.
---

##  Features
- **Register as a Donor** – Securely store donor details in a database.
- **Search & Filter** – Find donors by **city** and **blood group**.
- **Email Alerts** – Notify matching donors via Gmail SMTP.
- **Responsive UI** – User-friendly interface with Streamlit.
- **Cloud Deployment** – Fully deployable on Streamlit Cloud.
- **Secure Secrets Management** – `.env` for local, `st.secrets` for cloud.

---

## 🛠 Tech Stack
- **Frontend & Backend:** Streamlit
- **Database:** SQLite
- **Email Service:** Gmail SMTP with App Password
- **Environment Management:** `.env` locally, `st.secrets` in Streamlit Cloud

---


##  About SQLite Database

This project uses **SQLite** as the backend database for storing donor information.  
SQLite is:
- **Lightweight** – No external server required.
- **File-based** – All data is stored in a single `.db` file.
- **Cross-platform** – Works on Windows, macOS, Linux without extra setup.
- **Easy to manage** – Can be explored with tools like [DB Browser for SQLite](https://sqlitebrowser.org/).

##  Database Schema
The `donors` table stores:
| Column       | Type    | Description                              |
|--------------|--------|------------------------------------------|
| `id`         | INTEGER | Primary Key (Auto-increment)             |
| `name`       | TEXT    | Donor's full name                        |
| `age`        | INTEGER | Donor's age                              |
| `blood_type` | TEXT    | Blood type (A+, O-, etc.)                 |
| `city`       | TEXT    | City where donor resides                 |
| `phone`      | TEXT    | Donor's phone number                     |

##  Location
- Local: Defined in `.env` → `SQLALCHEMY_DATABASE_URI=sqlite:///database.db`
- Cloud: Stored inside **Streamlit Secrets**

## Let's Connect
If you found this project useful or would like to collaborate on similar socially impactful ideas, feel free to reach out:

 **LinkedIn:** [Hovarthan S](https://www.linkedin.com/in/hovarthan-s-06114b281/)  
 **Email:** hovarthan04@gmail.com

---

