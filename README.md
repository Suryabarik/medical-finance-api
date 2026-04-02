# 💰 Medical Finance Management System (FastAPI)

## 📌 Overview
This project is a Python-based finance tracking system built using FastAPI.  
It manages patients, invoices, transactions, and financial analytics.

---

## 🚀 Features

### 1. Patient Management
- Create, update, delete patients
- Store medical and personal details

### 2. Invoice Management
- Generate invoices for patients
- Track total, paid, and due amounts
- Status: pending, partial, paid

### 3. Transaction System
- Record payments
- Prevent overpayment
- Auto-update invoice status

### 4. Analytics Dashboard
- Total revenue
- Pending amount
- Paid vs partial invoices

### 5. Authentication & Roles
- JWT-based login
- Roles: admin, analyst, viewer

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
| Income/Expense | Payments & dues |
| Summary | Analytics API |
| Roles | Admin, Analyst, Viewer |
| CRUD | All modules |
| Validation | Overpayment prevention |

---

## 🛠 Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Streamlit (Frontend)

---

## ⚙️ Setup Instructions

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload