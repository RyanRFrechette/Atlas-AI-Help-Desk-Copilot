import streamlit as st
from src.atlas.demo_data import load_sample_tickets
from src.atlas.triage import triage_ticket

st.set_page_config(
    page_title="Atlas AI Help Desk Copilot",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

VALID_CATEGORIES = ["access", "email", "hardware", "network", "security"]
VALID_PRIORITIES = ["urgent", "high", "medium", "low"]

RISK_ICON = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
PRIORITY_ICON = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}


@st.cache_data
def _load_tickets() -> list[dict]:
    return load_sample_tickets()


@st.cache_data
def _precompute_all_triage() -> list[dict]:
    return [triage_ticket(t) for t in _load_tickets()]


# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛡 Atlas AI Help Desk Copilot")
st.markdown(
    "Deterministic triage assistant for IT help desk teams. "
    "Classifies tickets, surfaces knowledge base articles, and generates technician guidance "
    "— so agents spend less time on intake and more time resolving."
)
st.divider()

# ── Dashboard Metrics ─────────────────────────────────────────────────────────
tickets = _load_tickets()
all_triage = _precompute_all_triage()

total = len(tickets)
high_urgent = sum(1 for t in tickets if t["priority"] in ("high", "urgent"))
escalations = sum(1 for r in all_triage if r["escalation_recommended"])
security_count = sum(1 for r in all_triage if r["issue_category"] == "security")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Tickets", total)
m2.metric(
    "High / Urgent",
    high_urgent,
    delta=f"{round(high_urgent / total * 100)}% of queue",
    delta_color="inverse",
)
m3.metric(
    "Escalation Candidates",
    escalations,
    delta=f"{round(escalations / total * 100)}% of queue",
    delta_color="inverse",
)
m4.metric("Security Tickets", security_count)

st.divider()

# ── Ticket Input ───────────────────────────────────────────────────────────────
st.subheader("Ticket Input")
input_left, input_right = st.columns([3, 1])

with input_left:
    ticket_options = {f"[{t['id']}] {t['subject']}": t for t in tickets}
    selected_label = st.selectbox("Sample ticket", options=list(ticket_options.keys()))
    selected_ticket = ticket_options[selected_label]

    st.markdown(
        "**Custom ticket input** "
        "*(overrides sample selection above if subject or description is provided)*"
    )
    custom_subject = st.text_input(
        "Subject", placeholder="e.g. Cannot connect to corporate VPN"
    )
    custom_desc = st.text_area(
        "Description", placeholder="Describe the issue in detail...", height=100
    )

    cat_col, pri_col = st.columns(2)
    with cat_col:
        custom_category = st.selectbox(
            "Category",
            options=["(auto-detect)"] + VALID_CATEGORIES,
            help="Leave as auto-detect to let Atlas classify the category.",
        )
    with pri_col:
        custom_priority = st.selectbox(
            "Priority",
            options=["(auto-detect)"] + VALID_PRIORITIES,
            help="Leave as auto-detect to inherit from demo data or keyword analysis.",
        )

with input_right:
    st.markdown("**Sample Ticket Preview**")
    st.markdown(f"**ID:** `{selected_ticket['id']}`")
    pri = selected_ticket["priority"]
    st.markdown(f"**Priority:** {PRIORITY_ICON.get(pri, '')} `{pri.upper()}`")
    st.markdown(f"**Category:** `{selected_ticket['category']}`")
    st.markdown(f"**Status:** `{selected_ticket['status']}`")
    st.markdown(f"**Submitter:** {selected_ticket['submitter']}")
    st.markdown(f"**Dept:** {selected_ticket['department']}")

analyze = st.button("⚡ Analyze Ticket", type="primary", use_container_width=True)

# ── Triage Results ─────────────────────────────────────────────────────────────
if analyze:
    if custom_subject.strip() or custom_desc.strip():
        active_ticket: dict = {
            "id": "TKT-CUSTOM",
            "subject": custom_subject.strip() or "(no subject)",
            "description": custom_desc.strip(),
            "submitter": "Custom Input",
        }
        if custom_category != "(auto-detect)":
            active_ticket["category"] = custom_category
        if custom_priority != "(auto-detect)":
            active_ticket["priority"] = custom_priority
    else:
        active_ticket = selected_ticket

    result = triage_ticket(active_ticket)
    tid = result["ticket_id"]

    st.divider()
    st.subheader(f"Triage Results — `{tid}`")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Category", result["issue_category"].title())
    r2.metric("Priority", result["priority"].upper())
    r3.metric("Confidence", result["confidence"].title())
    risk = result["risk_level"]
    r4.metric("Risk Level", f"{RISK_ICON.get(risk, '')} {risk.title()}")

    if result["escalation_recommended"]:
        st.error(f"⚠ **Escalation Recommended** — {result['escalation_reason']}")
    else:
        st.success("✓ No escalation required based on current triage analysis.")

    st.divider()

    kb_col, chk_col = st.columns(2)

    with kb_col:
        st.subheader("Matching KB Articles")
        kb_articles = result["matching_kb_articles"]
        if kb_articles:
            for entry in kb_articles:
                with st.expander(f"{entry['id']} — {entry['title']}"):
                    if entry.get("symptoms"):
                        st.markdown("**Symptoms:**")
                        for s in entry["symptoms"]:
                            st.markdown(f"- {s}")
                    if entry.get("escalation_triggers"):
                        st.markdown("**Escalation Triggers:**")
                        for trigger in entry["escalation_triggers"]:
                            st.markdown(f"- ⚠ {trigger}")
        else:
            st.info("No KB articles matched this category.")

    with chk_col:
        st.subheader("Troubleshooting Checklist")
        checklist = result["troubleshooting_checklist"]
        if checklist:
            for i, step in enumerate(checklist, 1):
                st.checkbox(step, key=f"chk_{tid}_{i}")
        else:
            st.info("No checklist items available.")

    st.divider()

    st.subheader("Customer-Facing Response Draft")
    st.caption("Review and personalise before sending. Do not send unreviewed output.")
    st.text_area(
        "response_draft_area",
        value=result["customer_response_draft"],
        height=230,
        label_visibility="collapsed",
    )

    st.divider()

    notes_col, res_col = st.columns(2)

    with notes_col:
        st.subheader("Technician Notes")
        st.caption("Internal guidance — not visible to end users.")
        if result["technician_notes"]:
            st.markdown(result["technician_notes"])
        else:
            st.info("No technician notes available for this category.")

    with res_col:
        st.subheader("Resolution Documentation Template")
        st.caption("Complete after resolving the ticket.")
        st.text_area(
            "resolution_template_area",
            value=result["resolution_documentation_template"],
            height=320,
            label_visibility="collapsed",
        )

    st.divider()
    st.caption(
        "⚠ **Atlas assists technicians — it does not replace professional judgement.** "
        "All outputs are deterministic suggestions based on keyword matching and structured ticket data. "
        "Review every output before taking action. "
        "Atlas has no access to live systems, user accounts, or AI models."
    )
