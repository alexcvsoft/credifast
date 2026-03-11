from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from applications.models import Application, AddressProof
from applications.serializers.address_proof_serializer import AddressProofSerializer
from applications.services.decision_engine import evaluate_application
# IMPORTANT: Import AI service that will handle the document processing
from applications.services.ai_document_extractor import AIDocumentExtractor

class UploadAddressProofView(APIView):

    def post(self, request, application_id):
        # 1. Search for the application in the database using the provided application_id
        application = get_object_or_404(Application, id=application_id)

        # 2. Validate the initial input (we only expect the file_url or the file)
        serializer = AddressProofSerializer(data=request.data)

        if serializer.is_valid():
            file_url = serializer.validated_data.get('file_url')
            
            # 3. Call to AI
            print(f"--- Starting AI Extraction for: {file_url} ---")
            extracted_data = AIDocumentExtractor.extract_document_data(file_url)
            
            # AI error verification
            if "error" in extracted_data:
                return Response({
                    "error": "AI Extraction failed",
                    "details": extracted_data["error"]
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 4. Save in DB
            # Insert the extracted data into the AddressProof model, linking it to the application
            address_proof = serializer.save(
                application=application,
                extracted_name=extracted_data.get('extracted_name'),
                extracted_address=extracted_data.get('extracted_address'),
                extracted_date=extracted_data.get('extracted_date')
            )

            # 5. Rules engine
            # Send the extracted address to the decision engine to evaluate the application based on the rules defined
            decision = evaluate_application(
                application,
                address_proof.extracted_address
            )

            # 6. RESPUESTA FINAL
            return Response({
                "message": "Document processed and evaluated by AI",
                "extracted_data": {
                    "name": address_proof.extracted_name,
                    "address": address_proof.extracted_address,
                    "date": address_proof.extracted_date
                },
                "decision": {
                    "id": decision.id,
                    "approved": decision.approved,
                    "reason": "Check RuleLog for details" # Opcional
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)