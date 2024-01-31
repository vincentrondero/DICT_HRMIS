from .views import Login_View
from .views import login_user
from django.urls import path
from. import views

urlpatterns = [
    path('', Login_View.as_view(), name="Login"),
    path('login/', login_user, name='login_user'),
]


