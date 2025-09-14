from flask import Flask, request, send_from_directory

app = Flask(__name__)

# =====================
# STEP 1: Student Data
# =====================
students = {
    "1024071001": {"password": "ADCET@123", "name": "VAIDYA AACHAL RAJESH", "marks": {}},
    "1024071003": {"password": "ADCET@123", "name": "KUMARMATH SHREYA PRAMOD", "marks": {}},
    "1024071004": {"password": "ADCET@123", "name": "JADHAV ANUSHKA RAJENDRA", "marks": {}},
    "1024071005": {"password": "ADCET@123", "name": "TALGHARKAR FARHAN IMTIYAZ", "marks": {}},
    "1024071006": {"password": "ADCET@123", "name": "FADATARE POOJA ANIL", "marks": {}},
    "1024071007": {"password": "ADCET@123", "name": "NAME VINIT DEEPAK", "marks": {}},
    "1024071008": {"password": "ADCET@123", "name": "YEOLE VEDANT GIRISH", "marks": {}},
    "1024071009": {"password": "ADCET@123", "name": "DANDEKAR CHIRAG RAMESH", "marks": {}},
    "1024071010": {"password": "ADCET@123", "name": "GUPTA SONU NANDLAL", "marks": {}},
    "1024071011": {"password": "ADCET@123", "name": "TIWARI TANMAY VIJAY", "marks": {}},
    # (continue with rest of students + marks dictionary we prepared earlier)
}

# =====================
# STEP 2: Static route (for logo)
# =====================
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# =====================
# STEP 3: Login Page
# =====================
@app.route('/', methods=['GET'])
def login_form():
    return '''
    <html>
    <head>
        <title>Student Login</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            .login-box { width: 350px; margin: auto; border: 1px solid #ccc; padding: 30px; border-radius: 10px; }
            input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
            button { padding: 10px 20px; background-color: #0066cc; color: white; border: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <img src="/static/logo.png" alt="College Logo" style="height:100px;">
        <h3>Sant Dnyaneshwar Shikshan Sanstha's</h3>
        <h2 style="color:#b30000;">Annasaheb Dange College of Engineering and Technology</h2>
        <div class="login-box">
            <h2>Sign In</h2>
            <form action="/result" method="post">
                <input type="text" name="urn" placeholder="User Name" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <button type="submit">Show Result</button>
            </form>
        </div>
    </body>
    </html>
    '''

# =====================
# STEP 4: Result Page
# =====================
@app.route('/result', methods=['POST'])
def result():
    urn = request.form.get('urn')
    password = request.form.get('password')
    student = students.get(urn)

    if student and student['password'] == password:
        html = f'''
        <div style="max-width: 900px; margin: auto; font-family: Arial, sans-serif; border: 1px solid #ccc; padding: 20px;">
            <img src="/static/logo.png" alt="College Logo" style="display:block; margin:auto; height:100px;"><br/>
            <h3 style="text-align:center; margin-bottom: 0;">Sant Dnyaneshwar Shikshan Sanstha's</h3>
            <h2 style="text-align:center; margin-top: 5px;">Annasaheb Dange College of Engineering & Technology, Ashta</h2>
            <h4 style="text-align:center;">Office of Controller of Examinations</h4>
            <h4 style="text-align:center;">First Year Make-up Examination Provisional Result</h4>

            <p><strong>URN No:</strong> {urn}<br/>
            <strong>Student Name:</strong> {student['name']}<br/>
            <strong>Examination:</strong> First Year B.Tech End Semester</p>

            <table border="1" width="100%" style="border-collapse: collapse; text-align:center;">
                <tr style="background-color:#f2f2f2;">
                    <th>COURSE</th>
                    <th>COURSE CODE</th>
                    <th>ISE</th>
                    <th>MSE</th>
                    <th>LAB-ISE</th>
                    <th>TH-ESE/LAB ESE</th>
                    <th>LAB-ESE</th>
                    <th>TOTAL MARKS</th>
                    <th>GRADE</th>
                </tr>
        '''
        for subject, details in student['marks'].items():
            ise = details.get("ise", 0)
            mse = details.get("mse", 0)
            lab_ise = details.get("lab_ise", 0)
            ese = details.get("ese", 0)
            lab_ese = details.get("lab_ese", 0)

            total = ise + mse + lab_ise + ese + lab_ese

            if total >= 50:
                grade = "CD"
            elif total >= 40:
                grade = "DD"
            else:
                grade = "FF"

            html += f'''
                <tr>
                    <td>{subject}</td>
                    <td>{details.get("course_code", "-")}</td>
                    <td>{ise if ise > 0 else "-"}</td>
                    <td>{mse if mse > 0 else "-"}</td>
                    <td>{lab_ise if lab_ise > 0 else "-"}</td>
                    <td>{ese if ese > 0 else "-"}</td>
                    <td>{lab_ese if lab_ese > 0 else "-"}</td>
                    <td>{total}</td>
                    <td>{grade}</td>
                </tr>
            '''

        html += '''
            </table>
            <p><strong>CPI:</strong> -- &nbsp;&nbsp;&nbsp; <strong>Result Status:</strong> Provisional</p>
            <br/><a href="/">Logout</a>
        </div>
        '''
        return html

    return "<h3>Invalid URN or Password</h3><a href='/'>Try Again</a>"

# =====================
# STEP 5: Run app (Render/Cloud hosting compatible)
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
