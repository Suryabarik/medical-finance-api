Here’s your **fully corrected and clean `README.md`** — just copy & paste directly 👇

---

```md
# 💰 Medical Finance Management System (FastAPI)

## 📌 Overview
This project is a Python-based finance tracking system built using FastAPI and Streamlit.  
It manages patients, invoices, transactions, and financial analytics in a structured way.

The system simulates a real-world hospital/finance backend with proper business logic, validation, and role-based access.

---

## 🚀 Features

### 1. Patient Management
- Create, update, delete patients
- Store medical and personal details
- Linked with invoices

### 2. Invoice Management
- Generate invoices for patients
- Track total, paid, and due amounts
- Status: pending, partial, paid
- Auto updates after payment

### 3. Transaction System
- Record payments  
- ✅ Prevent overpayment  
- ✅ Auto-update invoice status  
- Maintains payment history  

### 4. Analytics Dashboard
- Total invoices  
- Total revenue  
- Pending amount  
- Paid vs partial invoices  

### 5. Authentication & Roles
- JWT-based login system  
- Roles:
  - Admin → Full access  
  - Analyst → View + insights  
  - Viewer → Read-only  

### 6. Streamlit Frontend
- Interactive dashboard UI  
- Login system  
- KPI cards  
- Data tables  
- Payment interface  

---

## 🔄 System Flow

**Patient → Invoice → Transaction → Analytics**

1. Patient is created  
2. Invoice is generated  
3. Payment is recorded (Transaction)  
4. Invoice updates automatically  
5. Analytics reflects real-time data  

---

## 🧠 Mapping to Assignment

| Assignment Requirement | Implementation |
|----------------------|--------------|
| Financial Records | Invoices & Transactions |
| Income/Expense | Payments (income) & due (pending) |
| Summary | Analytics API |
| Roles | Admin, Analyst, Viewer |
| CRUD | Patients, Invoices, Transactions |
| Validation | Overpayment prevention, role checks |

---

## 🛠 Tech Stack

- FastAPI  
- SQLAlchemy  
- SQLite  
- JWT Authentication (python-jose)  
- Streamlit (Frontend)  
- Requests  

---

## 📂 Project Structure

```

medical_finance_api/
│
├── app/                # Backend
├── frontend/           # Streamlit UI
├── medical.db
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
````

### 2. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

API Docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 3. Run Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

Frontend URL:
[http://localhost:8501](http://localhost:8501)

---

## 🔐 How to Use the System

1. Signup (first user becomes Admin)
2. Login
3. Create Patient
4. Generate Invoice
5. Make Payment
6. View Analytics Dashboard

---

## 📡 API Endpoints & Working

### 🔐 Authentication

* **POST /auth/signup** → Create new user (first user becomes admin)
* **POST /auth/token** → Login & get access token
* **POST /auth/refresh** → Refresh token
* **GET /auth/me** → Get current user info

---

### 👤 Patients

* **POST /patients/** → Create patient
* **GET /patients/** → Get all patients
* **GET /patients/{id}** → Get single patient
* **PUT /patients/{id}** → Update patient
* **DELETE /patients/{id}** → Delete patient (Admin only)

---

### 🧾 Invoices

* **POST /invoices/** → Create invoice (default: pending)
* **GET /invoices/** → Get all invoices
* **GET /invoices/{id}** → Get invoice details
* **DELETE /invoices/{id}** → Delete invoice (Admin only)

---

### 💳 Transactions

* **POST /transactions/** → Record payment

  * ✅ Prevents overpayment
  * ✅ Updates invoice (paid_amount, due_amount, status)
* **GET /transactions/** → Get all transactions
* **GET /transactions/{id}** → Get single transaction
* **DELETE /transactions/{id}** → Delete transaction (Admin only)

---

### 📊 Analytics

* **GET /analytics/summary**

Returns:

* Total invoices
* Total revenue
* Pending amount
* Paid invoices
* Partial invoices

---

## ⚠️ Important Business Logic

### ✅ Overpayment Prevention

Payment cannot exceed invoice due amount

### ✅ Invoice Status Logic

* **pending** → No payment
* **partial** → Partial payment
* **paid** → Fully paid

---

---

## 🧑‍💻 Author

**Suryakanta Barik**
Python Developer | Backend | AI/ML

