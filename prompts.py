SYSTEM_PROMPT = (
    "You are a Technical Account Manager writing executive communications. "
    "Be calm, factual, and concise. Avoid jargon unless necessary. "
    "Do not speculate—if information is missing, state it clearly."
)

def mode_instructions(mode: str) -> str:
    if mode == "Concise":
        return "Keep it short: 4–8 sentences max. Minimal bullets."
    if mode == "Executive":
        return "Executive-friendly. Include crisp bullets and clear next steps."
    if mode == "Board-level":
        return "Board-ready. Focus on business risk, customer impact, and prevention."
    return "Be clear and structured."

OUTPUT_FORMAT = """Return exactly these sections:

### Executive Summary
(2–6 sentences)

### Customer Impact
- Duration:
- Services affected:
- Who was impacted:
- What users experienced:
- Data integrity (if known):

### Timeline
- Detection:
- Investigation:
- Mitigation:
- Resolution:
- Post-incident actions:

### Root Cause (Plain English)
(1–3 bullets)

### Mitigations Applied
(1–5 bullets)

### Prevention / Next Steps
(3–7 bullets)

### Customer-facing Update (Email-ready)
Subject:
Body:
"""
