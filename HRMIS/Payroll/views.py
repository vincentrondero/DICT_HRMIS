from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import UserEditForm, UserCreationForm
from Authentication.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from io import BytesIO
import pandas as pd
import numpy as np
from .models import CleansedData
from django.contrib import messages


def dashboard_views(request, user_role):
    user_role = request.session.get('role', 'Guest')
    users = User.objects.all().count()
    active_users = User.objects.filter(role='JO', archived=False).count()
    return render(request, 'HR/dashboard.html', {'user_role': user_role, 'users': users, 'active_users': active_users})

from django.db.models import Max
def manage_payroll(request, user_role):
    latest_generated_dates = Attendance.objects.values('employee').annotate(latest_date=Max('generated_date'))

    users_with_attendance = User.objects.filter(attendance__generated_date__in=latest_generated_dates.values('latest_date'))
    print(users_with_attendance)
    cleansed_data_list = CleansedData.objects.all()

    return render(request, 'HR/manage_payroll.html', {'user_role': user_role, 'cleansed_data_list': cleansed_data_list, 'users_with_attendance': users_with_attendance})



def manage_employee(request, user_role):
    active_users = User.objects.filter(role='JO', archived=False)
    archive_users = User.objects.filter(role='JO', archived=True)
    return render(request, 'HR/manage_employee.html' , {'active_users': active_users,  'archive_users':  archive_users, 'user_role': user_role,})

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
        output_excel = f'{date_range}.xlsx'

        # Merge user details and attendance details by row index
        merged_df = pd.concat([users_df, attendance_df], axis=1)

        # Save the merged DataFrame to an Excel file in BytesIO
        output_excel_io = BytesIO()
        merged_df.to_excel(output_excel_io, index=False)
        output_excel_io.seek(0)

        # Save the cleansed data to the database without saving locally
        cleansed_data_instance = CleansedData(file_name=output_excel, file_binary=output_excel_io.read())
        cleansed_data_instance.save()

        return redirect('manage_payroll', user_role='HR')


