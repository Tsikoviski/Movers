from . import db, create_app
from .routes import bp

def create_app():
    app = Flask(__name__)
    # Configuration code as before
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        app.register_blueprint(bp)
    
    return app

