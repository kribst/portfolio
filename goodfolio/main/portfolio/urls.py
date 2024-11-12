from django.urls import path
from .views import index, work, Services, work_details, download_cv

urlpatterns = [
    path("", index, name="index"),
    path("work/", work, name="work"),
    path("Services/", Services, name="Services"),
    path('works_details/<int:work_id>/', work_details, name='work_details'),
    path('download/', download_cv, name='download_cv'),
]
