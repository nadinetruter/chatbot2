from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from resources.forms import ContactForm


from database.db import initialize_db
from flask_restful import Api
from resources.errors import errors



application = app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config["DEBUG"]= True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "bytecare01@gmail.com"
app.config["MAIL_PASSWORD"] = "Bytecare123"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"]="bytecare01@gmail.com"
#app.url_map.strict_slashes = False


mail = Mail(app)
# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)



app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://byteme:1234@cluster0.mlj40.mongodb.net/test?retryWrites=true&w=majority'
}

@app.route('/contact', methods=['POST'])
def contact():
    form = ContactForm()
    msg = Message(form.subject.data, sender='contact@example.com', recipients=['bytecare01@gmail.com'])
    msg.body = """
    From: %s
    Email: <%s>
    Message: %s
    """ % (form.name.data, form.email.data, form.message.data)
    mail.send(msg)
    return 'Form posted.'

@app.route('/chatbot', methods=['POST','GET'])
def chatbot():
    return render_template('chatbot.html')

initialize_db(app)
initialize_routes(api)
