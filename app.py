import streamlit as st

st.set_page_config(
    page_title="DiabetesVision — AI Diabetes Screening",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #070D1A;
    color: #E8EDF5;
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }

/* Tab navigation styling */
.stTabs [data-baseweb="tab-list"] {
    background: #0D1526;
    border-bottom: 1px solid #1E2D45;
    padding: 0 2rem;
    gap: 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7A8FA6;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    padding: 1rem 1.5rem;
    border: none;
    border-bottom: 2px solid transparent;
}

.stTabs [aria-selected="true"] {
    color: #00D4AA !important;
    border-bottom: 2px solid #00D4AA !important;
    background: transparent !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #0D1526;
    border: 1px solid #1E2D45;
    border-radius: 12px;
    padding: 1.2rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00D4AA, #0099FF);
    color: #070D1A;
    border: none;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.7rem 2rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3);
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #1E2D45;
    border-radius: 12px;
    background: #0D1526;
    transition: border-color 0.2s;
}

[data-testid="stFileUploader"]:hover {
    border-color: #00D4AA;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #00D4AA, #0099FF);
    border-radius: 10px;
}

/* Stat cards */
.stat-card {
    background: linear-gradient(135deg, #0D1526, #0F1E35);
    border: 1px solid #1E2D45;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: #00D4AA;
}

.stat-number {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #00D4AA;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: #7A8FA6;
    font-size: 0.9rem;
    font-weight: 400;
}

/* Hero section */
.hero {
    padding: 5rem 2rem 3rem;
    text-align: center;
}

.hero-badge {
    display: inline-block;
    background: rgba(0, 212, 170, 0.1);
    border: 1px solid rgba(0, 212, 170, 0.3);
    color: #00D4AA;
    padding: 0.4rem 1.2rem;
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.1;
    color: #E8EDF5;
    margin-bottom: 1.5rem;
}

.hero-title span {
    color: #00D4AA;
    font-style: italic;
}

.hero-subtitle {
    color: #7A8FA6;
    font-size: 1.15rem;
    max-width: 600px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
}

/* Section headers */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #E8EDF5;
    margin-bottom: 0.5rem;
}

.section-sub {
    color: #7A8FA6;
    margin-bottom: 2rem;
}

/* Problem/solution cards */
.problem-card {
    background: rgba(255, 80, 80, 0.05);
    border: 1px solid rgba(255, 80, 80, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
}

.solution-card {
    background: rgba(0, 212, 170, 0.05);
    border: 1px solid rgba(0, 212, 170, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
}

.mode-card {
    background: #0D1526;
    border: 1px solid #1E2D45;
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    transition: all 0.3s;
    cursor: pointer;
}

.mode-card:hover {
    border-color: #00D4AA;
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.mode-icon { font-size: 3rem; margin-bottom: 1rem; }
.mode-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #E8EDF5;
    margin-bottom: 0.5rem;
}
.mode-desc { color: #7A8FA6; font-size: 0.9rem; line-height: 1.6; }

/* Use case cards */
.usecase-card {
    background: #0D1526;
    border: 1px solid #1E2D45;
    border-radius: 12px;
    padding: 1.5rem;
}

.usecase-icon { font-size: 2rem; margin-bottom: 0.8rem; }
.usecase-title { font-weight: 600; color: #E8EDF5; margin-bottom: 0.4rem; }
.usecase-desc { color: #7A8FA6; font-size: 0.875rem; line-height: 1.6; }

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E2D45, transparent);
    margin: 3rem 0;
}

/* Result cards */
.result-card {
    background: #0D1526;
    border: 1px solid #1E2D45;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

/* Fix subheading label colors */
label, .stTextInput label, .stNumberInput label, 
.stSelectbox label, .stTextArea label, .stSlider label,
.stFileUploader label {
    color: #A0B0C5 !important;
    font-size: 0.875rem !important;
}

</style>
""", unsafe_allow_html=True)

# ── TOP NAVBAR VIA TABS ───────────────────────────────────
# Check session state for auto-tab switching from home buttons

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠  Home",
    "🟢  Patient Screening",
    "🔵  Doctor Dashboard",
    "📊  About & Research"
])

with tab1:
    from pages.home import run
    run()

with tab2:
    from pages.patient_mode import run as patient_run
    patient_run()

with tab3:
    from pages.doctor_mode import run as doctor_run
    doctor_run()

with tab4:
    from pages.about import run as about_run
    about_run()