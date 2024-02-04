from django.urls import path
from. import views
from .views import archive_user, save_user_changes

urlpatterns = [
    path('dashboard_views/<str:user_role>', views.dashboard_views, name="dashboard_views"),
    path('manage_employee/<str:user_role>', views.manage_employee, name="manage_employee"),
    path('manage_payroll/<str:user_role>', views.manage_payroll, name="manage_payroll"),
    path('create_user/', views.create_user, name='create_user'),
    path('archive_user/<int:user_id>/', archive_user, name='archive_user'),
    path('edit_user/<int:user_pk_id>/', views.edit_user, name='edit_user'),
    path('save_user_changes/<int:user_pk_id>/', save_user_changes, name='save_user_changes'),
]
