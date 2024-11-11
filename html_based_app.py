from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime


app = Flask(__name__)
#tasks = []
tasks = {}

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assignee = request.form['assignee']
        status = request.form['status']
        tasks.append({'title': title, 'description': description, 'assignee': assignee, 'status': status})
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assignee = request.form['assignee']
        status = request.form['status']
        tasks[task_id] = {'title': title, 'description': description, 'assignee': assignee, 'status': status}
        return redirect(url_for('index'))
    task = tasks[task_id]
    return render_template('edit_task.html', task=task, task_id=task_id)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks.pop(task_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

