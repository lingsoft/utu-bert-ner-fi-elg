import unittest
import os
import requests
import json


API_URL = 'http://localhost:8000/process'


def read_fixture(fname):
    fixture_path = "tests/integration/fixtures/"
    with open(os.path.join(fixture_path, fname)) as infile:
        return infile.read()


def call_api(text):
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"type": "text", "content": text})
    return  requests.post(
            API_URL, headers=headers, data=payload).json()


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.steady_text = "Vuonna 1978 Pauli asui Turussa."
        self.tag_change_text = "Se on Tuntematon sotilas."

    def test_valid_api_type(self):
        """Return annotations"""
        response = call_api(self.steady_text)['response']
        self.assertEqual(response.get('type'), 'annotations')

    def test_api_response_content(self):
        """Return correct content with tag change"""
        response = call_api(self.tag_change_text)['response']
        for entity in ('PERSON', 'WORK_OF_ART'):
            self.assertIn(entity, response['annotations'])

    def test_api_response_with_empty_request(self):
        """Return empty annotations"""
        response = call_api("")['response']
        self.assertIn('annotations', response)

    def test_api_response_with_too_large_request(self):
        """Return failure if MAX_CHAR is exceeded"""
        large_text = 'Aku Salo. ' * 3001
        response = call_api(large_text)
        self.assertEqual(response['failure']['errors'][0]['code'],
                         'elg.request.too.large')

    def test_api_response_with_long_token(self):
        """Return annotations with long tokens"""
        long_token = "å" * 10000
        response = call_api(long_token)['response']
        self.assertIn('annotations', response)

    def test_api_response_with_special_characters(self):
        """Return correct entities"""
        spec_text = "\N{grinning face}\u4e01\u0009" + self.steady_text + "\u0008"
        response = call_api(spec_text)['response']
        gpe = response['annotations']['GPE'][0]
        self.assertEqual(spec_text[gpe['start']:gpe['end']], 'Turussa')


if __name__ == '__main__':
    unittest.main()
