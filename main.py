from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import Column, Integer, String, Boolean
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# To create the database table
class Todo(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    date = Column(String(500), nullable=False)
    remove = Column(Boolean, nullable=False)

    def __repr__(self):
        rep = '<Task %r>' % self.id
        return rep


db.create_all()

now = datetime.now()
current_date = now.strftime("%d/%m/%Y %H:%M")


@app.route("/", methods=["POST", "GET"])
def start():
    if request.method == "POST":
        if request.form['content'] != '':
            task_content = request.form['content']
            new_task = Todo(content=task_content,
                            date=current_date,
                            remove=False)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an error while adding a task'
        else:
            tasks = Todo.query.all()
            return render_template("index.html", tasks=tasks)
    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)


@app.route("/remove/<int:id>")
def remove(id):
    task_to_cross = Todo.query.get_or_404(id)
    try:
        task_to_cross.remove = True
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an error while removing that task'

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an error while deleting that task'

@app.route("/return/<int:id>")
def return_to_list(id):
    task_to_return = Todo.query.get_or_404(id)
    try:
        task_to_return.remove = False
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an error while deleting that task'


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return 'There was an error while updating that task'
    else:
        return render_template("update.html", task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)
