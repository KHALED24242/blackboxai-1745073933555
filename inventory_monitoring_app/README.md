# AI-Powered Inventory Monitoring Application

This application monitors inventory using AI and a camera feed. It tracks stock levels, generates reports, and provides a dashboard for insights.

## Features

- Connects to a camera to monitor inventory visually
- AI-powered product detection (placeholder implementation)
- Tracks inventory and demand in a SQLite database
- Generates daily, weekly, monthly, and yearly reports
- Sends notifications (console placeholder)
- Dashboard to view low stock and demand reports

## Prerequisites

- Python 3.7 or higher
- OpenCV for Python

## Installation

1. Clone the repository or download the project files.

2. Install required Python packages:

```bash
pip install opencv-python
```

## Usage

1. Run the backend application:

```bash
python inventory_monitoring_app/main.py
```

This will start the camera monitoring and report scheduler.

2. Open the dashboard:

Open the file `inventory_monitoring_app/dashboard.html` in a web browser to view the inventory reports.

## Notes

- The AI product detection is currently a placeholder and returns dummy data.
- You may need to grant camera permissions for the app to access the camera.
- Report notifications are printed to the console; you can extend this to email or other notification methods.
- The report scheduler currently generates daily reports every hour for demonstration purposes.

## Future Improvements

- Implement AI model for real product detection.
- Add real-time data updates to the dashboard via API.
- Implement notification system (email, SMS, etc.).
- Add user authentication and settings.

## License

This project is provided as-is without warranty.
