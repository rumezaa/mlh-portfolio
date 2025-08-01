import unittest
from peewee import *
from app import TimelinePost  # Corrected model name

MODELS = [TimelinePost]
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
        first = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello')
        assert first.id == 1
        second = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hi')
        assert second.id == 2
        # Check the data
        posts = list(TimelinePost.select().order_by(TimelinePost.id))
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].name, 'John Doe')
        self.assertEqual(posts[1].email, 'jane@example.com')