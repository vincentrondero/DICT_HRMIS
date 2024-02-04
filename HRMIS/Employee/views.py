from django.shortcuts import render
from Authentication.models import User

def employee_dashboard(request, user_role):
    user_id = request.session.get('user_id')
    
    try:
        user = User.objects.get(USER_pkID=user_id)
        user_role = request.session.get('role', 'Guest')
        user_name = user.name if hasattr(user, 'name') else 'Guest'
    except User.DoesNotExist:
        user_name = 'Guest'

    return render(request, 'Employee/Employee.html', {'user_name': user_name, 'user_role': user_role})
