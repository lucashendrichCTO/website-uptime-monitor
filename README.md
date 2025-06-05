# Website Uptime Monitor

A web application that monitors a website's uptime for 10 minutes and calculates the average uptime percentage.

## Features

- Input any website URL to monitor
- Real-time monitoring for 10 minutes
- Calculates uptime percentage
- Modern, responsive UI
- Progress bar showing monitoring status

## Requirements

- Python 3.7 or higher
- Flask
- Requests

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you're in the project directory
2. Run the Flask application:
```bash
python app.py
```
3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter a website URL in the input field (e.g., example.com)
2. Click "Start Monitoring"
3. Wait for 10 minutes while the application monitors the website
4. View the results showing the uptime percentage and other statistics

## Notes

- The application checks the website every 30 seconds
- A successful check is counted when the website returns a 200 status code
- The monitoring runs for exactly 10 minutes
- Results are displayed immediately after monitoring is complete 