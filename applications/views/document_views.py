from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from applications.models import Application
from applications.models import AddressProof

from applications.serializers.address_proof_serializer import AddressProofSerializer
from applications.services.decision_engine import evaluate_application


class UploadAddressProofView(APIView):

    def post(self, request, application_id):

        application = get_object_or_404(Application, id=application_id)

        serializer = AddressProofSerializer(data=request.data)

        if serializer.is_valid():

            address_proof = serializer.save(application=application)

            decision = evaluate_application(
                application,
                address_proof.extracted_address
            )

            return Response({
                "message": "Document processed",
                "decision_id": decision.id,
                "approved": decision.approved
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)