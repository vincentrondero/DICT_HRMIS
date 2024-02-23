from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views import View
from .models import User

class Login_View(View):
    def get(self, request):
        user_role = request.session.get('role', 'Guest')
        return render(request, 'Authentication/Login.html', {'user_role': user_role})


from django.urls import reverse

def login_user(request):
    user_role = 'Guest'

    if request.method == 'POST':
        entered_username = request.POST.get("username")
        entered_password = request.POST.get("password")

        try:
            user = User.objects.get(username=entered_username)
            user_role = user.role
            request.session['user_id'] = user.USER_pkID
            request.session['username'] = user.username
            request.session['role'] = user.role
        except User.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return render(request, 'Authentication/Login.html', {'user_role': user_role})

        if check_password(entered_password, user.password):
            if user.role == 'HR':
                return redirect('dashboard_views', user_role=user_role)
            elif user.role == 'JO':
                return redirect('employee_dashboard', user_role=user_role)

        else:
            messages.error(request, "Invalid password. Please try again.")

    return render(request, 'Authentication/Login.html', {'user_role': user_role})

from Payroll.models import Payslip

def payroll_view(request):
    user = request.user
    active_payslip = Payslip.objects.filter(user=user, activated=True).first()
    return render(request, 'payroll_template.html', {'active_payslip': active_payslip})


