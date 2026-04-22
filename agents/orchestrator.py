'''
from agents.finance_agent import analyze_finance

def run_agents(data):
    return {
        "finance_agent": analyze_finance(data)
    }
'''




from agents.finance_agent import analyze_finance

# Intent keywords for routing
FINANCE_KEYWORDS = [
    "revenue", "invoice", "payment", "pending",
    "cash", "billing", "paid", "financial"
]

def detect_intent(query: str) -> str:
    """Route natural language queries to the right agent."""
    q = query.lower()
    if any(k in q for k in FINANCE_KEYWORDS):
        return "finance"
    return "finance"  # default — only one agent for now, extend later

def run_agents(data: dict, query: str = "") -> dict:
    """
    Main entry point. Routes data to appropriate agent.
    
    Args:
        data: Financial metrics dict from the API
        query: Optional natural language query from user
    
    Returns:
        Dict with agent results and routing metadata
    """
    
    # Validate input before sending to agent
    required_keys = [
        "total_revenue", "total_pending_amount",
        "total_invoices", "paid_invoices", "partial_invoices"
    ]
    
    missing = [k for k in required_keys if k not in data]
    if missing:
        return {
            "error": f"Missing required fields: {missing}",
            "status": "failed"
        }

    intent = detect_intent(query) if query else "finance"

    try:
        if intent == "finance":
            result = analyze_finance(data)
            return {
                "status": "success",
                "intent_detected": intent,
                "finance_agent": result
            }
    except Exception as e:
        return {
            "status": "error",
            "intent_detected": intent,
            "error": str(e),
            "finance_agent": None
        }