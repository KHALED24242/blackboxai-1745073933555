# AI-Powered Inventory Monitoring Application

This application monitors inventory using AI and a camera feed. It tracks stock levels, generates reports, and provides a dashboard for insights.

## Features

- Connects to a camera to monitor inventory visually
- AI-powered product detection (placeholder implementation with randomized data)
- Tracks inventory and demand in a SQLite database
- Provides API endpoints for inventory and demand data (e.g., `/api/low_stock`, `/api/demand`)
- Generates daily, weekly, monthly, and yearly reports
- Sends notifications (console placeholder)
- Dashboard dynamically fetches and displays low stock and demand reports from the backend API

## Prerequisites

- Python 3.7 or higher
- OpenCV for Python
- Flask

## Installation

1. Clone the repository or download the project files.

2. Install required Python packages:

```bash
pip install opencv-python Flask
```

## Usage

1. Run the backend application:

```bash
python inventory_monitoring_app/main.py
```

This will start the camera monitoring, report scheduler, and a Flask web server (typically on `http://localhost:5000`). The Flask server provides API endpoints for the dashboard.

2. Open the dashboard:

Open the file `inventory_monitoring_app/dashboard.html` in a web browser. The dashboard will fetch data from the local Flask server to display inventory and demand reports. Ensure the backend application (`main.py`) is running for the dashboard to function correctly.

## Notes

- The AI product detection is a placeholder and returns randomized dummy data for demonstration.
- Demand tracking is based on initial sample data and is not dynamically updated by product detection or sales events in this version.
- The Flask web server runs on port 5000 and provides API endpoints:
    - `/api/low_stock`: Returns products with quantity less than 5.
    - `/api/demand`: Returns the top 3 most and least demanded products.
- You may need to grant camera permissions for the app to access the camera.
- Report notifications are printed to the console; you can extend this to email or other notification methods.
- The report scheduler currently generates daily reports every hour for demonstration purposes.

## Future Improvements

- Implement AI model for real product detection.
- Implement dynamic demand tracking based on sales or consumption events.
- Implement notification system (email, SMS, etc.).
- Add user authentication and settings.
- Enhance dashboard with more visualizations and interactive features.

## License

This project is provided as-is without warranty.
