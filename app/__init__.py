from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # import the routes after creating the app
    from app.server import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

