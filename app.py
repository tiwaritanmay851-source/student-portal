@app.route('/result', methods=['POST'])
def result():
    urn = request.form.get('urn')
    password = request.form.get('password')
    student = students.get(urn)

    if student and student['password'] == password:
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Provisional Result</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <style>
                body {{ background-color: #f8f9fa; }}
                .result-card {{ max-width: 1000px; margin: 30px auto; padding: 30px; background: #fff; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }}
                .college-header {{ text-align: center; margin-bottom: 20px; }}
                .college-header h2 {{ color: #b30000; margin: 5px 0; }}
                .footer-text {{ font-size: 0.9rem; color: #555; text-align:center; margin-top: 30px; }}
                .status-pass {{ color: green; font-weight: bold; }}
                .status-fail {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="result-card">
                    <div class="college-header">
                        <img src="/static/logo.png" alt="College Logo" style="height:100px;">
                        <h5>Sant Dnyaneshwar Shikshan Sanstha's</h5>
                        <h2>Annasaheb Dange College of Engineering & Technology, Ashta</h2>
                        <h6>Office of Controller of Examinations</h6>
                        <h5 class="mt-3">First Year Make-up Examination Provisional Result</h5>
                    </div>

                    <div class="mb-4">
                        <p><strong>URN No:</strong> {urn}</p>
                        <p><strong>Student Name:</strong> {student['name']}</p>
                        <p><strong>Examination:</strong> First Year B.Tech End Semester</p>
                    </div>

                    <table class="table table-bordered text-center">
                        <thead class="table-dark">
                            <tr>
                                <th>COURSE</th>
                                <th>COURSE CODE</th>
                                <th>ISE</th>
                                <th>MSE</th>
                                <th>LAB-ISE</th>
                                <th>TH-ESE</th>
                                <th>LAB-ESE</th>
                                <th>TOTAL</th>
                                <th>GRADE</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        status = "Pass"
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
                status = "Fail"

            html += f"""
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
            """

        html += f"""
                        </tbody>
                    </table>

                    <p><strong>CPI:</strong> --</p>
                    <p><strong>Result Status:</strong> <span class="{'status-pass' if status=='Pass' else 'status-fail'}">{status}</span></p>
                    <a href="/" class="btn btn-danger mt-3">Logout</a>

                    <div class="footer-text">
                        <p>© 2025 Examination Cell - Annasaheb Dange College of Engineering & Technology</p>
                        <p>Generated on: {__import__('datetime').datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    return "<h3>Invalid URN or Password</h3><a href='/'>Try Again</a>"
