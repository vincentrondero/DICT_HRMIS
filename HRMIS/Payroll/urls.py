from django.urls import path
from. import views


urlpatterns = [
    path('dashboard_views/<str:user_role>', views.dashboard_views, name="dashboard_views"),
    path('manage_employee/<str:user_role>', views.manage_employee, name="manage_employee"),
    path('manage_payroll/<str:user_role>', views.manage_payroll, name="manage_payroll"),
]
