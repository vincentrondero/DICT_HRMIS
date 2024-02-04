from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserEditForm, UserCreationForm
from Authentication.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def dashboard_views(request, user_role):
    user_role = request.session.get('role', 'Guest')
    return render(request, 'HR/dashboard.html', {'user_role': user_role})

def manage_payroll(request, user_role):
    return render(request, 'HR/manage_payroll.html', {'user_role': user_role})

def manage_employee(request, user_role):
    active_users = User.objects.filter(role='JO', archived=False)
    archive_users = User.objects.filter(role='JO', archived=True)
    return render(request, 'HR/manage_employee.html' , {'active_users': active_users,  'archive_users':  archive_users, 'user_role': user_role})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return JsonResponse({'success': True, 'message': 'User created successfully'})
        else:
            # If the form is not valid, return the form errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # If the request is not a POST request, render the form
        form = UserCreationForm()
        return render(request, 'HR/manage_employee.html', {'form': form})

def archive_user(request, user_id):
    print(f"Received user_id: {user_id}")
    try:
        user = User.objects.get(USER_pkID=user_id) 
        user.archived = True
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist as e:
        print(f"User not found with ID {user_id}: {e}")
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        print(f"Error archiving user with ID {user_id}: {e}")
        return JsonResponse({'success': False, 'error': 'Internal server error'}, status=500)
    

@csrf_exempt  

def save_user_changes(request, user_pk_id):
    try:
        user = User.objects.get(USER_pkID=user_pk_id)

        if request.method == 'POST':
            
            payload = json.loads(request.body.decode('utf-8'))

          
            form = UserEditForm(payload, instance=user)

            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        import logging
        logging.error(str(e))
        return JsonResponse({'error': 'Internal server error'}, status=500)

def edit_user(request, user_pk_id):
    try:
        user = User.objects.get(USER_pkID=user_pk_id)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
            user_data = {
                'username': user.username,
                'name': user.name,
                'role': user.role,
                'salary_grade': user.salary_grade,
            }
            return JsonResponse(user_data)
        else:
            if request.method == 'POST':
                form = UserEditForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': True, 'message': 'User updated successfully'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            else:
                form = UserEditForm(instance=user)
            return render(request, 'HR/manage_employee.html', {'form': form, 'user': user})

    except User.DoesNotExist:
        return JsonResponse({'error': f'User with USER_pkID {user_pk_id} not found'}, status=404)

    except Exception as e:
        import logging
        logging.error(str(e))
        return JsonResponse({'error': 'Internal server error'}, status=500)