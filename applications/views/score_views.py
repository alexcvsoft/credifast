import random
from rest_framework.views import APIView
from rest_framework.response import Response

class CreditScoreView(APIView):

    def get(self, request):

        score = random.randint(300, 900)

        return Response({
            "credit_score": score
        })