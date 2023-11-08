from unittest import TestCase

from app import app
from models import db, User

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for model for User"""

    def setUp(self):
        """Clean up any existing Users"""

        User.query.delete()
        test_user = User(first_name="Mo", last_name="Adam", image_url="")

        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name="John", last_name="Smith", image_url="")
        self.assertEqual(user.get_full_name(), "John Smith")

    def test_user_list_page(self):
        with app.test_client() as client:
            resp = client.get('/');
            html= resp.get_data(as_text=True);

            self.assertEqual(resp.status_code,200);
            self.assertIn("Mo",html)

    def test_user_details_page(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}');
            html= response.get_data(as_text=True);

            self.assertEqual(response.status_code,200);
            self.assertIn("Mo Adam",html);

    def test_add_user_form_page(self):
        with app.test_client() as client:
            response = client.get(f'/users/new');
            html= response.get_data(as_text=True);

            self.assertEqual(response.status_code,200);
            self.assertIn("Create a user",html);
    
    def test_edit_user_form_page(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}/edit');
            html= response.get_data(as_text=True);

            self.assertEqual(response.status_code,200);
            self.assertIn("Edit a user",html);

