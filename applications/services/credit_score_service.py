import requests

class CreditScoreService:

    BASE_URL = "http://localhost:8000/api/v1"

    @staticmethod
    def get_credit_score():

        response = requests.get(f"{CreditScoreService.BASE_URL}/scorecredito")

        if response.status_code != 200:
            raise Exception("Credit score service unavailable")

        return response.json()["credit_score"]