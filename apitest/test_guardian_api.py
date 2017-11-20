from datetime import (
    datetime,
    timedelta,
)
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
        self.assertEqual(response.status_code, 200)
        results = response.json()['response']['results']
        for title in [r['webTitle'] for r in results]:
            self.assertIn('Deliveroo', title)

    def test_page_size(self):
        # Page size reflects the number of results returned
        response = guardianapi.get_response()
        results = response.json()['response']['results']
        page_size = response.json()['response']['pageSize']
        self.assertEqual(len(results), page_size)

    def test_not_older_than_from_date(self):
        # When specifying the from_date field, all results returned are
        # chronologically later than the from_date
        now = datetime.utcnow()
        year_ago = now - timedelta(days=365)
        response = guardianapi.get_response(
            query='Deliveroo',
            from_date=year_ago.strftime('%Y-%m-%d')
        )
        self.assertEqual(response.status_code, 200)
        for result in response.json()['response']['results']:
            pub_date = datetime.strptime(
                result['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ'
            )
            self.assertGreaterEqual(pub_date, year_ago)

    def test_not_newer_than_to_date(self):
        # When specifying the to_date field, all results returned are
        # chronologically prior to the to_date
        now = datetime.utcnow()
        year_ago = now - timedelta(days=365)
        response = guardianapi.get_response(
            query='Deliveroo',
            to_date=year_ago.strftime('%Y-%m-%d')
        )
        self.assertEqual(response.status_code, 200)
        for result in response.json()['response']['results']:
            pub_date = datetime.strptime(
                result['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ'
            )
            self.assertLessEqual(pub_date, year_ago)

    def test_from_date_in_future(self):
        # If a from_date is specified that is in the future, no results are
        # returned, nor is an error generated
        now = datetime.utcnow()
        year_from_now = now + timedelta(days=365)
        response = guardianapi.get_response(
            query='Deliveroo',
            from_date=year_from_now.strftime('%Y-%m-%d')
        )
        self.assertEqual(response.status_code, 200)
        results = response.json()['response']['results']
        self.assertEqual(len(results), 0)

    def test_from_date_not_valid(self):
        # If a date that is not valid is used as the from_date an appropriate
        # error message and status code are returned
        response = guardianapi.get_response(
            query='Deliveroo',
            from_date='xxxx-yy-zz'
        )
        self.assertEqual(response.status_code, 400)

    def test_to_date_not_valid(self):
         # If a date that is not valid is used as the to_date an appropriate
         # error message and status code are returned
         response = guardianapi.get_response(
             query='Deliveroo',
             to_date='xxxx-yy-zz'
         )
         self.assertEqual(response.status_code, 400)
