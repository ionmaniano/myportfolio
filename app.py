from flask import Flask, request, render_template
import sqlite3
from flask_mail import Mail, Message as MailMessage

# -------------------- Flask Setup --------------------
app = Flask(__name__)
app.secret_key = "bazenga"

# -------------------- Database Setup --------------------
def get_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
conn = get_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS contact_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL,
    Subject TEXT,
    Message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
cursor.close()
conn.close()

# -------------------- Email Setup --------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'odiwuorian@gmail.com'
app.config['MAIL_PASSWORD'] = 'xcvh igxl nwox cefm'
app.config['MAIL_DEFAULT_SENDER'] = 'odiwuorian@gmail.com'

mail = Mail(app)

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/project')
def project():
    return render_template('project.html')

# -------------------- CONTACT ROUTE (CLEAN) --------------------
@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Subject = request.form.get('Subject', 'No Subject')
        Message = request.form['Message']

        # ---- Save to SQLite ----
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contact_info (Name, Email, Subject, Message)
                VALUES (?, ?, ?, ?)
            """, (Name, Email, Subject, Message))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("DB Error:", e)

        # ---- Send Email ONLY ----
        try:
            msg = MailMessage(
                subject=f"New Contact Form: {Subject}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=['odiwuorian@gmail.com']
            )
            msg.body = f"""
From: {Name} <{Email}>

Subject: {Subject}

Message:
{Message}
"""
            mail.send(msg)
        except Exception as e:
            print("Email sending failed:", e)

        return render_template('contacts.html', message="Sent successfully")

    return render_template('contacts.html')


# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True, port=5050)