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

import base64

def video_autoplay_html(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode()
    return f"""
    <video autoplay muted loop playsinline
           style="width:100%; border-radius:12px; margin-top:.5rem;">
      <source src="data:video/mp4;base64,{data}" type="video/mp4">
    </video>
    """
def video_teaser_html(path: Path, size_px: int = 130) -> str:
    data = base64.b64encode(path.read_bytes()).decode()
    return f"""
    <div style="
        width:{size_px}px; height:{size_px}px;
        border-radius:12px; overflow:hidden;
        margin-top:.5rem; box-shadow:0 6px 24px rgba(0,0,0,.25);
    ">
      <video autoplay muted loop playsinline
             style="width:100%;height:100%;object-fit:cover;display:block;">
        <source src="data:video/mp4;base64,{data}" type="video/mp4">
      </video>
    </div>
    """
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
VIDEO_PATH = ASSETS / "hero.mp4"    
PAGE_ICON = str(LOGO_PATH) if LOGO_PATH.exists() else "🔊"

st.set_page_config(page_title=COMPANY_NAME, page_icon=PAGE_ICON, layout="wide")
hdr = st.container()
with hdr:
    # LEFT aligned (logo then spacer)
    col_logo, _ = st.columns([1, 9])   # for RIGHT: swap to [9,1] and put image in the second col
    with col_logo:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=80)
        else:
            st.warning(f"Logo not found: {LOGO_PATH}")# ---------------------------
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
#        if LOGO_PATH.exists():
#            st.image(str(LOGO_PATH), width=130)
            # --- video under the logo ---
        if VIDEO_PATH.exists():
            st.markdown(video_autoplay_html(VIDEO_PATH), unsafe_allow_html=True)
            st.image("assets/Screenshot 2025-11-26 010011.png", use_column_width=True)
            st.image("assets/WhatsApp Image 2025-11-01 at 03.07.00_f1d49696.jpg", use_column_width=True)
            
    with c2:
        st.markdown("## Dockyard Acoustics Sound Technology")
        st.markdown("<h3 style=\"margin:.1rem 0 .6rem 0\">State of the art Acoustic Simulation Software</h3>", unsafe_allow_html=True)
        st.write("Dockyard Acoustics is redefining how enthusiasts and professionals shape sound. Our Diffraction-Physics Room Acoustics Engine uses advanced, next-generation physics to deliver acoustic simulations with unprecedented speed, accuracy, and reliability. A all-in-one highly intuitive and portable platform.")
        st.write("We empower architects, acoustic consultants, and engineers to design and optimize acoustic environments with confidence. From early-stage concepts to final design refinement.")
        st.write("Dockyard Acoustics makes powerful acoustic analysis accessible, efficient, and effortless.")
        st.write("In addition to acoustics, we are expanding our core engine into Computational Fluid Dynamics (CFD) and real-time simulation pipelines. Our technology supports both recurring-license products and high-impact custom projects.
        st.markdown("### Custom Development & Engineering Expertise")
        st.write("""
        Dockyard Acoustics also provides custom simulation tools and consultancy, combining deep expertise in:
        - Mechanical Engineering
        - Structural Engineering
        - Embedded Systems
        - Acoustics & Computational Physics
        From bespoke simulations to entirely new physics engines, we design and implement custom methods of computation, solvers, and real-time pipelines. This includes diffraction-based acoustics, hybrid solvers, and emerging multi-physics systems, specific to your product, workflow, or platform.
        We build:
        - Custom physics engines and solvers
        - New computational methods
        - GPU-accelerated pipelines
        - Research-grade tools adapted for industry use
        
        Contact us and get your projects brought to life.
        """)
        if st.button("Contact", type="primary"):
            goto_tab("Contact")

    st.divider()

    # a, b, c = st.columns(3)
    # with a: st.markdown("<div class='card'><h4>Edge DSP + ML</h4><p class='muted'>On‑device RIR → auto‑EQ</p></div>", unsafe_allow_html=True)
    # with b: st.markdown("<div class='card'><h4>TWS + Rechargeable</h4><p class='muted'>Seamless pairing, OTA updates</p></div>", unsafe_allow_html=True)
    # with c: st.markdown("<div class='card'><h4>Verification</h4><p class='muted'>RT60, DRR, C50/C80, A/B audio</p></div>", unsafe_allow_html=True)

# ---------------------------
# ABOUT
# ---------------------------
with About:
    st.markdown("### About")
    st.write("""
    Dockyard Acoustics develops advanced simulation technologies designed to bring next-generation accuracy, speed, and usability to acoustic and physical modelling. 
    Our core product is a state-of-the-art Diffraction Physics Engine that enables precise room-acoustic simulation and forms the foundation for future expansion into CFD and broader physics-based applications. These expansions are designed to support long-term, recurring integrations for industry partners, alongside targeted one-off development projects.
    Beyond software, we offer tailored solutions and consultancy, adapting our engine to specific industry needs or building custom tools for unique challenges. Our interdisciplinary expertise spans Mechanical, Structural, Embedded Systems, and Acoustics Engineering, allowing us to deliver high-performance, science-driven solutions for architects, industry partners, and engineering teams seeking deeper insight and better design outcomes.
    At Dockyard Acoustics, we turn complex physics and acoustics into accessible, powerful tools that elevate engineering workflows and enable better environments one simulation at a time. 
    """)
    st.markdown("### Why Dockyard Acoustics")
    st.write("""
    Behind the code is a simple belief:
    Powerful tools should be accessible — not locked behind complexity.
    We’re creating an engine that architects, designers, consultants, and enthusiasts can use without needing a PhD in acoustics. A tool that demystifies sound, accelerates workflows, and reveals what the ear can’t see.
    And along the journey, we’re grateful for the support of the engineering community. Every connection, question, and conversation has helped shape where this technology is heading.
    """)
    left, right = st.columns([2,1])
    with left:
        st.markdown("#### Team")
        st.write("- **Burhanuddin Ibrahim Sakarwala** — Co‑founder & CTO (Acoustics/DSP/ML) · [LinkedIn](%s)" % LINKEDIN_URL)
        st.write("- **Pedro Correia** (Engineering/Management) · [LinkedIn](%s)" % "https://www.linkedin.com/in/pedrolcorreia")
        # st.info("Add your co‑founder here once details are final.")
    with right:
        st.markdown("#### Company & Legal")
        st.write(COMPANY_ADDR)
        st.write(f"Legal form: **{LEGAL_FORM}**")
        st.write(f"CVR: **{CVR_NUMBER}**")

# ---------------------------
# PROJECTS
# ---------------------------
with Projects:
    st.markdown("### Building the Future of Acoustic Simulation")
    st.write(""" 
    At Dockyard Acoustics, we believe advanced scientific tools shouldn’t be reserved only for scientists.
    Acoustic simulation should be intuitive, visual, and accessible, whether you’re an architect, designer, engineer, or simply someone passionate about sound.
    We’ve been pushing the boundaries of what room-acoustic software can do.
    """)
    
    st.markdown("#### Powerful Sound Visualization")
    st.write("""
    We’ve transformed the invisible physics of acoustics into something you can see, interact with, and understand at a glance. 
    From modal fields to toroidal rooms and multi-room simulations, our visualizations reveal:
    - Where energy builds and collapses
    - How resonances shift with design changes
    - How sound "breathes" inside a space
    These are real wave-physics outputs driven by Green’s Functions, hybrid solvers, and GPU-accelerated rendering.
    Each glowing volume, isosurface, and neon resonance comes directly from the underlying physics.
    """)    
    st.image("assets/Screenshot 2025-10-31 121113.png", use_column_width=True)
    st.markdown("#### Breakthroughs in Our Physics Engine")
    st.write("""
    Our diffraction-first acoustics engine has rapidly evolved into a hybrid system capable of handling:
    - Arbitrary, asymmetric geometry
    - Ducts, cavities, and obstacles
    - Real-time GPU-assisted previews
    - Multi-source volumetric fields
    - Modal and ray-tracing hybrids
    - Per-source slice visualization
    - Interactive parameter controls
    Our newest release simulates larger rooms, higher resolutions, and denser modal sums, all with smooth, responsive UI.
    """)
    st.markdown("#### Your Room, Your Model, Your Sound")
    st.write("""
    We’re building tools that let anyone “listen to their design” before it exists:
    1. Upload a 3D model → pick materials → simulate
    - 3D Green’s Function fields
    - RT60 and EDC curves
    - Full impulse responses (IRs)
    - Spectrograms (dry, wet, convolved audio)
    - Ray-based path visualizations
    2. or simply record your room on your phone
    - Clap / sweep → upload WAV → receive:
    - Per-octave RT60 analysis
    - Low-frequency problem detection
    - Auto-suggested acoustic treatments
    - a 3D modal visualization
    - a downloadable PDF with BOM + recommendations
All designed to help consultants, architects, and engineers solve acoustic problems faster.

    """)
    st.image("assets/WhatsApp Image 2025-09-26 at 17.46.22_06d07261.jpg", use_column_width=True)
    st.markdown("#### Physics + AI = Instant Acoustic Insight")
    st.write("""
    We’re also experimenting with Physics-Informed Neural Networks (PINNs) to model 2D and 3D fields instantly, without meshing:
    - Interactive sliders
    - Adjustable frequency and damping
    - Movable seats and sources
    - Real-time 3D results
    - Export to VTK or NumPy
    It’s like a virtual lab: perfect for rapid prototyping, teaching, and design exploration.
    """)
    st.markdown("#### What’s Next?")
    st.write("""
    These expansions are designed to support long-term, recurring integrations for industry partners, alongside targeted one-off development projects.
    Current & Upcoming Development Tracks:
    - Computational Fluid Dynamics (CFD)
    A high-performance CFD solver designed for continuous integration into engineering workflows and licensed deployments.
    - Real-Time Acoustics for Game Engines
    A focused, high-value development track delivering custom real-time acoustics engines for interactive applications and games. These projects are typically one-off, production-ready builds.
    - Multi-room 3D binaural simulations
    - Advanced audio rendering pipelines
    - Industry-ready plugins and standalone applications
    The future of acoustic design is interactive, visual, and physics-accurate, and we’re building it one breakthrough at a time.
    """)
    st.write("For more, see ongoing work on LinkedIn.")
    st.link_button("LinkedIn — @bisdansk", LINKEDIN_URL, use_container_width=False)

# ---------------------------
# CONTACT
# ---------------------------
with Contact:
    st.markdown("<a name='contact'></a>", unsafe_allow_html=True)
    st.markdown("### How We Work")
    st.write("""
    We engage through two primary models:
    1. Product & Platform Integration
    Long-term partnerships using our acoustics and CFD engines as licensed components within your products or workflows.
    2. Custom Engine Development
    Custom projects where we design and deliver new simulation systems, solvers, or real-time pipelines tailored to your needs.
    """)
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
                "Diffraction-Physics Room Acoustics Engine",
                "CFD engine",
                "Acoustic simulation",
                "Audio DSP / ML",
                "Measurement & QA",
                "Consultancy",
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
