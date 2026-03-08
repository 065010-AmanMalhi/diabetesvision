import streamlit as st
import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import tempfile
import os
import gdown

# ── LOAD SKIN MODEL ───────────────────────────────────────
@st.cache_resource
def load_skin_model():
    model_path = 'models/skin_model_best.h5'
    if not os.path.exists(model_path):
        os.makedirs('models', exist_ok=True)
        gdown.download(
            'https://drive.google.com/uc?id=1MpF6JHfGsx03p9lubLvbE_Db730Y0fqP',
            model_path, quiet=False
        )
    model = tf.keras.models.load_model(model_path)
    return model

def preprocess_skin_image(img_array, target_size=(128, 128)):
    """Resize and normalize uploaded skin image"""
    img = cv2.resize(img_array, target_size)
    img = img.astype(np.float32) / 255.0
    return img

def calculate_risk_score(pred_confidence, age, family_history, bmi_category):
    """
    Combine CNN confidence with patient metadata
    to produce a composite 0-100 risk score
    """
    # Base score from model confidence on 'Concerning' class
    base = pred_confidence * 70

    # Add metadata modifiers
    if age > 45: base += 8
    if age > 60: base += 5
    if family_history: base += 10
    if bmi_category == "Overweight": base += 4
    if bmi_category == "Obese": base += 8

    return min(int(base), 100)

def run():
    st.title("👁️ Your Personal Diabetes Risk Check")
    st.markdown("*Upload a photo of a skin lesion and answer a few questions. Our AI will assess your risk in seconds.*")
    st.markdown("---")

    # ── PATIENT METADATA FORM ─────────────────────────────
    st.subheader("Step 1 — Tell us about yourself")
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Your Age", 18, 90, 35)
        bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])

    with col2:
        family_history = st.checkbox("Family history of diabetes?")
        years_diabetic = st.number_input("Years since diabetes diagnosis (0 if none)", 0, 50, 0)

    # ── IMAGE UPLOAD ──────────────────────────────────────
    st.markdown("---")
    st.subheader("Step 2 — Upload a skin photo")
    st.markdown("*Take a clear, close-up photo of any skin lesion, dark patch, or area of concern.*")

    uploaded = st.file_uploader(
        "Upload skin image (JPG or PNG)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:
        # Convert uploaded file to numpy array
        pil_img = Image.open(uploaded).convert('RGB')
        img_array = np.array(pil_img)

        # Show uploaded image
        col1, col2 = st.columns(2)
        with col1:
            st.image(pil_img, caption="Your uploaded image", use_container_width=True)

        # ── PREDICT ───────────────────────────────────────
        with st.spinner("🔍 Analyzing your skin..."):
            model = load_skin_model()

            # Preprocess and predict
            processed = preprocess_skin_image(img_array)
            input_tensor = np.expand_dims(processed, 0)
            prediction = model.predict(input_tensor, verbose=0)

            not_concerning_conf = prediction[0][0]
            concerning_conf = prediction[0][1]
            pred_class = np.argmax(prediction[0])

            # Calculate composite risk score
            risk_score = calculate_risk_score(
                concerning_conf, age, family_history, bmi_category
            )

        # ── RESULTS ───────────────────────────────────────
        st.markdown("---")
        st.subheader("Step 3 — Your Results")

        # Risk meter
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Risk Score", f"{risk_score}/100")
        with col2:
            st.metric("AI Finding", "Concerning" if pred_class == 1 else "Not Concerning")
        with col3:
            st.metric("Confidence", f"{max(concerning_conf, not_concerning_conf)*100:.1f}%")

        # Risk level message
        if risk_score < 25:
            st.success("✅ Low Risk — No immediate concern detected. Maintain healthy habits.")
        elif risk_score < 50:
            st.warning("⚠️ Moderate Risk — Consider consulting a doctor for a routine check.")
        elif risk_score < 75:
            st.error("🔴 High Risk — We recommend scheduling a medical consultation soon.")
        else:
            st.error("🚨 Critical Risk — Please seek medical attention as soon as possible.")
            

        # Grad-CAM heatmap
        st.markdown("---")
        st.subheader("What the AI focused on")
        st.markdown("*The highlighted regions show which areas of your skin influenced the AI's decision.*")

        with col2:
            # Generate saliency map using input gradients
            # Simpler approach — no model rebuilding needed
            img_tensor = tf.cast(input_tensor, tf.float32)
        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            preds = model(img_tensor, training=False)
            class_score = preds[:, pred_class]

        grads = tape.gradient(class_score, img_tensor)
        heatmap = tf.reduce_mean(tf.abs(grads), axis=-1)[0].numpy()
        heatmap = heatmap / (heatmap.max() + 1e-8)

        # Overlay heatmap
        h, w = img_array.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))
        heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        blended = (img_array * 0.55 + heatmap_colored * 0.45).astype(np.uint8)

        st.image(blended, caption="Grad-CAM Heatmap", use_container_width=True)

        # Next steps
        st.markdown("---")
        st.subheader("📋 Recommended Next Steps")
        if pred_class == 1 or risk_score > 40:
            st.markdown("""
            1. **Book an appointment** with your general physician
            2. **Request a fasting blood glucose test**
            3. **Ask for a formal retinal screening** if diabetic
            4. **Monitor your skin** for any changes in size, color, or shape
            """)
        else:
            st.markdown("""
            1. **Maintain a healthy diet** — reduce sugar and processed foods
            2. **Exercise regularly** — 30 minutes daily
            3. **Annual health checkup** — include blood glucose screening
            4. **Monitor your BMI** and keep it in the healthy range
            """)