def view_excel_content(request, cleansed_data_id):
    cleansed_data = get_object_or_404(CleansedData, pk=cleansed_data_id)

    # Read the binary data and convert it to a DataFrame
    binary_data = BytesIO(cleansed_data.file_binary)
    df = pd.read_excel(binary_data)

    # Convert the DataFrame to HTML with styling
    html_content = df.to_html(classes='styled-table', index=False, escape=False)

    # Add custom styles and set the page title
    html_content = f"""
    <html>
    <head>
        <title>{cleansed_data.file_name}</title>
        <style>
            .styled-table {{
                border-collapse: collapse;
                width: 100%;
                font-size: 12px;
                text-align: left;
            }}
            .styled-table th, .styled-table td {{
                padding: 5px 5px;
                border-bottom: 1px solid #ddd;
                text-align: center;
            }}
            .styled-table th {{
                background-color: #0F5FC2;
                color:#FFFFFF;
            }}
            .styled-table tbody tr:hover {{
                background-color: #CDF4FF;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    return HttpResponse(html_content)

from django.utils.decorators import method_decorator
from django.views import View
from .models import CleansedData, User, Attendance
from datetime import datetime
import math

class SaveAttendanceView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def calculate_remark(self, time_in, time_out, date):
        if pd.isna(time_in) or pd.isna(time_out):
            # Treat as half day if either time entry is NaN
            return 'HALF'
        else:
            # Convert time_in and time_out to datetime.time objects with format %H:%M
            time_in = datetime.strptime(str(time_in), "%H:%M").time()
            time_out = datetime.strptime(str(time_out), "%H:%M").time()

            # Calculate hours worked (round up to the nearest whole number)
            hours_worked = math.ceil(abs((datetime.combine(date, time_out) - datetime.combine(date, time_in)).seconds) / 3600)

            # Classify based on the criteria
            if hours_worked >= 8:
                return 'FULL'
            elif 4 <= hours_worked < 8:
                return 'HALF'
            else:
                return 'ABSENT'

    def post(self, request, *args, **kwargs):
        try:
            cleansed_data_id = int(request.POST.get('cleansedDataId'))
            cleansed_data = CleansedData.objects.get(id=cleansed_data_id)

            # Assuming the Excel file is binary data stored in the 'file_binary' field
            file_content = cleansed_data.file_binary.tobytes()

            # Wrap the byte string in a BytesIO object
            file_content_io = BytesIO(file_content)

            # Assuming the Excel file format is supported by pandas (e.g., .xlsx)
            df = pd.read_excel(file_content_io)

            # Find the index of the columns "First_1" and "Last_1"
            first_col_index = df.columns.get_loc("First_1")

            # Use filter to select columns starting from "First_" and ending with "Last_"
            relevant_columns = df.filter(regex=f'^First_.*|Last_.*$')

            # Check if there are any relevant columns
            if not relevant_columns.empty:
                for index, row in df.iterrows():
                    employee_id = int(row['No'])

                    filename_parts = cleansed_data.file_name.split('_')
                    month_str = filename_parts[1].capitalize()
                    year_str = filename_parts[3].split('.')[0]

                    # Iterate through relevant columns
                    for col_name in relevant_columns:
                        col_index_str = col_name.split('_')[1]
                        
                        # Handle the case where col_index_str is a float or a string that can be converted to int
                        try:
                            col_index = int(float(col_index_str))  # Convert float to int
                        except ValueError:
                            print(f"Skipping row {index + 2} (Employee ID {employee_id}): Invalid column index")
                            continue

                        date_str = f"{month_str} {col_index}, {year_str}"

                        try:
                            date = datetime.strptime(date_str, '%B %d, %Y').date()
                        except Exception as e:
                            print(f"Error parsing date: {e}")
                            raise  # Reraise the exception for better debugging

                        time_in = row.get(f'First_{col_index}', '')
                        time_out = row.get(f'Last_{col_index}', '')

                        # Replace nan values with an empty string
                        if pd.isna(time_in):
                            time_in = ''
                        if pd.isna(time_out):
                            time_out = ''

                        # Skip rows where both time entries are empty
                        if not time_in and not time_out:
                            print(f"Skipping row {index + 2} (Employee ID {employee_id}): Both time entries are empty")
                            continue

                        # Handle the case where one of the time entries is missing
                        if not time_in or not time_out:
                            print(f"Skipping row {index + 2} (Employee ID {employee_id}): Incomplete time entries")
                            continue

                        print(f"Processing row {index + 2} (Employee ID {employee_id}), Date: {date}, Time In: {time_in}, Time Out: {time_out}")

                        # Calculate the remark based on time_in, time_out, and date
                        remark = self.calculate_remark(time_in, time_out, date)

                        # Creating the Attendance record
                        Attendance.objects.create(
                            employee_id=employee_id,
                            date=date,
                            time_in=time_in,
                            time_out=time_out,
                            excel_file=cleansed_data,
                            remark=remark
                        )
            else:
                print("No relevant columns found.")

            return JsonResponse({'success': True, 'message': 'Attendance saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

# views.py
from django.http import JsonResponse
from .models import Attendance

def get_latest_attendance(request, username):
    user = User.objects.get(username=username)
    print(f"Received username: {username}")
    attendances = Attendance.objects.filter(employee=user)

    attendance_data = []
    for attendance in attendances:

        data = {
            'date': attendance.date,
            'time_in': attendance.time_in,
            'time_out': attendance.time_out,
            'remark': attendance.get_remark_display(),
        }
        attendance_data.append(data)

    return JsonResponse({'attendances': attendance_data})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Authentication.models import User


from django.db.models import Count
from django.utils import timezone

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User, Attendance

def calculate_salary(request, username):
    if request.method == 'GET':
        # Your logic to fetch the user's salary grade
        user = get_object_or_404(User, username=username)

        # Define a dictionary with predefined salary grades and their daily salaries
        salary_grades = {
            '1': 626.3636,
            '2': 662.6364,
            '3': 703.9091,
            '4': 747.4091,
            '5': 793.3182,
            '6': 842.7273,
            '7': 893.8182,
            '8': 957.6818,
            '9': 1018.9091,
            '10': 1117.5909,
            '11': 1321.5909,
            '12': 1423.1818,
            '13': 1527.7727,
            '14': 1652.7727,
            '15': 1789.4091,
            '16': 1941.5455,
            '17': 2107.0455,
            '18': 2290.0909,
            '19': 2581.3636,
            '20': 2884.7727,
            '21': 3223.3182,
            '22': 3606.7727,
            '23': 4058.2273,
            '24': 4585.8182,
            '25': 5227.8182,
            '26': 5871.0909,
            '27': 6675.4091,
            '28': 7542.3182,
            '29': 8523.8636,
            '30': 9631.9091,
            '31': 14490.2727,
            '32': 17352.1818,
            '33': 20829.8182,
        }

        # Convert the user's salary grade to a string
        user_salary_grade_str = str(user.salary_grade)

        # Check if the user's salary grade is in the predefined grades
        if user_salary_grade_str in salary_grades:
            # Get the daily salary based on the user's salary grade
            daily_salary = salary_grades[user_salary_grade_str]

            # Fetch the latest generated_date with attendance "Full"
            try:
                latest_full_attendance = Attendance.objects.filter(
                    employee=user,
                    remark='FULL'
                ).latest('generated_date')
            except Attendance.DoesNotExist:
                latest_full_attendance = None

            # Count the number of remarks where attendance is "Full"
            full_attendance_count = 0
            if latest_full_attendance:
                full_attendance_count = Attendance.objects.filter(
                    employee=user,
                    remark='FULL',
                    generated_date=latest_full_attendance.generated_date
                ).count()

            # Assuming 22 working days in a month
            days_in_month = 22

            # Calculate the monthly salary
            monthly_salary = daily_salary * (days_in_month - full_attendance_count)
            print(days_in_month - full_attendance_count)
            return JsonResponse({
                'daily_salary': daily_salary,
                'monthly_salary': monthly_salary,
                'full_attendance_count': full_attendance_count
            })
        else:
            return JsonResponse({'error': 'Invalid salary grade'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

