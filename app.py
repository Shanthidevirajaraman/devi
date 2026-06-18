from flask import Flask, render_template, request
from dotenv import load_dotenv
import sqlite3
import os
import requests


load_dotenv()

app = Flask(__name__)

# Brevo API Key
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

print("API KEY:", BREVO_API_KEY)

# Create table automatically
def init_db():
    conn = sqlite3.connect('academy.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS enquiries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        course TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/enquiry/<course>')
def enquiry(course):
    return render_template('enquiry.html', course=course)


@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']

    # Save to database
    conn = sqlite3.connect('academy.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO enquiries(name,email,phone,course) VALUES(?,?,?,?)",
        (name, email, phone, course)
    )

    conn.commit()
    conn.close()

    # Send Email using Brevo API
    try:

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        data = {
            "sender": {
                "name": "Tech Park Academy",
                "email": "techparkacademy.kkdi@gmail.com"
            },
            "to": [
                {
                    "email": "techparkacademy.kkdi@gmail.com"
                }
            ],
            "subject": "New Course Enquiry",
            "htmlContent": f"""
            <h2>New Enquiry</h2>

            <p><b>Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Phone:</b> {phone}</p>
            <p><b>Course:</b> {course}</p>
            """
        }

        response = requests.post(
            url,
            json=data,
            headers=headers,
            timeout=20
        )

        print("Brevo Response:", response.status_code)
        print(response.text)

    except Exception as e:
        print("Email Error:", e)

    return render_template("thankyou.html", name=name)


@app.route('/course/<course>')
def course(course):
    return render_template('course_details.html', course=course)


@app.route('/admin')
def admin():

    conn = sqlite3.connect('academy.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM enquiries")
    data = cur.fetchall()

    conn.close()

    return render_template('admin.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)