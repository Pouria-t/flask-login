# import Flask and And other necessary items
import config 
from flask import (
    Flask,
    Response,
    redirect,
    url_for,
    request,
    session,
    abort,    
)
# import Flask login and And other necessary items
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user

app = Flask(__name__)

# config 
app.config.update(
    SECRET_KEY = config.SECRET_KEY
)

# config login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
    
    def __repr__(self):
        return "%d" % (self.id)


# create some users with ids 1 to 20       
users = User(0)


# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")

 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST': # TODO : Sotp the brute forec  
        username = request.form['username']
        password = request.form['password']        
        if password == config.PASSWORD and username == config.USERNAME:
            login_user()
            return redirect(request.args.get("next")) # TODO : check url validity 
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(error):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
    

if __name__ == "__main__":
    app.run()
