import streamlit as st
import requests
import pandas as pd
import time

BASE_URL = "http://127.0.0.1:8000"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="JeevanMed ERP",
    page_icon="🏥",
    layout="wide"
)

# ================= SESSION STATE =================
if "token" not in st.session_state:
    st.session_state.token = None

headers = {}
if st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}


# ================= SAFE HELPERS =================
def safe_df(data):
    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.DataFrame([data])
    return pd.DataFrame()


def api_get(url):
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        st.error(res.text)
        return None
    return res.json()


def api_post(url, payload, form=False):
    if form:
        res = requests.post(url, data=payload)
    else:
        res = requests.post(url, json=payload, headers=headers)

    if res.status_code not in [200, 201]:
        st.error(res.text)
        return None

    return res.json()


# ================= HEADER =================
st.markdown(
    """
    <h1 style='text-align:center; color:#1F618D;'>🏥 JeevanMed Hospital ERP</h1>
    <hr>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "📌 Navigation",
    ["Dashboard", "Patients", "Invoices", "Transactions", "Analytics", "Login", "Signup"]
)

# ================= LOGOUT =================
if st.sidebar.button("🚪 Logout"):
    st.session_state.token = None
    st.success("Logged out successfully")
    st.stop()


# =========================================================
# 🔐 SIGNUP
# =========================================================
if menu == "Signup":
    st.subheader("📝 Create Account")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Username")
        email = st.text_input("Email")
        contact = st.text_input("Contact Number")

    with col2:
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        res = api_post(f"{BASE_URL}/auth/signup", {
            "username": username,
            "email": email,
            "contact_number": contact,
            "full_name": full_name,
            "password": password,
            "confirm_password": confirm
        })

        if res:
            st.success("Account created successfully ✅")


# =========================================================
# 🔐 LOGIN (FIXED)
# =========================================================
elif menu == "Login":
    st.subheader("🔐 Login to JeevanMed")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = api_post(
            f"{BASE_URL}/auth/token",
            {"username": username, "password": password},
            form=True
        )

        if res and "access_token" in res:
            st.session_state.token = res["access_token"]

            # ✅ SHOW MESSAGE BEFORE RERUN
            st.success("Login successful ✅ Welcome to JeevanMed!")

            # small delay so user sees message
            time.sleep(1)

            st.rerun()

        else:
            st.error("Invalid credentials ❌")


# =========================================================
# 📊 DASHBOARD
# =========================================================
elif menu == "Dashboard":
    st.subheader("📊 Hospital Overview")

    data = api_get(f"{BASE_URL}/analytics/summary")

    if data:
        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Invoices", data["total_invoices"])
        c2.metric("Revenue", f"₹ {data['total_revenue']}")
        c3.metric("Pending", f"₹ {data['total_pending_amount']}")
        c4.metric("Paid", data["paid_invoices"])
        c5.metric("Partial", data["partial_invoices"])


# =========================================================
# 👤 PATIENTS
# =========================================================
elif menu == "Patients":
    st.subheader("👤 Patients")

    with st.expander("➕ Add Patient"):
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120)
        gender = st.text_input("Gender")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_input("Address")
        disease = st.text_input("Disease")

        if st.button("Create Patient"):
            res = api_post(f"{BASE_URL}/patients/", {
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "email": email,
                "address": address,
                "disease": disease
            })

            if res:
                st.success("Patient added successfully")

    data = api_get(f"{BASE_URL}/patients/")
    if data:
        st.dataframe(safe_df(data), use_container_width=True)


# =========================================================
# 🧾 INVOICES
# =========================================================
elif menu == "Invoices":
    st.subheader("🧾 Invoices")

    patient_id = st.number_input("Patient ID", 1)
    total = st.number_input("Total Amount", 0)

    if st.button("Generate Invoice"):
        res = api_post(f"{BASE_URL}/invoices/", {
            "patient_id": patient_id,
            "total_amount": total
        })

        if res:
            st.success("Invoice created")

    data = api_get(f"{BASE_URL}/invoices/")
    if data:
        st.dataframe(safe_df(data), use_container_width=True)


# =========================================================
# 💳 TRANSACTIONS
# =========================================================
elif menu == "Transactions":
    st.subheader("💳 Payments")

    col1, col2, col3 = st.columns(3)

    with col1:
        invoice_id = st.number_input("Invoice ID", min_value=1)

    with col2:
        amount = st.number_input("Amount", min_value=1)

    with col3:
        method = st.selectbox(
            "Payment Method",
            ["cash", "upi", "card", "net banking"]
        )

    if st.button("💰 Pay Now"):
        res = api_post(
            f"{BASE_URL}/transactions/",
            {
                "invoice_id": invoice_id,
                "amount": amount,
                "method": method   # ✅ FIX ADDED
            }
        )

        if res:
            st.success("Payment successful ✅")
            time.sleep(1)
            st.rerun()

    st.divider()

    # ================= TRANSACTION TABLE =================
    data = api_get(f"{BASE_URL}/transactions/")
    if data:
        st.dataframe(safe_df(data), use_container_width=True)
# =========================================================
# 📊 ANALYTICS
# =========================================================
elif menu == "Analytics":
    st.subheader("📈 Analytics")

    data = api_get(f"{BASE_URL}/analytics/summary")

    if data:
        st.success("Live Data Loaded")

        st.bar_chart({
            "Invoices": [data["total_invoices"]],
            "Revenue": [data["total_revenue"]],
            "Pending": [data["total_pending_amount"]],
            "Paid": [data["paid_invoices"]],
            "Partial": [data["partial_invoices"]]
        })