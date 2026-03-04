Project Status: Actively under development

# Incident → Executive Summary Generator 🚨

A lightweight Streamlit app that turns raw incident notes into executive-ready summaries and customer-facing updates.

## Why it exists
Technical incident write-ups are often too detailed for executives and too technical for customer updates. This tool converts incident details into:
- Executive Summary
- Customer Impact
- Timeline
- Root Cause (plain English)
- Mitigations
- Prevention / Next Steps
- Customer-facing email

## Features
- Clean Streamlit UI
- Tone modes: Concise / Executive / Board-level
- Optional customer email generation
- Markdown export
- No-API Template Mode (works without model calls)

## Tech Stack
- Python
- Streamlit
- OpenAI API 

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
