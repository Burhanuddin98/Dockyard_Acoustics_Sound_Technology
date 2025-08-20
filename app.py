# app.py — Dockyard Acoustics (minimal, clean, working)
# Run:
#   pip install streamlit pandas
#   streamlit run app.py
import smtplib, ssl
from email.message import EmailMessage
import streamlit.components.v1 as components

# app.py — Dockyard Acoustics (minimal + email leads)

import re
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------
# Company config
# ---------------------------
COMPANY_NAME   = "Dockyard Acoustics Sound Technology"
COMPANY_EMAIL  = "bisdansk@gmail.com"
COMPANY_ADDR   = "Guldblommevej 2, 1, th, 2750 Ballerup, Denmark"
LINKEDIN_URL   = "https://www.linkedin.com/in/bisdansk/"
LEGAL_FORM     = "Personligt ejet Mindre Virksomhed (PMV)"
CVR_NUMBER     = "45796256"

ASSETS = Path("assets"); ASSETS.mkdir(exist_ok=True)
LOGO_PATH = ASSETS / "logo.png"  # put your red cat-headphones logo here
PAGE_ICON = str(LOGO_PATH) if LOGO_PATH.exists() else "🔊"

st.set_page_config(page_title=COMPANY_NAME, page_icon=PAGE_ICON, layout="wide")

# ---------------------------
# Styles (kept simple to avoid syntax issues)
# ---------------------------
BRAND = {
    "primary": "#EF4444",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
    "panel": "rgba(255,255,255,0.04)",
    "panel_border": "rgba(255,255,255,0.08)",
    "bg_top": "#0b0a10",
    "bg_bottom": "#161722",
}

st.markdown(
    f"""
    <style>
      .main .block-container {{ max-width: 1100px; padding-top: 2rem; padding-bottom: 4rem; }}
      body, .main {{ background: linear-gradient(180deg, {BRAND['bg_top']} 0%, {BRAND['bg_bottom']} 100%); color: {BRAND['text']}; }}
      h1, h2, h3, h4, h5, h6 {{ color: {BRAND['text']}; }}
      .card {{ background: {BRAND['panel']}; border: 1px solid {BRAND['panel_border']}; padding: 1rem 1.2rem; border-radius: 14px; }}
      .pill {{ display:inline-block; padding:.35rem .7rem; border-radius:9999px; border:1px solid {BRAND['panel_border']}; background:{BRAND['panel']}; font-size:.85rem; color:{BRAND['text']}; margin-right:.5rem; }}
      .muted {{ color: {BRAND['muted']}; }}
      .btn {{ display:inline-block; padding:.6rem 1rem; border-radius: 10px; text-decoration:none; font-weight:600; }}
      .btn-primary {{ background:{BRAND['primary']}; color:white; }}
      .btn-ghost {{ background:transparent; color:{BRAND['text']}; border:1px solid {BRAND['panel_border']}; }}
    </style>
    """,
    unsafe_allow_html=True,
)
# ---------------------------
# Email helper (Streamlit Cloud)
# ---------------------------
def send_lead_email(row: dict) -> tuple[bool, str]:
    """Send the lead via SMTP using secrets in Streamlit Cloud. Returns (ok, msg)."""
    try:
        host = st.secrets["SMTP_HOST"]
        user = st.secrets["SMTP_USER"]
        pwd  = st.secrets["SMTP_PASS"]
        port = int(st.secrets.get("SMTP_PORT", 465))
        to_addr = st.secrets.get("LEADS_TO", COMPANY_EMAIL)
    except Exception:
        return False, "SMTP secrets not configured"

    try:
        msg = EmailMessage()
        msg["Subject"] = f"New lead — {row.get('name','')}"
        msg["From"] = user
        msg["To"] = to_addr

        lines = [
            f"Time: {row.get('timestamp','')}",
            f"Name: {row.get('name','')}",
            f"Email: {row.get('email','')}",
            f"Company: {row.get('company','')}",
            f"Topic: {row.get('topic','')}",
            f"Budget: {row.get('budget','')}",
            "",
            str(row.get('message','')),
            "",
        ]
        msg.set_content("\n".join(lines))

        with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as s:
            s.login(user, pwd)
            s.send_message(msg)
        return True, "Lead emailed"
    except Exception as e:
        return False, str(e)
def goto_tab(tab_label: str):
    # Click the Streamlit tab whose label matches tab_label (case-insensitive)
    components.html(f"""
    <script>
    setTimeout(function(){{
      const tabs = Array.from(window.parent.document.querySelectorAll('button[role="tab"]'));
      const t = tabs.find(el => el.innerText.trim().toLowerCase() === "{tab_label.lower()}");
      if (t) t.click();
    }}, 0);
    </script>
    """, height=0, width=0)

