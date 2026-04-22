# 🏥 JeevanMed AI ERP

## 📌 Overview
JeevanMed is an AI-powered healthcare ERP system built using FastAPI, Streamlit, and llama-3.1-8b-instant.  
It manages patients, invoices, transactions, and financial analytics — with an AI Decision Engine that converts raw financial data into prioritized, actionable decisions.

The system goes beyond a dashboard: it tells clinic owners **what to do next**, not just what the numbers are.

---

## 🎯 Why This Problem Was Priority #1

Three reasons:

1. **Underserved market** — Enterprise ERP tools (SAP, Oracle) are
   priced out of small clinic reach. No AI-native alternative exists
   for this segment in India.

2. **High stakes, bad consequences** — A clinic that misses cash flow
   warning signs cannot pay staff or restock supplies. Wrong financial
   decisions have immediate operational impact — not just lost revenue.

3. **Data exists but isn't used** — Clinics already record invoices and
   payments. The gap is not data collection — it is interpretation.
   JeevanMed closes that gap in under 1 second.

This is not a dashboard problem. It is a **decision-making problem**.
Dashboards show numbers. JeevanMed tells you what to do about them.

---

## 🚀 Features

### 1. Patient Management
- Create, update, delete patients
- Store medical and personal details
- Linked with invoices and transactions

### 2. Invoice Management
- Generate invoices for patients
- Track total, paid, and due amounts
- Status: pending, partial, paid
- Auto-updates after payment

### 3. Transaction System
- Record payments
- ✅ Prevent overpayment
- ✅ Auto-update invoice status
- Maintains full payment history

### 4. Financial Analytics Dashboard
- Total invoices
- Total revenue
- Pending amount
- Paid vs partial invoices

### 5. Authentication & Roles
- JWT-based login system
- Roles:
  - Admin → Full access
  - Viewer → Read-only

### 6. 🧠 AI Decision Engine (Core Feature)
- Analyzes real-time financial metrics
- Detects risks: high pending ratio, low payment completion
- Generates severity-ranked decisions (LOW / MEDIUM / HIGH / CRITICAL)
- Produces specific recommended actions — not generic advice
- Scores itself on every run (0–10,000 scale)
- Confidence-aware: reduces score for small sample sizes

### 7. Streamlit Frontend
- Interactive dashboard UI
- Login system
- KPI cards
- AI Decision output panel
- Payment interface

---

## 🔄 System Flow

**Patient → Invoice → Transaction → Analytics → AI Decision**

1. Patient is created
2. Invoice is generated
3. Payment is recorded (Transaction)
4. Invoice updates automatically
5. Analytics reflects real-time data
6. AI Engine analyzes metrics and returns prioritized decisions

---

## 🧠 How the AI Decision Engine Works

### Step 1 — Financial Data Input
```json
{
  "total_invoices": 5,
  "total_revenue": 13513,
  "total_pending_amount": 2399,
  "paid_invoices": 1,
  "partial_invoices": 2
}
```

### Step 2 — Metric Derivation
Three metrics calculated before the LLM is called:
- `pending_ratio` = pending / revenue
- `payment_completion_rate` = paid / total invoices
- `partial_ratio` = partial / total invoices

### Step 3 — LLM Decision Engine
Metrics sent to llama-3.1-8b-instant (via Groq) with a strict system prompt that enforces:
- Severity thresholds tied to actual values
- 2–4 decisions minimum, each addressing a different issue
- Confidence reduction for small sample sizes (n < 10)
- JSON-only output, no filler text

### Step 4 — Auto Evaluation
Every response scored across 5 dimensions before display.

---

## 📐 AI Performance Scoring (0–10,000)

| Dimension | Max Points | Method |
|-----------|-----------|--------|
| Accuracy | 2,500 | Severity matches pending_ratio threshold |
| Decision Quality | 2,500 | Field completeness × count penalty |
| Structure | 2,000 | Required JSON keys present |
| Hallucination Control | 2,000 | 2000 − (200 × forbidden word count) |
| Priority Definition | 1,000 | Sequential, unique, starts at 1 |
| **Total** | **10,000** | |

