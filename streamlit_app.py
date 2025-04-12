import streamlit as st
import requests
import plotly.express as px



if "prediction_history" not in st.session_state:
    st.session_state["prediction_history"] = []

FLASK_API_URL_RELOAD = "http://127.0.0.1:5000/reload"

# Button to reload the data
if st.button("Reload Data"):
    response = requests.post(FLASK_API_URL_RELOAD)
    if response.status_code == 200:
        st.success("Data reloaded successfully!")
        st.write(response.json())  # Optionally display the summary statistics
    else:
        st.error(f"Failed to reload data: {response.status_code}")
        

# API URL of your Flask backend
FLASK_API_URL = "http://127.0.0.1:5000/predict"

# List of valid job titles (same as in your Flask API)
valid_jobs = [
    "Research Scientist", "AI Engineer", "Data Analyst", "Associate", "Consultant", "Engineer",
    "Machine Learning Engineer", "Product Manager", "Software Engineer", "Research Engineer",
    "Systems Engineer", "Data Architect", "Data Governance", "Business Analyst", "AI Architect",
    "Architect", "BI Developer", "Business Intelligence Analyst", "Cloud Engineer", "Data Lead", "Research Associate",
    "Head of Data"
]

# Function to call the Flask API and get predictions
def get_salary_prediction(job_title, remote_ratio, location, work_year):
    data = {
        "job_title": job_title,
        "remote_ratio": remote_ratio,
        "company_location": location,
        "work_year": work_year
    }

    try:
        response = requests.post(FLASK_API_URL, json=data)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        return response.json()  # Return the response as a dictionary
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Streamlit app interface 
valid_jobs = [
    "Research Scientist", "AI Engineer", "Data Analyst", "Associate", "Consultant", "Engineer",
    "Machine Learning Engineer", "Product Manager", "Software Engineer", "Research Engineer",
    "Systems Engineer", "Data Architect", "Data Governance", "Business Analyst", "AI Architect",
    "Architect", "BI Developer", "Business Intelligence Analyst", "Cloud Engineer", "Data Lead", "Research Associate",
    "Head of Data"
]

valid_locations = [
    "US", "CA", "GB", "AU", "DE"
]

# Inputs for job title, location, work year, and remote ratio
job_titles = st.multiselect("Select Job Titles", valid_jobs, default=valid_jobs)  # Multiple job titles
location = st.selectbox("Enter Company Location", valid_locations)
work_year = st.number_input("Enter Work Year", min_value=2020, max_value=2025, value=2022)
remote_ratio = st.slider("Select Remote Work Ratio", min_value=0, max_value=100, value=50, step=10)

# Button to trigger salary prediction
if st.button("Generate Job Title vs Predicted Salary Chart"):
    if not location:
        st.error("Location is required!")
    elif not job_titles:
        st.error("Please select at least one job title!")
    else:
        job_titles_list = job_titles
        predicted_salaries = []

        # Loop through selected job titles to fetch predictions for each
        with st.spinner("Fetching predictions..."):
            for job_title in job_titles_list:
                result = get_salary_prediction(job_title, remote_ratio, location, work_year)
                if "predicted_salary" in result:
                    predicted_salaries.append(result["predicted_salary"])
                else:
                    predicted_salaries.append(None)  # Append None in case of an error or missing prediction

        # Plotting the results
        fig = px.bar(
            x=job_titles_list,
            y=predicted_salaries,
            labels={"x": "Job Title", "y": "Predicted Salary ($)"},
            title=f"📊 Predicted Salary for Selected Job Titles in {location} ({work_year}) with {remote_ratio}% Remote Work"
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
            
