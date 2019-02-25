from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import Cupcake, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)


@app.route('/cupcakes')
def show_cupcakes():
    """ """

    found_cupcakes = Cupcake.query.all()

    serialized_cupcakes = [
        {'flavor': found_cupcakes.flavor, 'size': found_cupcakes.size, 'rating': found_cupcakes.rating,
         'image': found_cupcakes.image}
        for cupcake in found_cupcakes
    ]

    return jsonify(response=serialized_cupcakes)


@app.route('/cupcakes', method=["POST"])
def create_cupcake():
    """ """
