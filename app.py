from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (roll_no TEXT PRIMARY KEY, 
                  name TEXT, 
                  marks INTEGER)''')
    conn.close()
init_db()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        roll = request.form['roll_no']
        name = request.form['name']
        marks = request.form['marks']
        
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT OR REPLACE INTO students VALUES (?,?,?)", 
                    (roll, name, marks))
        conn.commit()
        conn.close()
        return redirect('/admin')
    return render_template('admin.html')

@app.route('/result', methods=['POST'])
def result():
    roll = request.form['roll_no']
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM students WHERE roll_no=?", (roll,))
    student = cursor.fetchone()
    conn.close()
    return render_template('result.html', student=student)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
