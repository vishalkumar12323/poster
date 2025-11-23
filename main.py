from flask import Flask, render_template, request
from controllers.user_controllers import login_user, register_user


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')



@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return {"error": "Email and password are required"}, 400
    
    return login_user(user={"email": email, "password": password})


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if name is None or email is None or password is None:
        return "<h2>Name, Email or Password is required feild.</h2>"

    return register_user(user={"name": name, "email": email, "password": password})
    


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)