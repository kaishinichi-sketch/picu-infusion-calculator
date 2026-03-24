import streamlit as st
import pandas as pd
from PIL import Image
logo = Image.open("logo.png")
st.image(logo, width=140)

# Load your Excel data
file_path = "PICU_Infusion_Calculator.xlsx"

units = pd.read_excel(file_path, sheet_name="Units")
formulary = pd.read_excel(file_path, sheet_name="Formulary")

st.set_page_config(page_title="PICU Infusion Calculator", layout="centered")

### UI THEME: MEDICAL CLASSIC (Blue / White)
st.markdown("""
    <style>
        body {background-color: #ffffff;}
        .main {background-color: white;}
        h1 {color: #005EB8; font-weight: 900;}
        label, p {color: #003865;}
    </style>
""", unsafe_allow_html=True)

st.title("PICU Infusion Calculator")
st.markdown("**Created by: Katherine Casandra Sta. Ana, RN, MSN**")
st.write("Clinical Mode • Auto‑Fill Enabled")

# User Inputs
weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1)

drug = st.selectbox("Select Drug", formulary["Drug"])

selected = formulary[formulary["Drug"] == drug].iloc[0]

concentration_type = st.radio("Concentration Type", ["Standard", "Maximum"])

if concentration_type == "Standard":
    amount = selected["Std_Amount_mg"]
    volume = selected["Std_Final_mL"]
    diluent = selected["Std_Diluent"]
else:
    amount = selected["Max_Amount_mg"]
    volume = selected["Max_Final_mL"]
    diluent = selected["Max_Diluent"]

dose_unit = selected["Dose_Unit"]
stock_conc = selected["StockConc_mg_mL"]

st.subheader("Autofilled From Formulary")
st.write(f"Dose unit: **{dose_unit}**")
st.write(f"Stock concentration: **{stock_conc} mg/mL**")
st.write(f"Diluent: **{diluent}**")
st.write(f"Final volume: **{volume} mL**")

ordered_dose = st.number_input(f"Ordered Dose ({dose_unit})", min_value=0.0, step=0.01)

### CALCULATIONS

# 1. Dose mg/hr
if dose_unit == "mcg/kg/min":
    dose_mghr = ordered_dose * weight * 60 / 1000
elif dose_unit == "mcg/kg/hr":
    dose_mghr = ordered_dose * weight / 1000
elif dose_unit == "mg/kg/hr":
    dose_mghr = ordered_dose * weight
elif dose_unit == "unit/kg/hr":
    dose_mghr = ordered_dose * weight
else:
    dose_mghr = None

# 2. Resulting concentration
resulting_conc = amount / volume if volume > 0 else 0

# 3. Stock to draw
stock_to_draw = amount / stock_conc if stock_conc > 0 else 0

# 4. Diluent to add
diluent_add = volume - stock_to_draw

# 5. Infusion rate
infusion_rate = dose_mghr / resulting_conc if resulting_conc > 0 else 0

### DISPLAY RESULTS
st.header("Results")

st.write(f"**Resulting concentration:** {resulting_conc:.4f} mg/mL")
st.write(f"**Stock to draw:** {stock_to_draw:.2f} mL")
st.write(f"**Diluent to add:** {diluent_add:.2f} mL")
st.write(f"**Dose (mg/hr):** {dose_mghr:.3f}")
st.write(f"**Infusion rate:** {infusion_rate:.2f} mL/hr")

st.subheader("How to Prepare")
st.write(
    f"Draw **{stock_to_draw:.2f} mL** of stock + **{diluent_add:.2f} mL** of {diluent} → "
    f"Prepare **{volume} mL** of **{drug}** ({concentration_type})."
)

st.subheader("Special Consideration")
st.write(selected["Special consideration"])

st.subheader("Average Starting Dose")
st.write(selected["Average starting dose (Dose range)"])
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 13px; color: #555;'>
Drug data and preparation standards used in this application are derived from the
<b>Standardized Pediatric and Neonatal IV Drips List for Commonly Used Medications</b>,
issued by King Saud University Medical City (KSUMC), Department of Pharmacy Services – Pharmacy Practice Council.
</div>
""", unsafe_allow_html=True)
