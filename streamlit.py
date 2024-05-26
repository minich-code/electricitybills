import streamlit as st
import pandas as pd
import os
import sys
from src.ElectricityBill.pipelines.pip_06_prediction_pipeline import CustomData, PredictionPipeline
from src.ElectricityBill.exception import FileOperationError
from src.ElectricityBill import logging

# Function to train the pipeline
def train_pipeline():
    os.system("python main.py")
    st.success("Training Successful!")

# Function to predict the pipeline
def predict_data_point(form_data):
    try:
        # Create custom data object using kwargs
        custom_data = CustomData(**form_data)

        # Convert form data dictionary to a DataFrame
        pred_df = custom_data.get_data_as_dataframe()

        # Log message and display dataframe for debugging
        logging.info(f"Form data before prediction: {form_data}")
        st.write("Data for Prediction:", pred_df)

        # Initialize the prediction pipeline
        prediction_pipeline = PredictionPipeline()

        # Log message
        logging.info(f"Form data mid prediction: {form_data}")

        # Get the prediction
        prediction = prediction_pipeline.make_predictions(pred_df)

        # Log message
        logging.info(f"Form data after prediction: {form_data}")

        # Return results
        return prediction[0]
        
    except Exception as e:
        logging.exception(e)
        raise FileOperationError(e)

# Streamlit App
def main():
    st.title("Electricity Bill Predictor")

    menu = ["Home", "Train", "Predict"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Electricity Bill Predictor application.")

    elif choice == "Train":
        st.subheader("Train the Model")
        if st.button("Train"):
            train_pipeline()

    elif choice == "Predict":
        st.subheader("Predict Electricity Bill")

        # Create form fields for user input
        Fan = st.number_input("Number of Operation Hours: Fans", min_value=0)
        Refrigerator = st.number_input("Number of Operation Hours: Refrigerators", min_value=0)
        AirConditioner = st.number_input("Number of Operation Hours: Air Conditioners", min_value=0)
        Television = st.number_input("Number of Operation Hours: Televisions", min_value=0)
        Monitor = st.number_input("Number of Operation Hours: Monitors", min_value=0)
        MotorPump = st.number_input("Number of Operation Hours: Motor Pumps", min_value=0)
        Month = st.text_input("Month", placeholder="Enter Month")
        City = st.selectbox("City", ["Hyderabad", "Navi Mumbai", "Ratnagiri", "Faridabad", "Gurgaon", "Ahmedabad",
                                     "New Delhi", "Mumbai", "Chennai", "Dahej", "Nagpur", "Noida", "Pune", "Shimla",
                                     "Kolkata", "Vadodara"])
        Company = st.selectbox("Company", ["Ringfeder Power Transmission India Pvt. Ltd.", "JSW Energy Ltd.", "Guj Ind Power",
                                           "SJVN Ltd.", "Maha Transco – Maharashtra State Electricity Transmission Co, Ltd.",
                                           "NTPC Pvt. Ltd.", "Optibelt Power Transmission India Private Limited", "Kalpataru Power",
                                           "GE T&D India Limited", "KEC International", "Reliance Power", "Orient Green",
                                           "Torrent Power Ltd.", "L&T Transmission & Distribution", "Unitech Power Transmission Ltd.",
                                           "Power Grid Corp", "Jaiprakash Power", "NLC India", "Sunil Hitech Eng", "Sterlite Power Transmission Ltd",
                                           "Adani Power Ltd.", "Ratnagiri Gas and Power Pvt. Ltd. (RGPPL)", "NHPC",
                                           "Neueon Towers / Sujana Towers Ltd.", "Bonfiglioli Transmission Pvt. Ltd.", "Jyoti Structure",
                                           "TransRail Lighting", "Indowind Energy", "CESC", "Tata Power Company Ltd.", "Reliance Energy",
                                           "Toshiba Transmission & Distribution Systems (India) Pvt. Ltd."])
        MonthlyHours = st.number_input("Total Monthly Hours", min_value=0)
        TariffRate = st.number_input("Tariff Rate", min_value=0.0, format="%.2f")

        # Make prediction when the form is submitted
        if st.button("Predict"):
            form_data = {
                'Fan': Fan,
                'Refrigerator': Refrigerator,
                'AirConditioner': AirConditioner,
                'Television': Television,
                'Monitor': Monitor,
                'MotorPump': MotorPump,
                'Month': Month,
                'City': City,
                'Company': Company,
                'MonthlyHours': MonthlyHours,
                'TariffRate': TariffRate
            }

            prediction = predict_data_point(form_data)
            st.success(f"Predicted Bill Amount: {prediction}")

if __name__ == '__main__':
    main()
