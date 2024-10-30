from flask import Flask
from config import configure_routes

app = Flask(__name__)
configure_routes(app)

app.run(debug=True)