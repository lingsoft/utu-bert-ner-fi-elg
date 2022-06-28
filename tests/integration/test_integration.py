import unittest
import os
import requests


API_URL = 'http://localhost:8000/process'


def read_fixture(fname):
    fixture_path = "tests/integration/fixtures/"
    with open(os.path.join(fixture_path, fname)) as infile:
        return infile.read()


def call_api(text):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"type": "text", "content": text})
    return  requests.post(
            API_URL, headers=headers, data=payload).json()['response']


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.steady_text = "Vuonna 1978 Pauli asui Turussa."
        self.tag_change_text = "Se on Tuntematon sotilas."
        # emojis and control characters

    def test_valid_api_type(self):
        """Should be annotations"""
        response = call_api(self.steady_text)
        self.assertEqual(response.get('type'), 'annotations')

    def test_api_response_content(self):
        """Return correct content with tag change"""
        response = call_api(self.tag_change_text)
        for entity in ('PERSON', 'WORK_OF_ART'):
            self.assertIn(entity, response['annotations'])

    def test_api_response_with_empty_request(self):
        """Return empty annotations"""
        response = call_api("")
        self.assertIn('annotations', response)

    def test_api_response_with_too_large_request(self):
        """Return Failure if MAX_CHAR is exceeded"""
        large_text = 'Hei! ' * 3001
        response = call_api(large_text),
        self.assertEqual(response['failure']['errors'][0]['code'],
                         'elg.request.too.large')

    # Long tokens


if __name__ == '__main__':
    unittest.main()
