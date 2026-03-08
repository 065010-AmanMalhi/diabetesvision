import streamlit as st
import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import plotly.express as px
import pandas as pd

# ── LOAD RETINAL MODEL ────────────────────────────────────
@st.cache_resource
def load_retinal_model():
    model = tf.keras.models.load_model('models/retinal_model_full.h5')
    return model

def preprocess_retinal_image(img_array, target_size=(128, 128)):
    """CLAHE enhancement + resize + normalize"""
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    img_bgr = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype(np.float32) / 255.0
    return img

# DR grade information for clinical display
DR_INFO = {
    0: {
        "label": "No DR",
        "color": "success",
        "description": "No signs of diabetic retinopathy detected.",
        "recommendation": "Continue annual screening. Maintain good glycemic control."
    },
    1: {
        "label": "Mild DR",
        "color": "info",
        "description": "Microaneurysms present. Early stage retinopathy.",
        "recommendation": "Follow-up in 12 months. Optimize blood sugar and blood pressure."
    },
    2: {
        "label": "Moderate DR",
        "color": "warning",
        "description": "More than microaneurysms. Risk of progression to PDR.",
        "recommendation": "Follow-up in 6 months. Consider referral to ophthalmologist."
    },
    3: {
        "label": "Severe DR",
        "color": "error",
        "description": "Extensive retinal hemorrhages. High risk of vision loss.",
        "recommendation": "Urgent referral to ophthalmologist. Follow-up in 3 months."
    },
    4: {
        "label": "Proliferative DR",
        "color": "error",
        "description": "New blood vessel growth. Highest risk of blindness.",
        "recommendation": "Immediate ophthalmologist referral. Consider laser therapy."
    }
}

def run():
    st.title("🔬 Clinical Retinal Analysis Dashboard")
    st.markdown("*Upload a fundus scan for AI-powered diabetic retinopathy grading with Grad-CAM explainability.*")
    st.markdown("---")

    # ── PATIENT INFO ──────────────────────────────────────
    st.subheader("Patient Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        patient_id = st.text_input("Patient ID", placeholder="e.g. PT-2024-001")
    with col2:
        patient_age = st.number_input("Age", 18, 100, 45)
    with col3:
        patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    clinical_notes = st.text_area("Clinical Notes", placeholder="Add any relevant patient history...")

    # ── IMAGE UPLOAD ──────────────────────────────────────
    st.markdown("---")
    st.subheader("Upload Retinal Fundus Scan")
    uploaded = st.file_uploader(
        "Upload retinal scan (JPG or PNG)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:
        pil_img = Image.open(uploaded).convert('RGB')
        img_array = np.array(pil_img)

        with st.spinner("🔍 Analyzing retinal scan..."):
            model = load_retinal_model()
            processed = preprocess_retinal_image(img_array)
            input_tensor = np.expand_dims(processed, 0)
            prediction = model.predict(input_tensor, verbose=0)
            pred_class = int(np.argmax(prediction[0]))
            confidence = float(prediction[0][pred_class]) * 100

        # ── RESULTS ───────────────────────────────────────
        st.markdown("---")
        st.subheader("Analysis Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("DR Grade", f"Grade {pred_class}")
        with col2:
            st.metric("Diagnosis", DR_INFO[pred_class]['label'])
        with col3:
            st.metric("Confidence", f"{confidence:.1f}%")

        # Clinical finding
        info = DR_INFO[pred_class]
        if info['color'] == 'success':
            st.success(f"✅ {info['description']}")
        elif info['color'] == 'info':
            st.info(f"ℹ️ {info['description']}")
        else:
            st.error(f"⚠️ {info['description']}")
        if info['color'] == 'success':
            st.success(f"✅ {info['description']}")
        elif info['color'] == 'info':
            st.info(f"ℹ️ {info['description']}")
        else:
            st.error(f"⚠️ {info['description']}")

        st.markdown(f"**Clinical Recommendation:** {info['recommendation']}")

        # ── CONFIDENCE CHART ──────────────────────────────
        st.markdown("---")
        st.subheader("Confidence Scores Across All Grades")

        import plotly.express as px
        import pandas as pd

        chart_data = pd.DataFrame({
            'Grade': [f"Grade {i} — {DR_INFO[i]['label']}" for i in range(5)],
            'Confidence (%)': [float(p) * 100 for p in prediction[0]],
            'Highlight': ['Predicted' if i == pred_class else 'Other' for i in range(5)]
        })

        fig = px.bar(
            chart_data,
            x='Grade',
            y='Confidence (%)',
            color='Highlight',
            color_discrete_map={'Predicted': '#00D4AA', 'Other': '#1E3A5F'},
            template='plotly_dark',
        )

        fig.update_layout(
            paper_bgcolor='#0D1526',
            plot_bgcolor='#0D1526',
            font=dict(family='DM Sans', color='#A0B0C5'),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(gridcolor='#1E2D45'),
            yaxis=dict(gridcolor='#1E2D45'),
        )

        st.plotly_chart(fig, use_container_width=True)

        # ── GRAD-CAM ──────────────────────────────────────
        st.markdown("---")
        st.subheader("Grad-CAM — Region of Interest")
        st.markdown("*Highlighted areas show which retinal regions influenced the AI diagnosis.*")

        col1, col2 = st.columns(2)

        # Generate Grad-CAM
        img_tensor = tf.cast(input_tensor, tf.float32)
        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            preds = model(img_tensor, training=False)
            class_score = preds[:, pred_class]

        grads = tape.gradient(class_score, img_tensor)
        heatmap = tf.reduce_mean(tf.abs(grads), axis=-1)[0].numpy()
        heatmap = heatmap / (heatmap.max() + 1e-8)

        h, w = img_array.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))
        heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        blended = (img_array * 0.55 + heatmap_colored * 0.45).astype(np.uint8)

        with col1:
            st.image(img_array, caption="Original Fundus Scan", use_container_width=True)
        with col2:
            st.image(blended, caption="Grad-CAM Overlay", use_container_width=True)

        # ── CLINICAL RECOMMENDATIONS ──────────────────────
        st.markdown("---")
        st.subheader("📋 Clinical Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Immediate Actions**")
            if pred_class == 0:
                st.markdown("""
                - Schedule next screening in 12 months
                - Maintain HbA1c below 7%
                - Monitor blood pressure regularly
                """)
            elif pred_class == 1:
                st.markdown("""
                - Schedule follow-up in 12 months
                - Optimize glycemic control
                - Check blood pressure and lipids
                """)
            elif pred_class == 2:
                st.markdown("""
                - Refer to ophthalmologist within 6 months
                - Intensify glycemic management
                - Consider ACE inhibitor therapy
                """)
            else:
                st.markdown("""
                - **Urgent ophthalmologist referral**
                - Immediate glycemic optimization
                - Discuss laser photocoagulation
                - Anti-VEGF therapy evaluation
                """)
        
        with col2:
            st.markdown("**Patient Counseling Points**")
            st.markdown("""
            - Explain findings in simple terms
            - Stress importance of medication adherence
            - Discuss lifestyle modifications
            - Provide emergency contact if vision changes
            """)
        
        # Clinical notes summary
        if clinical_notes:
            st.markdown("---")
            st.markdown("**Recorded Clinical Notes:**")
            st.info(clinical_notes)