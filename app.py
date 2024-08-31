from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__,template_folder = 'templates' )


todos=[]

try:
    f = open('tasks.dat','rb')
    while True:
        a = pickle.load(f)
        todos.append(a)
    f.close()
except:
    pass


@app.route("/")

def index():
    return render_template("index2.html",todos = todos)

@app.route("/add",methods = ["POST"])
def add():
    todo = request.form['todo']
    todos.append({'task':todo, 'done': False})
    f = open('tasks.dat','ab')
    pickle.dump({'task':todo, 'done': False},f)
    f.close()
    return redirect(url_for('index'))


@app.route("/edit/<int:index>",methods = ["GET","POST"])
def edit(index):
    todo = todos[index]
    if request.method == 'POST':
        todo['task']= request.form["todo"]
        f = open("tasks.dat",'wb')
        for i in todos:
            pickle.dump(i,f)
        f.close()

        return redirect(url_for('index'))
    else:
        return render_template("edit.html",todo = todo, index = index)
    
@app.route("/check/<int:index>")
def check(index):
    todos[index]['done']= not todos[index]['done']
    f = open("tasks.dat",'wb')
    for i in todos:
        pickle.dump(i,f)
    f.close()

    return redirect(url_for('index'))

@app.route("/delete/<int:index>")
def delete(index):
    f = open("tasks.dat",'wb')
    del todos[index]
    for i in todos:
        pickle.dump(i,f)
    f.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug = True)
