from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
from email.mime.text import MIMEText

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
        (name,email,phone,course)
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

  #  msg['Subject'] = "New Course Enquiry"
   # msg['From'] = "techparkacademy.kkdi@gmail.com"
    #msg['To'] = "techparkacademy.kkdi@gmail.com"

   # server = smtplib.SMTP('smtp.gmail.com', 587)
   # server.starttls()

   # server.login(
   # "techparkacademy.kkdi@gmail.com",
   # "vain oeth nfqr fwfr"
   # )

   # server.send_message(msg)
   # server.quit()

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