import testtools

import guardianapi


class GuardianAPITests(testtools.TestCase):

    def test_basic_query(self):
        # A basic test to make sure that the API returns some results
        response = guardianapi.get_response()
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)
