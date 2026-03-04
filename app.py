import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from prompts import SYSTEM_PROMPT, mode_instructions, OUTPUT_FORMAT

load_dotenv()

APP_TITLE = "Incident → Executive Summary"
DEFAULT_MODEL = "gpt-4.1-mini"

st.set_page_config(page_title=APP_TITLE, page_icon="🚨", layout="wide")
st.title("🚨 Incident → Executive Summary Generator")
st.caption("Turn technical incident notes into executive-ready and customer-ready communications.")

with st.sidebar:
    st.header("Controls")
    mode = st.selectbox("Tone", ["Concise", "Executive", "Board-level"], index=1)
    include_customer_email = st.checkbox("Include customer-facing email", value=True)
    no_api_mode = st.checkbox("No-API Template Mode (no model calls)", value=False)
    model = st.selectbox("Model", [DEFAULT_MODEL], index=0)

    st.divider()
    if st.button("Clear form"):
        for k in list(st.session_state.keys()):
            if k.startswith("f_"):
                del st.session_state[k]
        st.rerun()

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incident details")
    f_title = st.text_input("Incident title", key="f_title", placeholder="e.g., Elevated 500 errors on API Gateway")
    f_severity = st.selectbox("Severity", ["SEV1", "SEV2", "SEV3", "SEV4"], index=1, key="f_severity")
    f_start = st.text_input("Start time", key="f_start", placeholder="e.g., 2026-03-03 14:10 ET")
    f_end = st.text_input("End time / Restored time", key="f_end", placeholder="e.g., 2026-03-03 14:52 ET")
    f_duration = st.text_input("Duration (if known)", key="f_duration", placeholder="e.g., 42 minutes")
    f_services = st.text_area("Services affected", key="f_services", placeholder="e.g., API Gateway, Auth service")

with col2:
    st.subheader("Impact + remediation")
    f_impact = st.text_area("Customer impact / symptoms", key="f_impact", placeholder="e.g., 25% of requests returned 500s; intermittent login failures")
    f_scope = st.text_input("Scope (who/what was impacted)", key="f_scope", placeholder="e.g., NA region, ~30% of customers")
    f_root_cause = st.text_area("Root cause (technical)", key="f_root_cause", placeholder="e.g., DB connection pool exhaustion after deploy")
    f_mitigation = st.text_area("Mitigation / resolution actions", key="f_mitigation", placeholder="e.g., rolled back deployment; increased pool size; restarted pods")
    f_next_steps = st.text_area("Prevention / next steps", key="f_next_steps", placeholder="e.g., add alerting; load test; deploy guardrails")

st.subheader("Optional")
f_internal_notes = st.text_area("Internal notes (optional)", key="f_internal_notes", placeholder="Links, ticket IDs, graphs, owners, etc.")
f_audience = st.selectbox("Audience", ["Executives", "Executives + Customer", "Internal stakeholders"], index=1, key="f_audience")

# --- Build a structured incident payload for the model ---
incident_payload = f"""
Incident Title: {f_title}
Severity: {f_severity}
Start Time: {f_start}
End/Restored Time: {f_end}
Duration: {f_duration}

Services Affected:
{f_services}

Customer Impact / Symptoms:
{f_impact}

Scope (who/what impacted):
{f_scope}

Root Cause (technical):
{f_root_cause}

Mitigation / Resolution Actions:
{f_mitigation}

Prevention / Next Steps:
{f_next_steps}

Internal Notes:
{f_internal_notes}
""".strip()

st.divider()

generate = st.button("Generate Executive Summary", type="primary", use_container_width=True)

def render_template_only():
    # Useful even with no API calls
    template = f"""### Executive Summary
{f_title or "(Add incident title)"} impacted customers for {f_duration or "(duration)"}.
Service was restored by {f_end or "(restored time)"}.

### Customer Impact
- Duration: {f_duration or "(unknown)"}
- Services affected: {f_services or "(unknown)"}
- Who was impacted: {f_scope or "(unknown)"}
- What users experienced: {f_impact or "(unknown)"}
- Data integrity (if known): (add if known)

### Timeline
- Detection: {f_start or "(unknown)"}
- Investigation: (add)
- Mitigation: {f_mitigation or "(add)"}
- Resolution: {f_end or "(unknown)"}
- Post-incident actions: {f_next_steps or "(add)"}

### Root Cause (Plain English)
- {f_root_cause or "(add root cause)"}

### Mitigations Applied
- {f_mitigation or "(add mitigation)"}

### Prevention / Next Steps
- {f_next_steps or "(add next steps)"}
"""
    if include_customer_email:
        template += """
### Customer-facing Update (Email-ready)
Subject: Service disruption update

Body:
Hi team,

We experienced a service disruption impacting <service> from <start> to <end>. During this time, some users may have seen <symptoms>.
Service has been restored and we are implementing preventive measures to reduce the likelihood of recurrence.

If you have any questions or need support validating recovery, reply here and we’ll help.

Best,
<Your Name>
"""
    return template

if generate:
    if no_api_mode:
        st.subheader("Output")
        st.code(render_template_only())
        st.info("Template Mode is on: no API calls were made.")
        st.stop()

    # API mode
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        st.error("OPENAI_API_KEY is not set. Add it to your .env file, then restart Streamlit.")
        st.stop()

    client = OpenAI()

    audience_note = {
        "Executives": "Primary audience is executives only.",
        "Executives + Customer": "Primary audience is executives and customer-facing stakeholders.",
        "Internal stakeholders": "Primary audience is internal stakeholders; still keep it clear and non-jargony."
    }[f_audience]

    instructions = mode_instructions(mode)
    if not include_customer_email:
        output_format = OUTPUT_FORMAT.replace("### Customer-facing Update (Email-ready)", "### Customer-facing Update (Email-ready)\n(omit this section)\n")
    else:
        output_format = OUTPUT_FORMAT

    prompt = f"""
{audience_note}

MODE INSTRUCTIONS:
{instructions}

INCIDENT REPORT:
{incident_payload}

{output_format}
""".strip()

    with st.spinner("Generating..."):
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        output = resp.output_text.strip()

    st.subheader("Output")
    st.write(output)

    st.download_button(
        "Download as Markdown (.md)",
        data=output.encode("utf-8"),
        file_name="incident_executive_summary.md",
        mime="text/markdown",
        use_container_width=True
    )
