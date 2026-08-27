BASELINE_RISK = {
    "Uncapped Liability": "High",
    "Ip Ownership Assignment": "High",
    "Non-Compete": "High",
    "Exclusivity": "Medium",
    "Termination For Convenience": "Medium",
    "Minimum Commitment": "Medium",
    "License Grant": "Medium",
    "Revenue/Profit Sharing": "Medium",
    "Audit Rights": "Medium",
    "Post-Termination Services": "Medium",
    "Cap On Liability": "Low",
    "Anti-Assignment": "Low",
    "Governing Law": "Low",
    "Insurance": "Low",
    "Non-Transferable License": "Low",
}

HIGH_RISK_KEYWORDS = {
    "discretionary_power": [
        "sole discretion", "sole and absolute discretion", "in its sole judgment",
        "at any time without cause", "without prior notice", "no obligation to"
    ],
    "absolute_terms": [
        "irrevocable", "irrevocably", "perpetual", "in perpetuity",
        "unconditional", "unconditionally", "indefinitely", "without limitation"
    ],
    "liability_exposure": [
        "unlimited", "uncapped", "joint and several liability", "hold harmless",
        "indemnify and hold harmless", "consequential damages", "punitive damages",
        "liquidated damages"
    ],
    "waiver_language": [
        "waives all rights", "waives any and all claims", "no liability whatsoever",
        "at its own risk", "sole and exclusive remedy"
    ]
}

def escalate_risk(base_risk: str, clause_text: str) -> str:
    text_lower = clause_text.lower()
    all_keywords = [kw for group in HIGH_RISK_KEYWORDS.values() for kw in group]
    matches = sum(1 for keyword in all_keywords if keyword in text_lower)

    if matches == 0:
        return base_risk

    risk_levels = ["Low", "Medium", "High"]
    current_index = risk_levels.index(base_risk)
    new_index = min(current_index + 1, len(risk_levels) - 1)

    return risk_levels[new_index]

def get_risk_level(category: str, clause_text: str) -> str:
    base_risk = BASELINE_RISK.get(category, "Medium")
    return escalate_risk(base_risk, clause_text)

if __name__ == "__main__":
    print(escalate_risk("Low", "This agreement is governed by the laws of California."))
    print(escalate_risk("Low", "Party may terminate this agreement in its sole discretion, irrevocably."))
    print(escalate_risk("High", "This liability shall be uncapped and unlimited."))