from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import csv
import os
import pdfkit
from io import BytesIO
import platform

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Constants
USERNAME = 'admin'
PASSWORD = 'password123'
CSV_FILE = 'students_data.csv'

# wkhtmltopdf
if platform.system() == 'Windows':
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
else:
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  # Unix/Mac path

def load_students_from_csv():
    """Load students data from CSV file"""
    students_data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert subjects string back to dictionary
                subjects = eval(row['subjects'])
                student_id = int(row['id'])
                students_data[student_id] = {
                    "name": row['name'],
                    "grade": row['grade'],
                    "status": row['status'],
                    "subjects": subjects,
                    "contact": row['contact'],
                    "username": row['username'],
                    "password": row['password']
                }
    return students_data

def save_students_to_csv(students_data):
    """Save students data to CSV file"""
    fieldnames = ['id', 'name', 'grade', 'status', 'subjects', 'contact', 'username', 'password']
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for student_id, data in students_data.items():
            row = {
                'id': student_id,
                'name': data['name'],
                'grade': data['grade'],
                'status': data['status'],
                'subjects': str(data['subjects']),  # Convert dict to string
                'contact': data['contact'],
                'username': data['username'],
                'password': data['password']
            }
            writer.writerow(row)

# use default data if file doesn't exist
if os.path.exists(CSV_FILE):
    students_data = load_students_from_csv()
else:
    # Default data if no CSV exists
    students_data = {
        1: {
            "name": "John Doe",
            "grade": "A",
            "status": "Passed",
            "subjects": {
                "Math": 90,
                "Physics": 85,
                "Chemistry": 88,
                "Biology": 92,
                "English": 87,
            },
            "contact": "123-456-7890",
            "username": "john",
            "password": "john123",
        },
        2: {
            "name": "Jane Smith",
            "grade": "B",
            "status": "Passed",
            "subjects": {
                "Math": 78,
                "Physics": 80,
                "Chemistry": 75,
                "Biology": 83,
                "English": 89,
            },
            "contact": "234-567-8901",
            "username": "jane",
            "password": "jane123",
        },
    }
    save_students_to_csv(students_data)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('admin'))  # Redirect to admin page if login is successful
        elif next((s for s in students_data.values() if s['username'] == username and s['password'] == password), None):
            student = next((s for s in students_data.values() if s['username'] == username and s['password'] == password), None)
            if student:
                # If student is found, redirect to their individual page
                student_id = next(key for key, value in students_data.items() if value == student)
                return redirect(url_for('student', student_id=student_id))
        else:
            flash('Invalid username or password!', 'error')  
        
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', students=students_data)

@app.route('/student/<int:student_id>')
def student(student_id):
    # Fetch the student details using the student_id
    student_info = students_data.get(student_id)
    if student_info:
        return render_template('student.html', student=student_info, student_id=student_id)
    else:
        flash("Student not found!", "error")
        return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Generate a new student ID
        new_id = max(students_data.keys()) + 1

        # Get data from form
        name = request.form['name']
        grade = request.form['grade']
        status = request.form['status']
        subjects = {
            "Math": int(request.form['math']),
            "Physics": int(request.form['physics']),
            "Chemistry": int(request.form['chemistry']),
            "Biology": int(request.form['biology']),
            "English": int(request.form['english']),
        }
        contact = request.form['contact']
        username = request.form['username']
        password = request.form['password']

        # Add the new student to the data
        students_data[new_id] = {
            "name": name,
            "grade": grade,
            "status": status,
            "subjects": subjects,
            "contact": contact,
            "username": username,
            "password": password,
        }
        
        # Save to CSV after adding
        save_students_to_csv(students_data)

        flash("New student added successfully!", "success")
        return redirect(url_for('admin'))
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = students_data.get(student_id)
    if not student:
        flash("Student not found!", "error")
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['grade'] = request.form['grade']
        student['status'] = request.form['status']
        student['contact'] = request.form['contact']
        
        # Update subjects
        student['subjects'] = {
            "Math": int(request.form['math']),
            "Physics": int(request.form['physics']),
            "Chemistry": int(request.form['chemistry']),
            "Biology": int(request.form['biology']),
            "English": int(request.form['english'])
        }
        
        # Save to CSV after editing
        save_students_to_csv(students_data)
        
        flash("Student updated successfully!", "success")
        return redirect(url_for('admin'))
    
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if student_id in students_data:
        del students_data[student_id]
        # Save to CSV after deleting
        save_students_to_csv(students_data)
        flash("Student deleted successfully!", "success")
    else:
        flash("Student not found!", "error")
    
    return redirect(url_for('admin'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/download_report/<int:student_id>')
def download_report(student_id):
    student = students_data.get(student_id)
    if not student:
        flash("Student not found!", "error")
        return redirect(url_for('login'))
    
    # Create HTML content for the PDF
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: #333; text-align: center; }}
            .info {{ margin: 20px 0; }}
            .info p {{ margin: 10px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f5f5f5; }}
        </style>
    </head>
    <body>
        <h1>Student Report</h1>
        <div class="info">
            <p><strong>Name:</strong> {student['name']}</p>
            <p><strong>Grade:</strong> {student['grade']}</p>
            <p><strong>Status:</strong> {student['status']}</p>
            <p><strong>Contact:</strong> {student['contact']}</p>
        </div>
        <h2>Academic Performance</h2>
        <table>
            <tr>
                <th>Subject</th>
                <th>Marks</th>
            </tr>
            {''.join(f"<tr><td>{subject}</td><td>{marks}</td></tr>" for subject, marks in student['subjects'].items())}
        </table>
    </body>
    </html>
    """
    
    try:
        # Convert HTML to PDF using the configuration
        pdf = pdfkit.from_string(html_content, False, configuration=config)
        
        # Create response
        stream = BytesIO(pdf)
        stream.seek(0)
        
        return send_file(
            stream,
            download_name=f"student_report_{student['name']}.pdf",
            mimetype='application/pdf',
            as_attachment=True
        )
    except Exception as e:
        flash(f"Error generating PDF: {str(e)}", "error")
        return redirect(url_for('student', student_id=student_id))

if __name__ == '__main__':
    app.run(debug=True,port=8080)
