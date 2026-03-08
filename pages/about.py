import streamlit as st

def run():
    st.markdown("""
    <div style="padding: 3rem 0 1rem">
        <div class="hero-badge">Research & Methodology</div>
        <div class="section-header" style="margin-top:1rem">About DiabetesVision</div>
    </div>
    """, unsafe_allow_html=True)

    # ── MODELS ────────────────────────────────────────────
    st.markdown("### 🧠 Model Architecture")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="usecase-card">
            <div class="usecase-title">Model 1 — Skin Lesion Classifier</div>
            <br>
            <table style="width:100%; color:#B0BEC5; font-size:0.875rem">
                <tr><td>Architecture</td><td style="color:#E8EDF5">MobileNetV2</td></tr>
                <tr><td>Dataset</td><td style="color:#E8EDF5">HAM10000 (10,015 images)</td></tr>
                <tr><td>Classes</td><td style="color:#E8EDF5">Concerning / Not Concerning</td></tr>
                <tr><td>Accuracy</td><td style="color:#00D4AA">85.07%</td></tr>
                <tr><td>Training</td><td style="color:#E8EDF5">Transfer learning + Fine-tuning</td></tr>
                <tr><td>Input Size</td><td style="color:#E8EDF5">128 × 128 × 3</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="usecase-card">
            <div class="usecase-title">Model 2 — Retinal DR Grader</div>
            <br>
            <table style="width:100%; color:#B0BEC5; font-size:0.875rem">
                <tr><td>Architecture</td><td style="color:#E8EDF5">MobileNetV2</td></tr>
                <tr><td>Dataset</td><td style="color:#E8EDF5">APTOS 2019 (2,930 images)</td></tr>
                <tr><td>Classes</td><td style="color:#E8EDF5">DR Grade 0–4</td></tr>
                <tr><td>Accuracy</td><td style="color:#00D4AA">70.6%</td></tr>
                <tr><td>Training</td><td style="color:#E8EDF5">Transfer learning + Fine-tuning</td></tr>
                <tr><td>Input Size</td><td style="color:#E8EDF5">128 × 128 × 3</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── GRAD-CAM ──────────────────────────────────────────
    st.markdown("### 🔥 Explainability — Grad-CAM")
    st.markdown("""
    <div class="solution-card">
        <p style="color:#B0BEC5; line-height:1.8; margin:0">
        DiabetesVision uses <strong style="color:#E8EDF5">Gradient-weighted Class Activation Mapping (Grad-CAM)</strong> 
        to generate visual explanations for every prediction. Instead of a black-box result, 
        clinicians see exactly which region of the retina or skin lesion drove the AI's decision 
        — building trust and enabling verification.
        <br><br>
        Grad-CAM computes the gradient of the predicted class score with respect to the final 
        convolutional layer, producing a heatmap that highlights the most influential pixels. 
        Red/yellow regions = high influence. Blue = low influence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── BUSINESS CASE ─────────────────────────────────────
    st.markdown("### 💼 Business Case")

    col1, col2, col3 = st.columns(3)
    metrics = [
        ("₹200–500", "Cost per AI screening vs ₹3,000–8,000 specialist visit"),
        ("10x", "Faster screening — seconds vs 30+ min specialist consultation"),
        ("18M+", "Underserved diabetic patients in rural India alone"),
    ]
    for col, (num, label) in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="font-size:2rem">{num}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── DATASET SOURCES ───────────────────────────────────
    st.markdown("### 📂 Datasets & References")
    st.markdown("""
    <div class="usecase-card">
        <ul style="color:#B0BEC5; line-height:2; margin:0">
            <li><strong style="color:#E8EDF5">APTOS 2019 Blindness Detection</strong> — 
            Kaggle competition dataset, retinal fundus images graded 0–4 for DR severity</li>
            <li><strong style="color:#E8EDF5">HAM10000</strong> — 
            Human Against Machine with 10,000 training images, dermatoscopic skin lesion dataset</li>
            <li><strong style="color:#E8EDF5">Transfer Learning</strong> — 
            MobileNetV2 pretrained on ImageNet (14M images, 1,000 classes)</li>
            <li><strong style="color:#E8EDF5">Grad-CAM</strong> — 
            Selvaraju et al., 2017 — "Grad-CAM: Visual Explanations from Deep Networks"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)