from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from models import Users, db
from views import views
from forms import forms

migrate = Migrate()

app = Flask(__name__)
app.register_blueprint(views)
app.register_blueprint(forms)
# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.login'
login_manager.login_message = "Please log in to access this page"
login_manager.login_message_category = "alert alert-danger alert-dismissible fade show"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(port=5000, debug=True)