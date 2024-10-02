from flask import Flask, request, render_template, jsonify, send_file
import pandas as pd
import joblib
import traceback
import os


# Initialize the Flask application
app = Flask(__name__)

# Load the saved pipeline from local storage
pipeline_path = 'models/randomforest_pipeline.pkl' 
try:
    loaded_pipeline = joblib.load(pipeline_path)
except Exception as e:
    print(f"Error loading pipeline from {pipeline_path}: {e}")
    traceback.print_exc()


# Route for single test form
@app.route('/single_test')
def single_test():
    # Render the template and pass the predictions data
    return render_template('single_test.html')

# Define the API endpoint for single predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the POST request
        data = request.get_json(force=True)
        
        # Convert the JSON data into a DataFrame
        input_df = pd.DataFrame([data])
        
        # Predict using the loaded pipeline
        prediction = loaded_pipeline.predict(input_df)
        
        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction[0]})
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/bulk_upload_test')
def bulk_upload_test():
    return render_template('bulk_upload_test.html')

# Define the API endpoint for bulk predictions using a CSV file
@app.route('/bulk_predict', methods=['POST'])
def bulk_predict():
    try:
        # Check if a file is part of the POST request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        # Check if the file has a valid filename
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read the CSV file into a DataFrame
        input_df = pd.read_csv(file)
        
        # Ensure the input DataFrame matches the expected format
        required_columns = ['Area', 'Item', 'average_rain_fall_mm_per_year', 'avg_temp']
        if not all(col in input_df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the input CSV'}), 400
        
        # Predict using the loaded pipeline
        predictions = loaded_pipeline.predict(input_df)
        
        # Add predictions to the DataFrame
        input_df['hg/ha_Predicted_yield'] = predictions
        
        # Save the resulting DataFrame with predictions to a new CSV file
        output_filename = 'predictions.csv'
        input_df.to_csv(output_filename, index=False)
        
        # Return the CSV file as a response
        return send_file(output_filename, mimetype='text/csv', as_attachment=True)
    
    except Exception as e:
        print(f"Error during bulk prediction: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# Route for rendering index.html
@app.route('/')
def index():
    return render_template('index.html')


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
