import cv2
import sqlite3
import threading
import time
import random # Added import
from datetime import datetime, timedelta
from flask import Flask, jsonify

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            quantity INTEGER,
            last_updated TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS demand (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            demand_count INTEGER,
            last_updated TIMESTAMP
        )
    ''')
    init_demand_data(conn)
    conn.commit()
    conn.close()

def init_demand_data(conn):
    """Populates the demand table with sample data if it's empty."""
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM demand")
    if c.fetchone()[0] == 0:
        # Using product names consistent with detect_products output
        sample_demand_data = [
            ('product_a', 100), ('product_b', 20), ('product_c', 150), 
            ('product_d_sample', 75), ('product_e_sample', 30) # Adding some other products for demand
        ]
        now = datetime.now()
        for name, count in sample_demand_data:
            # Ensure products exist in inventory before adding to demand, or handle appropriately
            # For now, we assume product_a, product_b, product_c might come from detection
            # and product_d_sample, product_e_sample are just for demand table demonstration
            c.execute("INSERT OR IGNORE INTO inventory (product_name, quantity, last_updated) VALUES (?, ?, ?)", (name, 0, now))
            c.execute("INSERT INTO demand (product_name, demand_count, last_updated) VALUES (?, ?, ?)", (name, count, now))
    conn.commit()

# API Endpoints
@app.route('/api/low_stock', methods=['GET'])
def get_low_stock():
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT product_name, quantity FROM inventory WHERE quantity < 5")
    low_stock_products = [{"product_name": row[0], "quantity": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(low_stock_products)

@app.route('/api/demand', methods=['GET'])
def get_demand():
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    c = conn.cursor()

    # Most demanded
    c.execute("SELECT product_name, demand_count FROM demand ORDER BY demand_count DESC LIMIT 3")
    most_demanded = [{"product_name": row[0], "demand_count": row[1]} for row in c.fetchall()]

    # Least demanded
    c.execute("SELECT product_name, demand_count FROM demand ORDER BY demand_count ASC LIMIT 3")
    least_demanded = [{"product_name": row[0], "demand_count": row[1]} for row in c.fetchall()]

    conn.close()
    return jsonify({"most_demanded": most_demanded, "least_demanded": least_demanded})

# Placeholder for AI product detection from camera frame
def detect_products(frame):
    # TODO: Implement AI model to detect and count products
    # For now, return dummy data with some randomness
    detected_products = {
        'product_a': random.randint(0, 15), # Fluctuates around threshold
        'product_b': random.randint(1, 7),  # Often near or below threshold
        'product_c': random.randint(0, 4)   # Usually low stock
    }
    # 'product_d_sample' and 'product_e_sample' from init_demand_data
    # are not updated here, so their stock will remain as initialized (likely 0).
    return detected_products

# Update inventory in database
def update_inventory(detected_products):
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    c = conn.cursor()
    for product, quantity in detected_products.items():
        c.execute('SELECT id FROM inventory WHERE product_name = ?', (product,))
        row = c.fetchone()
        now = datetime.now()
        if row:
            c.execute('''
                UPDATE inventory SET quantity = ?, last_updated = ? WHERE product_name = ?
            ''', (quantity, now, product))
        else:
            c.execute('''
                INSERT INTO inventory (product_name, quantity, last_updated) VALUES (?, ?, ?)
            ''', (product, quantity, now))
    conn.commit()
    conn.close()

# Camera monitoring thread
def camera_monitor():
    cap = cv2.VideoCapture(0)  # Use default camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        detected_products = detect_products(frame)
        update_inventory(detected_products)
        time.sleep(10)  # Wait 10 seconds before next capture
    cap.release()

# Report generation (daily, weekly, monthly, yearly)
def generate_report(period='daily'):
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    c = conn.cursor()
    now = datetime.now()
    if period == 'daily':
        since = now - timedelta(days=1)
    elif period == 'weekly':
        since = now - timedelta(weeks=1)
    elif period == 'monthly':
        since = now - timedelta(days=30)
    elif period == 'yearly':
        since = now - timedelta(days=365)
    else:
        since = now - timedelta(days=1)

    c.execute('''
        SELECT product_name, quantity FROM inventory WHERE last_updated >= ?
    ''', (since,))
    rows = c.fetchall()
    conn.close()

    low_stock = [row for row in rows if row[1] < 5]  # Threshold for low stock is 5
    report = f"Inventory Report ({period.capitalize()}) - {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "Low stock products:\n"
    for product, qty in low_stock:
        report += f"- {product}: {qty}\n"
    return report

# Notification placeholder
def send_notification(message):
    # TODO: Implement notification (email, SMS, etc.)
    print("Notification:")
    print(message)

# Scheduler for reports
def schedule_reports():
    while True:
        now = datetime.now()
        # For demo, generate daily report every minute
        if now.minute == 0:  # At the start of every hour for demo
            report = generate_report('daily')
            send_notification(report)
        time.sleep(60)

if __name__ == '__main__':
    init_db()
    # Start camera monitoring in a separate thread
    camera_thread = threading.Thread(target=camera_monitor, daemon=True)
    camera_thread.start()

    # Start Flask app in a new thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()

    # Start report scheduler in main thread (or as a daemon thread)
    # For graceful shutdown, it might be better to manage threads more explicitly
    # but for this task, daemon=True for Flask thread is fine.
    # The schedule_reports itself is a blocking loop, so it runs in the main thread.
    print("Starting Flask server on port 5000...")
    print("Starting camera monitor and report scheduler...")
    schedule_reports()
