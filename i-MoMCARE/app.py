from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "imomcare_secret_key"

DATABASE = "database.db"


# =========================
# DATABASE CONNECTION
# =========================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# HOME
# =========================

@app.route('/')
def home():
    return render_template('index.html')


# =========================
# REGISTER
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()

        try:

            cur.execute("""
            INSERT INTO users
            (name,email,password,role)
            VALUES(?,?,?,?)
            """,
            (name, email, hashed_password, role))

            conn.commit()

            flash("Registration Successful")

            return redirect('/login')

        except:
            flash("Email already exists")

        finally:
            conn.close()

    return render_template('register.html')


# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM users
        WHERE email=?
        """, (email,))

        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']

            return redirect('/dashboard')

        flash("Invalid Login Details")

    return render_template('login.html')


# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM mothers")
    mothers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM children")
    children = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointments")
    appointments = cur.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        mothers=mothers,
        children=children,
        appointments=appointments
    )


# =========================
# MOTHER PAGE
# =========================

@app.route('/mother')
def mother():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM mothers")
    mothers = cur.fetchall()

    conn.close()

    return render_template(
        'mother.html',
        mothers=mothers
    )


# =========================
# ADD MOTHER
# =========================

@app.route('/add_mother', methods=['POST'])
def add_mother():

    name = request.form['name']
    age = request.form['age']
    weight = request.form['weight']
    bp = request.form['bp']
    risk = request.form['risk']

    pregnancy_week = request.form.get('pregnancy_week')
    contact = request.form.get('contact')
    address = request.form.get('address')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO mothers
    (
    mother_name,
    age,
    weight,
    bp,
    risk_level,
    pregnancy_week,
    contact,
    address
    )
    VALUES(?,?,?,?,?,?,?,?)
    """,
    (
        name,
        age,
        weight,
        bp,
        risk,
        pregnancy_week,
        contact,
        address
    ))

    conn.commit()
    conn.close()

    return redirect('/mother')


# =========================
# CHILD PAGE
# =========================

@app.route('/child')
def child():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM children")
    children = cur.fetchall()

    conn.close()

    return render_template(
        'child.html',
        children=children
    )


# =========================
# ADD CHILD
# =========================

@app.route('/add_child', methods=['POST'])
def add_child():

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    weight = request.form['weight']
    height = request.form['height']
    vaccination = request.form['vaccination']

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO children
    (
    child_name,
    age,
    gender,
    weight,
    height,
    vaccination
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        name,
        age,
        gender,
        weight,
        height,
        vaccination
    ))

    conn.commit()
    conn.close()

    return redirect('/child')


# =========================
# APPOINTMENT PAGE
# =========================

@app.route('/appointment')
def appointment():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointments")
    appointments = cur.fetchall()

    conn.close()

    return render_template(
        'appointment.html',
        appointments=appointments
    )


# =========================
# ADD APPOINTMENT
# =========================

@app.route('/add_appointment', methods=['POST'])
def add_appointment():

    patient_name = request.form['patient_name']
    doctor_name = request.form['doctor_name']
    appointment_date = request.form['appointment_date']

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO appointments
    (
    patient_name,
    doctor_name,
    appointment_date
    )
    VALUES(?,?,?)
    """,
    (
        patient_name,
        doctor_name,
        appointment_date
    ))

    conn.commit()
    conn.close()

    return redirect('/appointment')


# =========================
# DOCTOR PAGE
# =========================

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')


# =========================
# RISK PREDICTION
# =========================
@app.route('/risk', methods=['GET', 'POST'])
def risk():

    result = None

    if request.method == 'POST':

        age = int(request.form['age'])

        height = float(request.form['height'])
        weight = float(request.form['weight'])

        height = height / 100
        bmi = weight / (height * height)

        pcos = request.form['pcos']
        thyroid = request.form['thyroid']
        diabetes = request.form['diabetes']
        bp = request.form['bp']
        hb = float(request.form['hb'])
        lifestyle = request.form['lifestyle']
        history = request.form['history']
        cycle = request.form['cycle']

        score = 0

        if age > 35:
            score += 1

        if bmi < 18.5 or bmi > 30:
            score += 1

        if pcos == "Yes":
            score += 1

        if thyroid == "Yes":
            score += 1

        if diabetes == "Yes":
            score += 1

        if bp == "High":
            score += 1

        if hb < 11:
            score += 1

        if lifestyle == "Yes":
            score += 1

        if history == "Yes":
            score += 1

        if cycle == "Irregular":
            score += 1

        if score <= 2:
            result = f"""
            🟢 Ready for Pregnancy

            BMI: {bmi:.2f}

            Your health indicators are generally suitable
            for planning a pregnancy.
            """

        elif score <= 5:
            result = f"""
            🟡 Need Medical Consultation Before Pregnancy

            BMI: {bmi:.2f}

            Some health factors require attention before
            planning a pregnancy.
            """

        else:
            result = f"""
            🔴 High Pre-Conception Risk

            BMI: {bmi:.2f}

            Please consult a gynecologist before planning
            pregnancy.
            """

    return render_template(
        'risk.html',
        result=result
    )
# =========================
# CHATBOT
# =========================

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    response = ""

    if request.method == "POST":

        msg = request.form['message'].lower()

        if "diet" in msg:
            response = "Eat iron-rich foods, fruits, vegetables, and drink plenty of water."

        elif "bp" in msg or "blood pressure" in msg:
            response = "Monitor BP regularly and consult your doctor if it remains high."

        elif "vaccination" in msg:
            response = "Follow the vaccination schedule recommended by your healthcare provider."

        elif "pregnancy" in msg:
            response = "Regular checkups, proper nutrition, and adequate rest are important during pregnancy."

        elif "fever" in msg:
            response = "If fever persists, contact a healthcare professional immediately."

        else:
            response = "Please consult your doctor for detailed medical advice."

    return render_template(
        'chatbot.html',
        response=response
    )
# =========================
# PROFILE
# =========================

@app.route('/profile')
def profile():

    if 'user_name' not in session:
        return redirect('/login')

    return render_template('profile.html')


# =========================
# ADMIN PANEL
# =========================

@app.route('/admin')
def admin():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        users=users
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == '__main__':
    app.run(debug=True)