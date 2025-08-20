# app.py — Dockyard Acoustics (minimal + better leads)
# Run:
#   pip install streamlit pandas
#   streamlit run app.py

from __future__ import annotations
import re
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# --- Company config ---
COMPANY_NAME   = "Dockyard Acoustics Sound Technology"
COMPANY_EMAIL  = "bisdansk@gmail.com"
COMPANY_ADDR   = "Guldblommevej 2, 1, th, 2750 Ballerup, Denmark"
LINKEDIN_URL   = "https://www.linkedin.com/in/bisdansk/"
LEGAL_FORM     = "Personligt ejet Mindre Virksomhed (PMV)"
CVR_NUMBER     = "45796256"

ASSETS = Path("assets"); ASSETS.mkdir(exist_ok=True)
LOGO_PATH = ASSETS / "logo.png"   # put your logo here
PAGE_ICON = str(LOGO_PATH) if LOGO_PATH.exists() else "🔊"
st.set_page_config(page_title=COMPANY_NAME, page_icon=PAGE_ICON, layout="wide")

# --- Styles ---
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
      .muted {{ color: {BRAND['muted']}; }}
      .btn {{ display:inline-block; padding:.6rem 1rem; border-radius: 10px; text-decoration:none; font-weight:600; }}
      .btn-primary {{ background:{BRAND['primary']}; color:white; }}
      .hp {{ position:absolute; left:-10000px; top:auto; width:1px; height:1px; overflow:hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Tabs ---
Home, About, Projects, Contact = st.tabs(["Home", "About", "Projects", "Contact"])

# --- HOME ---
with Home:
    c1, c2 = st.columns([1,3])
    with c1:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=130)
    with c2:
        st.markdown("### Dockyard Acoustics Sound Technology")
        st.markdown("<h1 style='margin:.1rem 0 .6rem 0'>Self-tuning wireless speakers</h1>", unsafe_allow_html=True)
        st.write("True Wireless Stereo (TWS), rechargeable, and able to estimate the Room Impulse Response (RIR) to auto-tune for optimum performance.")
        st.markdown(f"<a class='btn btn-primary' href='#contact'>Contact</a>", unsafe_allow_html=True)
    st.divider()
    a, b, c = st.columns(3)
    with a: st.markdown("<div class='card'><h4>Edge DSP + ML</h4><p class='muted'>On-device RIR → auto-EQ</p></div>", unsafe_allow_html=True)
    with b: st.markdown("<div class='card'><h4>TWS + Rechargeable</h4><p class='muted'>Seamless pairing, OTA updates</p></div>", unsafe_allow_html=True)
    with c: st.markdown("<div class='card'><h4>Verification</h4><p class='muted'>RT60, DRR, C50/C80, A/B audio</p></div>", unsafe_allow_html=True)

# --- ABOUT ---
with About:
    st.markdown("### About")
    st.write("We build self-tuning TWS speakers and collaborate with select teams on acoustics/DSP/ML.")
    left, right = st.columns([2,1])
    with left:
        st.markdown("#### Team")
        st.write(f"- **Burhanuddin Ibrahim Sakarwala** — Co-founder & CTO (Acoustics/DSP/ML) · [LinkedIn]({LINKEDIN_URL})")
        st.info("Add your co-founder here once details are final.")
    with right:
        st.markdown("#### Company & Legal")
        st.write(COMPANY_ADDR)
        st.write(f"Legal form: **{LEGAL_FORM}**")
        st.write(f"CVR: **{CVR_NUMBER}**")

# --- PROJECTS ---
with Projects:
    st.markdown("### Projects & Updates")
    st.write("For now, see ongoing work on LinkedIn.")
    st.link_button("LinkedIn — @bisdansk", LINKEDIN_URL, use_container_width=False)

# --- CONTACT (better leads) ---
with Contact:
    st.markdown("<a name='contact'></a>", unsafe_allow_html=True)
    st.markdown("### Contact")
    st.write("Tell us about your product or space. We reply within one business day.")

    sid = st.session_state.setdefault("sid", str(uuid4()))

    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *")
            email = st.text_input("Email *")
            company = st.text_input("Company")
        with col2:
            topic = st.selectbox("Topic", [
                "Self-tuning TWS speaker",
                "Acoustic simulation",
                "Audio DSP / ML",
                "Measurement & QA",
                "Other",
            ])
            budget = st.selectbox("Budget", ["< €5k", "€5–20k", "€20–100k", "> €100k", "Not sure"])
        message = st.text_area("Message *", height=140)

        # honeypot for bots
        st.markdown("<div class='hp'>", unsafe_allow_html=True)
        hp = st.text_input("Leave this empty", value="")
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Send")

        if submitted:
            if hp:
                st.warning("Submission flagged as spam.")
            elif not (name and email and message):
                st.error("Please fill the required fields (Name, Email, Message).")
            elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                st.error("Please enter a valid email address.")
            else:
                row = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": sid,
                    "name": name,
                    "email": email,
                    "company": company,
                    "topic": topic,
                    "budget": budget,
                    "message": message.replace("\n", " "),
                }
                leads = Path("leads.csv")
                df = pd.DataFrame([row])
                if leads.exists():
                    df.to_csv(leads, mode="a", index=False, header=False)
                else:
                    df.to_csv(leads, index=False)
                st.success("Thanks! Your message has been recorded.")

    # Admin view (toggle with secrets)
    if st.secrets.get("SHOW_LEADS", "0") == "1":
        st.markdown("#### Leads (private)")
        leads = Path("leads.csv")
        if leads.exists():
            try:
                df = pd.read_csv(leads)
            except Exception:
                df = pd.read_csv(leads, header=None)
            st.dataframe(df, use_container_width=True)
            with open(leads, "rb") as f:
                st.download_button("Download leads.csv", f, file_name="leads.csv", mime="text/csv")
        else:
            st.info("No leads yet.")

    st.markdown(
        f"<div class='muted' style='margin-top:1rem'>Email: {COMPANY_EMAIL} · Address: {COMPANY_ADDR} · CVR: {CVR_NUMBER} · © {datetime.utcnow().year} {COMPANY_NAME}</div>",
        unsafe_allow_html=True,
    )
