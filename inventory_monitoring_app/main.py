import cv2
import sqlite3
import threading
import time
from datetime import datetime, timedelta

# Database setup
def init_db():
    conn = sqlite3.connect('inventory.db')
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
    conn.commit()
    conn.close()

# Placeholder for AI product detection from camera frame
def detect_products(frame):
    # TODO: Implement AI model to detect and count products
    # For now, return dummy data
    detected_products = {
        'product_a': 10,
        'product_b': 5,
        'product_c': 0
    }
    return detected_products

# Update inventory in database
def update_inventory(detected_products):
    conn = sqlite3.connect('inventory.db')
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
    conn = sqlite3.connect('inventory.db')
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
    # Start report scheduler in main thread
    schedule_reports()