### Severity Thresholds (Strict)
```
pending_ratio > 0.60  →  CRITICAL
pending_ratio > 0.40  →  HIGH
pending_ratio > 0.20  →  MEDIUM
pending_ratio ≤ 0.20  →  LOW

If payment_completion_rate < 0.30 → escalate one level
If total_invoices < 10 → confidence_score must be below 60
```

---

## 📊 Benchmark: Agent vs Vanilla LLM

Run: `python tests/benchmark.py`

5 test cases, same data sent to both:
- **JeevanMed Agent** — system prompt + derived metrics + structured evaluation
- **Vanilla LLM** — raw data dump, no system prompt, no schema

| Test Case | Agent Score | Vanilla Score | Delta | Latency |
|-----------|------------|---------------|-------|---------|
| Critical cash flow crisis | 10,000 | 500 | +9,500 | 1.449s |
| Healthy clinic | 10,000 | 0 | +10,000 | 0.857s |
| High partial payments | 8,800 | 0 | +8,800 | 0.792s |
| Zero revenue edge case | 9,700 | 0 | +9,700 | 0.441s |
| All invoices unpaid | 10,000 | 500 | +9,500 | 0.594s |

**Avg Agent Score : 9,700 / 10,000**  
**Avg Vanilla Score: 200 / 10,000**  
**Improvement : +9,500 points**  
**Avg Latency : 0.827s**

> Vanilla LLM scored 0 on 3 of 5 cases — returned unstructured prose with no JSON schema and ignored severity thresholds entirely.

---

## 🔥 Live AI Output Example

Input: 5 invoices, ₹13,513 revenue, ₹2,399 pending

```json
{
  "decisions": [
    {
      "priority": 1,
      "issue": "PENDING RATIO",
      "severity": "LOW",
      "impact_score": 18,
      "recommended_action": "Send payment reminders for pending invoices"
    },
    {
      "priority": 2,
      "issue": "PAYMENT COMPLETION",
      "severity": "MEDIUM",
      "impact_score": 42,
      "recommended_action": "Call overdue patients directly"
    },
    {
      "priority": 3,
      "issue": "PARTIAL PAYMENTS",
      "severity": "MEDIUM",
      "impact_score": 38,
      "recommended_action": "Audit unpaid invoices older than 30 days"
    }
  ],
  "summary": "Low pending ratio but payment completion and partial payments need attention; small sample limits confidence.",
  "confidence_score": 40
}
```

**Evaluation Score: 10,000 / 10,000**

---

## 🧠 Mapping to Assignment Requirements

| Requirement | Implementation |
|-------------|---------------|
| Build your own Agent | AI Decision Engine (finance_agent.py + llm.py) |
| Cursor-based setup | .cursorrules at project root |
| Performance metrics (1–10,000) | 5-dimension auto-scorer in evaluation.py |
| Benchmark vs default Claude | tests/benchmark.py — +9,500 point improvement |
| Problem specialization | Small clinic cash flow risk detection |
| Documentation | This README + inline code comments |
| Security | .env for secrets, .env.example committed |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + SQLAlchemy |
| AI Model | llama-3.1-8b-instant via Groq API |
| Frontend | Streamlit |
| Auth | JWT (python-jose) |
| Evaluation | Custom 5-dimension scorer |
| Config | python-dotenv |
| Database | SQLite |

---

## 📂 Project Structure

