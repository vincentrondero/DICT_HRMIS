from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import UserEditForm, UserCreationForm
from Authentication.models import User
from .models import CleansedData, Attendance, Payslip, SalaryGrade
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from io import BytesIO
import pandas as pd
import numpy as np
from .models import CleansedData
from django.db.models import Min, Max
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime
import math


def dashboard_views(request, user_role):
    user_role = request.session.get('role', 'Guest')
    
    users = User.objects.filter(role='JO').count()
    active_users = User.objects.filter(role='JO', archived=False).count()
    archive_users = User.objects.filter(role='JO', archived=True).count()
    
    attendance_count = Attendance.objects.all().count()
    full_day_attendance_count = Attendance.objects.filter(remark='FULL').count()
    late_attendance_count = Attendance.objects.filter(remark='LATE').count()
    absent_attendance_count = Attendance.objects.filter(remark='ABSENT').count()

    percentage_full_attendance = 0
    percentage_late_attendance = 0
    percentage_absent_attendance = 0

    if attendance_count > 0:
        percentage_full_attendance = round(((full_day_attendance_count / attendance_count) * 100))
        percentage_late_attendance = round(((late_attendance_count / attendance_count) * 100))
        percentage_absent_attendance =round(( (absent_attendance_count / attendance_count) * 100))

    context = {
        'user_role': user_role,
        'users': users,
        'active_users': active_users,
        'archive_users': archive_users,
        'attendance_count': attendance_count,
        'full_day_attendance_count': full_day_attendance_count,
        'late_attendance_count': late_attendance_count,
        'absent_attendance_count': absent_attendance_count,
        'percentage_full_attendance': percentage_full_attendance,
        'percentage_late_attendance': percentage_late_attendance,
        'percentage_absent_attendance': percentage_absent_attendance,
    }

    return render(request, 'HR/dashboard.html', context)



from django.db.models import Max
def manage_payroll(request, user_role):
    latest_generated_dates = Attendance.objects.values('employee').annotate(latest_date=Max('generated_date'))

    users_with_attendance = User.objects.filter(attendance__generated_date__in=latest_generated_dates.values('latest_date'))
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


