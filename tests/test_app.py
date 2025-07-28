import os, unittest

os.environ["TESTING"] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        r = self.client.get("/")
        assert r.status_code == 200
        html = r.get_data(as_text=True)
        assert "<h1>Ahmad Basyouni</h1>" in html

    def test_timeline_api_get(self):
        r = self.client.get("/api/timeline_post")
        assert r.status_code == 200
        assert r.is_json
        js = r.get_json()
        assert "timeline_posts" in js
        assert len(js["timeline_posts"]) == 0
    
    def test_timeline_api_post(self):
        """POST valid data to /api/timeline_post and then GET it back."""
        payload = {
            "name": "Alice",
            "email": "alice@example.com",
            "content": "Hey there!"
        }
        # 1) POST should succeed
        r1 = self.client.post("/api/timeline_post", data=payload)
        self.assertEqual(r1.status_code, 200)
        obj = r1.get_json()
        self.assertEqual(obj["name"], "Alice")
        self.assertEqual(obj["email"], "alice@example.com")
        self.assertEqual(obj["content"], "Hey there!")

        # 2) GET now returns exactly one post, matching our payload
        r2 = self.client.get("/api/timeline_post")
        data = r2.get_json()
        self.assertEqual(len(data["timeline_posts"]), 1)
        entry = data["timeline_posts"][0]
        self.assertEqual(entry["name"], "Alice")
        self.assertEqual(entry["email"], "alice@example.com")
        self.assertEqual(entry["content"], "Hey there!")
    
    def test_timeline_page(self):
        """GET /timeline should render the timeline.html page."""
        r = self.client.get("/timeline")
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        self.assertIn("<form", html)
        self.assertIn('name="name"', html)
        self.assertIn('name="email"', html)
        self.assertIn('name="content"', html)

    def test_malformed_timeline_post(self):
        # missing name → should be 400 + “Invalid name” in response
        r = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hi"
        })
        assert r.status_code == 400
        html = r.get_data(as_text=True)
        assert "Invalid name" in html

        # 2) empty content
        r = self.client.post("/api/timeline_post", data={
            "name": "John", "email": "john@example.com", "content": ""
        })
        self.assertEqual(r.status_code, 400)
        self.assertIn("Invalid content", r.get_data(as_text=True))

        # 3) malformed email
        r = self.client.post("/api/timeline_post", data={
            "name": "John", "email": "not-an-email", "content": "Hello!"
        })
        self.assertEqual(r.status_code, 400)
        self.assertIn("Invalid email", r.get_data(as_text=True))

