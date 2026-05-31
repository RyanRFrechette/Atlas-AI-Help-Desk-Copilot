import streamlit as st
from src.atlas.demo_data import load_sample_tickets

st.set_page_config(page_title="Atlas AI Help Desk Copilot", layout="wide")

st.title("Atlas AI Help Desk Copilot")
st.caption("AI-powered triage and knowledge assistant — Phase 1 scaffold")

st.info("Full UI coming in Phase 2. Showing raw sample tickets for now.")

tickets = load_sample_tickets()
for ticket in tickets:
    with st.expander(f"[{ticket['id']}] {ticket['subject']}"):
        st.write(f"**Category:** {ticket['category']}")
        st.write(f"**Priority:** {ticket['priority']}")
        st.write(f"**Status:** {ticket['status']}")
        st.write(f"**Description:** {ticket['description']}")
