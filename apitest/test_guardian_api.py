from datetime import (
    datetime,
    timedelta,
)
import testtools

import guardianapi


PAGE_ERROR = "requested page is beyond the number of available pages"
DATE_ERROR = ("Dates must be an ISO8601 date or datetime (e.g. 2010-07-20 "
              "or 2010-07-20T10:00:00+05:00). Remember to URL-encode the '+' "
              "if you provide a timezone offset.")

class GuardianAPITests(testtools.TestCase):

    def test_basic_search(self):
        """
        The API returns some results
        """
        response = guardianapi.get_response()
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

    def test_search_results(self):
        """
        When searching with query terms, all results contain
        the term
        """
        response = guardianapi.get_response(query='Deliveroo')
        self.assertEqual(response.status_code, 200)
        results = response.json()['response']['results']
        for title in [r['webTitle'] for r in results]:
            self.assertIn('Deliveroo', title)

    def test_page_size(self):
        """
        Page size reflects the number of results returned
        """
        response = guardianapi.get_response()
        results = response.json()['response']['results']
        page_size = response.json()['response']['pageSize']
        self.assertEqual(len(results), page_size)

    def test_not_older_than_from_date(self):
        """
        When specifying the from_date field, all results returned are
        chronologically later than the from_date
        """
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
        """
        When specifying the to_date field, all results returned are
        chronologically prior to the to_date
        """
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
        """
        If a from_date is specified that is in the future, no results are
        returned, nor is an error generated
        """
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
        """
        If a date that is not valid is used as the from_date an appropriate
        error message and status code are returned
        """
        response = guardianapi.get_response(
            query='Deliveroo',
            from_date='xxxx-yy-zz'
        )
        self.assertEqual(response.status_code, 400)

    def test_to_date_not_valid(self):
        """
        If a date that is not valid is used as the to_date an appropriate
        error message and status code are returned
        """
        response = guardianapi.get_response(
            query='Deliveroo',
            to_date='xxxx-yy-zz'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['response']['message'], DATE_ERROR)

    def test_page_greater_than_number_pages(self):
        """
        If the page provided in the parameters is larger than the total
        number of pages, an appropriate error message and status code should
        be returned
        """
        response = guardianapi.get_response(
            query='Deliveroo'
        )
        total_pages = response.json()['response']['pages']
        error_response = guardianapi.get_response(
            query='Deliveroo',
            page=total_pages+1
        )
        self.assertEqual(error_response.status_code, 400)
        self.assertEqual(error_response.json()['response']['message'], PAGE_ERROR)
