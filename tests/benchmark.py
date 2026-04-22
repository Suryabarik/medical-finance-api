'''
import time
from agents.orchestrator import run_agents
from agents.performance_evaluator import evaluate_performance

def benchmark():
    start = time.time()

    result = run_agents()

    end = time.time()

    performance = evaluate_performance(result["finance_agent"])

    return {
        "latency": round(end - start, 3),
        "performance": performance,
        "insight_preview": result["finance_agent"]["ai_analysis"][:200]
    }

if __name__ == "__main__":
    print(benchmark())
'''

import time
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.finance_agent import analyze_finance
from agents.llm import generate_response

# ── Test cases representing real clinic scenarios ──────────────────────────
TEST_CASES = [
    {
        "name": "Critical cash flow crisis",
        "data": {
            "total_revenue": 100000,
            "total_pending_amount": 75000,
            "total_invoices": 50,
            "paid_invoices": 10,
            "partial_invoices": 8
        },
        "expected_severity": "CRITICAL"
    },
    {
        "name": "Healthy clinic",
        "data": {
            "total_revenue": 200000,
            "total_pending_amount": 20000,
            "total_invoices": 80,
            "paid_invoices": 70,
            "partial_invoices": 5
        },
        "expected_severity": "LOW"
    },
    {
        "name": "High partial payments",
        "data": {
            "total_revenue": 150000,
            "total_pending_amount": 45000,
            "total_invoices": 60,
            "paid_invoices": 30,
            "partial_invoices": 25
        },
        "expected_severity": "HIGH"
    },
    {
        "name": "Zero revenue edge case",
        "data": {
            "total_revenue": 0,
            "total_pending_amount": 0,
            "total_invoices": 0,
            "paid_invoices": 0,
            "partial_invoices": 0
        },
        "expected_severity": "INSUFFICIENT"
    },
    {
        "name": "All invoices unpaid",
        "data": {
            "total_revenue": 80000,
            "total_pending_amount": 80000,
            "total_invoices": 40,
            "paid_invoices": 0,
            "partial_invoices": 0
        },
        "expected_severity": "CRITICAL"
    }
]


def run_vanilla_llm(data: dict) -> dict:
    """Vanilla LLM — no system prompt, no context engineering"""
    prompt = f"Analyze this clinic financial data and give me insights: {json.dumps(data)}"
    
    start = time.time()
    raw = generate_response.__wrapped__(prompt) if hasattr(generate_response, '__wrapped__') else _vanilla_call(prompt)
    latency = round(time.time() - start, 3)
    
    return {"raw_output": raw, "latency": latency}


def _vanilla_call(prompt: str) -> str:
    """Direct LLM call bypassing our system prompt"""
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def score_vanilla(raw_output: str) -> int:
    """Simple scorer for vanilla output — no structured eval possible"""
    score = 0
    try:
        json.loads(raw_output)
        score += 3000   # got valid JSON without being told to
    except:
        score += 0      # most likely plain text

    text = raw_output.lower()
    if any(w in text for w in ["severity", "priority", "action"]):
        score += 1000
    if any(w in text for w in ["may", "might", "could", "perhaps"]):
        score -= 500

    return max(0, score)


def run_benchmark():
    print("\n" + "="*60)
    print("BENCHMARK: Your Agent vs Vanilla LLM")
    print("="*60)

    results = []

    for case in TEST_CASES:
        print(f"\n📋 Test: {case['name']}")
        print(f"   Expected severity: {case['expected_severity']}")

        # ── Your Agent ──────────────────────────────────────────
        start = time.time()
        agent_result = analyze_finance(case["data"])
        agent_latency = round(time.time() - start, 3)
        agent_score = agent_result["evaluation"]["final_score"]

        # ── Vanilla LLM ─────────────────────────────────────────
        vanilla_result = run_vanilla_llm(case["data"])
        vanilla_score = score_vanilla(vanilla_result["raw_output"])

        delta = agent_score - vanilla_score

        print(f"   Your Agent  → score: {agent_score}/10000  latency: {agent_latency}s")
        print(f"   Vanilla LLM → score: {vanilla_score}/10000  latency: {vanilla_result['latency']}s")
        print(f"   Delta: {'+' if delta >= 0 else ''}{delta}")

        results.append({
            "test_case": case["name"],
            "expected_severity": case["expected_severity"],
            "agent_score": agent_score,
            "vanilla_score": vanilla_score,
            "delta": delta,
            "agent_latency": agent_latency
        })

    # ── Summary ─────────────────────────────────────────────────
    avg_agent = sum(r["agent_score"] for r in results) / len(results)
    avg_vanilla = sum(r["vanilla_score"] for r in results) / len(results)
    avg_latency = sum(r["agent_latency"] for r in results) / len(results)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Avg Agent Score  : {round(avg_agent)}/10000")
    print(f"  Avg Vanilla Score: {round(avg_vanilla)}/10000")
    print(f"  Improvement      : +{round(avg_agent - avg_vanilla)} points")
    print(f"  Avg Latency      : {round(avg_latency, 3)}s")
    print("="*60)

    return {
        "results": results,
        "summary": {
            "avg_agent_score": round(avg_agent),
            "avg_vanilla_score": round(avg_vanilla),
            "improvement": round(avg_agent - avg_vanilla),
            "avg_latency_seconds": round(avg_latency, 3)
        }
    }


if __name__ == "__main__":
    final = run_benchmark()
    print("\nFull results saved.")
    with open("tests/benchmark_results.json", "w") as f:
        json.dump(final, f, indent=2)