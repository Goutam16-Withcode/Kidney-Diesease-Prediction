import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os
import requests
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Page Configuration
st.set_page_config(
    page_title="Kidney Disease Risk Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN CLINICAL THEME (Forced Update) ---
st.markdown("""
    <style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* BASE SETTINGS */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc !important; /* Very Light Slate */
        color: #0f172a !important; /* Slate 900 */
    }

    /* HEADER BLOCK */
    h1 {
        background-color: #0c4a6e !important;
        color: #ffffff !important;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    h2, h3, h4 {
        color: #0284c7 !important;
        font-weight: 700;
    }
    
    /* SPECIFIC TEXT COLORING (Avoiding Global Overrides) */
    p, label, .stMarkdown p {
        color: #334155 !important; /* Slate 700 */
    }
    
    /* Allow Streamlit Alerts (Success/Error/Warning) to use their native text colors (usually white/dark mixed correctly) 
       or force them if needed, but removing global div override solves 90% of issues. */
    
    /* INPUT FIELDS - FORCE BLACK TEXT */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important; /* Pure Black for inputs */
        font-weight: 500;
        border: 2px solid #e2e8f0 !important;
        border-radius: 0.5rem;
        height: 45px;
    }
    
    /* Fix Selectbox Sidebar/Dropdown Options */
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    
    /* SIDEBAR - COLORED */
    [data-testid="stSidebar"] {
        background-color: #f0f9ff !important;
        border-right: 1px solid #bae6fd;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus {
        border-color: #0284c7 !important;
    }
    
    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(to right, #0284c7, #0ea5e9) !important;
        color: white !important;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ASSETS & HELPERS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

try:
    from streamlit_lottie import st_lottie
    lottie_header = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")
except ImportError:
    lottie_header = None

@st.cache_resource
def load_model():
    try:
        return pickle.load(open('kindey.pkl', 'rb'))
    except Exception:
        return None

model = load_model()

# --- PROFESSIONAL FEATURES ---
def create_gauge(value, title, min_val, max_val, thresholds):
    """Creates a professional gauge chart."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title, 'font': {'size': 20, 'color': "#0c4a6e"}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "#334155"},
            'bar': {'color': "#0c4a6e"}, 
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#cbd5e1",
            'steps': [
                {'range': [min_val, thresholds[0]], 'color': "#10b981"}, # Green
                {'range': [thresholds[0], thresholds[1]], 'color': "#f59e0b"}, # Yellow
                {'range': [thresholds[1], max_val], 'color': "#ef4444"}  # Red
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    # Increased height and margins to prevent cropping
    fig.update_layout(height=300, margin=dict(l=30, r=30, t=50, b=30), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#334155"})
    return fig

def create_pdf(patient_data, prediction_text, confidence, alerts):
    """Generates PDF report."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.01, 0.29, 0.43) # Medical Navy
    c.drawString(50, height - 50, "Kidney Disease Risk Assessment")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.gray)
    c.drawString(50, height - 70, "Generated by KidneyGuard AI • Medical Screening Tool")
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.line(50, height - 80, width - 50, height - 80)

    # Result Section
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.05, 0.09, 0.16) # Dark Slate
    c.drawString(50, height - 120, "1. Assessment Result")
    
    c.setFont("Helvetica-Bold", 14)
    if "Positive" in prediction_text:
        c.setFillColor(colors.red)
    else:
        c.setFillColor(colors.green)
    c.drawString(70, height - 145, f"Diagnosis: {prediction_text}")
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(70, height - 165, f"Confidence Level: {confidence:.2f}%")

    # Patient Data
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.05, 0.09, 0.16)
    c.drawString(50, height - 210, "2. Key Vitals & Chemistry")
    
    y = height - 240
    c.setFont("Helvetica", 11)
    
    metrics = [
        f"Age: {patient_data['age']} years",
        f"Blood Pressure: {patient_data['blood_pressure']} mm/Hg",
        f"Serum Creatinine: {patient_data['serum_creatinine']} mgs/dl",
        f"Blood Urea: {patient_data['blood_urea']} mgs/dl",
        f"Hemoglobin: {patient_data['haemoglobin']} gms",
        f"Specific Gravity: {patient_data['specific_gravity']}"
    ]
    
    for metric in metrics:
        c.drawString(70, y, metric)
        y -= 20

    # Risk Factors
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.05, 0.09, 0.16)
    c.drawString(50, y - 30, "3. Clinical Flags")
    y -= 60
    
    c.setFont("Helvetica", 11)
    if alerts:
        c.setFillColor(colors.firebrick)
        for alert in alerts:
            c.drawString(70, y, f"• {alert}")
            y -= 20
    else:
        c.setFillColor(colors.darkgreen)
        c.drawString(70, y, "• No immediate critical flags.")

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(50, 40, "Disclaimer: AI screening tool. Not a substitute for professional medical advice.")
    
    c.save()
    buffer.seek(0)
    return buffer

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/medical-doctor.png", width=64)
    st.markdown("### Clinical Assessment Tool")
    st.markdown("---")
    st.markdown("""
    **Instructions:**
    1. Enter standard unit values.
    2. Review real-time gauge indicators.
    3. Generate PDF for patient files.
    """)
    st.info("Medical Grade: v3.1")

# --- MAIN CONTENT ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("Kidney Disease Risk Assessment")
    st.markdown("**Patient Screening Form** | Enter Clinical Parameters")
with c2:
    if lottie_header:
        st_lottie(lottie_header, height=100, key="header")
    else:
        st.write("")

# --- FORM ---
def section_header(title):
    st.markdown(f"## {title}")

with st.form("assessment_form"):
    
    section_header("1. Patient Demographics & Vitals")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age (Years)", 1, 120, 50)
        bp = st.number_input("Blood Pressure (mm/Hg)", 40, 250, 80)
    with col2:
        sg = st.selectbox("Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025], index=3)
        al = st.selectbox("Albumin", [0, 1, 2, 3, 4, 5], index=0)
    with col3:
        su = st.selectbox("Sugar", [0, 1, 2, 3, 4, 5], index=0)
        
    section_header("2. Blood Chemistry")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bgr = st.number_input("Blood Glucose (Rand)", 0.0, 500.0, 120.0, help="mgs/dl")
        bu = st.number_input("Blood Urea", 0.0, 300.0, 36.0, help="mgs/dl")
    with col2:
        sc = st.number_input("Serum Creatinine", 0.0, 50.0, 1.2, help="mgs/dl")
        sod = st.number_input("Sodium", 100.0, 200.0, 137.0, help="mEq/L")
    with col3:
        pot = st.number_input("Potassium", 1.0, 10.0, 4.0, help="mEq/L")
        hemo = st.number_input("Hemoglobin", 1.0, 25.0, 15.0, help="gms")
    with col4:
        ba = st.selectbox("Bacteria", ["notpresent", "present"])
        
    section_header("3. Hematology & Medical History")
    col1, col2, col3 = st.columns(3)
    with col1:
        pcv = st.number_input("Packed Cell Vol.", 10.0, 60.0, 44.0)
        wc = st.number_input("WBC Count", 0.0, 30000.0, 7800.0)
        rc = st.number_input("RBC Count", 0.0, 10.0, 5.2, help="millions/cmm")
    with col2:
        htn = st.selectbox("Hypertension", ["no", "yes"])
        dm = st.selectbox("Diabetes Mellitus", ["no", "yes"])
        cad = st.selectbox("Coronary Artery Dis.", ["no", "yes"])
    with col3:
        pe = st.selectbox("Pedal Edema", ["no", "yes"])
        ane = st.selectbox("Anemia", ["no", "yes"])
        appet = st.selectbox("Appetite", ["good", "poor"])
        
    st.write("---")
    st.markdown("**Microscopic Examination**")
    m1, m2, m3 = st.columns(3)
    with m1: rbc = st.selectbox("RBC", ["normal", "abnormal"])
    with m2: pc = st.selectbox("Pus Cell", ["normal", "abnormal"])
    with m3: pcc = st.selectbox("Pus Cell Clumps", ["notpresent", "present"])

    submit_btn = st.form_submit_button("Generate Clinical Assessment")

# --- EXECUTION ---
if submit_btn:
    if not model:
        st.error("Error: Model file 'kindey.pkl' unavailable.")
    else:
        mapping = {
            'normal': 1, 'abnormal': 0, 'present': 1, 'notpresent': 0,
            'yes': 1, 'no': 0, 'poor': 1, 'good': 0
        }
        
        try:
            data = {
                'age': age, 'blood_pressure': bp, 'specific_gravity': sg, 'albumin': al, 'sugar': su,
                'red_blood_cells': mapping.get(rbc, 0), 'pus_cell': mapping.get(pc, 0),
                'pus_cell_clumps': mapping.get(pcc, 0), 'bacteria': mapping.get(ba, 0),
                'blood_glucose_random': bgr, 'blood_urea': bu, 'serum_creatinine': sc,
                'sodium': sod, 'potassium': pot, 'haemoglobin': hemo,
                'packed_cell_volume': pcv, 'white_blood_cell_count': wc,
                'red_blood_cell_count': rc, 'hypertension': mapping.get(htn, 0),
                'diabetes_mellitus': mapping.get(dm, 0), 'coronary_artery_disease': mapping.get(cad, 0),
                'appetite': mapping.get(appet, 0), 'peda_edema': mapping.get(pe, 0),
                'aanemia': mapping.get(ane, 0)
            }
            
            df = pd.DataFrame([data])
            df = df.apply(pd.to_numeric, errors='coerce')
            
            prediction = model.predict(df)[0]
            try:
                probs = model.predict_proba(df)[0]
                confidence = probs[prediction] * 100
            except:
                confidence = 0.0

            st.divider()
            is_ckd = (prediction == 0)
            
            res_c1, res_c2 = st.columns([1, 4])
            with res_c1:
                if is_ckd:
                    st.error("⚠️ HIGH RISK")
                    result_string = "Positive for Chronic Kidney Disease"
                else:
                    st.success("✅ LOW RISK")
                    result_string = "Negative for Chronic Kidney Disease"
            
            with res_c2:
                st.markdown(f"### Diagnosis: {result_string}")
                st.markdown(f"**Confidence:** {confidence:.1f}%")

            st.markdown("### 📊 Key Markers")
            g1, g2, g3 = st.columns(3)
            with g1: st.plotly_chart(create_gauge(bp, "Blood Pressure", 0, 200, [120, 140]), use_container_width=True)
            with g2: st.plotly_chart(create_gauge(sc, "Creatinine", 0, 10, [1.2, 1.5]), use_container_width=True)
            with g3: st.plotly_chart(create_gauge(hemo, "Hemoglobin", 0, 18, [12, 13.5]), use_container_width=True)

            alerts = []
            if bp >= 140: alerts.append("Hypertension")
            if bgr >= 200: alerts.append("Hyperglycemia")
            if sc > 1.2: alerts.append("High Creatinine")
            if hemo < 12: alerts.append("Anemia (Low Hemoglobin)")
            
            if alerts:
                st.warning(f"**Clinical Flags:** {', '.join(alerts)}")

            col_pdf, _ = st.columns([1, 4])
            with col_pdf:
                pdf_data = {
                    'age': int(age), 'blood_pressure': int(bp),
                    'serum_creatinine': sc, 'blood_urea': bu, 'haemoglobin': hemo,
                    'specific_gravity': sg
                }
                pdf_file = create_pdf(pdf_data, result_string, confidence, alerts)
                st.download_button("📄 Download Report", pdf_file, "report.pdf", "application/pdf")

        except Exception as e:
            st.error(f"Error: {str(e)}")
