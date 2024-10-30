from routes.analisador import analisador

def configure_routes(app):
    app.register_blueprint(analisador)