from flask import Flask, request, render_template
import os
import sys 


from src.ElectricityBill.pipelines.pip_06_prediction_pipeline import CustomData, PredictionPipeline
from src.ElectricityBill.exception import FileOperationError

from src.ElectricityBill import logging

# Create flask app 
application = Flask(__name__)
app=application

# Route for the homepage
@app.route('/') 
def index():
    return render_template('index.html')


# Route to train the pipeline 
@app.route('/train', methods=['GET'])
def train():
    os.system("python main.py")
    return render_template('train.html')

# Route to predict the pipeline
@app.route('/predict', methods=['GET','POST'])
def predict_data_point():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Initialize an empty dictionary to store the data 
            form_data = {}

            # Iterate over form fields and populate the dictionary 
            for field in [
                'Fan', 'Refrigerator', 'AirConditioner', 'Television',  'Monitor', 'MotorPump',  
                'Month',  'City', 'Company', 'MonthlyHours',  'TariffRate' ]:
                form_data[field] = request.form.get(field)

            # Create custom dta object using kwargs 
            custom_data = CustomData(**form_data)

            # Convert form data dictionary to a dataframe 
            pred_df = custom_data.get_data_as_dataframe()

            # Print the dataframe for debugging 
            print(pred_df)

            # Log message 
            logging.info(f"Form data before prediction: {form_data}")
            print('before prediction')

            # Initialize the prediction pipeline 
            prediction_pipeline = PredictionPipeline()

            # log message 
            logging.info(f"Form data mid prediction: {form_data}")
            print('Mid prediction')

            # Get the prediction 
            prediction = prediction_pipeline.make_predictions(pred_df)

            # Log message 
            logging.info(f"Form data after prediction: {form_data}")
            print('after prediction')

            # Return results 
            return render_template('home.html', prediction=prediction[0])
        
        except Exception as e:
            logging.exception(e)
            raise FileOperationError(e)
        

# Run the flask app 

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True)





            