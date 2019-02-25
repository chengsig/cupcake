from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_url = "https://tinyurl.com/truffle-cupcake"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Create cupcake models"""
    
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), default=DEFAULT_url)
