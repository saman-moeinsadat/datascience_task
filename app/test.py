import unittest

from app import app

class FlaskTestCase(unittest.TestCase):

    # check for response 200 in "/".
    def test_index_home(self):
        tester = app.test_client(self)
        response = tester.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # check for response 200 in "/mostSimilar".
    def test_index_similar(self):
        tester = app.test_client(self)
        response = tester.post("/mostSimilar", data =dict(word='mask'),\
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # check the type of content returned.
    def test_index_return_type(self):
        tester = app.test_client(self)
        response = tester.post("/mostSimilar", data =dict(word='mask'),\
            follow_redirects=True)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
    

    # check for content of html in "/".
    def test_load_serving(self):
        tester = app.test_client(self)
        response = tester.get("/", follow_redirects=True)
        self.assertTrue(b'Serving Word Similarities' in response.data)
        self.assertTrue(b'Please Enter The Query Word:' in response.data)

    # check response for query words, in vocab.
    def test_query_btn(self):
        tester = app.test_client(self)
        response = tester.post("/mostSimilar", data =dict(word='mask'),\
            follow_redirects=True)
        self.assertIn(b'Similar Words:', response.data)

    # check response for query words, blocked.
    def test_query_btn_blocked(self):
        tester = app.test_client(self)
        response = tester.post("/mostSimilar", data =dict(word='covid'),\
            follow_redirects=True)
        self.assertIn(b'Please Note That, This Application Does Not',\
            response.data)
    
    # check response for query words, not in vocab.
    def test_try_again_btn(self):
        tester = app.test_client(self)
        response = tester.post("/mostSimilar", data =dict(word='fauucci'),
        follow_redirects=True)
        self.assertIn(b'The Words Contain In This Application, Does',\
            response.data)


if __name__ == "__main__":
    unittest.main()
