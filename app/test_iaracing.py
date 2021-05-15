import unittest
from app import app


class TestConfig(unittest.TestCase):

    def test_config_loading(self):
        assert app.config['DEBUG'] is True
        assert app.config['SECRET_KEY'] == '0123456'
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////Users/afougere/Git/e1/app/app/base_de_donnees/db.sqlite'
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == True


class FlaskTestCase(unittest.TestCase):

    # Check if response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    #Check for data returned
    def test_index_dat(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'Predict' in response.data)

   

if __name__ == "__main__":
    unittest.main()
