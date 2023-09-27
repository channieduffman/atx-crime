from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load instance config when no test_config
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/hello/<int>')
    def hello(int):
        return f'Hello, {int}'
    
    from . import home
    app.register_blueprint(home.bp)
    
    return app