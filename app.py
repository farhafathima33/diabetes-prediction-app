import streamlit as st
import pickle
import mysql.connector


# Load trained ML model

with open("diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)

# Database connection

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="farha",
        password="farha123",          # add password if you set one
        database="diabatese_db"
    )


# Streamlit UI

st.title("Diabetes Prediction System")
st.write("Enter patient details below")

with st.form("patient_form"):
    patient_name = st.text_input("Patient Name")

    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20)
    glucose = st.number_input("Glucose Level", min_value=50, max_value=300)
    blood_pressure = st.number_input("Blood Pressure", min_value=40, max_value=200)
    skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100)
    insulin = st.number_input("Insulin Level", min_value=0, max_value=900)
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, format="%.2f")
    diabetes_pedigree = st.number_input(
        "Diabetes Pedigree Function", min_value=0.0, max_value=3.0, format="%.2f"
    )
    age = st.number_input("Age", min_value=1, max_value=120)

    submit = st.form_submit_button("Predict")


# Prediction + DB insert

if submit:
    input_data = [[
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        diabetes_pedigree,
        age
    ]]

    prediction = model.predict(input_data)[0]
    result = "Diabetes Positive" if prediction == 1 else "Diabetes Negative"

    # Insert into database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO patient_records
        (patient_name, pregnancies, glucose, blood_pressure,
         skin_thickness, insulin, bmi, diabetes_pedigree, age, prediction)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            patient_name,
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age,
            result
        )
    )
    conn.commit()
    conn.close()

    st.success(f"Prediction Result: {result}")