```
medical_finance_api/
│
├── app/                        # FastAPI backend
│   ├── main.py
│   ├── routers/                # patients, invoices, transactions, auth
│   ├── models/                 # SQLAlchemy ORM models
│   └── services/               # Business logic
│
├── agents/                     # AI layer
│   ├── llm.py                  # Groq/LLaMA client
│   ├── finance_agent.py        # Metric calculation + LLM call
│   ├── orchestrator.py         # Intent routing + validation
│   ├── evaluation.py           # 5-dimension scorer (0–10,000)
│   └── performance_evaluator.py
│
├── prompts/
│   └── finance.md              # System prompt with strict thresholds
│
├── frontend/
│   └── app.py                  # Streamlit UI
│
├── tests/
│   ├── benchmark.py            # Agent vs Vanilla LLM
│   └── benchmark_results.json
│
├── .cursorrules
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Run Backend
```bash
uvicorn app.main:app --reload
```

Backend URL: http://127.0.0.1:8000  


### 4. Run Frontend
```bash
streamlit run frontend/app.py
```

Frontend URL: http://localhost:8501

### 5. Run Benchmark
```bash
python tests/benchmark.py
```

---

## 🔐 How to Use the System

1. Signup (first user becomes Admin)
2. Login
3. Create Patient
4. Generate Invoice
5. Make Payment
6. View Analytics Dashboard
7. Open AI Decision Engine tab → get prioritized decisions

---

## 📡 API Endpoints

### 🔐 Authentication
- **POST /auth/signup** → Create new user
- **POST /auth/token** → Login & get access token
- **GET /auth/me** → Get current user info

### 👤 Patients
- **POST /patients/** → Create patient
- **GET /patients/** → Get all patients
- **GET /patients/{id}** → Get single patient
- **PUT /patients/{id}** → Update patient
- **DELETE /patients/{id}** → Delete patient (Admin only)

### 🧾 Invoices
- **POST /invoices/** → Create invoice (default: pending)
- **GET /invoices/** → Get all invoices
- **GET /invoices/{id}** → Get invoice details
- **DELETE /invoices/{id}** → Delete invoice (Admin only)

### 💳 Transactions
- **POST /transactions/** → Record payment
  - ✅ Prevents overpayment
  - ✅ Updates invoice status automatically
- **GET /transactions/** → Get all transactions
- **DELETE /transactions/{id}** → Delete transaction (Admin only)

### 📊 Analytics
- **GET /analytics/summary** → Returns total invoices, revenue, pending, paid, partial

### 🧠 AI Decision Engine
- **GET /analytics/ai-decision** → Returns severity-ranked decisions with evaluation score

---

## ⚠️ Business Logic

### ✅ Overpayment Prevention
Payment cannot exceed invoice due amount

### ✅ Invoice Status Logic
- **pending** → No payment made
- **partial** → Partial payment made
- **paid** → Fully paid

### ✅ AI Severity Logic
- Thresholds based on pending_ratio and payment_completion_rate
- Small sample sizes (< 10 invoices) reduce confidence automatically
- Fallback JSON returned if data is insufficient

---

## 🔐 Security
- All API keys loaded from environment variables
- `.env` is in `.gitignore` — never committed
- `.env.example` provided with placeholder values
- JWT authentication on all API routes
- Role-based access: Admin and Viewer

---

## 🖥️ Cursor Configuration
This project is fully Cursor-ready. The `.cursorrules` file configures:
- FastAPI + Python conventions
- Agent file structure awareness
- Prompt engineering context for finance domain

Open the project root in Cursor — all agents, routes, and prompts are immediately navigable.

---



## 🔍 Feedback on Must Company's Agent

I spent time with the agent at chat.must.company before submitting this quest.

**Strengths:**
- Handles multi-turn conversation naturally — context carries across messages
- Response tone is clean and professional
- Fast — no noticeable latency on simple queries

**Gaps I identified:**

1. **No output schema consistency** — the same question asked twice
   returned a paragraph and a bullet list respectively. Downstream
   systems cannot parse inconsistent formats reliably.

2. **No self-evaluation layer** — there is no signal indicating whether
   a response is high-confidence or uncertain. Users cannot distinguish
   a reliable answer from a guess.

3. **No domain grounding** — the agent is general-purpose. For
   high-stakes domains like finance or healthcare, generic responses
   reduce trust and increase the risk of wrong decisions.

**How JeevanMed addresses each gap:**

| Gap | JeevanMed's Solution |
|-----|---------------------|
| Inconsistent output | Strict JSON schema enforced in every response via system prompt |
| No self-evaluation | Auto-scores every response 0–10,000 with dimension breakdown |
| No domain grounding | Specialized to healthcare finance — severity thresholds tied to real clinic metrics |

The core difference: Must's agent is a **conversation tool**.
JeevanMed is a **decision tool** — it tells you what to do, not just what the data says.

---

## 🧑‍💻 Author

**Suryakanta Barik**  
Python Developer | Backend | AI/ML | Generative Ai