from django.urls import path
from applications.views.application_views import CreateApplicationView, GetApplicationView
from applications.views.document_views import UploadAddressProofView


urlpatterns = [

    path(
        "applications",
        CreateApplicationView.as_view(),
        name="create-application"
    ),
    path(
        "applications/<uuid:application_id>",
        GetApplicationView.as_view(),
        name="get-application"
    ),
    path(
        "applications/<uuid:application_id>/documents",
        UploadAddressProofView.as_view(),
        name="upload-document"
    ),
]