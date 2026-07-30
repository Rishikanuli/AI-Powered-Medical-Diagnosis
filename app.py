import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time

# --- Page Config ---
st.set_page_config(
    page_title="Clinical Diagnostic Assistant",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Global App Styling */
        .stApp {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background-color: #f4f7f6;
            color: #111827 !important;
            font-size: 18px;
        }
        
        /* FULL WIDTH FIX */
        .main .block-container {
            max-width: 1300px;
            padding: 3rem;
        }

        /* Typography */
        h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
        h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
        h3 { font-size: 1.5rem !important; font-weight: 700 !important; }
        
        label, p {
            color: #111827 !important;
        }
        
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: #111827 !important;
        }
        div[data-baseweb="select"] input {
            color: #111827 !important;
        }
        div[data-baseweb="select"] ::placeholder {
            color: #6b7280 !important;
            opacity: 1;
        }



        /* Cards */
        .dashboard-card {
            background-color: white;
            padding: 28px;
            border-radius: 16px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: 0.2s ease;
            box-sizing: border-box;
        }

        /* Force Streamlit Columns & Card Wrappers to Stretch Equal Height */
        div[data-testid="stColumn"], div[data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
        }
        div[data-testid="stColumn"] > div, div[data-testid="column"] > div {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
            height: 100% !important;
        }
        div[data-testid="stColumn"] [data-testid="stElementContainer"], 
        div[data-testid="column"] [data-testid="stElementContainer"],
        div[data-testid="stColumn"] [data-testid="stVerticalBlockContainer"], 
        div[data-testid="column"] [data-testid="stVerticalBlockContainer"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
            height: 100% !important;
        }
        div[data-testid="stColumn"] [data-testid="stMarkdownContainer"], 
        div[data-testid="column"] [data-testid="stMarkdownContainer"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
            height: 100% !important;
        }
        div[data-testid="stColumn"] [data-testid="stMarkdownContainer"] > div, 
        div[data-testid="column"] [data-testid="stMarkdownContainer"] > div {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
            height: 100% !important;
        }

        .match-card {
            background-color: white;
            padding: 24px 20px;
            border-radius: 16px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: 0.2s ease;
            min-height: 185px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            box-sizing: border-box;
        }
        .match-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 8px 18px rgba(0,0,0,0.08);
        }
        .match-card-badge {
            font-size: 13px;
            color: #6b7280;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .match-card-title {
            font-size: 20px;
            font-weight: 700;
            color: #111827;
            line-height: 1.3;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-grow: 1;
            margin: 8px 0;
            word-break: break-word;
        }
        .match-card-conf {
            font-size: 18px;
            font-weight: 800;
        }
        
        /* Custom Button Styling */
        div[data-testid="stButton"] button[kind="primary"] {
            background: #2563eb !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stButton"] button[kind="primary"] * {
            color: white !important;
            font-weight: 600 !important;
            font-size: 18px !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background: #1d4ed8 !important;
            box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4) !important;
        }

        div[data-testid="stButton"] button[kind="secondary"] {
            background: white !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stButton"] button[kind="secondary"] * {
            color: #111827 !important;
            font-weight: 600 !important;
            font-size: 18px !important;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: #f8fafc !important;
            border-color: #94a3b8 !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.05) !important;
        }
        
        /* Input Cards for Vitals */
        div[data-testid="stTextInput"], div[data-testid="stNumberInput"] {
            background-color: white;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
            border: 1px solid #e5e7eb;
            margin-bottom: 10px;
        }
        div[data-testid="stTextInput"] label, div[data-testid="stNumberInput"] label {
            font-weight: 600 !important;
            color: #1e3a8a !important;
            font-size: 15px !important;
            margin-bottom: 8px !important;
        }
        div[data-testid="stTextInput"] > div[data-baseweb="input"], 
        div[data-testid="stNumberInput"] > div[data-baseweb="input"] {
            background-color: #f8fafc !important;
            border-radius: 8px !important;
            border: 1px solid #cbd5e1 !important;
        }

        .dashboard-card:hover {
            transform: translateY(-4px) scale(1.01);
        }

        /* Primary Diagnosis */
        .primary-diagnosis-card {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 28px;
            border-radius: 16px;
            margin-bottom: 24px;
        }

        .primary-diagnosis-title {
            font-size: 20px;
            font-weight: 600;
            opacity: 0.9;
            margin-bottom: 8px;
        }

        .primary-diagnosis-value {
            font-size: 48px;
            font-weight: 800;
        }

        /* Metrics */
        .metric-label {
            font-size: 18px;
            color: #6b7280;
        }
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            margin: 8px 0;
        }
        .metric-sub {
            font-size: 14px;
            font-weight: 500;
            color: #6b7280;
        }
        
        /* Severity Colors */
        .warning { color: #d97706 !important; font-weight: 700; }
        .danger { color: #dc2626 !important; font-weight: 700; }
        .success { color: #16a34a !important; font-weight: 700; }

        /* Multiselect Bigger */
        div[data-baseweb="select"] {
            min-height: 55px;
            font-size: 16px;
        }

        /* Section Title */
        .dashboard-section-title {
            font-size: 26px;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 20px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 10px;
        }
        /* Image Constraints */
        div[data-testid="stImage"] {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 5px;
        }
        div[data-testid="stImage"] img {
            max-width: 100% !important;
            height: auto !important;
            object-fit: contain;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

# --- Advanced Medical Dictionary (100 Symptoms) ---
SYMPTOM_CATEGORIES = {
    "General": ["Fever", "Fatigue", "Chills", "Night Sweats", "Weight Loss", "Weight Gain", "Lethargy", "Malaise", "Weakness", "Loss of Appetite", "Excessive Thirst", "Excessive Sweating", "Swollen Lymph Nodes", "Unexplained Bruising", "Hot Flashes", "Cold Intolerance", "Heat Intolerance", "Generalized Pain", "Mild Fever", "Body Aches", "Sweating", "Dehydration", "Muscle Aches", "Itchy Eyes"],
    "Respiratory": ["Cough", "Dry Cough", "Productive Cough", "Shortness of Breath", "Wheezing", "Chest Tightness", "Rapid Breathing", "Painful Breathing", "Blood in Sputum", "Hoarseness", "Nasal Congestion", "Runny Nose", "Sneezing", "Sore Throat", "Loss of Smell", "Postnasal Drip"],
    "Gastrointestinal": ["Nausea", "Vomiting", "Diarrhea", "Constipation", "Abdominal Cramps", "Bloating", "Heartburn", "Indigestion", "Loss of Taste", "Difficulty Swallowing", "Blood in Stool", "Dark Urine", "Jaundice", "Belching", "Flatulence", "Hiccups", "Rectal Pain"],
    "Neurological": ["Headache", "Severe Headache", "Dizziness", "Vertigo", "Confusion", "Memory Loss", "Seizures", "Tremors", "Numbness", "Tingling", "Muscle Weakness", "Difficulty Speaking", "Difficulty Walking", "Fainting", "Blurred Vision", "Double Vision", "Sensitivity to Light", "Sensitivity to Sound", "Neck Stiffness", "Loss of Balance", "Visual Disturbances", "Anxiety"],
    "Cardiovascular": ["Chest Pain", "Palpitations", "Irregular Heartbeat", "Swelling in Legs", "Swelling in Ankles", "Cold Sweats", "Cyanosis (Blue Lips/Fingers)", "Pain in Arm", "Pain in Jaw", "Lightheadedness", "High Blood Pressure", "Low Blood Pressure"],
    "Dermatological": ["Rash", "Itching", "Hives", "Dry Skin", "Oily Skin", "Acne", "Skin Peeling", "Ulcers", "Changes in Moles", "Skin Redness", "Flushing", "Petechiae", "Hair Loss", "Nail Changes", "Psoriasis plaques", "Eczema patches", "Blisters"]
}

# Flatten list of all 100+ symptoms
ALL_SYMPTOMS = sorted([sym for cat in SYMPTOM_CATEGORIES.values() for sym in cat])

# Enhanced Disease Mapping
DISEASE_PROFILES = {
    "Common Cold": {
        "core": ["Runny Nose", "Sneezing", "Sore Throat", "Nasal Congestion"],
        "secondary": ["Mild Fever", "Cough", "Fatigue", "Headache", "Malaise", "Loss of Smell"]
    },
    "Flu (Influenza)": {
        "core": ["Fever", "Chills", "Body Aches", "Fatigue", "Dry Cough"],
        "secondary": ["Headache", "Sore Throat", "Runny Nose", "Nausea", "Weakness", "Sweating"]
    },
    "COVID-19": {
        "core": ["Loss of Taste", "Loss of Smell", "Fever", "Dry Cough", "Shortness of Breath"],
        "secondary": ["Fatigue", "Body Aches", "Sore Throat", "Diarrhea", "Headache", "Chest Tightness"]
    },
    "Allergies": {
        "core": ["Sneezing", "Runny Nose", "Itchy Eyes", "Nasal Congestion"],
        "secondary": ["Dry Cough", "Postnasal Drip", "Fatigue", "Rash", "Itching", "Hives"]
    },
    "Food Poisoning": {
        "core": ["Nausea", "Vomiting", "Diarrhea", "Abdominal Cramps"],
        "secondary": ["Mild Fever", "Fatigue", "Weakness", "Chills", "Loss of Appetite", "Dehydration"]
    },
    "Migraine": {
        "core": ["Severe Headache", "Sensitivity to Light", "Sensitivity to Sound", "Nausea"],
        "secondary": ["Vomiting", "Dizziness", "Blurred Vision", "Visual Disturbances", "Neck Stiffness"]
    },
    "Gastroenteritis": {
        "core": ["Diarrhea", "Vomiting", "Abdominal Cramps", "Nausea"],
        "secondary": ["Fever", "Chills", "Fatigue", "Muscle Aches", "Loss of Appetite", "Weight Loss"]
    },
    "Pneumonia": {
        "core": ["Productive Cough", "Fever", "Chills", "Shortness of Breath"],
        "secondary": ["Chest Pain", "Fatigue", "Confusion", "Sweating", "Rapid Breathing", "Painful Breathing"]
    },
    "Asthma": {
        "core": ["Wheezing", "Shortness of Breath", "Chest Tightness", "Dry Cough"],
        "secondary": ["Rapid Breathing", "Fatigue", "Difficulty Speaking", "Anxiety"]
    },
    "Hypertension Crisis": {
        "core": ["Severe Headache", "Shortness of Breath", "Chest Pain"],
        "secondary": ["Dizziness", "Blurred Vision", "Nausea", "Confusion", "Palpitations"]
    }
}

# --- Dos and Don'ts Dictionary ---
DOS_AND_DONTS = {
    "Influenza": {"severity": "Moderate Viral Infection", "severity_color": "warning", "action": "Rest & Antivirals", "dos": ["Rest at home and isolate to prevent spreading the virus", "Stay well-hydrated with water, warm broths, or herbal teas", "Take fever-reducing medication (acetaminophen/ibuprofen) as needed"], "donts": ["Do not return to work or school until fever-free for at least 24 hours", "Do not ask for antibiotics (they are ineffective against viral influenza)", "Do not engage in strenuous physical activity or exercise"]},
    "COVID-19": {"severity": "Highly Contagious", "severity_color": "warning", "action": "Isolate & Monitor", "dos": ["Isolate immediately in a dedicated, well-ventilated room", "Monitor oxygen levels regularly with a pulse oximeter", "Stay hydrated, rest, and use acetaminophen for fever control"], "donts": ["Do not delay seeking emergency care if oxygen falls below 92%", "Do not self-medicate with unverified clinical therapeutics", "Do not leave isolation or gather in unmasked spaces"]},
    "Pneumonia": {"severity": "Severe Respiratory", "severity_color": "danger", "action": "Antibiotics & Care", "dos": ["Take all prescribed antibiotics or medications exactly as directed", "Get plenty of rest and drink lots of fluids to loosen chest congestion", "Use a cool-mist humidifier or take a warm bath to help clear lungs"], "donts": ["Do not stop taking prescribed antibiotics early, even if you feel better", "Do not take cough suppressants without consulting a doctor (coughing clears mucus)", "Do not expose yourself to smoke or cold air"]},
    "Tuberculosis": {"severity": "Chronic Infectious", "severity_color": "", "action": "Prolonged Antibiotics", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Dengue": {"severity": "Acute Viral/Mosquito", "severity_color": "warning", "action": "Vector Control & Fluids", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Malaria": {"severity": "Severe Parasitic", "severity_color": "danger", "action": "Urgent Antimalarials", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Typhoid": {"severity": "Bacterial Enteric", "severity_color": "", "action": "Antibiotics & Hydration", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Sepsis": {"severity": "Life-Threatening Emergency", "severity_color": "danger", "action": "Immediate Resuscitation", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Gastroenteritis": {"severity": "Acute/Mild-Moderate", "severity_color": "warning", "action": "Fluid Replacement", "dos": ["Drink plenty of fluids in small, frequent sips to prevent dehydration", "Eat bland, easy-to-digest foods when ready", "Wash your hands frequently to prevent spreading the infection"], "donts": ["Do not take anti-diarrheal drugs without consulting a doctor", "Do not eat highly seasoned, fatty, sweet, or dairy foods", "Do not prepare food for others while you are symptomatic"]},
    "Food Poisoning": {"severity": "Acute/Moderate Risk", "severity_color": "warning", "action": "Hydration Focus", "dos": ["Let your stomach settle by avoiding solid foods for a few hours", "Stay hydrated by sipping water, diluted sports drinks, or ORS", "Gradually introduce bland foods like bananas, rice, applesauce, and toast"], "donts": ["Do not take anti-diarrheal medications without checking with a doctor (they delay clearing toxins)", "Do not consume dairy, caffeine, alcohol, nicotine, or fatty foods", "Do not try to force eating when nauseous"]},
    "GERD": {"severity": "Chronic/Manageable", "severity_color": "", "action": "Dietary Modification", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Peptic Ulcer": {"severity": "Acute/GI Risk", "severity_color": "warning", "action": "GI Rest & Meds", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Gastritis": {"severity": "Acute/Gastrointestinal", "severity_color": "warning", "action": "Bland Diet & Antacids", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "IBS": {"severity": "Chronic/Discomfort", "severity_color": "", "action": "Symptomatic Relief", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Crohn’s Disease": {"severity": "Chronic Inflammatory", "severity_color": "", "action": "Immunosuppressive Care", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Ulcerative Colitis": {"severity": "Severe Inflammatory", "severity_color": "danger", "action": "Specialist GI Consult", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Hepatitis": {"severity": "Acute/Hepatic Risk", "severity_color": "warning", "action": "Liver Function Monitor", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Cirrhosis": {"severity": "End-Stage/Severe", "severity_color": "danger", "action": "Urgent Hepatology Consult", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Pancreatitis": {"severity": "Severe Abdominal", "severity_color": "danger", "action": "ER/Possible Surgery", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Gallstones": {"severity": "Acute Biliary", "severity_color": "warning", "action": "Surgical Evaluation", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Diabetes": {"severity": "Chronic/High Monitoring", "severity_color": "", "action": "Strict Glycemic Control", "dos": ["Check blood glucose levels immediately", "Maintain a balanced, low-glycemic eating schedule", "Take prescribed insulin or oral glucose-lowering medication as scheduled"], "donts": ["Do not skip scheduled meals or medication doses", "Do not consume high-sugar carbonated beverages or sweets", "Do not ignore slow-healing minor cuts or foot lesions"]},
    "Hypoglycemia": {"severity": "Metabolic Emergency", "severity_color": "danger", "action": "Consume Fast Sugar", "dos": ["Consume 15 grams of fast-acting sugar (fruit juice, regular soda, glucose tabs)", "Recheck blood glucose in 15 minutes (Rule of 15)", "Eat a complex carbohydrate and protein snack (crackers, bread) after recovery"], "donts": ["Do not inject insulin when blood sugar is already low", "Do not eat high-fat foods like chocolate (fat delays sugar absorption)", "Do not drive or operate heavy machinery during an episode"]},
    "Hyperthyroidism": {"severity": "Endocrine Imbalance", "severity_color": "", "action": "Endocrinologist Consult", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Hypothyroidism": {"severity": "Chronic/Manageable", "severity_color": "", "action": "Daily Hormone Therapy", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Addison’s Disease": {"severity": "Severe Endocrine", "severity_color": "danger", "action": "Steroid Replacement", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Cushing’s Syndrome": {"severity": "Metabolic Excess", "severity_color": "", "action": "Specialist Evaluation", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Electrolyte Imbalance": {"severity": "Acute Metabolic", "severity_color": "warning", "action": "IV Fluid Correction", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Dehydration": {"severity": "Acute/Fluid Loss", "severity_color": "warning", "action": "Aggressive Hydration", "dos": ["Sip Oral Rehydration Salts (ORS) or water slowly", "Rest in a cool, well-ventilated, or shaded space", "Monitor urine color (aim for a pale straw yellow or clear color)"], "donts": ["Do not gulp large quantities of plain water too rapidly", "Do not consume alcohol, strong coffee, or sugary energy drinks", "Do not ignore symptoms like dizziness, dry mouth, or rapid heart rate"]},
    "Vitamin B12 Deficiency": {"severity": "Nutritional Deficiency", "severity_color": "", "action": "Dietary/Vitamin Supps", "dos": ["Include Vitamin B12 rich foods (fish, meat, poultry, eggs, milk) in your diet", "Take prescribed B12 oral supplements or schedule B12 injections", "Keep track of neurological symptoms (tingling, memory issues)"], "donts": ["Do not ignore persistent tingling in hands or feet", "Do not stop taking supplements without consulting your doctor", "Do not assume symptoms are just due to fatigue or aging"]},
    "Iron Deficiency Anemia": {"severity": "Chronic/Nutritional", "severity_color": "", "action": "Iron Supplementation", "dos": ["Consume iron-rich foods (lean meats, leafy greens, legumes)", "Take iron supplements with Vitamin C (enhances absorption)", "Schedule a follow-up blood test to track hemoglobin levels"], "donts": ["Do not take iron supplements with calcium, tea, or coffee", "Do not ignore persistent severe fatigue or pale skin", "Do not exceed the recommended iron dosage without supervision"]},
    "Stroke": {"severity": "Critical Neurological", "severity_color": "danger", "action": "Urgent Stroke Protocol", "dos": ["Call emergency services (911/112) immediately", "Note the exact time symptoms first started", "Keep patient calm, warm, and lying down with head slightly elevated"], "donts": ["Do not give the patient food, drink, or medications", "Do not give aspirin (unless explicitly directed by a doctor)", "Do not allow the patient to sleep or drive themselves"]},
    "TIA": {"severity": "Acute Neurological", "severity_color": "warning", "action": "Immediate Neuro Eval", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Brain Tumor": {"severity": "Severe Neurological", "severity_color": "danger", "action": "Oncology/Neuro Consult", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Parkinson’s": {"severity": "Chronic/Progressive", "severity_color": "", "action": "Long-term Neuro Care", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Alzheimer’s": {"severity": "Progressive Cognitive", "severity_color": "", "action": "Supportive Care Plan", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Multiple Sclerosis": {"severity": "Chronic Autoimmune", "severity_color": "", "action": "Disease Modifying Rx", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Migraine": {"severity": "Disabling/Moderate", "severity_color": "warning", "action": "Dark Room & Meds", "dos": ["Rest in a dark, quiet, well-ventilated room", "Apply a cold or warm compress to your forehead or neck", "Take prescribed abortive medications at the first sign of aura or onset"], "donts": ["Do not look at bright phone, TV, or laptop screens", "Do not skip meals or disrupt your normal sleep schedule", "Do not consume strong caffeine or alcoholic triggers"]},
    "Epilepsy": {"severity": "Chronic Seizure Risk", "severity_color": "", "action": "Neurology Management", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Vertigo Disorder": {"severity": "Acute Vestibular", "severity_color": "warning", "action": "Balance Therapy", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Concussion": {"severity": "Acute/Trauma Risk", "severity_color": "warning", "action": "Cognitive Rest", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Asthma": {"severity": "Chronic/Acute Flare", "severity_color": "warning", "action": "Use Rescue Inhaler", "dos": ["Use your rescue inhaler (albuterol) immediately", "Sit upright and try to remain calm to ease breathing", "Remove yourself from potential environmental triggers (dust, smoke, cold air)"], "donts": ["Do not lie down (this restricts chest expansion and airways)", "Do not ignore severe chest tightness or difficulty speaking", "Do not engage in physical exertion until breathing is fully stabilized"]},
    "COPD": {"severity": "Chronic Respiratory", "severity_color": "", "action": "Pulmonology Care", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Lung Cancer": {"severity": "Oncological/High Risk", "severity_color": "", "action": "Oncology Management", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Pulmonary Embolism": {"severity": "Life-Threatening Clot", "severity_color": "danger", "action": "Immediate ER Protocol", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Sinusitis": {"severity": "Acute Respiratory", "severity_color": "warning", "action": "Decongestants & Rest", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Allergic Rhinitis": {"severity": "Mild Allergic/Low Risk", "severity_color": "", "action": "Allergen Avoidance", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Bronchitis": {"severity": "Acute/Chest Risk", "severity_color": "warning", "action": "Symptomatic Rest", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Interstitial Lung Disease": {"severity": "Progressive Pulmonary", "severity_color": "", "action": "Specialist Pulmonology", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "Bronchiectasis": {"severity": "Chronic Lung Damage", "severity_color": "", "action": "Airway Clearance", "dos": ["Follow your prescribed medical protocol", "Get adequate rest to support recovery", "Stay well-hydrated with clean water or fluids"], "donts": ["Do not ignore worsening or severe symptoms", "Do not self-medicate or change dosages without consulting a doctor", "Do not engage in strenuous physical activity or overexert yourself"]},
    "COVID Pneumonia": {"severity": "Severe Viral Complication", "severity_color": "danger", "action": "Oxygen & Hospital Care", "dos": ["Isolate immediately in a dedicated, well-ventilated room", "Monitor oxygen levels regularly with a pulse oximeter", "Stay hydrated, rest, and use acetaminophen for fever control"], "donts": ["Do not delay seeking emergency care if oxygen falls below 92%", "Do not self-medicate with unverified clinical therapeutics", "Do not leave isolation or gather in unmasked spaces"]},
    "Appendicitis": {"severity": "Severe Abdominal / ER Risk", "severity_color": "danger", "action": "Immediate Surgical Consult", "dos": ["Seek emergency medical care immediately", "Rest quietly and avoid movement", "Keep track of exactly when pain started and its migration to the lower right abdomen"], "donts": ["Do not eat, drink, or consume fluids (needs NPO for potential surgery)", "Do not take laxatives or use enemas (can cause appendix rupture)", "Do not apply heat or hot packs to the abdomen"]},
    "Urinary Tract Infection (UTI)": {"severity": "Acute Bacterial Infection", "severity_color": "warning", "action": "Clinician Visit & Antibiotics", "dos": ["Drink plenty of water to help flush out bacteria", "Complete the full course of prescribed antibiotics", "Practice proper front-to-back hygiene"], "donts": ["Do not ignore burning or pain during urination", "Do not consume bladder irritants like caffeine, alcohol, or spicy food", "Do not delay urinating when the urge arises"]},
    "Kidney Stones": {"severity": "Acute Renal / Severe Pain", "severity_color": "danger", "action": "Nephrology / ER Care", "dos": ["Drink aggressive amounts of water (2-3 liters/day) to help pass the stone", "Take prescribed pain medications and muscle relaxants as directed", "Strain your urine to catch the stone for laboratory analysis"], "donts": ["Do not consume high-oxalate foods (like spinach, rhubarb, beets)", "Do not ignore signs of fever, chills, or inability to urinate (indicates obstruction/infection)", "Do not self-medicate with high-dose calcium supplements"]},
    "Otitis Media": {"severity": "Acute Otic Infection", "severity_color": "warning", "action": "ENT / Pediatrician Consult", "dos": ["Apply a warm compress to the affected ear to relieve pain", "Administer pain-relieving ear drops or oral analgesics as prescribed", "Keep the ear clean and dry"], "donts": ["Do not insert cotton swabs, bobby pins, or sharp objects into the ear canal", "Do not allow water or soap to enter the ear during showers", "Do not ignore persistent fluid drainage or hearing loss"]},
    "Conjunctivitis": {"severity": "Highly Contagious Ocular", "severity_color": "warning", "action": "Ophthalmic Drops & Hygiene", "dos": ["Wash your hands thoroughly and frequently", "Use separate clean towels and pillowcases daily", "Apply cool or warm compresses to the eyes to reduce swelling"], "donts": ["Do not rub or touch your eyes", "Do not wear contact lenses until the infection is completely resolved", "Do not share eye makeup, eye drops, or sunglasses with others"]},
    "Anaphylaxis": {"severity": "Life-Threatening Emergency", "severity_color": "danger", "action": "Immediate Epinephrine Injection", "dos": ["Administer an epinephrine auto-injector (EpiPen) immediately", "Call emergency services (911/112) without delay", "Lay the patient flat with their legs elevated, keeping them warm"], "donts": ["Do not give oral medications if the patient is struggling to breathe", "Do not wait to see if symptoms improve on their own", "Do not allow the patient to stand up or walk around"]},
    "Gout": {"severity": "Acute Arthritic Flare", "severity_color": "warning", "action": "Anti-inflammatory Care", "dos": ["Elevate and rest the affected joint", "Apply ice packs wrapped in a towel for 15-20 minutes at a time", "Drink plenty of water to dilute uric acid in the body"], "donts": ["Do not consume purine-rich foods like red meat, shellfish, or beer", "Do not wear tight or restrictive footwear over the painful joint", "Do not stop long-term gout medications (like allopurinol) without consulting a doctor"]},
    "Rheumatoid Arthritis": {"severity": "Chronic Autoimmune Joint", "severity_color": "", "action": "Rheumatologist Care", "dos": ["Engage in low-impact joint-friendly exercises like swimming or walking", "Apply warm baths or heating pads to ease morning joint stiffness", "Take prescribed disease-modifying antirheumatic drugs (DMARDs) consistently"], "donts": ["Do not push through severe joint pain during flare-ups", "Do not consume pro-inflammatory processed foods or high sugars", "Do not self-adjust steroid dosages without medical supervision"]},
    "Osteoarthritis": {"severity": "Chronic Degenerative Joint", "severity_color": "", "action": "Joint Mobility & Support", "dos": ["Maintain a healthy body weight to reduce stress on weight-bearing joints", "Use supportive footwear or joint braces as recommended", "Keep active with gentle, structured physical therapy"], "donts": ["Do not engage in high-impact jumping or running if knee/hip joints are degraded", "Do not remain sedentary for prolonged periods (causes joint locking)", "Do not ignore sudden increases in swelling or localized warmth"]},
    "Fibromyalgia": {"severity": "Chronic Pain Disorder", "severity_color": "", "action": "Multimodal Symptom Relief", "dos": ["Establish a strict, calming sleep hygiene routine", "Practice gentle stress-reduction techniques like meditation, yoga, or deep breathing", "Engage in very gradual, low-impact daily exercise"], "donts": ["Do not overexert yourself physically on 'good days' (causes crash cycles)", "Do not consume high levels of caffeine or artificial sweeteners", "Do not isolate yourself from social support networks"]},
    "Meningitis": {"severity": "Critical Neuro Emergency", "severity_color": "danger", "action": "Immediate ER Assessment", "dos": ["Seek emergency hospital admission immediately", "Keep the patient in a quiet, dark, and calm environment while waiting", "Monitor neurological responsiveness and breathing closely"], "donts": ["Do not delay emergency care waiting for a rash to appear (rash is a late sign)", "Do not administer oral pain relievers that might mask diagnostic symptoms", "Do not expose others to salivary contact (extremely contagious)"]},
    "Lyme Disease": {"severity": "Acute Vector Infection", "severity_color": "warning", "action": "Immediate Antibiotics", "dos": ["Complete a full 14-21 day course of oral doxycycline as prescribed", "Note the date of the tick bite and take a photo of any bullseye rash", "Wear tick-repellent clothing and check for ticks after outdoor activities"], "donts": ["Do not crush a tick with your bare hands during removal (use fine-tipped tweezers)", "Do not leave tick mouthparts embedded in the skin", "Do not assume you are cured if the rash disappears without treatment"]},
    "Mononucleosis": {"severity": "Acute Viral Fatigue", "severity_color": "warning", "action": "Symptomatic Care & Rest", "dos": ["Get aggressive physical rest and avoid all heavy lifting", "Stay hydrated with water, herbal teas, or broths", "Use warm saline gargles to relieve severe throat discomfort"], "donts": ["Do not participate in contact sports or vigorous exercise (risk of spleen rupture)", "Do not share cups, utensils, or saliva with others (extremely contagious)", "Do not take amoxicillin or ampicillin (can cause a severe drug rash in mono patients)"]},
    "Chickenpox": {"severity": "Highly Contagious Viral", "severity_color": "warning", "action": "Antipruritic Care & Rest", "dos": ["Apply calamine lotion or take cool colloidal oatmeal baths to relieve itching", "Keep fingernails trimmed short or wear mittens to prevent scratching", "Provide loose, breathable cotton clothing"], "donts": ["Do not give aspirin to children with chickenpox (associated with fatal Reye's Syndrome)", "Do not scratch the blisters (can lead to secondary bacterial infections and permanent scarring)", "Do not visit public spaces or interact with unvaccinated individuals"]},
    "Shingles": {"severity": "Acute Viral Rash", "severity_color": "warning", "action": "Antiviral Rx & Pain Care", "dos": ["Consult a doctor within 72 hours of rash onset to start antivirals", "Keep the rash clean, dry, and loosely covered with a sterile bandage", "Apply cool, wet compresses to the blistered area to soothe burning"], "donts": ["Do not scratch or pop the blisters", "Do not touch or expose the rash to pregnant women, infants, or immunocompromised individuals", "Do not use harsh soaps, perfumes, or heavy oils on the affected skin"]},
    "Tonsillitis": {"severity": "Acute Throat Infection", "severity_color": "warning", "action": "Symptomatic Relief & Meds", "dos": ["Gargle warm saltwater several times a day to ease throat soreness", "Rest your voice and consume soft, cool foods like yogurt, ice cream, or broths", "Use a cool-mist humidifier in your room"], "donts": ["Do not force swallowing of hard, dry, or highly acidic foods", "Do not smoke or expose yourself to secondhand smoke", "Do not stop taking prescribed throat medications early"]},
    "Strep Throat": {"severity": "Acute Bacterial Throat", "severity_color": "warning", "action": "Antibiotic Therapy & Care", "dos": ["Take your prescribed course of antibiotics to prevent rheumatic fever", "Replace your toothbrush 24 hours after starting antibiotics", "Stay home from work or school until you have been on antibiotics for 24 hours"], "donts": ["Do not attempt to scrape or wipe white patches from your tonsils", "Do not share food, drinks, or eating utensils with others", "Do not consume highly acidic juices or spicy foods"]},
    "Laryngitis": {"severity": "Acute Vocal Cord Inflam", "severity_color": "warning", "action": "Strict Vocal Rest", "dos": ["Rest your voice completely\u2014avoid speaking, and do not whisper (whispering strains vocal cords more)", "Inhale steam or use a personal steam inhaler to moisturize vocal cords", "Drink plenty of warm, caffeine-free liquids"], "donts": ["Do not clear your throat repeatedly (this causes harsh vocal cord impact)", "Do not whisper or attempt to shout or sing", "Do not consume decongestants, as they dry out the throat and vocal tract"]},
    "Otitis Externa": {"severity": "Acute Swimmer's Ear", "severity_color": "warning", "action": "Otic Antibiotic Drops", "dos": ["Apply prescribed antibiotic ear drops exactly as directed", "Keep the ear completely dry\u2014use earplugs or a shower cap when bathing", "Use a blow dryer on the lowest heat setting held away from the ear to dry the canal"], "donts": ["Do not swim or submerge your head under water until cleared by a doctor", "Do not scratch the inside of the ear with fingers, keys, or cotton swabs", "Do not wear earplugs or hearing aids while the ear is actively draining"]},
    "Chronic Hypertension": {"severity": "Chronic Cardiovascular", "severity_color": "", "action": "Daily BP Control & Diet", "dos": ["Take your prescribed blood pressure medication daily at the same time", "Adhere to a low-sodium, heart-healthy diet (like the DASH diet)", "Engage in moderate aerobic exercise (e.g., 30 minutes of walking) daily"], "donts": ["Do not skip or suddenly discontinue blood pressure medications (can cause rebound hypertensive crisis)", "Do not consume excessive alcohol, sodium, or processed foods", "Do not use over-the-counter decongestants without checking (they raise blood pressure)"]},
    "Coronary Artery Disease (CAD)": {"severity": "Chronic Ischemic Risk", "severity_color": "", "action": "Cardiologist Management", "dos": ["Eat a diet low in saturated fats, trans fats, and cholesterol", "Take your daily aspirin, beta-blockers, or statins exactly as directed", "Learn to recognize the signs of a heart attack and keep nitroglycerin close if prescribed"], "donts": ["Do not ignore chest tightness, pressure, or shortness of breath during mild exertion", "Do not smoke or use any tobacco/nicotine products", "Do not engage in sudden, highly intense physical strain without medical clearance"]},
    "Congestive Heart Failure (CHF)": {"severity": "Severe Cardiovascular", "severity_color": "danger", "action": "Strict Fluid/Weight Mon", "dos": ["Weigh yourself every morning and report a sudden gain of 2-3 lbs in a day", "Adhere to strict daily fluid and sodium limits as directed by your cardiologist", "Elevate your legs when sitting to reduce lower extremity swelling"], "donts": ["Do not consume high-salt canned soups, processed meats, or salty snacks", "Do not ignore worsening shortness of breath, especially when lying flat in bed", "Do not skip your daily diuretic (water pill) medications"]},
    "Atrial Fibrillation": {"severity": "Chronic Arrhythmia Risk", "severity_color": "", "action": "Rate & Anticoagulant Rx", "dos": ["Take your prescribed blood thinners (anticoagulants) consistently to prevent stroke", "Monitor your heart rate and pulse regularly", "Avoid stress, anxiety, and panic which can trigger episodes"], "donts": ["Do not consume high amounts of caffeine, energy drinks, or alcohol (triggers episodes)", "Do not ignore sudden episodes of dizziness, fainting, or chest discomfort", "Do not take herbal supplements like ginseng or St. John's Wort without consulting your cardiologist"]},
    "Deep Vein Thrombosis (DVT)": {"severity": "Critical Vascular Risk", "severity_color": "danger", "action": "ER Care & Anticoagulation", "dos": ["Seek immediate emergency care if you develop sudden calf swelling, pain, or warmth", "Keep your leg elevated when resting to reduce swelling", "Wear fitted compression stockings if prescribed by a vascular specialist"], "donts": ["Do not massage, rub, or squeeze the painful calf/leg (can dislodge the clot and cause a fatal pulmonary embolism)", "Do not sit or stand still for long periods without moving your ankles and legs", "Do not perform strenuous leg exercises until cleared by your physician"]},
    "Angina": {"severity": "Acute Coronary / Chest Pain", "severity_color": "warning", "action": "Cardiology Care / Nitros", "dos": ["Stop what you are doing, sit down, and rest immediately when chest pain starts", "Use your prescribed nitroglycerin spray or sublingual tablet under your tongue as directed", "Seek emergency services if pain persists for more than 5 minutes after resting/nitroglycerin"], "donts": ["Do not attempt to push through chest pain or walk it off", "Do not eat a heavy meal during or immediately after an episode", "Do not expose yourself to freezing cold air or sudden emotional stress (constricts arteries)"]},
    "Pericarditis": {"severity": "Acute Cardiac Inflamm", "severity_color": "warning", "action": "NSAIDs & Cardiologist", "dos": ["Sit upright and lean forward slightly to ease the chest pain", "Take prescribed high-dose anti-inflammatories (NSAIDs/colchicine) exactly as directed", "Ensure complete physical rest to allow the heart lining to heal"], "donts": ["Do not lie flat on your back (greatly exacerbates the sharp chest pain)", "Do not engage in physical exercise or athletic training until fully cleared", "Do not ignore symptoms like swelling in legs or severe shortness of breath"]},
    "Celiac Disease": {"severity": "Chronic Autoimmune GI", "severity_color": "", "action": "Strict Gluten-Free Diet", "dos": ["Adhere to a strict, 100% lifetime gluten-free diet", "Read all food, medicine, and cosmetic labels carefully for hidden wheat, barley, or rye", "Use separate kitchen utensils and toasters to prevent cross-contact"], "donts": ["Do not consume standard bread, pasta, beer, or baked goods made with wheat", "Do not cheat on your diet, even for small amounts (microscopic gluten damages the small intestine)", "Do not assume food is safe because it is served at a high-end restaurant without double-checking"]},
    "Diverticulitis": {"severity": "Acute Colonic Inflam", "severity_color": "warning", "action": "Antibiotics & Gut Rest", "dos": ["Switch to a clear liquid diet during an active acute flare-up to let your bowel rest", "Take all prescribed antibiotics exactly as directed", "Gradually introduce a high-fiber diet once the inflammation has completely resolved"], "donts": ["Do not consume solid or high-fiber foods during an active painful flare-up", "Do not strain during bowel movements (use a stool softener if recommended)", "Do not take pain relievers like ibuprofen or naproxen (can increase risk of bowel perforation)"]},
    "Hemorrhoids": {"severity": "Acute/Chronic GI Pain", "severity_color": "warning", "action": "Symptomatic Care & Diet", "dos": ["Eat a high-fiber diet and drink plenty of water to keep stools soft and easy to pass", "Take warm sitz baths for 15-20 minutes, 2-3 times a day", "Apply over-the-counter hydrocortisone creams or hazel wipes to relieve itching"], "donts": ["Do not strain or hold your breath during bowel movements", "Do not sit on the toilet for prolonged periods (e.g., reading or browsing your phone)", "Do not use dry, rough toilet paper (use wet wipes or a bidet instead)"]},
    "Lactose Intolerance": {"severity": "Chronic GI Deficiency", "severity_color": "", "action": "Lactose Avoidance & Enz", "dos": ["Limit or avoid dairy foods like milk, cream, soft cheeses, and ice cream", "Take lactase enzyme supplements (Lactaid) immediately before consuming dairy products", "Choose lactose-free dairy or plant-based milks (almond, soy, oat)"], "donts": ["Do not consume large portions of dairy on an empty stomach", "Do not ignore hidden dairy ingredients in processed foods, baked goods, or sauces", "Do not completely cut out calcium\u2014ensure alternative sources like leafy greens or fortified foods"]},
    "Psoriasis": {"severity": "Chronic Dermatological", "severity_color": "", "action": "Topicals & Specialist Care", "dos": ["Moisturize your skin immediately after bathing to lock in hydration", "Apply prescribed corticosteroid or vitamin D creams exactly as directed", "Expose skin to short, controlled periods of natural sunlight"], "donts": ["Do not pick, scratch, or aggressively scrub psoriasis plaques (can trigger new lesions, known as Koebner phenomenon)", "Do not take hot, long showers which dry out the skin", "Do not ignore joint pain or stiffness, which can indicate psoriatic arthritis"]},
    "Eczema": {"severity": "Chronic/Acute Skin Care", "severity_color": "warning", "action": "Aggressive Moisturization", "dos": ["Apply thick, fragrance-free ointments or creams twice daily", "Take short, lukewarm baths or showers using mild, soap-free cleansers", "Wear soft, loose, breathable cotton clothing"], "donts": ["Do not scratch or rub the itchy skin (leads to secondary infection and skin thickening)", "Do not use heavily fragranced laundry detergents, fabric softeners, or soaps", "Do not let your skin get excessively sweaty or overheated"]},
    "Urticaria (Hives)": {"severity": "Acute Allergic Skin", "severity_color": "warning", "action": "Oral Antihistamines", "dos": ["Take non-drowsy over-the-counter antihistamines to control itching and swelling", "Apply cool, damp cloths to the hives to soothe the burning sensation", "Wear loose-fitting, smooth-textured clothing"], "donts": ["Do not scratch or vigorously rub the hives", "Do not take hot showers, baths, or enter saunas (heat releases more histamine)", "Do not expose skin to harsh sunlight or tight elastic bands"]},
    "Scabies": {"severity": "Contagious Parasitic Skin", "severity_color": "warning", "action": "Permethrin Topical Treatment", "dos": ["Apply permethrin 5% cream to your entire body from the neck down and wash off after 8-14 hours", "Treat all household members and close contacts at the exact same time", "Wash all worn clothing, towels, and bedding in hot water and dry on high heat"], "donts": ["Do not scratch the intense itching (can lead to severe bacterial infections)", "Do not skip hard-to-reach areas like skin folds, between fingers, and under nails during treatment", "Do not return to work or school until 24 hours after completing the permethrin treatment"]},
    "Rosacea": {"severity": "Chronic Vascular Skin", "severity_color": "", "action": "Gentle Skin & Topicals", "dos": ["Apply broad-spectrum SPF 30+ sunscreen daily (sun exposure is a major trigger)", "Use highly gentle, soap-free cleansers and wash with lukewarm water", "Keep a journal to identify your personal triggers (e.g. spicy food, wind, stress)"], "donts": ["Do not consume hot beverages, spicy foods, alcohol, or red wine (causes severe flushing flares)", "Do not use harsh facial scrubs, astringents, or alcohol-based skin products", "Do not rub or massage your facial skin"]},
    "Alopecia Areata": {"severity": "Autoimmune Hair Loss", "severity_color": "", "action": "Dermatologist Care", "dos": ["Protect bald patches on the scalp with sun-protective hats or sunscreen", "Explore treatment options like corticosteroid injections or topical minoxidil", "Seek emotional support or counseling to cope with the stress of hair loss"], "donts": ["Do not use harsh chemical dyes, perms, or heating irons on remaining hair", "Do not style hair in tight, pulling styles like braids or ponytails", "Do not buy expensive, unproven 'miracle hair growth' products from unverified sources"]},
    "Osteoporosis": {"severity": "Chronic Bone Density", "severity_color": "", "action": "Calcium, Vitamin D & Phys", "dos": ["Ensure adequate intake of calcium and Vitamin D daily through diet or supplements", "Engage in weight-bearing exercises like walking or resistance training to strengthen bones", "Modify your home environment to eliminate fall hazards (throw rugs, poor lighting)"], "donts": ["Do not engage in high-impact jumping, heavy forward bending, or twisting motions", "Do not consume excessive amounts of alcohol, caffeine, or carbonated beverages", "Do not lift extremely heavy objects without proper body mechanics"]},
    "Polycystic Ovary Syndrome (PCOS)": {"severity": "Chronic Endocrine Care", "severity_color": "", "action": "Hormonal & Lifestyle Care", "dos": ["Maintain a balanced, low-glycemic, anti-inflammatory diet", "Engage in regular physical exercise to improve insulin sensitivity", "Take prescribed medications (e.g., birth control, metformin) exactly as directed"], "donts": ["Do not skip meals or consume diets high in refined sugars and simple carbs", "Do not ignore irregular or absent menstrual periods (increases risk of endometrial lining issues)", "Do not get discouraged by slow weight management\u2014focus on consistency"]},
    "Chronic Fatigue Syndrome": {"severity": "Chronic Systemic/Neuro", "severity_color": "", "action": "Pacing & Supportive Care", "dos": ["Practice daily structured activity pacing to stay within your energy limits", "Ensure a highly relaxing, consistent sleep routine", "Maintain a balanced, easily digestible, nutrient-dense diet"], "donts": ["Do not attempt to 'push through' fatigue (causes severe post-exertional malaise crashes)", "Do not engage in vigorous, high-intensity exercise programs", "Do not schedule multiple stressful activities in a single day"]},
    "Sleep Apnea": {"severity": "Chronic Respiratory Sleep", "severity_color": "", "action": "CPAP Therapy & Sleep Study", "dos": ["Use your CPAP machine consistently every single night as prescribed", "Sleep on your side or stomach rather than on your back", "Avoid alcohol and sedatives, especially in the evening (they relax throat muscles)"], "donts": ["Do not sleep on your back (causes the tongue and throat tissues to collapse into the airway)", "Do not ignore daytime sleepiness, morning headaches, or loud snoring", "Do not drive or operate machinery if you feel fatigued or un-rested"]},
    "Insomnia": {"severity": "Chronic Sleep Disorder", "severity_color": "", "action": "CBT-I & Sleep Hygiene", "dos": ["Go to bed and wake up at the exact same time every single day (even weekends)", "Keep your bedroom dark, quiet, and cool (60-67F)", "Use your bed ONLY for sleep and intimacy"], "donts": ["Do not look at blue-light emitting phone, TV, or computer screens in bed", "Do not consume caffeine, nicotine, or heavy meals within 4-6 hours of bedtime", "Do not lie in bed awake for more than 20 minutes (get up and do a quiet activity)"]},
    "Generalized Anxiety Disorder (GAD)": {"severity": "Chronic Psychiatric", "severity_color": "", "action": "Psychotherapy & Meds", "dos": ["Practice daily relaxation techniques (deep breathing, progressive muscle relaxation)", "Limit caffeine and stimulant intake (they mimic and trigger physical panic symptoms)", "Engage in regular, structured physical exercise to burning off stress hormones"], "donts": ["Do not use alcohol or recreational substances to self-medicate anxiety symptoms", "Do not isolate yourself when feeling anxious or overwhelmed", "Do not catastrophize or dwell on negative 'what-if' scenarios"]},
    "Major Depressive Disorder (MDD)": {"severity": "Severe Psychiatric Risk", "severity_color": "danger", "action": "Therapy & Antidepressants", "dos": ["Attend scheduled therapy sessions (CBT) and take medications exactly as prescribed", "Stay connected with family, friends, or support groups", "Break large tasks down into tiny, easily manageable daily steps"], "donts": ["Do not isolate yourself in your room or cut off communications", "Do not make major life-changing decisions during a severe depressive episode", "Do not suddenly discontinue antidepressant medications (can cause severe withdrawal)"]},
    "Panic Disorder": {"severity": "Acute Psychiatric Flare", "severity_color": "warning", "action": "Coping Skills & Meds", "dos": ["Practice slow, deep, diaphragmatic breathing during an active panic attack", "Remind yourself that panic attacks are temporary and not life-threatening", "Focus on a physical object in your surroundings to ground yourself"], "donts": ["Do not fight or resist the panic attack (this increases adrenaline\u2014let it peak and pass)", "Do not flee the situation immediately if safe (teaches your brain that the environment is dangerous)", "Do not consume energy drinks, coffee, or decongestants"]},
    "Obsessive-Compulsive Disorder (OCD)": {"severity": "Chronic Neuro-Psychiatric", "severity_color": "", "action": "CBT & Exposure Therapy", "dos": ["Practice Exposure and Response Prevention (ERP) techniques as guided by your therapist", "Delay performing compulsions by a few minutes, gradually increasing the time", "Recognize that intrusive thoughts are just noise and do not define you"], "donts": ["Do not seek constant reassurance from family or friends (fuels the OCD loop)", "Do not attempt to actively suppress intrusive thoughts (causes them to return stronger)", "Do not structure your daily life around avoiding triggers"]},
    "Vascular Dementia": {"severity": "Severe Progressive Cognitive", "severity_color": "danger", "action": "Neurology & Card Care", "dos": ["Maintain tight control over cardiovascular factors (blood pressure, diabetes, cholesterol)", "Keep a highly structured daily routine with visual memory aids (calendars, checklists)", "Engage in daily cognitive exercises and social interactions"], "donts": ["Do not make sudden, drastic changes to the patient's home environment", "Do not argue with or aggressively correct the patient when they are confused", "Do not leave dangerous items (stoves, car keys, medications) accessible"]},
    "Glaucoma": {"severity": "Critical Ocular Emergency", "severity_color": "danger", "action": "Daily Pressure-Lowering Drops", "dos": ["Apply your prescribed pressure-lowering eye drops daily without fail", "Attend all scheduled ophthalmologist visits to monitor optic nerve health", "Wear protective eyewear during sports or home improvement"], "donts": ["Do not rub your eyes, especially after applying drops", "Do not assume your eyes are fine because you have no pain or noticeable vision loss", "Do not double up on drops if you miss a dose"]},
    "Cataracts": {"severity": "Progressive Visual Care", "severity_color": "", "action": "Ophthalmology / Surgery", "dos": ["Wear UV-blocking sunglasses outdoors to slow cataract progression", "Ensure bright, direct lighting in your reading and work areas", "Update your lens prescription regularly and schedule surgical evaluation when ready"], "donts": ["Do not drive at night if you experience severe glare, halos around lights, or double vision", "Do not use eye drops that promise to dissolve cataracts (there are no drops that cure them)", "Do not delay surgery if cataracts are severely impacting your daily independence"]},
    "Dry Eye Syndrome": {"severity": "Chronic Ocular Discomfort", "severity_color": "", "action": "Lubricating Drops & Care", "dos": ["Use preservative-free artificial tears frequently throughout the day", "Follow the 20-20-20 rule during screen use (look 20 feet away for 20 seconds every 20 minutes)", "Use a warm compress on your eyes daily to help release natural oils"], "donts": ["Do not let air from fans, air conditioners, or car vents blow directly onto your face", "Do not rub your dry eyes (causes corneal abrasion)", "Do not wear contact lenses for prolonged hours without lubricating them"]},
    "Restless Legs Syndrome (RLS)": {"severity": "Chronic Sleep/Neuro Care", "severity_color": "", "action": "Neurology & Iron Check", "dos": ["Engage in regular, moderate exercise (like walking or yoga) in the morning or afternoon", "Take a warm bath or massage your leg muscles before bedtime", "Get your iron levels (ferritin) checked by your physician"], "donts": ["Do not perform intense, strenuous workouts close to bedtime (triggers RLS)", "Do not consume alcohol, caffeine, or nicotine in the evening", "Do not ignore symptoms\u2014there are effective prescription medications available"]},
}

# --- Model Loading ---
import joblib

@st.cache_resource
def load_models():
    """Loads the pre-trained ML model and MultiLabelBinarizer."""
    model = joblib.load("model.pkl")
    mlb = joblib.load("mlb.pkl")
    return model, mlb

def analyze_patient_vitals(bp_str, glucose_val, hr_val, cholesterol_val):
    """Analyzes the vitals and returns clinical status with CSS classes."""
    # Heart Rate status
    if hr_val > 100:
        hr_status = "Tachycardia (High) ⚠️"
        hr_class = "danger"
    elif hr_val < 60:
        hr_status = "Bradycardia (Low) ⚠️"
        hr_class = "warning"
    else:
        hr_status = "Normal Range ✅"
        hr_class = "success"

    # Cholesterol status
    if cholesterol_val >= 240:
        chol_status = "High Risk ⚠️"
        chol_class = "danger"
    elif cholesterol_val >= 200:
        chol_status = "Borderline High ⚠️"
        chol_class = "warning"
    else:
        chol_status = "Optimal Range ✅"
        chol_class = "success"

    # Glucose status
    if glucose_val >= 126:
        gluc_status = "Diabetic Range ⚠️"
        gluc_class = "danger"
    elif glucose_val >= 100:
        gluc_status = "Elevated (Pre-diabetic)"
        gluc_class = "warning"
    elif glucose_val < 70:
        gluc_status = "Hypoglycemia (Low) ⚠️"
        gluc_class = "danger"
    else:
        gluc_status = "Normal Range ✅"
        gluc_class = "success"

    # Blood Pressure status
    bp_status = "Normal Range ✅"
    bp_class = "success"
    try:
        if "/" in bp_str:
            sys_str, dia_str = bp_str.split("/")
            systolic = int(sys_str.strip())
            diastolic = int(dia_str.strip())
            if systolic > 180 or diastolic > 120:
                bp_status = "Hypertensive Crisis 🚨"
                bp_class = "danger"
            elif systolic >= 140 or diastolic >= 90:
                bp_status = "Hypertension Stage 2 ⚠️"
                bp_class = "danger"
            elif (130 <= systolic <= 139) or (81 <= diastolic <= 89):
                bp_status = "Hypertension Stage 1 ⚠️"
                bp_class = "warning"
            elif (121 <= systolic <= 129) and diastolic <= 80:
                bp_status = "Elevated BP"
                bp_class = "warning"
            elif systolic < 90 or diastolic < 60:
                bp_status = "Hypotension (Low) ⚠️"
                bp_class = "warning"
            else:
                bp_status = "Normal Range ✅"
                bp_class = "success"
    except Exception:
        bp_status = "Invalid Format ⚠️"
        bp_class = "warning"

    return {
        "bp": {"val": bp_str, "status": bp_status, "class": bp_class},
        "hr": {"val": f"{hr_val} bpm", "status": hr_status, "class": hr_class},
        "glucose": {"val": f"{glucose_val} mg/dl", "status": gluc_status, "class": gluc_class},
        "cholesterol": {"val": f"{cholesterol_val} mg/dl", "status": chol_status, "class": chol_class}
    }

# --- Main Application ---
def main():
    inject_custom_css()
    import os
    
    # Initialize session state keys for the widgets if they don't exist
    if "symptoms" not in st.session_state:
        st.session_state.symptoms = []
    if "bp" not in st.session_state:
        st.session_state.bp = "120/80"
    if "glucose" not in st.session_state:
        st.session_state.glucose = 90
    if "hr" not in st.session_state:
        st.session_state.hr = 72
    if "cholesterol" not in st.session_state:
        st.session_state.cholesterol = 150
        
    def clear_form():
        st.session_state.symptoms = []
        st.session_state.bp = "120/80"
        st.session_state.glucose = 90
        st.session_state.hr = 72
        st.session_state.cholesterol = 150
        
    # --- Top Section Layout ---
    top_col_left, top_col_right = st.columns([1.4, 1])
    
    with top_col_left:
        # --- Main Header ---
        st.title("🩺 Clinical Diagnostic Assistant")
        st.markdown("#### Patient Symptom Assessment Tool")
        
        # --- Pipeline Execution ---
        with st.spinner("Loading Clinical Models..."):
            model, mlb = load_models()
            all_symptoms = list(mlb.classes_)
        
        # --- User Input Section ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("📋 Symptom Assessment")
        
        selected_symptoms = st.multiselect(
            "Select all reported symptoms:",
            options=all_symptoms,
            placeholder="Search from 100 clinical symptoms...",
            key="symptoms"
        )
        
        # Functional Vitals Input Cards
        st.markdown("<div style='font-size: 18px; font-weight: 600; color: #4b5563; margin-top: 20px; margin-bottom: 10px;'>📊 Patient Vitals</div>", unsafe_allow_html=True)
        
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            bp = st.text_input("Blood Pressure (mmHg) 🩺", placeholder="e.g., 120/80", key="bp")
            glucose = st.number_input("Glucose (mg/dl) 🩸", min_value=0, max_value=500, key="glucose")
            
        with v_col2:
            hr = st.number_input("Heart Rate (bpm) ❤️", min_value=0, max_value=300, key="hr")
            cholesterol = st.number_input("Cholesterol (mg/dl) 🧬", min_value=0, max_value=500, key="cholesterol")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            predict_btn = st.button("🔬 Generate Diagnosis Report", type="primary")
        with btn_col2:
            st.button("🔄 Clear Form", type="secondary", on_click=clear_form)
            
    with top_col_right:
        if os.path.exists("assets/bg_image.png"):
            st.markdown("<div style='padding-top: 40px;'></div>", unsafe_allow_html=True)
            st.image("assets/bg_image.png", use_container_width=True)
        else:
            st.empty()
        
    # --- Prediction & Results ---
    if predict_btn:
        if len(selected_symptoms) == 0:
            st.error("⚠️ Please select at least one symptom to generate a report.")
        elif len(selected_symptoms) < 2:
            st.warning("⚠️ Warning: Selecting only one symptom may lead to low-confidence predictions.")
            
        if len(selected_symptoms) > 0:
            with st.spinner("🧠 Analyzing clinical profile..."):
                time.sleep(1) 
                
                input_data = mlb.transform([selected_symptoms])
                probabilities = model.predict_proba(input_data)[0]
                classes = model.classes_
                
                top_idx = np.argsort(probabilities)[::-1]
                top_diseases = classes[top_idx]
                top_probs = probabilities[top_idx]
                
                primary_disease = top_diseases[0]
                primary_confidence = top_probs[0] * 100
                
                # --- Rendering the New Report Layout ---
                st.markdown("---")
                st.markdown('<div class="dashboard-section-title">🩺 Prediction Results</div>', unsafe_allow_html=True)
                
                # 1. Top 3 Diseases (CSS Grid for guaranteed equal height)
                match_cards_html = '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; align-items: stretch;">'
                for i in range(3):
                    if i < len(top_probs):
                        conf = top_probs[i] * 100
                        if conf > 70:
                            conf_color = "#dc2626" # Red
                        elif conf >= 40:
                            conf_color = "#f97316" # Orange
                        else:
                            conf_color = "#16a34a" # Green
                            
                        match_cards_html += (
                            f'<div class="match-card">'
                            f'<div class="match-card-badge">Match #{i+1}</div>'
                            f'<div class="match-card-title">{top_diseases[i]}</div>'
                            f'<div class="match-card-conf" style="color: {conf_color};">{conf:.1f}% Confidence</div>'
                            f'</div>'
                        )
                match_cards_html += '</div>'
                st.markdown(match_cards_html, unsafe_allow_html=True)
                            
                # 2. Primary Diagnosis Details
                st.markdown('<div class="dashboard-section-title" style="margin-top: 30px;">📋 Primary Diagnosis Details</div>', unsafe_allow_html=True)
                
                # Define simple clinical rules for dashboard
                disease_info = DOS_AND_DONTS.get(primary_disease, {})
                severity = disease_info.get("severity", "Unknown Risk")
                severity_color = disease_info.get("severity_color", "")
                action = disease_info.get("action", "Consult Physician")

                # Primary Diagnosis Card
                st.markdown(
                    f'<div class="primary-diagnosis-card">'
                    f'<div class="primary-diagnosis-title">Most Probable Condition</div>'
                    f'<div class="primary-diagnosis-value">{primary_disease}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Metrics Row (CSS Grid for guaranteed equal height & uniform alignment)
                st.markdown(
                    f'<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; align-items: stretch;">'
                    f'<div class="dashboard-card" style="display: flex; flex-direction: column; justify-content: space-between; padding: 24px; box-sizing: border-box;">'
                    f'<div><div class="metric-label">🏥 Severity Assessment</div>'
                    f'<div style="font-size: 22px; font-weight: 700; color: #111827; margin: 10px 0; line-height: 1.3;">{severity}</div></div>'
                    f'<div class="metric-sub {severity_color}">Based on clinical guidelines</div></div>'
                    f'<div class="dashboard-card" style="display: flex; flex-direction: column; justify-content: space-between; padding: 24px; box-sizing: border-box;">'
                    f'<div><div class="metric-label">⚕️ Recommended Action</div>'
                    f'<div style="font-size: 22px; font-weight: 700; color: #111827; margin: 10px 0; line-height: 1.3;">{action}</div></div>'
                    f'<div class="metric-sub">Primary directive</div></div></div>',
                    unsafe_allow_html=True
                )

                # 2.5 Patient Vitals & Clinical Indicators Summary (CSS Grid)
                st.markdown('<div class="dashboard-section-title" style="margin-top: 30px;">📊 Patient Vitals & Clinical Indicators</div>', unsafe_allow_html=True)
                
                vitals_data = analyze_patient_vitals(bp, glucose, hr, cholesterol)
                v_keys = ["bp", "hr", "glucose", "cholesterol"]
                v_labels = ["🩺 Blood Pressure", "❤️ Heart Rate", "🩸 Glucose", "🧬 Cholesterol"]
                
                vitals_html = '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; align-items: stretch;">'
                for idx, key in enumerate(v_keys):
                    data = vitals_data[key]
                    val = data["val"]
                    status = data["status"]
                    css_class = data["class"]
                    vitals_html += (
                        f'<div class="dashboard-card" style="text-align: center; padding: 20px 12px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; box-sizing: border-box;">'
                        f'<div style="font-size: 15px; color: #6b7280; font-weight: 600;">{v_labels[idx]}</div>'
                        f'<div style="font-size: 22px; font-weight: 700; color: #111827; margin: 8px 0;">{val}</div>'
                        f'<div class="{css_class}" style="font-size: 14px; font-weight: 700;">{status}</div></div>'
                    )
                vitals_html += '</div>'
                st.markdown(vitals_html, unsafe_allow_html=True)
                
                # 3. Dos and Don'ts Section (CSS Grid)
                st.markdown('<div class="dashboard-section-title" style="margin-top: 30px;">✅ Do\'s & ❌ Don\'ts</div>', unsafe_allow_html=True)
                
                dos_list = DOS_AND_DONTS.get(primary_disease, {}).get("dos", ["Consult a doctor", "Rest", "Stay hydrated"])
                donts_list = DOS_AND_DONTS.get(primary_disease, {}).get("donts", ["Ignore symptoms", "Self-medicate", "Overexert yourself"])
                
                dos_items_html = "".join([f"<li style='margin-bottom: 10px; line-height: 1.4;'>{item}</li>" for item in dos_list])
                donts_items_html = "".join([f"<li style='margin-bottom: 10px; line-height: 1.4;'>{item}</li>" for item in donts_list])
                
                dos_donts_html = (
                    f'<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; align-items: stretch;">'
                    f'<div class="dashboard-card" style="border-top: 4px solid #10b981; display: flex; flex-direction: column; justify-content: flex-start; padding: 24px; box-sizing: border-box;">'
                    f'<h4 style="color: #111827; margin-top: 0; margin-bottom: 16px; font-size: 18px; font-weight: 700;">✅ Recommended Do\'s</h4>'
                    f'<ul style="color: #111827; padding-left: 20px; margin: 0; flex-grow: 1;">{dos_items_html}</ul></div>'
                    f'<div class="dashboard-card" style="border-top: 4px solid #ef4444; display: flex; flex-direction: column; justify-content: flex-start; padding: 24px; box-sizing: border-box;">'
                    f'<h4 style="color: #111827; margin-top: 0; margin-bottom: 16px; font-size: 18px; font-weight: 700;">❌ Critical Don\'ts</h4>'
                    f'<ul style="color: #111827; padding-left: 20px; margin: 0; flex-grow: 1;">{donts_items_html}</ul></div></div>'
                )
                st.markdown(dos_donts_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
