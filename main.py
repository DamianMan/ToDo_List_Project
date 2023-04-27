from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
KEY = os.urandom(32)
app.secret_key = KEY

list_tasks_do = []
list_tasks_doing = []
list_tasks_done = []
wrong_task = False
wrong_task_done = False

@app.route("/",methods=["GET", "POST"])
def home():
    global list_tasks_do, wrong_task, wrong_task_done
    if request.method == "POST":
        text = (request.form.get('text'))
        text_doing = (request.form.get('text-doing'))
        text_done = (request.form.get('text-done'))


        if text != None:
            list_tasks_do.append(text.lower())

        if text_doing != None:
            if text_doing.lower() in list_tasks_do:
                list_tasks_doing.append(text_doing.lower())
                list_tasks_do.remove(text_doing.lower())

                wrong_task = False
            else:
                wrong_task = True
                redirect(url_for('home', wrong_task=wrong_task))

        if text_done != None:
            print(text_done)
            if text_done.lower() in list_tasks_doing:
                print('yes')
                print(list_tasks_done)
                list_tasks_done.append(text_done.lower())
                list_tasks_doing.remove(text_done.lower())
                wrong_task_done = False
            else:
                wrong_task_done = True

                redirect(url_for('home', wrong_task_done=wrong_task_done, wrong_task=wrong_task))





        return render_template("index.html", list_do=list_tasks_do,
                               list_doing=list_tasks_doing, list_done=list_tasks_done, wrong_task=wrong_task, wrong_task_done=wrong_task_done)
    return render_template("index.html", list_do=list_tasks_do, list_doing=list_tasks_doing, list_done=list_tasks_done, wrong_task=wrong_task, wrong_task_done=wrong_task_done)

@app.route("/delete/<task>", methods=["GET", "POST"])
def delete(task):
    print(task)
    list_tasks_do.remove(list_tasks_do[-1])
    print(list_tasks_do)
    return redirect(url_for('home', list_do=list_tasks_do))

@app.route("/delete_done")
def delete_done():
    global list_tasks_done, list_tasks_doing, list_tasks_do, wrong_task_done
    wrong_task_done = False
    list_tasks_done = []
    return redirect(url_for('home', list_done=list_tasks_done, list_doing=list_tasks_doing, list_do=list_tasks_do, wrong_task_done=wrong_task_done))

if "__main__" == __name__:
    app.run(debug=True)