from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date
from datetime import datetime
import os



app = Flask(__name__)

def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app

app.secret_key = os.urandom(24)      
basedir = os.path.abspath(os.path.dirname(__file__))
app.SECRET_KEY = 'bace1b5adc790cfb9027f100ff9e1478'
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:''@localhost/taschedo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#class Personal_task(db.Model):
     #id = db.Column(db.Integer, primary_key=True)
     #title = db.Column(db.String(20))
     #task = db.Column(db.String(20))

class Personal_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    task = db.Column(db.String(100))
    description = db.Column(db.String(250))
    start_date = db.Column(Date, nullable=False, default=datetime.utcnow)
    deadline = db.Column(Date,nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __init__(self, title, task, description, start_date, deadline, complete):
        self.title = title
        self.task = task
        self.description = description
        self.start_date = start_date
        self.deadline = deadline
        self.complete = complete


@app.route("/")
def index():
    return render_template('index.html') 

@app.route('/personal')
def personal():
    tasks = Personal_task.query.all()
    return render_template('personal.html', tasks=tasks) 


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        title = request.form.get('title')
        task = request.form.get('task')
        description = request.form.get('description')
        start_date_string = request.form.get('start_date')
        deadline_string = request.form.get('deadline')
    
       # start_date_object = datetime.strptime(start_date_string, '%Y-%m-%d').date()
       # deadline_object = datetime.strptime(deadline_string, '%Y-%m-%d').date()
        
        if not title or not task or not start_date_string or not deadline_string:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add'))

        try:
            start_date = datetime.strptime(start_date_string, '%Y-%m-%d')
            deadline = datetime.strptime(deadline_string, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format!', 'danger')
            return redirect(url_for('add'))
        
        new_task = Personal_task(title=title, task=task, description=description, start_date=start_date, deadline=deadline, complete=False) 
        db.session.add(new_task)
        db.session.commit() 
        flash('Task added successfully!', 'success')
    return redirect(url_for('personal'))
    return render_template(add)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Personal_task.query.filter_by(id=id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('view'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Personal_task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view'))

@app.route('/work')
def work():
    return render_template('work.html') 

@app.route('/view', methods=['GET'])
def view():
    tasks = Personal_task.query.all()
    if tasks:
        return render_template('view.html', tasks=tasks)
    #return f"Your task list is empty"
    return render_template('personal.html', tasks=tasks) 

@app.route('/notify')
def notify():
    return render_template('notify.html') 

@app.route('/about')
def about():
    return render_template('about.html') 


if __name__=="__main__":
    # start the flask development server
    # Listen on all available interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