# ---------------------------
# Layout
# ---------------------------
Home, About, Projects, Contact = st.tabs(["Home", "About", "Projects", "Contact"])

# ---------------------------
# HOME
# ---------------------------
with Home:
    c1, c2 = st.columns([1,3])
    with c1:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=130)
    with c2:
        st.markdown("### Dockyard Acoustics Sound Technology")
        st.markdown("<h1 style=\"margin:.1rem 0 .6rem 0\">Self‑tuning wireless speakers</h1>", unsafe_allow_html=True)
        st.write(
            "True Wireless Stereo (TWS), rechargeable, and able to estimate the Room Impulse Response (RIR) to auto‑tune for optimum performance."
        )
        if st.button("Contact", type="primary"):
            goto_tab("Contact")

    st.divider()

    a, b, c = st.columns(3)
    with a: st.markdown("<div class='card'><h4>Edge DSP + ML</h4><p class='muted'>On‑device RIR → auto‑EQ</p></div>", unsafe_allow_html=True)
    with b: st.markdown("<div class='card'><h4>TWS + Rechargeable</h4><p class='muted'>Seamless pairing, OTA updates</p></div>", unsafe_allow_html=True)
    with c: st.markdown("<div class='card'><h4>Verification</h4><p class='muted'>RT60, DRR, C50/C80, A/B audio</p></div>", unsafe_allow_html=True)

# ---------------------------
# ABOUT
# ---------------------------
with About:
    st.markdown("### About")
    st.write("We build self‑tuning TWS speakers and collaborate with select teams on acoustics/DSP/ML.")
    left, right = st.columns([2,1])
    with left:
        st.markdown("#### Team")
        st.write("- **Burhanuddin Ibrahim Sakarwala** — Co‑founder & CTO (Acoustics/DSP/ML) · [LinkedIn](%s)" % LINKEDIN_URL)
        st.info("Add your co‑founder here once details are final.")
    with right:
        st.markdown("#### Company & Legal")
        st.write(COMPANY_ADDR)
        st.write(f"Legal form: **{LEGAL_FORM}**")
        st.write(f"CVR: **{CVR_NUMBER}**")

# ---------------------------
# PROJECTS
# ---------------------------
with Projects:
    st.markdown("### Projects & Updates")
    st.write("For now, see ongoing work on LinkedIn.")
    st.link_button("LinkedIn — @bisdansk", LINKEDIN_URL, use_container_width=False)

# ---------------------------
# CONTACT
# ---------------------------
with Contact:
    st.markdown("<a name='contact'></a>", unsafe_allow_html=True)
    st.markdown("### Contact")
    st.write("Tell us about your product or space. We reply within one business day.")

    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *")
            email = st.text_input("Email *")
            company = st.text_input("Company")
        with col2:
            topic = st.selectbox("Topic", [
                "Self‑tuning TWS speaker",
                "Acoustic simulation",
                "Audio DSP / ML",
                "Measurement & QA",
                "Other",
            ])
            budget = st.selectbox("Budget", ["< €5k", "€5–20k", "€20–100k", "> €100k", "Not sure"]) 
        message = st.text_area("Message *", height=140)
        submitted = st.form_submit_button("Send")

        if submitted:
            if not (name and email and message):
                st.error("Please fill the required fields (Name, Email, Message).")
            else:
                row = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "name": name,
                    "email": email,
                    "company": company,
                    "topic": topic,
                    "budget": budget,
                    "message": message,
                }
                leads = Path("leads.csv")
                df = pd.DataFrame([row])
                if leads.exists():
                    df.to_csv(leads, mode="a", index=False, header=False)
                else:
                    df.to_csv(leads, index=False)
                st.success("Thanks! Your message has been recorded.")
                try:
                    st.caption(f"Saved to {leads.resolve()}")
                except Exception:
                    pass

                ok, info_msg = send_lead_email(row)
                if ok:
                    st.toast(f"Lead emailed to {COMPANY_EMAIL}")
                else:
                    st.info(f"Lead saved. Email not sent: {info_msg}")


    st.markdown(
        f"<div class='muted' style='margin-top:1rem'>Email: {COMPANY_EMAIL} · Address: {COMPANY_ADDR} · CVR: {CVR_NUMBER} · © {datetime.now(timezone.utc).year} {COMPANY_NAME}</div>",
        unsafe_allow_html=True,
    )
