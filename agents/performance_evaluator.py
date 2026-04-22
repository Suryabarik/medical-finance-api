'''
def evaluate_performance(result):
    score = 0

    if "ai_analysis" in result:
        score += 4000

    if len(result.get("ai_analysis", "")) > 100:
        score += 3000

    if result.get("raw_data"):
        score += 2000

    return {
        "score": score,
        "max_score": 10000
    }
'''

import json
import time

def evaluate_performance(result: dict) -> dict:
    """
    Scores agent output on 5 dimensions, max 10,000 points.
    
    Scoring breakdown:
    - Response validity     : 2000 pts (is output structured and parseable)
    - Decision completeness : 2500 pts (are all required fields present)
    - Severity accuracy     : 2000 pts (does severity match the metrics)
    - Actionability         : 2000 pts (are recommendations specific)
    - Confidence alignment  : 1500 pts (does confidence match decision count)
    """

    scores = {
        "response_validity": 0,
        "decision_completeness": 0,
        "severity_accuracy": 0,
        "actionability": 0,
        "confidence_alignment": 0
    }

    # ── Pull data out of result ──────────────────────────────────
    decision_engine = result.get("decision_engine", {})
    metrics = result.get("metrics", {})

    # ── 1. Response Validity (max 2000) ─────────────────────────
    if isinstance(decision_engine, dict) and "error" not in decision_engine:
        scores["response_validity"] = 2000
    elif isinstance(decision_engine, dict):
        scores["response_validity"] = 500   # parsed but has error key
    else:
        scores["response_validity"] = 0

    decisions = decision_engine.get("decisions", [])

    # ── 2. Decision Completeness (max 2500) ──────────────────────
    required_fields = ["issue", "severity", "priority", "recommended_action"]
    valid_severities = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    if decisions:
        field_scores = []
        for d in decisions:
            present = sum(1 for f in required_fields if d.get(f))
            valid_sev = d.get("severity", "") in valid_severities
            field_scores.append((present / len(required_fields)) * (1.1 if valid_sev else 1.0))

        avg_completeness = sum(field_scores) / len(field_scores)
        
        # Penalise if too few or too many decisions
        count = len(decisions)
        if 2 <= count <= 4:
            count_multiplier = 1.0
        elif count == 1:
            count_multiplier = 0.6
        elif count > 4:
            count_multiplier = 0.75
        else:
            count_multiplier = 0.3

        scores["decision_completeness"] = int(
            min(avg_completeness, 1.0) * count_multiplier * 2500
        )

    # ── 3. Severity Accuracy (max 2000) ──────────────────────────
    # Check if severity matches what the metrics actually indicate
    pending_ratio = metrics.get("pending_ratio", 0)
    payment_rate = metrics.get("payment_completion_rate", 0)

    severities_given = {d.get("severity") for d in decisions}

    if pending_ratio > 0.6 or payment_rate < 0.3:
        # Data says CRITICAL/HIGH situation
        if "CRITICAL" in severities_given or "HIGH" in severities_given:
            scores["severity_accuracy"] = 2000
        elif "MEDIUM" in severities_given:
            scores["severity_accuracy"] = 1000
        else:
            scores["severity_accuracy"] = 200  # missed the severity entirely

    elif pending_ratio > 0.3 or payment_rate < 0.6:
        # Data says MEDIUM situation
        if "HIGH" in severities_given or "MEDIUM" in severities_given:
            scores["severity_accuracy"] = 2000
        else:
            scores["severity_accuracy"] = 800

    else:
        # Data says healthy / LOW risk
        if "LOW" in severities_given or not decisions:
            scores["severity_accuracy"] = 2000
        else:
            scores["severity_accuracy"] = 1200  # over-alarming on good data

    # ── 4. Actionability (max 2000) ──────────────────────────────
    # Penalise vague actions, reward specific ones
    vague_phrases = [
        "improve", "enhance", "consider", "try to",
        "look into", "may want", "think about", "review the"
    ]
    specific_phrases = [
        "call", "send", "schedule", "reduce", "increase",
        "contact", "follow up", "collect", "audit", "resubmit"
    ]

    if decisions:
        action_scores = []
        for d in decisions:
            action = d.get("recommended_action", "").lower()
            vague_hits = sum(1 for p in vague_phrases if p in action)
            specific_hits = sum(1 for p in specific_phrases if p in action)
            
            action_score = max(0, min(1.0, (specific_hits * 0.4) - (vague_hits * 0.3) + 0.4))
            action_scores.append(action_score)

        scores["actionability"] = int(
            (sum(action_scores) / len(action_scores)) * 2000
        )

    # ── 5. Confidence Alignment (max 1500) ───────────────────────
    # Confidence should be proportional to data richness
    confidence = decision_engine.get("confidence_score", 0)

    if isinstance(confidence, (int, float)):
        # If we have good data and decisions, confidence should be 60-90
        # If data is sparse, confidence should be low
        has_good_data = metrics.get("pending_ratio") is not None

        if has_good_data and 60 <= confidence <= 90:
            scores["confidence_alignment"] = 1500
        elif has_good_data and 40 <= confidence <= 95:
            scores["confidence_alignment"] = 1000
        elif not has_good_data and confidence < 40:
            scores["confidence_alignment"] = 1500  # correctly uncertain
        else:
            scores["confidence_alignment"] = 400

    final_score = sum(scores.values())

    return {
        "final_score": final_score,
        "max_possible": 10000,
        "breakdown": scores,
        "calculation_method": {
            "response_validity":     "Valid JSON with no error key = 2000",
            "decision_completeness": "Avg field presence × count penalty (max 2500)",
            "severity_accuracy":     "Severity matches pending_ratio threshold (max 2000)",
            "actionability":         "Specific verbs − vague phrases per action (max 2000)",
            "confidence_alignment":  "Confidence score in expected range (max 1500)"
        }
    }
