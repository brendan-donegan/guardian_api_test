import os
import requests


GUARDIAN_API = "https://content.guardianapis.com/search"


def get_response(query=None, from_date=None, to_date=None):
    params = {'api-key': os.environ['API_KEY']}
    if query is not None:
        params['q'] = query
    if from_date is not None:
        params['from_date'] = from_date
    if to_date is not None:
        params['to_date'] = to_date
    return requests.get(GUARDIAN_API, params=params)
