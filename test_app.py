import unittest
from flask_testing import TestCase
from flask import Flask
from app import app
from models import db, connect_db, User, Post, Tag

class FlaskRouteTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/test_db'
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        db.drop_all()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        test_user = User(first_name='Vinny', last_name='Testerverde', image_URL='Imageurl.com')
        db.session.add(test_user)
        db.session.commit()
        return test_user
    
    def test_full_name(self):
        """Test Full Name Method"""
        test_user = self.create_test_user()
        self.assertEqual(test_user.full_name(), 'Vinny Testerverde')
    
    def create_test_post(self, user_id=None):
        test_post = Post(title="Test Post", content='This is just some test content', created_at='2024-01-01 12:00:00')
        if user_id is not None:
            test_post.user_id = user_id
        db.session.add(test_post)
        db.session.commit()
        return test_post
    
    def create_test_tag(self):
        test_tag = Tag(name='Test Tag')
        db.session.add(test_tag)
        db.session.commit()
        return test_tag

    def test_show_user_list(self):
        """Test Show User List"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        users = User.query.all()
        for user in users:
            self.assertIn(user.first_name.encode(), response.data)

    def test_user_profile(self):
        """Test User Profile View"""
        test_user = self.create_test_user()

        response = self.client.get(f'/users/{test_user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_user.first_name.encode(), response.data)
    
    def test_add_new_user_get(self):
        """Test Add a New User GET"""
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)
    
    def test_add_new_user_post(self):
        """Test Add New User POST"""
        num_users_before = User.query.count()

        response = self.client.post('/users/new', data={
            'first-name' : 'Vincent',
            'last-name' : 'Testerverde',
            'img-url' : 'Testimage.com'
        })

        num_users_after = User.query.count()

        self.assertEqual(num_users_after, num_users_before +1)
        self.assertEqual(response.status_code, 302)

    def test_edit_user_get(self):
        """Test Edit User GET"""
        test_user = self.create_test_user()

        response = self.client.get(f'/users/{test_user.id}')
        self.assertEqual(response.status_code, 200)

        
    def test_edit_user_post(self):
        test_user = self.create_test_user()

        response = self.client.post(f'/users/{test_user.id}/edit', data={
            'first-name': 'NewFirstName',
            'last-name': 'NewLastName',
            'img-url': 'NewImgURL.com'
        })

        self.assertEqual(response.status_code, 302)

        self.assertEqual(test_user.first_name,'NewFirstName')
        self.assertEqual(test_user.last_name, 'NewLastName')
        self.assertEqual(test_user.image_URL, "NewImgURL.com")
    
    def test_delete_user_get(self):
        test_user = self.create_test_user()

        response = self.client.get(f'/users/{test_user.id}/delete')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_post(self):
        test_user = self.create_test_user()
        response = self.client.post(f'/users/{test_user.id}/delete')
        user = User.query.get(test_user.id)
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(user)
        
## Post Class Route Tests
    def test_new_post_get(self):
        """Test New Post Get Route"""
        test_user = self.create_test_user()
        response = self.client.get(f'/users/{test_user.id}/posts/new')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_user.full_name(), 'Vinny Testerverde')
    
    def test_new_post_post(self):
        """Test New Post Post Route"""
        test_user = self.create_test_user()
        test_tag = self.create_test_tag()
        new_post_data ={
            'title': 'Test Post',
            'content': 'This is just some test content',
            'tags': [str(test_tag.id)]
        }
        response = self.client.post(f'/users/{test_user.id}/posts/new', data=new_post_data)
        test_post = Post.query.filter_by(title=new_post_data['title']).first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_post.title, new_post_data['title'])
        self.assertEqual(test_post.content, new_post_data['content'])
        self.assertEqual(test_post.user_id, test_user.id)
        self.assertEqual(len(test_post.tags), 1)
        with self.client as c:
            with c.session_transaction() as sess: sess['user_id'] = test_user.id
            response = self.client.get(f'/users/{test_user.id}/posts/{test_post.id}')
            self.assertIn(test_user.full_name(), 'Vinny Testerverde')

    def test_show_post(self):
        """Test Show Post"""
        test_user = self.create_test_user()
        test_post = self.create_test_post(user_id=test_user.id)
        response = self.client.get(f'/posts/{test_post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_user.full_name(), response.get_data(as_text=True))

    def test_edit_post_get(self):
        """Test Edit Post Get Route"""
        test_user = self.create_test_user()
        test_post = self.create_test_post(user_id=test_user.id)
        response = self.client.get(f'/posts/{test_post.id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_user.full_name(), response.get_data(as_text=True))

    def test_edit_post_post(self):
        """Test Edit Post Post Route"""
        test_user = self.create_test_user()
        test_post = self.create_test_post()
        response = self.client.post(f'/posts/{test_post.id}/edit', data={
            'title': 'New Test Title',
            'content':'Here is a new test content.'
        })
        db.session.refresh(test_post)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_post.title, 'New Test Title')
        self.assertEqual(test_post.content, 'Here is a new test content.')

    def test_delete_post_get(self):
        """Test Delete Post Get Route"""
        test_post = self.create_test_post()
        response = self.client.get(f'/posts/{test_post.id}/delete')
        self.assertEqual(response.status_code, 200)

    def test_delete_post_post(self):
        """Test Delete Post Post Route"""
        test_post = self.create_test_post()
        test_user = self.create_test_user
        response = self.client.post(f'/posts/{test_post.id}/delete')
        self.assertEqual(response.status_code, 302)
        post = Post.query.get(test_post.id)
        self.assertIsNone(post)

    def test_tag_list(self):
        """Test Tag List"""
        test_tag = self.create_test_tag()
        response = self.client.get('/tags')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_tag.name, 'Test Tag')

    def test_add_tag(self):
        """Test Add Tag"""
        response = self.client.get('/tags/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add A Tag', response.get_data(as_text=True))



if __name__ == '__main__':
    unittest.main()

