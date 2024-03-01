from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('employee_dashboard/<str:user_role>', views.employee_dashboard, name="employee_dashboard"),
    path('profile_view/', views.profile_view, name="profile_view"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
