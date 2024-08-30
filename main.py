from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
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
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:''@localhost/taschedo"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
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
        
#with app.app_context():
    #create all tables
    #db.create_all()


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

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # Check if the method was intended to be DELETE
    if request.form.get('_method') == 'DELETE':
        task = Personal_task.query.filter_by(id=id).first()
        if task is None:
            return jsonify({'success': False, 'message': 'Task not found!'}), 404

        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Task successfully deleted!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'An error occurred while deleting the task.'}), 500
    else:
        return jsonify({'success': False, 'message': 'Invalid method.'}), 405




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

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
     # Fetch the task based on the id for both GET and POST requests
    task = Personal_task.query.get(id)
    
    if task is None:
        # Handle case where task is not found (optional)
        flash("Task not found")
        return redirect(url_for('view'))
    
    if request.method == "POST":
        task = Personal_task.query.get(request.form.get('id'))
        
        task.title = request.form['title']
        task.task = request.form['task']
        task.description = request.form['description']
        task.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        task.deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()
        
        db.session.commit()
        flash("task successfully updated")
        return redirect(url_for('view'))
    
    task = Personal_task.query.filter_by(id=id).first()  
    return render_template('personal.html', task=task) 

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

