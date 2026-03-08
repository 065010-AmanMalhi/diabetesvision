import streamlit as st

def run():

    # ── HERO ──────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🇮🇳 Built for India's Healthcare Gap</div>
        <div class="hero-title">
            Early Detection.<br>
            <span>Clearer Vision. Longer Life.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center; color:#7A8FA6; font-size:1.15rem; 
    max-width:600px; margin:0 auto 2.5rem; line-height:1.7; font-family:'DM Sans', sans-serif">
        DiabetesVision uses deep learning to screen for Diabetic Retinopathy 
        and skin-based diabetes indicators — making specialist-level diagnosis 
        accessible at every primary health centre.
    </p>
    """, unsafe_allow_html=True)

    # ── STATS ─────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("77M+", "Diabetics in India"),
        ("1 in 3", "Will develop Retinopathy"),
        ("70%", "Cases go undetected"),
        ("₹500", "vs ₹5,000+ specialist visit"),
    ]
    for col, (num, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── PROBLEM → SOLUTION ────────────────────────────────
    st.markdown('<div class="section-header">The Problem</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Why 18 million Indians are at risk of preventable blindness</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="problem-card">
            <h4 style="color:#FF6B6B; margin-top:0">🚨 The Screening Gap</h4>
            <p style="color:#B0BEC5; line-height:1.8">
            India has <strong style="color:#E8EDF5">1 ophthalmologist per 70,000 people</strong> 
            in rural areas. Diabetic Retinopathy requires annual retinal screening — 
            but most patients never receive one until it's too late.
            </p>
            <p style="color:#B0BEC5; line-height:1.8">
            A specialist retinal screening costs <strong style="color:#E8EDF5">₹3,000–₹8,000</strong> 
            at private clinics — unaffordable for 60% of diabetic patients in Tier 3 cities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="solution-card">
            <h4 style="color:#00D4AA; margin-top:0">✅ The DiabetesVision Solution</h4>
            <p style="color:#B0BEC5; line-height:1.8">
            A deep learning model trained on <strong style="color:#E8EDF5">10,000+ clinical images</strong> 
            that grades Diabetic Retinopathy (0–4) with 85%+ accuracy — 
            deployable on a basic tablet at any PHC.
            </p>
            <p style="color:#B0BEC5; line-height:1.8">
            Every result includes a <strong style="color:#E8EDF5">Grad-CAM heatmap</strong> showing 
            exactly which retinal region drove the diagnosis — 
            making AI decisions explainable to clinicians.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── WHO IS THIS FOR ───────────────────────────────────
    st.markdown('<div class="section-header">Who Uses DiabetesVision</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Designed for three distinct healthcare contexts</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    usecases = [
        ("🏥", "Primary Health Centres", 
         "Rural PHC staff upload retinal scans taken with low-cost fundus cameras. AI grades severity and flags urgent cases for specialist referral — no ophthalmologist on-site needed."),
        ("🏨", "Private Clinics & Hospitals",
         "Dermatologists and general physicians use the skin screening module for early diabetes indicators. Saves consultation time and provides documented AI-assisted evidence."),
        ("🧑‍⚕️", "Diabetic Patients",
         "Patients use the self-screening module to assess skin lesion risk between doctor visits. Plain-English results and clear next steps — no medical jargon.")
    ]

    for col, (icon, title, desc) in zip([col1, col2, col3], usecases):
        with col:
            st.markdown(f"""
            <div class="usecase-card">
                <div class="usecase-icon">{icon}</div>
                <div class="usecase-title">{title}</div>
                <div class="usecase-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── MODE SELECTOR ─────────────────────────────────────
    st.markdown('<div class="section-header" style="text-align:center">Start Screening</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub" style="text-align:center">Choose your role to get started</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🟢</div>
            <div class="mode-title">Patient Screening</div>
            <div class="mode-desc">
                Upload a skin photo and answer a few questions. 
                Get a plain-English risk assessment with AI heatmap 
                and personalised next steps.
            </div>
            <br>
            <div style="color:#00D4AA; font-weight:600; font-size:0.9rem; margin-top:1rem">
                → Click <strong>🟢 Patient Screening</strong> tab above
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🔵</div>
            <div class="mode-title">Doctor Dashboard</div>
            <div class="mode-desc">
                Upload a retinal fundus scan for clinical DR grading (0–4), 
                Grad-CAM explainability, confidence scores, 
                and clinical recommendations.
            </div>
            <br>
            <div style="color:#0099FF; font-weight:600; font-size:0.9rem; margin-top:1rem">
                → Click <strong>🔵 Doctor Dashboard</strong> tab above
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)