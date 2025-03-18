import pytest
from app import app, db

# Define valid input for prediction test
valid_input = {
    "salary_in_usd": 400000,
    "remote_ratio": 0,
    "company_location": "US",
    "job_title": "AI Architect",
    "work_year": 2025
}

# Define invalid neighborhood input for prediction test
invalid_job_input = {
    "salary_in_usd": 400000,
    "remote_ratio": 0,
    "company_location": "US",
    "job_title": "Invalid Job",
    "work_year": 2025
}

# Define missing field input for prediction test
missing_field_input = {
    "salary_in_usd": 400000,
    "remote_ratio": 0,
    "company_location": "US",
    "job_title": "AI Architect",
}


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_reload_data(client):
    """Test the reload endpoint that loads the data."""
    response = client.post('/reload')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'total_jobs' in json_data
    assert 'average_salary' in json_data

def test_predict_after_reload(client):
    """Test prediction endpoint after reloading the data."""
    # Reload the data first
    client.post('/reload')

    # Test valid prediction
    response = client.post('/predict', json=valid_input)
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'predicted_salary' in json_data


def test_invalid_neighbourhood(client):
    """Test prediction with an invalid neighbourhood."""
    # Reload the data first
    client.post('/reload')

    # Test invalid neighborhood
    response = client.post('/predict', json=invalid_job_input)
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Invalid job" in json_data['error']


def test_missing_fields(client):
    """Test prediction with missing fields."""
    # Reload the data first
    client.post('/reload')

    # Test with missing fields
    response = client.post('/predict', json=missing_field_input)
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Invalid numeric values for remote_ratio or salary_in_usd" in json_data['error']


