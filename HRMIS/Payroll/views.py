from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserEditForm, UserCreationForm
from Authentication.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def dashboard_views(request, user_role):
    user_role = request.session.get('role', 'Guest')
    users = User.objects.all().count()
    active_users = User.objects.filter(role='JO', archived=False).count()
    return render(request, 'HR/dashboard.html', {'user_role': user_role, 'users': users, 'active_users': active_users})

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
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
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
    
def unarchive_user(request, user_id):
    print(f"Received user_id for unarchive: {user_id}")
    try:
        user = User.objects.get(USER_pkID=user_id)
        user.archived = False
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist as e:
        print(f"User not found with ID {user_id}: {e}")
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        print(f"Error unarchiving user with ID {user_id}: {e}")
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
    
from io import BytesIO
import pandas as pd
import numpy as np
from django.http import HttpResponse
from .models import CleansedData

def extract_timestamps(cell):
    if pd.notna(cell):
        timestamps = [timestamp.strip()[:5] for timestamp in str(cell).split('\n')]
        return timestamps
    return [np.nan]

def upload_and_cleanse(request):
    if request.method == 'POST' and 'file' in request.FILES:
        # Get the uploaded file
        uploaded_file = request.FILES['file']

        # Load user details
        user_df = pd.read_excel(uploaded_file, sheet_name='Logs', header=None)

        # Identify user dates dynamically
        user_dates = user_df.iloc[3, 10::2].astype(str).tolist()

        # Extract user details
        users = []

        # Iterate over rows, starting from row 5 and skipping every other row
        for index in range(4, len(user_df), 2):
            # New user details
            user_details = {'No': user_df.iloc[index, 2], 'Name': user_df.iloc[index, 10]}
            users.append(user_details)

        # Create a DataFrame for user details
        users_df = pd.DataFrame(users)

        # Load attendance details
        attendance_df = pd.read_excel(uploaded_file, sheet_name='Logs', header=None)

        # Identify attendance dates dynamically
        attendance_dates = attendance_df.iloc[3, 0::1].astype(str).tolist()

        # Explicitly set the number of attendance columns based on the length of attendance_dates
        num_attendance_columns = len(attendance_dates)

        # Extract timestamp and timeout timestamp details for each cell
        attendance_data = []

        for index in range(5, len(attendance_df), 2):
            # Extract attendance for the user at the current row
            user_attendance = attendance_df.iloc[index, 0:(1 + num_attendance_columns * 2):1].tolist()

            # Process each cell to extract timestamp and timeout timestamp
            processed_attendance = []
            for cell in user_attendance:
                timestamps = extract_timestamps(cell)
                first_instance = timestamps[0]

                # Check if the last timestamp is present in the last line, otherwise take it from the previous line
                last_instance = timestamps[-1] if '\n' in str(cell).strip()[-1] else timestamps[-2] if len(timestamps) > 1 else np.nan

                processed_attendance.extend([first_instance, last_instance])

            attendance_data.append(processed_attendance)

        # Create a DataFrame for attendance details with first and last instances
        columns = sum([[f'First_{col}', f'Last_{col}'] for col in attendance_dates], [])
        attendance_df = pd.DataFrame(attendance_data, columns=columns[:num_attendance_columns*2])

        # Extract the date range from the Excel sheet
        date_range_str = user_df.iloc[2, 2:12].astype(str).tolist()[0]

        # Remove leading and trailing spaces
        date_range_str = date_range_str.strip()

        # Split the date range string into start and end dates
        start_date_str, end_date_str = date_range_str.split('~')

        # Remove leading and trailing spaces from start and end dates
        start_date_str = start_date_str.strip()
        end_date_str = end_date_str.strip()

        # Determine the year from the first date
        common_year = pd.to_datetime(start_date_str, format='%Y/%m/%d').year

        # Convert start and end dates to datetime objects
        start_date = pd.to_datetime(start_date_str, format='%Y/%m/%d')
        end_date = pd.to_datetime(f'{common_year}/{end_date_str}', format='%Y/%m/%d')

        # Format the date strings
        formatted_start_date = start_date.strftime('%B_%d')
        formatted_end_date = end_date.strftime('%d_%Y')

        # Generate the output Excel file name based on the formatted date range
        date_range = f"{formatted_start_date}-{formatted_end_date}"
        output_excel = f'attendance_{date_range}.xlsx'

        # Merge user details and attendance details by row index
        merged_df = pd.concat([users_df, attendance_df], axis=1)

        # Save the merged DataFrame to an Excel file
        merged_df.to_excel(output_excel, index=False)

        # Save the cleansed data to a new Excel file
        cleaned_output_excel = BytesIO()
        merged_df.to_excel(cleaned_output_excel, index=False)
        cleaned_output_excel.seek(0)

        # Save the cleansed data to the database
        cleansed_data_instance = CleansedData(file_name=output_excel, file_binary=cleaned_output_excel.read())
        cleansed_data_instance.save()


        return HttpResponse("File uploaded and cleansed successfully. Cleansed data saved to the database.")

    return HttpResponse("File upload failed.")

from .forms import CleansedDataSelectionForm
def view_excel_content(request):
    if request.method == 'POST':
        form = CleansedDataSelectionForm(request.POST)

        if form.is_valid():
            # Retrieve the selected CleansedData instance
            cleansed_data = form.cleaned_data['cleansed_data']

            # Read the binary data and convert it to a DataFrame
            binary_data = BytesIO(cleansed_data.file_binary)
            df = pd.read_excel(binary_data)

            # Convert the DataFrame to HTML for rendering
            html_content = df.to_html()

            return HttpResponse(html_content)
    else:
        form = CleansedDataSelectionForm()

    return render(request, 'HR/manage_payroll.html', {'form': form})