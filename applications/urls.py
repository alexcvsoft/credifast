from django.urls import path
from applications.views.application_views import CreateApplicationView


urlpatterns = [

    path(
        "applications",
        CreateApplicationView.as_view(),
        name="create-application"
    ),

]