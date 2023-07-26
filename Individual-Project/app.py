from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
"apiKey": "AIzaSyDeUVEgBlIzZbNU6P3kRfLeXsxDlmc-zVQ",
"authDomain": "individual-project-f613b.firebaseapp.com",
"projectId": "individual-project-f613b",
"storageBucket": "individual-project-f613b.appspot.com",
"messagingSenderId": "438539544698",
"appId": "1:438539544698:web:7928ce09d9ce0bf9f7f3c3",
"measurementId": "G-TP9K42RECD",
"databaseURL": "https://individual-project-f613b-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # fullname = request.form['full_name']
        try:
            print("0")
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            print("0")
            UID = login_session['user']['localId']
            print("0")
            user = {"full_name":request.form['full_name'],
            "username":request.form["username"]}
            print("0")
            # user['full_name'] = request.form['full_name']
            # user['username'] = request.form['username']
            db.child("Users").child(UID).set(user)
            print("0")
            return redirect(url_for('home_page'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


            
            # db.child("users").push(user)
            

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home_page'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/home_page',methods=['GET', 'POST'])
def home_page():
    
    if request.method == 'POST':
        try:
            uid = login_session["user"]["localId"]
            tweet= {"title": request.form['title'],"feedback": request.form['feedback'],"text": request.form['text']}
            db.child("Tweets").child(uid).set(tweet)
            # return render_template("home_page")
        except:
            print("Couldn't comment")
    # try:
    tweets=db.child("Tweets").get().val()
    for uid in tweets:
        tweets[uid]["full_name"]=db.child("Users").child(uid).get().val()["full_name"]
    # for tweet in tweets:
    #     print(tweets[tweet])
    return render_template("home_page.html",tweets=tweets)
    # except:
        # return render_template("home_page.html")

@app.route('/signout')
def signout():
    login_session['user']=None
    auth.current_user = None
    return redirect(url_for('signin'))




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)