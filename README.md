
# Job Salary Prediction API

This is a Flask-based API that predicts job salaries based on several factors like job type, company location, remote work, and work year. The API has two main endpoints:
- `/reload`: Reloads the data and trains the model.
- `/predict`: Predicts the salary for a given job.

## Data Source and Prediction Process

### Data Source

The data used for this project comes from [Kaggle](https://www.kaggle.com/datasets/saurabhbadole/latest-data-science-job-salaries-2024?resource=download&select=DataScience_salaries_2025.csv), which provides detailed information about data job listings in various countries.

The dataset includes important features such as:
- **Salary**: The salary of a data job listing in USD.
- **Company Location**: The country that the company is located in.
- **Remote Ratio**: The amount of work that is done remotely for the job.
- **Work Year**: The year that the job was posted.
- **Job Title**: The title of the particular job.

The full dataset can be accessed and downloaded from the Kaggle website at [Kaggle](https://www.kaggle.com/datasets/saurabhbadole/latest-data-science-job-salaries-2024?resource=download&select=DataScience_salaries_2025.csv).

### Prediction Process

The application makes use of a simple **Linear Regression Model** to predict the job salary of a data job listing based on various input features such as the company location, remote work, work year, and job type.

The process of prediction is as follows:
1. **Data Preprocessing**: The data is cleaned and processed. Non-numeric values are removed or converted, and categorical variables like `job type` are one-hot encoded to make them suitable for machine learning models.
2. **Model Training**: A linear regression model is trained on the cleaned dataset using features like company location, remote work, work year, and one-hot encoded job type.
3. **Prediction**: Once trained, the model can predict the job salary based on user input, such as the company location, remote work, work year, and job type.

By using this model, the app can provide quick salary predictions for job listings in the data field based on historical data.


## Prerequisites

Before you can set up and run this app, ensure you have the following software installed:

- **Python 3.9+**
- **pip** (Python package installer)
- **Virtualenv** (Optional but recommended)

## Setting up on macOS and Windows

### 1. Clone the Repository
First, clone this repository to your local machine:
```bash
git clone https://github.com/jbrown2002/jobs.git
cd jobs
```
### 2. 
Second, download the data to your local device using this code:

```bash
pip install kaggle
kaggle datasets download -d saurabhbadole/latest-data-science-job-salaries-2024
```

### 3. 
Lastly, unzip the data file on your local device and read it into the API using this code:

```bash
unzip latest-data-science-job-salaries-2024.zip
```

### 4. Create a Virtual Environment (Optional but Recommended)

You can create a virtual environment to isolate the project dependencies.

For macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 5. Install the Dependencies

Install the required Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 6. Set Up Environment Variables

Flask requires some environment variables to run the app correctly. Create a `.env` file in the project root with the following content:

```bash
FLASK_APP=app.py
FLASK_ENV=development
```

For macOS, you can set the environment variables using the following commands:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

For Windows, you can set the environment variables using the following commands in PowerShell:

```bash
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
```

### 7. Initialize the SQLite Database

To set up the SQLite database for the first time, run:

```bash
flask shell
```

Inside the shell, run:
```python
from app import db
db.create_all()
exit()
```

### 8. Running the Application

Once everything is set up, you can run the application with the following command:

```bash
flask run
```

By default, the app will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 9. Swagger Documentation

You can access the Swagger documentation for the API at:

```
http://127.0.0.1:5000/apidocs/
```

### 10. Testing the Endpoints

#### Reload Data

To reload the data and train the model, use the `/reload` endpoint:

```bash
curl -X POST http://127.0.0.1:5000/reload
```

#### Predict Price

To predict a rental price, you can use the `/predict` endpoint. Here's an example request:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "remote_ratio": 0,
    "company_location": "US",
    "job_title": "AI Architect",
    "work_year": 2025
}'
```

### 11. Stopping the Application

To stop the Flask app, you can press `Ctrl + C` in the terminal window where the app is running.

---

## Troubleshooting

### Common Issues

- **Environment variables not being set**: Ensure you have set the environment variables correctly, especially when switching between macOS and Windows.

- **Database initialization issues**: If the app crashes because of database-related errors, make sure you have run the `flask shell` commands to initialize the database properly.

- **Dependency issues**: Ensure that you are using the correct version of Python (3.9+) and have installed the dependencies using `pip install -r requirements.txt`.

---

## License

This project is licensed under the MIT License.

## Running Tests

We use `pytest` for running tests on this application. Before running the tests, ensure all dependencies are installed and the application is properly set up.

### Setting up for Testing

1. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

2. Export the `PYTHONPATH` environment variable to ensure Python can locate the app module.

For macOS/Linux:
```bash
export PYTHONPATH=.
```

For Windows (PowerShell):
```bash
$env:PYTHONPATH="."
pytest
```

3. Run the tests:

```bash
pytest
```

This will execute all the tests located in the `tests/` folder and provide feedback on the application behavior.

## Deploying to Heroku

### 1. Install the Heroku CLI

Before deploying the application to Heroku, you need to install the Heroku CLI. You can follow the steps below to install it on your machine.

#### macOS:

You can install the Heroku CLI using Homebrew:
```bash
brew tap heroku/brew && brew install heroku
```

#### Windows:

Download and run the Heroku installer from the [Heroku Dev Center](https://devcenter.heroku.com/articles/heroku-cli).

#### Verify Installation:

Once installed, verify the installation by running:

```bash
heroku --version
```

You should see the version of Heroku CLI installed.

### 2. Log in to Heroku

Log in to your Heroku account from the terminal:

```bash
heroku login
```

This will open a web browser for you to log in to your Heroku account.

### 3. Prepare the App for Deployment

Ensure your `requirements.txt` and `Procfile` are present in the project root.

- **Procfile**: Create a `Procfile` in the root directory with the following content to tell Heroku how to run the app:

```bash
web: flask run --host=0.0.0.0 --port=$PORT
```

### 4. Create a Heroku App

Run the following command to create a new Heroku app:

```bash
heroku create
```

### 5. Deploy to Heroku

After you've created your Heroku app, deploy your app using Git:

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

### 6. Scale the Application

Heroku apps require at least one running dyno. Scale your app to run one web dyno:

```bash
heroku ps:scale web=1
```

### 7. Open the App

Once your app is deployed, you can open it in the browser using:

```bash
heroku open
```

Your app should now be live on Heroku!