class SaveAttendanceView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def calculate_remark(self, time_in, time_out, date):
        minutes_late = 0 
        if pd.isna(time_in) or pd.isna(time_out):
            # Treat as half day if either time entry is NaN
            return 'HALF', 0
        elif not time_in or not time_out:
            return 'ABSENT', 0
        else:
            # Convert time_in and time_out to datetime.time objects with format %H:%M
            time_in = datetime.strptime(str(time_in), "%H:%M").time()
            time_out = datetime.strptime(str(time_out), "%H:%M").time()

            # Calculate hours worked (round up to the nearest whole number)
            hours_worked = math.ceil(abs((datetime.combine(date, time_out) - datetime.combine(date, time_in)).seconds) / 3600)

            # Classify based on the criteria
            if hours_worked >= 8:
                if date.weekday() == 0:  # Monday
                    if time_in > datetime.strptime("08:00", "%H:%M").time():
                        minutes_late = (time_in.hour - 8) * 60 + time_in.minute
                        return 'LATE', minutes_late
                elif 1 <= date.weekday() <= 4:  # Tuesday to Friday
                    if time_in > datetime.strptime("09:00", "%H:%M").time():
                        minutes_late = (time_in.hour - 9) * 60 + time_in.minute
                        return 'LATE', minutes_late
                return 'FULL', 0
            elif 4 <= hours_worked < 8:
                if date.weekday() == 0:  # Monday
                    if time_in > datetime.strptime("12:00", "%H:%M").time():
                        minutes_late = (time_in.hour - 12) * 60 + time_in.minute
                        return 'LATE', minutes_late
                elif 1 <= date.weekday() <= 4:  # Tuesday to Friday
                    if time_in > datetime.strptime("12:00", "%H:%M").time():
                        minutes_late = (time_in.hour - 12) * 60 + time_in.minute
                        return 'LATE', minutes_late
                return 'HALF', 0
            else:
                return 'ABSENT', 0



    def post(self, request, *args, **kwargs):
        try:
            # Get cleansed data ID from the request
            cleansed_data_id = int(request.POST.get('cleansedDataId'))
            cleansed_data = CleansedData.objects.get(id=cleansed_data_id)

            # Assuming the Excel file is binary data stored in the 'file_binary' field
            file_content = cleansed_data.file_binary.tobytes()

            # Wrap the byte string in a BytesIO object
            file_content_io = BytesIO(file_content)

            # Assuming the Excel file format is supported by pandas (e.g., .xlsx)
            df = pd.read_excel(file_content_io)

            # Iterate through rows using iterrows
            for index, row in df.iterrows():
                employee_id = int(row['No'])

                # Check if the employee_id exists in the User model
                user = User.objects.filter(username=str(employee_id)).first()
                if not user:
                    print(f"Skipping row {index + 2} (Employee ID {employee_id}): No matching user found")
                    continue

                filename_parts = cleansed_data.file_name.split('_')
                month_str = filename_parts[1].capitalize()
                year_str = filename_parts[3].split('.')[0]

                # Iterate through relevant columns within each row
                for col_name in df.columns:
                    if col_name.startswith('First_') and col_name.replace('First_', '').isdigit():
                        col_index = int(col_name.replace('First_', ''))

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

                        # Check if both time entries are empty and it's a weekend
                        if not time_in and not time_out and date.weekday() >= 5:
                            print(f"Skipping row {index + 2} (Employee ID {employee_id}): Both time entries are empty, but it's a weekend")
                            continue

                        print(f"Processing row {index + 2} (Employee ID {employee_id}), Date: {date}, Time In: {time_in}, Time Out: {time_out}")

                        # Calculate the remark based on time_in, time_out, and date
                        remark, minutes_late = self.calculate_remark(time_in, time_out, date)

                        # Check if an attendance record already exists for the user and date
                        existing_attendance = Attendance.objects.filter(employee=user, date=date).first()

                        if existing_attendance:
                            print(f"Attendance record already exists for Employee ID {employee_id}, Date: {date}")
                        else:
                            # Creating the Attendance record
                            Attendance.objects.create(
                                employee=user,
                                date=date,
                                time_in=time_in if time_in else None,
                                time_out=time_out if time_out else None,
                                excel_file=cleansed_data,
                                remark=remark,
                                minutes_late=minutes_late
                            )

            return JsonResponse({'success': True, 'message': 'Attendance saved successfully'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})




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

from django.db.models import Sum

