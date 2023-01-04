from flask import Flask,redirect,url_for,render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return f'This is home page <h1>Hello</h1>'

@app.route("/<name>")
def user(name):
    return f"This is user page, Myself {name}"

@app.route("/admin1")
def admin():
    return redirect(url_for("user",name = 'Admin!!!'))

list1 = [1,2,3,4,5,6,7,8,9,10,12,324,42,325,342,42,34]
@app.route("/list")
def redering():
    return render_template("index.html",content =list1)

@app.route("/rederingboostrap=<name>")
def rederingboostrap_name(name):
    return render_template('home.html',content =name)

@app.route("/rederingboostrap")
def rederingboostrap_home():
    return render_template('base.html')



if __name__ == "__main__":
    app.run(debug=True)
