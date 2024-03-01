from django.urls import include, path
from .views import hr_module

urlpatterns = [
    path("", hr_module.as_view(), name="hr_dashboard"),
    
]


