from flask import Flask, request, render_template
import sqlite3
from flask_mail import Mail, Message as MailMessage

# -------------------- APP SETUP --------------------
app = Flask(__name__)
app.secret_key = "bazenga"

# -------------------- DATABASE --------------------
def get_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB safely
with get_db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS contact_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL,
        Subject TEXT,
        Message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

# -------------------- EMAIL CONFIG --------------------
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='odiwuorian@gmail.com',
    MAIL_PASSWORD='xcvh igxl nwox cefm',
    MAIL_DEFAULT_SENDER='odiwuorian@gmail.com',
    MAIL_TIMEOUT=10
)

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

# -------------------- CONTACT (STABLE VERSION) --------------------
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Subject = request.form.get('Subject', 'No Subject')
        Message = request.form['Message']

        # -------- SAVE TO DB (SAFE) --------
        try:
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO contact_info (Name, Email, Subject, Message)
                    VALUES (?, ?, ?, ?)
                """, (Name, Email, Subject, Message))
        except Exception as e:
            print("DB Error:", e)

        # -------- EMAIL (NON-BLOCKING) --------
        try:
            msg = MailMessage(
                subject=f"Portfolio Contact: {Subject}",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=['odiwuorian@gmail.com']
            )

            msg.body = f"""
New Portfolio Message

Name: {Name}
Email: {Email}
Subject: {Subject}

Message:
{Message}
"""

            mail.send(msg)
            print("Email sent successfully")

        except Exception as e:
            print("Email failed (ignored):", e)

        # IMPORTANT: always respond fast (prevents Render timeout)
        return render_template('contacts.html', message="Message received successfully!")

    return render_template('contacts.html')

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True, port=5050)