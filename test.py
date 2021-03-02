from unittest import TestCase
from app import app
from models import db, User, Post 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserTests(TestCase):

    def setUp(self):
        """Add sample user """

        User.query.delete()

        user = User(first_name="Test", last_name="Test")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id 

    def tearDown(self):
        """ Clean up after testing """
        
        db.session.rollback()

    def test_index(self):
        """ test that the home page loads """

        with app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 302)

    def test_user_listing(self):
        """ check if the test user just created exists """

        with app.test_client() as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Test', html)

    def test_users_new(self):
        """ test that create new users loads correctly """

        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Create A User', html)

    def test_users_new_post(self):
        """ create a new user John Smith to test the create a new user form """
        
        with app.test_client() as client:
            d = {"first_name": "John", "last_name": "Smith", "image_url": ""}
            response = client.post("/users/new", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("John Smith", html)

    
    """ post test cases """

    # def test_new_post_form(self):
    #     """ Test that the add new post page displays correctly """

    #     with app.test_client() as client:
    #         response = client.get(f'/users/{user_id}/posts/new')
    #         html = response.get_data(as_text=True)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('Add Post', html)

    
    # def test_add_post(self):
    #     """ Test the form submission for adding a new post """

    #     with app.test.client() as client: 
    #         d = {"title": "Test Title", "content": "Test content", "user_id": f"{user_id}"}
    #         response = client.post(f"/users/{user_id}/posts/new", data=d, follow_redirects=True)
    #         html = response.get_data(as_text=True)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn("Test Title", html) 