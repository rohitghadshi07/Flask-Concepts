from flask import Flask, redirect,url_for,render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Secret key is required for the session
app.secret_key = 'mykey'
#SET a session time 
app.permanent_session_lifetime = timedelta(minutes= 5)
#config DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3' # user is the table name
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column('id',db.Integer,primary_key =True)
    name = db.Column('name',db.String(100))
    email = db.Column('email',db.String(100))

    def __init__(self,name,email) -> None:
        super().__init__()
        self.name = name
        self.email = email

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login",methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        session.permanent = True #session started
        myVar = request.form['nam'] #pick the name from form 
        session['usr'] = myVar # stored values in session
        found_user = User.query.filter_by(name = myVar).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = User(myVar,"")
            db.session.add(usr) # if user doesnot exist we are adding 
            db.session.commit()
        flash('Login successfully!')
        return redirect(url_for("user")) 
    else:
        if "usr" in session: # check the value in session
            flash('User is already Logged In!')
            return redirect(url_for("user"))
        else:
            flash('User is not logged in Yet!')
            return render_template("login.html")





@app.route("/user",methods = ['POST','GET'])
def user():
    if request.method == 'GET':
        if "usr" in session:# check the value in session
            myuservar = session['usr'] # get the value from session 
            flash('User is already Logged In! Fill the below detials!')
            return render_template('userdetails.html',name =myuservar)
    else:
        if request.form.get('action2') == 'add':
            email = request.form['email']
            session['email'] = email
            if "usr" in session:
                myuservar = session['usr']
                found_user = User.query.filter_by(name = myuservar).first()
                found_user.email = email
                db.session.commit()          
                flash('Email were saved')
                return redirect(url_for('userdetails',email=email,user=myuservar))
        
        if request.form.get('action1') == 'view':
            session.pop("usr",None) # remove all session data
            session.pop("email",None) # remove all session data            
            return redirect(url_for('view'))

        
        if request.form.get('action3') == 'delete':
            if "usr" in session:
                myuservar = session['usr']
                found_user = User.query.filter(User.name == myuservar).delete()
                db.session.commit()
                session.pop("usr",None) # remove all session data
                session.pop("email",None) # remove all session data
                flash('user is deleted')
                return redirect(url_for('view'))

        if request.form.get('action4') == 'deleteall':
            found_user = User.query.delete()
            db.session.commit()
            session.pop("usr",None) # remove all session data
            session.pop("email",None) # remove all session data
            flash('All users are deleted')
            return redirect(url_for('view'))

            
    

@app.route('/userdetails',methods = ['POST','GET'])
def userdetails():
    if request.method == 'GET':
        if ("usr" in session) and ("email" in session):
            myuservar = session['usr']
            email =session['email']
            return render_template('logout.html',user=myuservar,email=email)
    if request.form.get('action1') == 'view':
        session.pop("usr",None) # remove all session data
        session.pop("email",None) # remove all session data            
        return redirect(url_for('view'))        
    if request.form.get('action2') == 'logout':
        session.pop("usr",None) # remove all session data
        session.pop("email",None) # remove all session data
        flash('User is logged out successfully!')
        return redirect(url_for("login"))



@app.route('/view')
def view():
    return render_template('view.html',values = User.query.all())


@app.route("/logout")
def logout():
    session.pop("usr",None) # remove all session data
    session.pop("email",None)
    flash('User is logged out successfully!')
    return redirect(url_for("login"))



if __name__ == "__main__":
    db.create_all() #create DB if it is not created whenever we run the application
    app.run(debug=True,port=8000) # debug = True ---> Allow us to not rerun the server everytime