'''
from agents.llm import generate_response
from agents.evaluation import evaluate_agent
import json


def analyze_finance(data):

    # ✅ Step 1: Derived Metrics
    pending_ratio = (
        data["total_pending_amount"] / data["total_revenue"]
        if data["total_revenue"] > 0 else 0
    )

    payment_completion_rate = (
        data["paid_invoices"] / data["total_invoices"]
        if data["total_invoices"] > 0 else 0
    )

    # ✅ Step 2: PROMPT (THIS WAS MISSING ❌)
    prompt = f"""
    DATA:
    total_revenue = {data['total_revenue']}
    total_pending_amount = {data['total_pending_amount']}
    paid_invoices = {data['paid_invoices']}
    partial_invoices = {data['partial_invoices']}

    METRICS:
    pending_ratio = {round(pending_ratio, 2)}
    payment_completion_rate = {round(payment_completion_rate, 2)}
    """

    # ✅ Step 3: Call LLM
    ai_output = generate_response(prompt)

    # ✅ Step 4: Parse JSON safely
    try:
        parsed_output = json.loads(ai_output)
    except:
        parsed_output = {
            "error": "Invalid JSON from AI",
            "raw_output": ai_output
        }

    # ✅ Step 5: Evaluate
    evaluation = evaluate_agent(ai_output, data)

    # ✅ Step 6: Final Response
    return {
        "metrics": {
            "pending_ratio": round(pending_ratio, 2),
            "payment_completion_rate": round(payment_completion_rate, 2)
        },
        "decision_engine": parsed_output,
        "evaluation": evaluation
    }
'''

from agents.llm import generate_response
from agents.evaluation import evaluate_agent
import json

def analyze_finance(data):

    # Step 1: Derived Metrics
    pending_ratio = (
        data["total_pending_amount"] / data["total_revenue"]
        if data["total_revenue"] > 0 else 0
    )
    payment_completion_rate = (
        data["paid_invoices"] / data["total_invoices"]
        if data["total_invoices"] > 0 else 0
    )
    partial_ratio = (
        data["partial_invoices"] / data["total_invoices"]
        if data["total_invoices"] > 0 else 0
    )
    
    # Step 2: Sample size warning for prompt
    sample_warning = (
        "WARNING: total_invoices < 10 — small sample, set confidence_score below 60"
        if data["total_invoices"] < 10 else ""
    )

    # Step 3: Rich prompt with all context
    prompt = f"""
CLINIC FINANCIAL DATA:
- total_revenue: {data['total_revenue']}
- total_pending_amount: {data['total_pending_amount']}
- total_invoices: {data['total_invoices']}
- paid_invoices: {data['paid_invoices']}
- partial_invoices: {data['partial_invoices']}

CALCULATED METRICS:
- pending_ratio: {round(pending_ratio, 2)}
- payment_completion_rate: {round(payment_completion_rate, 2)}
- partial_ratio: {round(partial_ratio, 2)}

{sample_warning}

Apply severity thresholds exactly as defined.
Return 2 to 4 decisions, each for a different issue.
"""

    # Step 4: Call LLM
    ai_output = generate_response(prompt)

    # Step 5: Parse safely
    try:
        parsed_output = json.loads(ai_output)
    except json.JSONDecodeError:
        parsed_output = {
            "decisions": [],
            "summary": "AI output parsing failed.",
            "confidence_score": 0,
            "error": ai_output[:300]
        }

    # Step 6: Evaluate
    evaluation = evaluate_agent(ai_output, data)

    return {
        "metrics": {
            "pending_ratio": round(pending_ratio, 2),
            "payment_completion_rate": round(payment_completion_rate, 2),
            "partial_ratio": round(partial_ratio, 2)
        },
        "decision_engine": parsed_output,
        "evaluation": evaluation
    }