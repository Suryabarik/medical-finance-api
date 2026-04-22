import streamlit as st
import requests
import pandas as pd
import time

BASE_URL = "http://127.0.0.1:8000"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="JeevanMed AI",
    page_icon="🏥",
    layout="wide"
)

# ================= SESSION =================
if "token" not in st.session_state:
    st.session_state.token = None

headers = {}
if st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}


# ================= HELPERS =================
def safe_df(data):
    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.DataFrame([data])
    return pd.DataFrame()


def api_get(url):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            st.error(res.text)
            return None
        return res.json()
    except:
        st.error("Backend not reachable")
        return None


def api_post(url, payload, form=False):
    try:
        if form:
            res = requests.post(url, data=payload)
        else:
            res = requests.post(url, json=payload, headers=headers)

        if res.status_code not in [200, 201]:
            st.error(res.text)
            return None

        return res.json()
    except:
        st.error("Request failed")
        return None


# ================= HEADER =================
st.markdown(
    "<h1 style='text-align:center;'>🏥 JeevanMed AI ERP</h1><hr>",
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Patients", "Invoices", "Transactions", "Analytics", "Login", "Signup"]
)

if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.success("Logged out")
    st.stop()


# =========================================================
# LOGIN
# =========================================================
if menu == "Login":
    st.subheader("Login")

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
            st.success("Login success")
            time.sleep(1)
            st.rerun()




# =========================================================
# SIGNUP (FIXED)
# =========================================================
elif menu == "Signup":
    st.subheader("Signup")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Username")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")

    with col2:
        contact_number = st.text_input("Contact Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        # 🔒 Basic validation
        if not all([username, email, full_name, contact_number, password, confirm_password]):
            st.warning("All fields are required")
            st.stop()

        if password != confirm_password:
            st.error("Passwords do not match")
            st.stop()

        payload = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "contact_number": contact_number,
            "password": password,
            "confirm_password": confirm_password
        }

        with st.spinner("Creating account..."):
            res = api_post(f"{BASE_URL}/auth/signup", payload)

        if res:
            st.success(f"✅ {res.get('message', 'Account created successfully')}")
            st.info(f"Assigned Role: {res.get('role', 'viewer')}")

            # Optional: auto redirect to login
            time.sleep(1)
            st.rerun()



# =========================================================
# DASHBOARD
# =========================================================
elif menu == "Dashboard":
    st.subheader("Overview")

    # 🔐 Check login
    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    data = api_get(f"{BASE_URL}/analytics/summary")

    if data:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Invoices", data.get("total_invoices", 0))
        c2.metric("Revenue", f"₹ {data.get('total_revenue', 0)}")
        c3.metric("Pending", f"₹ {data.get('total_pending_amount', 0)}")
        c4.metric("Paid", data.get("paid_invoices", 0))
        c5.metric("Partial", data.get("partial_invoices", 0))


# =========================================================
# PATIENTS (FULLY FIXED)
# =========================================================
elif menu == "Patients":
    st.subheader("Patients")

    # 🔐 Check login
    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    st.markdown("### ➕ Add Patient")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone (Required)")

    with col2:
        email = st.text_input("Email")
        blood_group = st.text_input("Blood Group")
        disease = st.text_input("Disease")
        address = st.text_area("Address")

    if st.button("Add Patient"):
        # ✅ Validation
        if not name or not phone:
            st.error("Name and Phone are required")
            st.stop()

        payload = {
            "name": name,
            "age": age,
            "gender": gender,
            "phone": phone,
            "email": email,
            "address": address,
            "disease": disease,
            "blood_group": blood_group
        }

        with st.spinner("Creating patient..."):
            res = api_post(f"{BASE_URL}/patients/", payload)

        if res:
            st.success("✅ Patient added successfully")
            time.sleep(1)
            st.rerun()

    # ================= LIST =================
    st.markdown("### 📋 Patient List")

    data = api_get(f"{BASE_URL}/patients/")

    if data:
        df = safe_df(data)

        # Optional: better UI formatting
        if not df.empty:
            st.dataframe(
                df,
                use_container_width=True
            )
        else:
            st.info("No patients found")


# =========================================================
# INVOICES
# =========================================================
elif menu == "Invoices":
    st.subheader("Invoices")

    patient_id = st.number_input("Patient ID", 1)
    total = st.number_input("Amount", 0)

    # 🔐 Check login
    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    if st.button("Create Invoice"):
        api_post(f"{BASE_URL}/invoices/", {
            "patient_id": patient_id,
            "total_amount": total
        })

    data = api_get(f"{BASE_URL}/invoices/")
    if data:
        st.dataframe(safe_df(data))


# =========================================================
# TRANSACTIONS
# =========================================================
elif menu == "Transactions":
    st.subheader("Payments")

    invoice_id = st.number_input("Invoice ID", 1)
    amount = st.number_input("Amount", 1)

        # 🔐 Check login
    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    if st.button("Pay"):
        api_post(f"{BASE_URL}/transactions/", {
            "invoice_id": invoice_id,
            "amount": amount,
            "method": "cash"
        })

    data = api_get(f"{BASE_URL}/transactions/")
    if data:
        st.dataframe(safe_df(data))


# =========================================================
# 🔥 AI ANALYTICS (FIXED)
# =========================================================
elif menu == "Analytics":
    st.subheader("🧠 AI Decision Engine")

    col1, col2 = st.columns(2)

    # 🔐 Check login
    if not st.session_state.token:
        st.warning("Please login first")
        st.stop()

    # ================= RAW =================
    with col1:
        st.markdown("### Raw Data")
        data = api_get(f"{BASE_URL}/analytics/summary")

        if data:
            st.json(data)

    # ================= AI =================
    with col2:
        st.markdown("### AI Output")

        ai = api_get(f"{BASE_URL}/analytics/ai-insights")

        if ai:
            agent = ai.get("finance_agent", {})

            # METRICS
            st.markdown("#### Metrics")
            st.json(agent.get("metrics", {}))

            # DECISION ENGINE SAFE
            decision_engine = agent.get("decision_engine", {})

            if "error" in decision_engine:
                st.error("AI returned invalid JSON")
                st.text(decision_engine.get("raw_output", ""))
            else:
                decisions = decision_engine.get("decisions", [])

                if decisions:
                    st.markdown("#### Decisions")
                    for d in decisions:
                        st.warning(
                            f"{d.get('severity','')} | Priority {d.get('priority','')}\n\n"
                            f"{d.get('issue','')}\n\n"
                            f"👉 {d.get('recommended_action','')}"
                        )
                else:
                    st.info("No decisions generated")

                st.markdown("#### Summary")
                st.success(decision_engine.get("summary", "No summary"))

                st.markdown("#### Confidence")
                st.write(decision_engine.get("confidence_score", 0))

            # EVALUATION
            st.markdown("#### Score")
            eval_data = agent.get("evaluation", {})
            st.success(f"{eval_data.get('final_score', 0)} / 10000")

            with st.expander("Breakdown"):
                st.json(eval_data.get("breakdown", {}))