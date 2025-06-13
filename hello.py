from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Form(db.Model):
    email = db.Column(db.String(120), primary_key=True) 
    password = db.Column(db.String(10), unique=False)
    role = db.Column(db.String(100), default="")
    salary_per_annum = db.Column(db.Integer, default=0)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Form('{self.email}', '{self.password}')"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        salary = request.form.get('salary')
        role = request.form.get('role')

        existing_user = Form.query.filter_by(email=email).first()
        if not existing_user:
            entry = Form(email=email, password=password, role=role, salary_per_annum=int(salary))
            db.session.add(entry)
            db.session.commit()

    allinfo = Form.query.all()
    return render_template('index.html', allinfo=allinfo)

@app.route('/delete/<email>')
def delete(email):
    user = Form.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect('/')

@app.route('/update/<old_email>', methods=['POST'])
def update_user(old_email):
    user = Form.query.filter_by(email=old_email).first()
    if user:
        user.email = request.form['email']
        user.password = request.form['password']
        user.role = request.form['role']
        user.salary_per_annum = int(request.form['salary'])
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

