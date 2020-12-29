from datetime import datetime

#import sqlalchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


#from config import DevConfig

app = Flask(__name__)
#engine = create_engine('sqlite:///:memory:', echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem'

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task_to_edit = todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There waas a problem'
    else:
        return render_template('edit.html', task=task_to_edit)




if __name__ == '__main__':
    app.run(debug=True)
