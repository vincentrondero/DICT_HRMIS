function openCleansedDataModal() {
    var cleansedDataModal = document.getElementById('cleansedDataModal');
    if (cleansedDataModal) {
        cleansedDataModal.style.display = 'block';
    }
}

function closeCleansedDataModal() {
    var cleansedDataModal = document.getElementById('cleansedDataModal');

    if (cleansedDataModal) {
        cleansedDataModal.style.display = 'none';
    }
}
function openImportModal() {
    var uploadModal = document.getElementById('importDataModal');
    if (uploadModal) {
        uploadModal.style.display = 'block';
    }
}

function closeImportModal() {
    var uploadModal = document.getElementById('importDataModal');
    if (uploadModal) {
        uploadModal.style.display = 'none';
    }
}
function toggleSpeedDial() {
    const toggleButton = document.querySelector('[data-dial-toggle]');
    const menu = document.querySelector('#speed-dial-menu-square');

    menu.classList.toggle('hidden');
    const expanded = toggleButton.getAttribute('aria-expanded') === 'true' || false;
    toggleButton.setAttribute('aria-expanded', !expanded);
    toggleButton.classList.toggle('rotate-45', !expanded);
    if (expanded) {
        toggleButton.classList.remove('bg-red-200')
        toggleButton.classList.remove('focus:ring-4');
        toggleButton.classList.remove('focus:outline-none');
        toggleButton.classList.remove('focus:ring-red-300');
        toggleButton.classList.remove('hover:bg-red-400');
        toggleButton.classList.add('bg-blue-500');
    } else {
        toggleButton.classList.remove('bg-blue-500');
        toggleButton.classList.add('bg-red-200');
        toggleButton.classList.add('focus:ring-4');
        toggleButton.classList.add('focus:outline-none');
        toggleButton.classList.add('focus:ring-red-300');
        toggleButton.classList.add('hover:bg-red-400');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('[data-dial-toggle]');
    toggleButton.classList.add('bg-blue-500');
    toggleButton.addEventListener('click', toggleSpeedDial);
});

function viewExcel(cleansedDataId) {
    console.log('button clicked')
    $.ajax({
        url: '/hr_views/view_excel_content/' + cleansedDataId + '/',
        type: 'GET',
        success: function(response) {
            var newWindow = window.open();
            newWindow.document.write(response);
        },
        error: function(xhr, status, error) {
            console.error('Error fetching Excel content:', error);
        }
    });
}
function updateFileName(input) {
    var fileName = input.files[0].name;
    var fileNameDisplay = document.getElementById('file-name');
    fileNameDisplay.textContent = fileName;
    fileNameDisplay.classList.remove('hidden');
}

function saveAttendance(cleansedDataId) {
    console.log('Save Attendance for Cleansed Data ID:', cleansedDataId);

    fetch('/hr_views/save-attendance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: `cleansedDataId=${cleansedDataId}`,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Attendance saved successfully:', data);
    })
    .catch(error => {
        console.error('Error saving attendance:', error);
    });
}
function showUserAttendance(username) {
    $.ajax({
        url: `get_latest_attendance/${username}/`,
        type: 'GET',
        success: function(data) {
            if ('error' in data) {
                alert(data.error);
            } else {
                // Clear existing content
                $('#userAttendanceDetails').empty();

                // Loop through each attendance entry and append to the modal content
                var tableBody = $('#attendanceModal tbody');
                tableBody.empty();

                data.attendances.forEach(function(attendance) {
                    var rowHtml = `
                        <tr>
                            <td class="px-4 py-2">${attendance.date}</td>
                            <td class="px-4 py-2">${attendance.time_in}</td>
                            <td class="px-4 py-2">${attendance.time_out}</td>
                            <td class="px-4 py-2">${attendance.remark}</td>
                            <td class="px-4 py-2">
                            <button type="button" class="bg-red-100 hover:bg-yellow-500 text-yellow-500 font-semibold hover:text-white py-2 px-4 border border-yellow-500 hover:border-transparent rounded mr-2" onclick="editAttendance()">Edit</button>
                            </td>
                        </tr>`;
                    tableBody.append(rowHtml);
                });

                // Show the modal
                $('#attendanceModal').show();
            }
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

// Function to close the modal
function closeAttendanceModal() {
    $('#attendanceModal').hide();
}
function calculateSalary(username) {
    // Use jQuery.ajax() to make the asynchronous request
    console.log('Username:', username);
    $.ajax({
        url: `/hr_views/calculate_salary/${username}/`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            // Update the modal content with the calculated values
            $('#dailySalary').text(data.daily_salary);
            $('#fullAttendanceCount').text(data.full_attendance_count);
            $('#halfAttendanceCount').text(data.half_attendance_count);
            $('#absentAttendanceCount').text(data.absent_attendance_count);
            $('#monthlySalary').text(data.monthly_salary);
            $('#dateRange').text(data.date_range);
            $('#employeeName').text(data.employee_name);
            $('#employeeId').text(username);
            // Show the modal
            $('#salaryModal').show();
        },
        error: function(error) {
            console.error('Error calculating salary:', error);
        }
    });
}

// Close modal when clicking the close button
function closeSalaryModal() {
    $('#salaryModal').hide();
}

// Close modal when clicking outside the modal content
$(window).click(function(event) {
    if (event.target.id === 'salaryModal') {
        $('#salaryModal').hide();
    }
});

// Function to open the activate payslip modal
function openActivatePayslipModal(username) {
    $('#activatePayslipModal').attr('data-username', username);
    $('#activatePayslipModal').show();
}

// Function to close the activate payslip modal
function closeActivatePayslipModal() {
    $('#activatePayslipModal').hide();
}

function activatePayslip() {
    var username = $('#activatePayslipModal').data('username');
    var csrftoken = getCookie('csrftoken');

    // Make a GET request to calculate_salary endpoint
    $.ajax({
        url: `/hr_views/calculate_salary/${username}/`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log('calculate_salary response:', data);

            // Use the returned data as the payload for the activate_payslip endpoint
            $.ajax({
                url: `/hr_views/activate_payslip/${username}/`,
                method: 'POST',
                data: JSON.stringify(data),  // Send the data as JSON string
                contentType: 'application/json',  // Specify the content type
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(response) {
                    console.log('Payslip activated successfully:', response);
                    // Optionally, perform additional actions or close the modal
                },
                error: function(error) {
                    console.error('Error activating payslip:', error.responseText);
                    // Display a user-friendly error message or handle the error
                }
            });
        },
        error: function(error) {
            console.error('Error calculating salary:', error);
            // Display a user-friendly error message or handle the error
        }
    });
}
function downloadPdf() {
    // Show the PDF content section
    $('#pdfContent').show();

    // Capture the PDF content
    const element = document.getElementById('pdfContent');

    // Use html2pdf to generate the PDF
    html2pdf(element, {
        margin: 5,
        filename: 'salary_receipt.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: [160, 105], orientation: 'portrait' },
        onAfterPdf: function (pdf) {
            $('#pdfContent').hide();
        }
    });
}