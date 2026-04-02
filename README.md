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

Patient → Invoice → Transaction → Analytics

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

medical_finance_api/
│
├── app/                # Backend
├── frontend/           # Streamlit UI
├── medical.db
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt