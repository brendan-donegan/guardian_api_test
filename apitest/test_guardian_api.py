import testtools

import guardianapi


class GuardianAPITests(testtools.TestCase):

    def test_basic_search(self):
        # The API returns some results
        response = guardianapi.get_response()
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

    def test_search_results(self):
        #  When searching with query terms, all results contain
        # the term
        response = guardianapi.get_response(query='Deliveroo')
        results = response.json()['response']['results']
        for title in [r['webTitle'] for r in results]:
            self.assertIn('Deliveroo', title)

    def test_page_size(self):
        # Page size reflects the number of results returned
        response = guardianapi.get_response()
        results = response.json()['response']['results']
        page_size = response.json()['response']['pageSize']
        self.assertEqual(len(results), page_size)
