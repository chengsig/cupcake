from flask import Flask, jsonify, request, render_template
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


@app.route('/')
def render_cupcakes():
    """ Generates homepage template with list of cupcakes """
   
    return render_template('index.html')


@app.route('/cupcakes')
def show_cupcakes():
    """ Show a list of dictionaries containing individual cupcakes """

    found_cupcakes = Cupcake.query.all()

    serialized_cupcakes = [
        {'flavor': cupcake.flavor, 'size': cupcake.size,
         'rating': cupcake.rating, 'image': cupcake.image}
        for cupcake in found_cupcakes
    ]

    return jsonify(response=serialized_cupcakes)


@app.route('/cupcakes', methods=["POST"])
def create_cupcake():
    """ Create a new cupcake with a dictionary containing
        {id, flavor, size, rating, image} """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_cupcake = {'id': new_cupcake.id,
                          'flavor': new_cupcake.flavor,
                          'size': new_cupcake.size,
                          'rating': new_cupcake.rating,
                          'image': new_cupcake.image}

    return jsonify(response=serialized_cupcake)

@app.route('/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """ Update information about a specific cupcake
    one or all of the data attributes"""

    cupcake = Cupcake.query.get(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image'] or None

    db.session.commit()

    serialized_cupcake = {'id': cupcake.id,
                          'flavor': cupcake.flavor,
                          'size': cupcake.size,
                          'rating': cupcake.rating,
                          'image': cupcake.image}
                        
    return jsonify(response=serialized_cupcake)


@app.route('/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Deletes specified cupcake """

    cupcake = Cupcake.query.get(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    message = {"message": "Deleted"}

    return jsonify(response=message)