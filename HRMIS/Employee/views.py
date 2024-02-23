from django.shortcuts import render
from Authentication.models import User, Profile
from Payroll.models import Payslip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import base64

def employee_dashboard(request, user_role):
    user_id = request.session.get('user_id')

    try:
        user = User.objects.get(USER_pkID=user_id)
        user_role = request.session.get('role', 'Guest')
        user_name = user.name if hasattr(user, 'name') else 'Guest'

        user_profile = Profile.objects.filter(user=user).first()

        if user_profile and user_profile.profile_picture:
            user_profile.profile_picture = base64.b64encode(user_profile.profile_picture).decode('utf-8')

    except User.DoesNotExist:
        user_name = 'Guest'
        user_profile = None
        activated_payslip = None

    return render(request, 'Employee/Employee.html', {'user_name': user_name, 'user_role': user_role, 'user': user, 'user_profile': user_profile,})


@csrf_exempt
def profile_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        profile_picture = request.FILES.get('profile_picture')

        user = get_object_or_404(User, pk=user_id)

        profile, created = Profile.objects.get_or_create(user=user)

        profile.profile_picture = profile_picture.read()
        profile.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_activated_payslip(user_id):
    user = get_object_or_404(User, USER_pkID=user_id)
    
    # Fetch all activated payslips for the user
    activated_payslips = Payslip.objects.filter(user=user, activated=True)

    return activated_payslips


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def activated_payslip(request):
    # Get user_id from the session
    user_id = request.session.get('user_id')

    # Fetch all activated payslips for the logged-in user
    activated_payslips = get_activated_payslip(user_id)

    if activated_payslips:
    # Customize the data you want to include in the response
        response_data = {
            'payrolls': [{
                'user': payslip.user.username,
                'monthly_salary': payslip.monthly_salary,
                'full_attendance_count': payslip.full_attendance_count,
                'half_attendance_count': payslip.half_attendance_count,
                'absent_attendance_count': payslip.absent_attendance_count,
                'date_range': payslip.date_range,
                'activated_date': payslip.activated_date.strftime('%Y-%m-%d'),
                'activated': payslip.activated,
            } for payslip in activated_payslips]
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No activated payslips found for the user'})

