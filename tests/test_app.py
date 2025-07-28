# tests/test_app.py

import os
import unittest
import json

os.environ['TESTING'] = 'true'

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "ahmad" in html or "MLH Fellow" in html
        
        response = self.client.get("/?profile=rumeza")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "rumeza" in html
        
        # Test invalid profile parameter
        response = self.client.get("/?profile=invalid")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Should default to ahmad profile
        assert "ahmad" in html or "MLH Fellow" in html
        
        # Test navigation elements
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        assert "Home" in html
        assert "Hobbies" in html
        assert "Switch to" in html
    
        # Test Visibility of Sections
        assert "About Me" in html
        assert "Work Experience" in html
        assert "Education" in html
        assert "Places I've Traveled" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert "timeline_posts" in json_data

        assert len(json_data["timeline_posts"]) == 0
        
        # Test POST timeline post
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test post'
        }
        response = self.client.post("/api/timeline_post", data=post_data)
        assert response.status_code == 200
        assert response.is_json
        post_response = response.get_json()
        assert post_response['name'] == 'Test User'
        assert post_response['email'] == 'test@example.com'
        assert post_response['content'] == 'This is a test post'
        assert 'created_at' in post_response
        
        # Test GET timeline posts after creating one
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data["timeline_posts"]) == 1
        assert json_data["timeline_posts"][0]['name'] == 'Test User'
        
        # Test DELETE timeline post
        post_id = post_response['id']
        response = self.client.delete(f"/api/timeline_post/{post_id}")
        assert response.status_code == 200
        delete_response = response.get_json()
        assert delete_response['status'] == 'deleted'
        assert delete_response['id'] == post_id
        
        # Test DELETE non-existent post
        response = self.client.delete("/api/timeline_post/999")
        assert response.status_code == 404
        
        # Test clear all timeline posts
        response = self.client.delete("/api/timeline_post/clear")
        assert response.status_code == 200
        clear_response = response.get_json()
        assert clear_response['status'] == 'cleared'
        assert 'deleted_count' in clear_response
        
        # Verify all posts are cleared
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data["timeline_posts"]) == 0
        
        # Test timeline page visibility
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Create a New Post" in html
        assert "All Posts" in html
        assert "timeline-form" in html
        assert "posts-container" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            'email': 'test@example.com',
            'content': 'This is a test post'
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html
        
        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            'name': 'Test User',
            'email': 'test@example.com',
            'content': ''
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            'name': 'Test User',
            'content': 'This is a test post',
            'email': 'not-an-email'
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


if __name__ == '__main__':
    unittest.main()
