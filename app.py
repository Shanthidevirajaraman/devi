from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


app = Flask(__name__)

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

    conn = sqlite3.connect('academy.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO enquiries(name,email,phone,course) VALUES(?,?,?,?)",
        (name, email, phone, course)
    )

    conn.commit()
    conn.close()

    msg = MIMEText(f"""


    New Enquiry

    Name: {name}
    Email: {email}
    Phone: {phone}
    Course: {course}
    """)


    msg['Subject'] = "New Course Enquiry"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=20)
        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        server.send_message(msg)
        server.quit()

        print("Email sent successfully")

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