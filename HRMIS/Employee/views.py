from django.shortcuts import render
from Authentication.models import User, Profile
from Payroll.models import Payslip, Attendance
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
        user_category = user.category if hasattr(user, 'category') else 'TOD'

        user_profile = Profile.objects.filter(user=user).first()

        if user_profile and user_profile.profile_picture:
            user_profile.profile_picture = base64.b64encode(user_profile.profile_picture).decode('utf-8')

        try:
            last_generated_date = user.attendance_set.latest('generated_date').generated_date
            all_attendances = Attendance.objects.filter(employee=user, generated_date__date=last_generated_date.date())
        except Attendance.DoesNotExist:
            last_generated_date = None
            all_attendances = None

        user_payslips = Payslip.objects.filter(user=user, activated=True)

    except User.DoesNotExist:
        user_name = 'Guest'
        user_profile = None
        user_payslips = None
        user_category = 'TOD'

    return render(request, 'Employee/Employee.html', {'user_name': user_name, 'user_role': user_role, 'user': user, 'user_profile': user_profile, 'user_payslips': user_payslips, 'all_attendances':all_attendances, 'user_category': user_category})

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
