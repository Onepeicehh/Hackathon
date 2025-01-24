@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form[username]
        password=request.form[password]
    if username == "admin" and password == "password":
        return "login sucsessful"
    else:
        return "invalid username or password"
    return
*/

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Secret key for session management (needed for flashing messages)
app.secret_key = 'your_secret_key'

# Dummy student login credentials
students_data = {
    1: {"name": "John Doe", "grade": "A", "status": "Passed", "subjects": ["Math", "Science", "History"], "contact": "123-456-7890", "username": "john", "password": "john123"},
    2: {"name": "Jane Smith", "grade": "B", "status": "Passed", "subjects": ["English", "Biology"], "contact": "234-567-8901", "username": "jane", "password": "jane123"},
    3: {"name": "Sam Brown", "grade": "C", "status": "Failed", "subjects": ["Chemistry", "Math"], "contact": "345-678-9012", "username": "sam", "password": "sam123"},
    4: {"name": "Emily Davis", "grade": "A", "status": "Passed", "subjects": ["Physics", "Art"], "contact": "456-789-0123", "username": "emily", "password": "emily123"},
}

@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find student by username
        student = next((s for s in students_data.values() if s['username'] == username and s['password'] == password), None)
        
        if student:
            # If student is found, redirect to their individual page
            student_id = next(key for key, value in students_data.items() if value == student)
            return redirect(url_for('student', student_id=student_id))
        else:
            flash('Invalid username or password!', 'error')  # Show error message
        
    return render_template('login.html')

@app.route('/student/<int:student_id>')
def student(student_id):
    # Fetch the student details using the student_id
    student_info = students_data.get(student_id)
    if student_info:
        return render_template('student.html', student=student_info)
    else:
        flash("Student not found!", "error")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
