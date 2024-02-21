from django.urls import path
from. import views
from .views import SaveAttendanceView
from .views import archive_user, save_user_changes, unarchive_user,calculate_salary, activate_payslip

urlpatterns = [
    path('dashboard_views/<str:user_role>', views.dashboard_views, name="dashboard_views"),
    path('manage_employee/<str:user_role>', views.manage_employee, name="manage_employee"),
    path('manage_payroll/<str:user_role>', views.manage_payroll, name="manage_payroll"),
    path('create_user/', views.create_user, name='create_user'),
    path('archive_user/<int:user_id>/', archive_user, name='archive_user'),
     path('unarchive_user/<int:user_id>/', unarchive_user, name='unarchive_user'),
    path('edit_user/<int:user_pk_id>/', views.edit_user, name='edit_user'),
    path('save_user_changes/<int:user_pk_id>/', save_user_changes, name='save_user_changes'),
    path('upload_and_cleanse/', views.upload_and_cleanse, name='upload_and_cleanse'),
    path('view_excel_content/<int:cleansed_data_id>/', views.view_excel_content, name='view_excel_content'),
    path('save-attendance/', SaveAttendanceView.as_view(), name='save-attendance'),
    path('manage_payroll/get_latest_attendance/<str:username>/', views.get_latest_attendance, name='get_latest_attendance'),
    path('calculate_salary/<str:username>/', calculate_salary, name='calculate_salary'),
    path('activate_payslip/<str:username>/', activate_payslip, name='activate_payslip'),    

]
