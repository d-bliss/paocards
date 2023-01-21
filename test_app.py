import unittest
from app import app

class TestPlay(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.user_id = 1
        self.card_index = 0

    def test_play_route(self):
        # Test initial GET request
        response = self.app.get('/play')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Yourself', response.data)

    def test_play_route_post_flip(self):
        # Test POST request with form data 'Flip'
        response = self.app.post('/play', data={'Flip': 'Flip'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Person:', response.data)
        self.assertIn(b'Action:', response.data)
        self.assertIn(b'Object:', response.data)

    def test_play_route_post_next(self):
        # Test POST request with form data 'Next'
        response = self.app.post('/play', data={'Next': 'Next'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Yourself', response)
if __name__ == '__main__':
    unittest.main()
