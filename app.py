import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="PICU Infusion Calculator",
    page_icon="🧪",
    layout="centered"
)

# ---------------------------------------------------------
# HEADER + LOGO
# ---------------------------------------------------------
st.markdown(
    """
    <div style='text-align:center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Star_of_life2.svg/1200px-Star_of_life2.svg.png'
             width='90'>
        <h1 style='margin-top:10px;'>PICU Infusion Calculator</h1>
        <p style='font-size:16px; color:gray;'>Modern • Accurate • Pediatric‑Focused</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------------------------
# LOAD FORMULARY
# ---------------------------------------------------------
formulary = pd.DataFrame({
    "Drug": [
        "Epinephrine (1mg/mL) 1mL",
        "Norepinephrine (1mg/mL) 4mL",
        "Dopamine (40mg/mL) 5mL",
        "Dobutamine (50mg/mL) 5mL",
        "Labetalol (5mg/mL) 20mL",
        "Fentanyl (50mcg/mL) 10mL",
        "Midazolam (5mg/mL) 3mL",
        "Ketamine (50mg/mL) 10mL",
        "Cisatracurium (2mg/mL) 10mL",
        "Dexmedetomidine (100mcg/mL) 2mL",
        "Furosemide (10mg/mL) 2mL",
        "Heparin (5000 units/mL)",
        "Insulin (100 units/mL)"
    ],
    "Dose_Unit": [
        "mcg/kg/min", "mcg/kg/min", "mcg/kg/min", "mcg/kg/min",
        "mg/kg/hr", "mcg/kg/hr", "mcg/kg/min", "mcg/kg/min",
        "mcg/kg/min", "mcg/kg/hr", "mg/kg/hr", "unit/kg/hr", "unit/kg/hr"
    ],
    "StockConc": [1, 4, 200, 250, 100, 0.5, 15, 500, 20, 0.2, 20, 5000, 1000]
})

# ---------------------------------------------------------
# INPUT PANEL
# ---------------------------------------------------------
st.subheader("Enter Patient & Infusion Details")

with st.container():
    st.markdown(
        "<div style='padding:15px; border:2px solid #4A90E2; border-radius:10px; background:#F0F8FF;'>",
        unsafe_allow_html=True
    )

    weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1)

    drug = st.selectbox("Select Drug", formulary["Drug"].tolist())

    dose = st.number_input("Ordered Dose", min_value=0.0, step=0.01)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# CALCULATION ENGINE
# ---------------------------------------------------------
def calculate_rate(weight, dose, stock_conc, dose_unit):
    if "mcg" in dose_unit:
        mg_per_min = (dose / 1000) * weight
    elif "mg" in dose_unit:
        mg_per_min = (dose * weight) / 60
    elif "unit" in dose_unit:
        mg_per_min = dose * weight
    else:
        return None

    mL_per_min = mg_per_min / stock_conc
    mL_per_hr = mL_per_min * 60
    return mL_per_hr

# ---------------------------------------------------------
# IMMEDIATE OUTPUT
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Result")

if weight > 0 and dose > 0:
    row = formulary[formulary["Drug"] == drug].iloc[0]
    stock = row["StockConc"]
    dose_unit = row["Dose_Unit"]

    rate = calculate_rate(weight, dose, stock, dose_unit)

    if rate:
        st.success(f"**Infusion Rate:** {rate:.2f} mL/hr")
    else:
        st.error("Unable to calculate. Check inputs.")
else:
    st.info("Enter weight and dose to see the result.")

# ---------------------------------------------------------
# DISCLAIMER + ATTRIBUTION
# ---------------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <div style='font-size:13px; color:gray;'>
    <strong>Disclaimer:</strong><br>
    Drug data and preparation standards used in this application are derived from the
    <em>Standardized Pediatric and Neonatal IV Drips List for Commonly Used Medications</em>,
    issued by <strong>King Saud University Medical City (KSUMC), Department of Pharmacy Services – Pharmacy Practice Council</strong>.
    <br><br>
    This tool is for educational support only and must not replace clinical judgment.
    <br><br>
    <strong>Created by:</strong> Katherine Casandra Sta. Ana, RN, MSN.
    </div>
    """,
    unsafe_allow_html=True
)