def calculate_salary(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        user_name = user.name

        salary_grades = {str(grade.grade): grade.salary for grade in SalaryGrade.objects.all()}

        user_salary_grade_str = str(user.salary_grade)

        if user_salary_grade_str in salary_grades:
            daily_salary = salary_grades[user_salary_grade_str]
          # Fetch all attendance entries for the user based on the last generated date
            last_generated_date = user.attendance_set.latest('generated_date').generated_date
            all_attendances = Attendance.objects.filter(employee=user, generated_date__date=last_generated_date.date())

            # Calculate the number of days in the date range
            number_of_days = all_attendances.count()

            min_date = all_attendances.aggregate(Min('date'))['date__min']
            max_date = all_attendances.aggregate(Max('date'))['date__max']

            date_range = f"{min_date.strftime('%B %d, %Y')} - {max_date.strftime('%B %d, %Y')}"

            full_attendance_count = all_attendances.filter(remark='FULL').count()
            half_attendance_count = all_attendances.filter(remark='HALF').count()
            absent_attendance_count = all_attendances.filter(remark='ABSENT').count()
            late_attendance_count = all_attendances.filter(remark='LATE').count()

            full_day_salary = daily_salary * full_attendance_count
            half_day_salary = (daily_salary * half_attendance_count) / 2
            monthly_salary = full_day_salary + half_day_salary

            # Calculate late deduction
            total_late_minutes = all_attendances.aggregate(Sum('minutes_late'))['minutes_late__sum']
            late_deduction = round((daily_salary / 22) / 480 * total_late_minutes, 2)


            # Calculate absent deduction
            absent_deduction = round((daily_salary / 22) * absent_attendance_count, 2)

            #Calculate absent + late deduction
            pre_deduction = round(( absent_deduction + late_deduction),2)

            # Calculate basic salary and premium
            basic_salary = round(monthly_salary,4)
            premium =round( (0.2 * basic_salary ) , 4) 

            # Calculate gross pay
            gross_pay = basic_salary + premium

            # Calculate net before tax
            net_before_tax = gross_pay - (late_deduction + absent_deduction)

            # Calculate tax
            tax_2_percent =round(( 0.02 * net_before_tax),2)
            tax_3_percent =round(( 0.03 * net_before_tax),2)

            # Calculate total deduction
            total_deduction = round( late_deduction + absent_deduction + tax_2_percent + tax_3_percent,4)

            # Calculate total net pay
            total_net_pay =round( gross_pay - total_deduction, 4)

            current_date = datetime.now().date()

            return JsonResponse({
                'username': username,
                'name': user_name,
                'basic_salary': basic_salary,
                'premium': premium,
                'gross_pay': gross_pay,
                'daily_salary': daily_salary,
                'total_late_minutes': total_late_minutes,
                'late_attendance_count':late_attendance_count,
                'late_deduction': late_deduction,
                'absent_count': absent_attendance_count,
                'absent_deduction': absent_deduction,
                'pre_deduction': pre_deduction,
                'total_deduction': total_deduction,
                'net_before_tax': net_before_tax,
                'tax_2_percent': tax_2_percent,
                'tax_3_percent': tax_3_percent,
                'number_of_days': number_of_days,
                'date_range': date_range,
                'total_net_pay': total_net_pay,
                'current_date':current_date,
            })
        else:
            return JsonResponse({'error': 'Invalid salary grade'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def activate_payslip(request, username):
    print('Request method:', request.method)

    if request.method == 'POST':
        try:
            # Extract the JSON data from the request body
            salary_data = json.loads(request.body.decode('utf-8'))

            # Extract the data from the JSON data
            basic_salary = salary_data.get('basic_salary')
            premium = salary_data.get('premium')
            gross_pay = salary_data.get('gross_pay')
            daily_salary = salary_data.get('daily_salary')
            total_late_minutes = salary_data.get('total_late_minutes')
            late_attendance_count = salary_data.get('late_attendance_count')
            late_deduction = salary_data.get('late_deduction')
            absent_count = salary_data.get('absent_count')
            absent_deduction = salary_data.get('absent_deduction')
            pre_deduction = salary_data.get('pre_deduction')
            total_deduction = salary_data.get('total_deduction')
            net_before_tax = salary_data.get('net_before_tax')
            tax_2_percent = salary_data.get('tax_2_percent')
            tax_3_percent = salary_data.get('tax_3_percent')
            number_of_days = salary_data.get('number_of_days')
            date_range = salary_data.get('date_range')
            total_net_pay = salary_data.get('total_net_pay')
            current_date = salary_data.get('current_date')

            # Get the user object
            user = get_object_or_404(User, username=username)

            # Create and save the Payslip instance
            payslip = Payslip.objects.create(
                user=user,
                basic_salary=basic_salary,
                premium=premium,
                gross_pay=gross_pay,
                daily_salary=daily_salary,
                total_late_minutes=total_late_minutes,
                late_attendance_count=late_attendance_count,
                late_deduction=late_deduction,
                absent_count=absent_count,
                absent_deduction=absent_deduction,
                pre_deduction=pre_deduction,
                total_deduction=total_deduction,
                net_before_tax=net_before_tax,
                tax_2_percent=tax_2_percent,
                tax_3_percent=tax_3_percent,
                number_of_days=number_of_days,
                date_range=date_range,
                total_net_pay=total_net_pay,
                current_date=current_date,
                activated=True
            )

            return JsonResponse({'success': 'Payslip activated successfully'})
        except Exception as e:
            # Handle any exceptions or errors during the creation
            return JsonResponse({'error': f'Error activating payslip: {e}'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

