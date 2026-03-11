from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application
from applications.serializers.application_serializer import ApplicationSerializer


class CreateApplicationView(APIView):

    def post(self, request):

        serializer = ApplicationSerializer(data=request.data)

        if serializer.is_valid():

            application = serializer.save()

            return Response(
                ApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetApplicationView(APIView):

    def get(self, request, application_id):

        application = get_object_or_404(Application, id=application_id)

        serializer = ApplicationSerializer(application)

        return Response(serializer.data)