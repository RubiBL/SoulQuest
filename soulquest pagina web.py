from flask import Flask,redirect,url_for, render_template,request,session
from datetime import timedelta
app= Flask(__name__)
app.permament_session_lifetime= timedelta(days=5)
app.secret_key="hello"
@app.route("/",methods=["POST","GET"])
def home():
    if "user" in session:
        user=session["user"]
        return render_template("Home.html",usr=user)
    else:   
        return render_template("Start.html")
@app.route("/Login",methods=["POST","GET"])
def Login():
    if request.method=="POST":
            session.permanent=True
            user=request.form["username"]
            session["user"]= user
            return render_template("Home.html",usr=user)
    else:
        if "user" in session:
            user=session["user"]
            redirect(url_for("home"))
        return render_template("Login.html")
@app.route("/Lessons",methods=["POST","GET"])
def Lessons():
    if "user" in session:
        user=session["user"]
        return render_template("lessons.html",usr=user)
    else:
        return redirect(url_for("Login"))  
@app.route("/Logoff",methods=["POST","GET"])
def Logoff():
    session.pop("user",None)
    return redirect(url_for("home"))
@app.route("/Signup",methods=["POST","GET"])
def Signup():
    if request.method=="POST":
            session.permanent=True
            user=request.form["username"]
            session["user"]= user
            email = request.form['email']
            password = request.form['password']
            return render_template("Home.html",usr=user)
    else:
        if "user" in session:
            user=session["user"]
            redirect(url_for("home"))
        return render_template("Signup.html")

if __name__=="__main__":
	app.run()