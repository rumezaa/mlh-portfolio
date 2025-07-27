import unittest
from peewee import *
from app import TimeLinePost  # Import your model from the app

MODELS = [TimeLinePost]
# In-memory SQLite DB (used only for testing)
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind the model to the test DB and create the table
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Drop the table and close the DB after every test
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeLine_post(self):
        first = TimeLinePost.create(name='John Doe', email='john@example.com', content='Hello')
        assert first.id == 1
        second = TimeLinePost.create(name='Jane Doe', email='jane@example.com', content='Hi')
        assert second.id == 2
        # Check the data
        posts = list(TimeLinePost.select().order_by(TimeLinePost.id))
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].name, 'John Doe')
        self.assertEqual(posts[1].email, 'jane@example.com')
