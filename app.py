import streamlit as st
from src.atlas.demo_data import load_sample_tickets
from src.atlas.triage import triage_ticket

st.set_page_config(
    page_title="Atlas AI Help Desk Copilot",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("Atlas AI Help Desk Copilot")
st.markdown(
    "Triage assistant for IT help desk teams. Classifies incoming tickets, surfaces relevant "
    "knowledge base articles, and generates technician guidance — so agents spend less time "
    "on intake and more time resolving."
)
st.divider()

# ── Data ─────────────────────────────────────────────────────────────────────
tickets = load_sample_tickets()
all_triage = [triage_ticket(t) for t in tickets]

# ── Metrics Row ───────────────────────────────────────────────────────────────
total = len(tickets)
high_urgent = sum(1 for t in tickets if t["priority"] in ("high", "urgent"))
open_count = sum(1 for t in tickets if t["status"] == "open")
escalation_count = sum(1 for r in all_triage if r["escalation_recommended"])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Tickets", total)
m2.metric("High / Urgent", high_urgent, delta=f"{round(high_urgent/total*100)}% of queue", delta_color="inverse")
m3.metric("Open", open_count)
m4.metric("Escalation Candidates", escalation_count, delta_color="inverse")

st.divider()

# ── Input Section ─────────────────────────────────────────────────────────────
st.subheader("Ticket Input")

left, right = st.columns([3, 1])

with left:
    ticket_options = {f"[{t['id']}] {t['subject']}": t for t in tickets}
    selected_label = st.selectbox("Sample ticket", options=list(ticket_options.keys()))
    selected_ticket = ticket_options[selected_label]

    st.markdown("**Or enter a custom ticket below** *(overrides selection above)*")
    custom_subject = st.text_input("Subject", placeholder="e.g. Cannot connect to corporate VPN")
    custom_desc = st.text_area("Description", placeholder="Describe the issue in detail...", height=100)

with right:
    st.markdown("**Ticket Preview**")
    st.markdown(f"**ID:** `{selected_ticket['id']}`")
    st.markdown(f"**Priority:** `{selected_ticket['priority'].upper()}`")
    st.markdown(f"**Category:** `{selected_ticket['category']}`")
    st.markdown(f"**Status:** `{selected_ticket['status']}`")
    st.markdown(f"**Submitter:** {selected_ticket['submitter']}")

analyze = st.button("Analyze Ticket", type="primary", use_container_width=True)

# ── Analysis Results ──────────────────────────────────────────────────────────
if analyze:
    if custom_subject.strip() or custom_desc.strip():
        active_ticket = {
            "id": "TKT-CUSTOM",
            "subject": custom_subject.strip() or "(no subject)",
            "description": custom_desc.strip(),
        }
    else:
        active_ticket = selected_ticket

    result = triage_ticket(active_ticket)

    st.divider()
    st.subheader(f"Triage Results — `{result['ticket_id']}`")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Category", result["suggested_category"].title())
    r2.metric("Suggested Priority", result["suggested_priority"].upper())
    r3.metric("Confidence", result["confidence"].title())
    with r4:
        if result["escalation_recommended"]:
            st.error(f"⚠ Escalate\n\n{result['escalation_reason']}")
        else:
            st.success("✓ No escalation needed")

    st.divider()

    # KB + Checklist
    kb_col, check_col = st.columns(2)

    with kb_col:
        st.subheader("Knowledge Base Matches")
        if result["kb_matches"]:
            for entry in result["kb_matches"]:
                with st.expander(f"{entry['id']} — {entry['title']}"):
                    for step in entry["steps"]:
                        st.markdown(f"- {step}")
        else:
            st.info("No KB articles found for this category.")

    with check_col:
        st.subheader("Troubleshooting Checklist")
        all_steps = [step for entry in result["kb_matches"] for step in entry["steps"]]
        if all_steps:
            for i, step in enumerate(all_steps, 1):
                st.checkbox(step, key=f"chk_{i}")
        else:
            st.info("No checklist items available.")

    st.divider()

    # Response Draft
    st.subheader("Customer-Facing Response Draft")
    st.caption("Review and edit before sending to the user.")
    st.text_area(
        "Response draft",
        value=result["response_draft"],
        height=180,
        label_visibility="collapsed",
    )

    st.divider()

    # Technician Notes + Resolution Template
    notes_col, res_col = st.columns(2)

    with notes_col:
        st.subheader("Technician Notes")
        st.caption("Internal guidance — not visible to end users.")
        st.markdown(result["technician_notes"])

    with res_col:
        st.subheader("Resolution Documentation Template")
        st.caption("Complete after resolving the ticket.")
        st.text_area(
            "Resolution template",
            value=result["resolution_template"],
            height=300,
            label_visibility="collapsed",
        )

    st.divider()
    st.caption(
        "⚠ **Atlas assists technicians — it does not replace judgement.** "
        "All outputs are suggestions based on keyword matching and should be reviewed before acting. "
        "Atlas has no access to live systems, user data, or AI models."
    )
