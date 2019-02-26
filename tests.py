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

    def test_add_cupcake(self):
        """ POST /cupcakes should add a new cupcake """
        
        response = self.client.post("/cupcakes",
                                    json={"flavor": "caramel",
                                          "size": "medium",
                                          "rating": 8,
                                          "id": 10001,
                                          "image": None})

        self.assertEqual(response.json['response']['flavor'], 'caramel')
        self.assertEqual(response.json['response']['size'], 'medium')
        self.assertEqual(response.json['response']['rating'], 8)
        self.assertEqual(response.status_code, 200)

        all_cupcakes = self.client.get('/cupcakes')
        all_cupcakes_data = all_cupcakes.json['response']
        self.assertEqual(len(all_cupcakes_data), 2)

    def test_update_cupcake(self):
        """ PATCH a /cupcake/id should update the cupcake
        with updated information"""

        response = self.client.patch("/cupcakes/10000",
                                     json={"flavor": "chocolate",
                                           "size": "giant",
                                           "rating": 11,
                                           "id": 10000,
                                           "image": None})

        self.assertEqual(response.json['response']['flavor'], "chocolate")
        self.assertEqual(response.json['response']['size'], 'giant')
        self.assertEqual(response.json['response']['rating'], 11)
        self.assertEqual(response.status_code, 200)

        all_cupcakes = self.client.get('/cupcakes')
        all_cupcakes_data = all_cupcakes.json['response']
        self.assertEqual(len(all_cupcakes_data), 1)

    def test_delete_cupcake(self):
        """ DELETE a certain /cupcake/id """

        response = self.client.delete('/cupcakes/10000')

        self.assertEqual(response.json['response']['message'], "Deleted")

        all_cupcakes = self.client.get('/cupcakes')
        all_cupcakes_data = all_cupcakes.json['response']
        self.assertEqual(len(all_cupcakes_data), 0)