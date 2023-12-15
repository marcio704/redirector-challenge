from unittest import TestCase

from .views import app
from .utils import clean_querystring, get_available_domains_for_pool


class LambdaTesting(TestCase):

    def test_ping(self):
        with app.test_client() as client:
            response = client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('ok!', response.text)


class LambdaUtilsTest(TestCase):

    def test_clean_querystring(self):
        original_querystring = 'test=123&domain_pool_id=1'
        cleaned_querystring = clean_querystring(original_querystring)
        self.assertEqual(cleaned_querystring, 'test=123')

    def test_get_available_domains_for_pool(self):
        domains_from_first_pool = get_available_domains_for_pool(1, source_file='./mock_files/domains.jsonl')
        self.assertEqual(len(list(domains_from_first_pool)), 2)

        domains_from_second_pool = get_available_domains_for_pool(2, source_file='./mock_files/domains.jsonl')
        self.assertEqual(len(list(domains_from_second_pool)), 3)
