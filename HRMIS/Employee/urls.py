from django.urls import path
from. import views


urlpatterns = [
     path('employee_dashboard/<str:user_role>', views.employee_dashboard, name="employee_dashboard"),
]
