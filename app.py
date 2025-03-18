from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from flasgger import Swagger

app = Flask(__name__)

# Swagger config
app.config['SWAGGER'] = {
    'title': 'Data Job Salary Prediction API',
    'uiversion': 3
}
swagger = Swagger(app)

# SQLite DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salaries.db'
db = SQLAlchemy(app)

# Define a database model
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer, nullable=False)
    remote = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

def preprocess_data(df):
    # Drop rows where any of the key fields are NaN
    df = df.dropna(subset=['salary_in_usd', 'remote_ratio', 'work_year', 'company_location', 'job_title'])

    # Fill missing numerical values with the median
    df['salary_in_usd'] = df['salary_in_usd'].fillna(df['salary_in_usd'].median())

    # Fill missing categorical values (company_location) with the most frequent value
    df['company_location'] = df['company_location'].fillna(df['company_location'].mode()[0])

    # One-hot encode the 'job_title' column
    encoder = OneHotEncoder(sparse_output=False)
    jobs_encoded = encoder.fit_transform(df[['job_title']])
    
    # One-hot encode the 'company_location' column
    encoder2 = OneHotEncoder(sparse_output=False)
    location_encoded = encoder2.fit_transform(df[['company_location']])

    # Create a DataFrame for the one-hot encoded job titles and company locations
    jobs_encoded_df = pd.DataFrame(jobs_encoded, columns=encoder.get_feature_names_out(['job_title']))
    locations_encoded_df = pd.DataFrame(location_encoded, columns=encoder2.get_feature_names_out(['company_location']))

    # Concatenate the encoded job titles with the original dataframe and drop the 'job_title' column
    df = pd.concat([df, jobs_encoded_df, locations_encoded_df], axis=1).drop(columns=['job_title', 'company_location'])

    # Drop any rows that still have NaN values at this point
    df = df.dropna()
    return df, encoder, encoder2

# Global variables for model and encoder
model = None
encoder = None
encoder2 = None

@app.route('/reload', methods=['POST'])
def reload_data():
    '''
    Reload data from the Data Science Job dataset, clear the database, load new data, and return summary stats
    ---
    responses:
      200:
        description: Summary statistics of reloaded data
    '''
    global model, encoder, encoder2

    # Step 1: Download data
    #url = 'https://www.kaggle.com/datasets/saurabhbadole/latest-data-science-job-salaries-2024/data/DataScience_salaries_2025.csv'
    #response = requests.get(url)
    #csv_file = BytesIO(response.content)
    csv_file = '~/Downloads/DataScience_salaries_2025.csv'

    # Step 2: Load data into pandas
    jobs = pd.read_csv(csv_file)

    # Step 3: Clear the database
    db.session.query(Listing).delete()

    # Step 4: Process data and insert it into the database
    jobs = jobs[['salary_in_usd', 'remote_ratio', 'work_year', 'company_location', 'job_title']].dropna()

    for _, row in jobs.iterrows():
        new_job = Listing(
            salary = row['salary_in_usd'],
            remote = row['remote_ratio'],
            year =row['work_year'],  
            location = row['company_location'],  
            job = row['job_title'])
        
        db.session.add(new_job)
    db.session.commit()

    # Step 5: Preprocess and train model
    df, encoder, encoder2 = preprocess_data(jobs)
    X = df.drop(columns='salary_in_usd')
    y = df['salary_in_usd']
    model = LinearRegression()
    model.fit(X, y)

    # Step 6: Generate summary statistics
    summary = {
        'total_jobs': len(jobs),
        'average_salary': jobs['salary_in_usd'].mean(),
        'min_salary': jobs['salary_in_usd'].min(),
        'max_salary': jobs['salary_in_usd'].max(),
        'average_remote': jobs['remote_ratio'].mean(),
        'top_jobs': jobs['job_title'].value_counts().head().to_dict()
    }

    return jsonify(summary)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the salary for a data science job listing
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            job_title:
              type: string
            remote_ratio:
              type: number
            company_location:
              type: string
            work_year:
              type: integer
    responses:
      200:
        description: Predicted salary
    '''
    global model, encoder, encoder2  # Ensure that the encoder and model are available for prediction

    # Define the list of valid job titles
    valid_jobs = [
        "Research Scientist", "AI Engineer", "Data Analyst", "Associate", "Consultant", "Engineer",
        "Machine Learning Engineer", "Product Manager", "Software Engineer", "Research Scientist", "Research Engineer",
        "Systems Engineer", "Data Architect", "Data Governance", "Business Analyst", "AI Architect",
        "Architect", "BI Developer", "Business Intelligence Analyst", "Cloud Engineer", "Data Lead", "Research Associate",
        "Head of Data"
    ]

    # Check if the model and encoder are initialized
    if model is None or encoder is None or encoder2 is None:
        return jsonify({"error": "The data has not been loaded. Please refresh the data by calling the '/reload' endpoint first."}), 400

    data = request.json
    try:
        jobs = data.get('job_title')
        remote = pd.to_numeric(data.get('remote_ratio'), errors='coerce')
        year = data.get('work_year')
        location = data.get('company_location')

        if None in [jobs, remote, year, location]:
            return jsonify({"error": "Missing or invalid required parameters"}), 400

        # Check if the job title is valid
        if jobs not in valid_jobs:
            return jsonify({"error": f"Invalid job title. Please choose one of the following: {', '.join(valid_jobs)}"}), 400

        # Transform the input using the global encoder
        job_encoded = encoder.transform([[jobs]])
        location_encoded = encoder2.transform([[location]])
        input_data = np.concatenate(([remote, year], job_encoded[0], location_encoded[0]))
        input_data = input_data.reshape(1, -1)

        # Predict the salary
        predicted_salary = model.predict(input_data)[0]

        return jsonify({"predicted_salary": predicted_salary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
