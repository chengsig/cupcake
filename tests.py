from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        new_cupcake = Cupcake(
            flavor='sour', size='small', rating=10, id=10000)
        db.session.add(new_cupcake)
        db.session.commit()

    def test_all_cupcakes(self):
        """ /cupcakes should show all cupcakes """

        response = self.client.get("/cupcakes")
        response_data = response.json['response']

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['flavor'], 'sour')
        self.assertEqual(response_data[0]['size'], 'small')
        self.assertEqual(response_data[0]['rating'], 10)
        self.assertEqual(response.status_code, 200)
