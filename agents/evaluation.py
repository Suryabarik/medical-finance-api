

import json

def evaluate_agent(ai_output: str, input_data: dict) -> dict:
    score = {
        "accuracy": 0,        # max 2500
        "decision_quality": 0, # max 2500
        "structure": 0,        # max 2000
        "hallucination_control": 0,  # max 2000
        "priority_definition": 0     # max 1000
    }

    try:
        parsed = json.loads(ai_output)
    except json.JSONDecodeError:
        return {
            "final_score": 0,
            "breakdown": score,
            "error": "Invalid JSON output from AI",
            "max_possible": 10000
        }

    decisions = parsed.get("decisions", [])

    # 1. STRUCTURE (max 2000)
    has_decisions = "decisions" in parsed
    has_summary = "summary" in parsed
    has_confidence = "confidence_score" in parsed
    structure_fields = sum([has_decisions, has_summary, has_confidence])
    score["structure"] = int((structure_fields / 3) * 2000)

    # 2. ACCURACY (max 2500)
    # Does the AI's severity match what the data actually suggests?
    pending_ratio = (
        input_data["total_pending_amount"] / input_data["total_revenue"]
        if input_data["total_revenue"] > 0 else 0
    )
    
    severities = [d.get("severity", "") for d in decisions]
    
    if pending_ratio > 0.6 and "CRITICAL" in severities:
        score["accuracy"] = 2500  # correctly identified critical situation
    elif pending_ratio > 0.4 and any(s in severities for s in ["HIGH", "CRITICAL"]):
        score["accuracy"] = 2000
    elif pending_ratio > 0.2 and any(s in severities for s in ["MEDIUM", "HIGH"]):
        score["accuracy"] = 1500
    elif pending_ratio <= 0.2 and "LOW" in severities:
        score["accuracy"] = 2500  # correctly identified healthy situation
    else:
        score["accuracy"] = 800  # severity doesn't match data

    # 3. DECISION QUALITY (max 2500)
    if len(decisions) == 0:
        score["decision_quality"] = 0
    else:
        quality_points = 0
        for d in decisions:
            # Each decision graded on having all required fields
            has_issue = bool(d.get("issue", "").strip())
            has_action = bool(d.get("recommended_action", "").strip())
            has_severity = d.get("severity") in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            has_priority = isinstance(d.get("priority"), int)
            
            field_score = sum([has_issue, has_action, has_severity, has_priority])
            quality_points += field_score / 4  # 0.0 to 1.0 per decision

        # Ideal: 2-4 decisions. Too few or too many = lower score
        count_penalty = 1.0
        if len(decisions) < 2:
            count_penalty = 0.6
        elif len(decisions) > 5:
            count_penalty = 0.7

        avg_quality = quality_points / len(decisions)
        score["decision_quality"] = int(avg_quality * count_penalty * 2500)

    # 4. HALLUCINATION CONTROL (max 2000)
    text = ai_output.lower()
    penalties = 0
    
    forbidden = ["may", "might", "could", "perhaps", "possibly", "i think", "i believe"]
    for word in forbidden:
        if word in text:
            penalties += 200

    # Check no raw input data was repeated verbatim
    revenue_str = str(input_data["total_revenue"])
    if revenue_str in ai_output and ai_output.count(revenue_str) > 1:
        penalties += 300  # repeated input data

    score["hallucination_control"] = max(0, 2000 - penalties)

    # 5. PRIORITY DEFINITION (max 1000)
    priorities = [d.get("priority") for d in decisions if isinstance(d.get("priority"), int)]
    if not priorities:
        score["priority_definition"] = 0
    else:
        is_sequential = priorities == list(range(1, len(priorities) + 1))
        no_duplicates = len(priorities) == len(set(priorities))
        starts_at_one = priorities[0] == 1 if priorities else False
        
        checks = sum([is_sequential, no_duplicates, starts_at_one])
        score["priority_definition"] = int((checks / 3) * 1000)

    final_score = sum(score.values())

    return {
        "final_score": final_score,          # 0–10,000
        "max_possible": 10000,
        "breakdown": score,
        "calculation_method": {
            "accuracy": "Severity vs pending_ratio alignment (max 2500)",
            "decision_quality": "Field completeness × count penalty (max 2500)",
            "structure": "Required JSON fields present (max 2000)",
            "hallucination_control": "2000 - (200 per forbidden word) (max 2000)",
            "priority_definition": "Sequential, unique, starts at 1 (max 1000)"
        }
    }