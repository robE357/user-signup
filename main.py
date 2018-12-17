from flask import Flask, request, redirect, render_template, url_for
import html
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

#validation functions
def isvalid(value):
    if (len(value) >= 3 and len(value) <= 20) and value != "" and " " not in value:
        return True
    else:
        return False

def validemail(email):
    checker = r'(\w+[.|\w])*@(\w+[.])*\w+'

    if 0 > len(email) < 3:
        return False
    if len(email) > 20:
        return False
    if not re.match(checker, email):
        return False
    else:
        return True



@app.route("/success", methods=['POST'])
def success():
    render_template('success.html')

@app.route("/signup", methods=['POST'])
def signup():

    user_error = ""
    pass_error = ""
    email_error = ""
    verify_error = ""
    error = ""

    password = request.form['password']
    password = html.escape(password,quote=True)
    username = request.form['username']
    username = html.escape(username,quote=True)
    passwordVerify = request.form['passwordVerify']
    passwordVerify = html.escape(passwordVerify, quote=True)
    email = request.form['email']
    email = html.escape(email,quote=True)


    if not isvalid(username):
        user_error += "The username you input is invalid or blank! username must be 3-20 chars, no spaces!"
        error += (user_error + "+")
    
    if not isvalid(password):
        pass_error += "The password you entered is invalid or blank! password must be 3-20 chars, no spaces!"
        error += (pass_error + "+")
       
    
    if passwordVerify != password:
        verify_error = "Password validation error, the entered passwords do not match!"
        error += (verify_error + "+")

    

    if (not validemail(email)):
        email_error = "Please enter a valid email! e.g. username@site.com"
        error += (email_error + "+")

    if not user_error and not pass_error and not verify_error and not email_error:
        return render_template('success.html', username=username)
    else:  
        return render_template(
            "/index.html", 
            username=username,
            user_error=user_error,
            pass_error=pass_error,
            verify_error=verify_error,
            email_error=email_error
            )

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    template = jinja_env.get_template('index.html')
    return render_template('index.html', error=encoded_error and html.escape(encoded_error, quote=True))

app.run()
