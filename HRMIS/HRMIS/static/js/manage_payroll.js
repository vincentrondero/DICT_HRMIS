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

function calculateSalary(username) {
    console.log('Username:', username);
    $.ajax({
        url: `/hr_views/calculate_salary/${username}/`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            $('#dailySalary').text(data.daily_salary);
            $('#basic_salary').text(data.basic_salary);
            $('#cooperative_deduction').text(data.cooperative_deduction);
            $('#premium').text(data.premium);
            $('#another_gross_pay').text(data.gross_pay);
            $('#gross_pay').text(data.gross_pay);
            $('#fullAttendanceCount').text(data.full_attendance_count);
            $('#halfAttendanceCount').text(data.half_attendance_count);
            $('#absentAttendanceCount').text(data.absent_count);
            $('#dateRange').text(data.date_range);
            $('#employeeName').text(data.name);
            $('#employeeId').text(username);late_count
            $('#late_count').text(data.late_attendance_count);
            $('#late_deduction').text(data.late_deduction);
            $('#member_status').text(data.member_status);
            $('#absent_deduction').text(data.absent_deduction);
            $('#pre_deduction').text(data.pre_deduction);
            $('#total_deduction').text(data.total_deduction);
            $('#net_before_tax').text(data.net_before_tax)
            $('#2_percent').text(data.tax_2_percent);
            $('#3_percent').text(data.tax_3_percent);
            $('#number_of_days').text(data.number_of_days);
            $('#total_net_pay').text(data.total_net_pay);
            $('#current_date').text(data.current_date);

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
    console.log('clicked')
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
        jsPDF: { unit: 'mm', format: [162, 125], orientation: 'portrait' },
        onAfterPdf: function (pdf) {
            $('#pdfContent').hide();
        }
    });
}

function fetchUserAttendance(username) {
    console.log('Username:', username);
    userRole = 'HR'
    console.log('User Role:', userRole);
    window.location.href = `/hr_views/get_user_attendance/${userRole}/${username}/`;
}

// Function to show the progress bar
function showProgressBar() {
    document.getElementById('progress-bar-container').style.display = 'inline-block';
}

// Function to update the progress bar
function updateProgressBar(progress) {
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = progress + '%';
    progressBar.innerText = progress + '%';
    console.log('Progress:', progress);
}

// Function to simulate the import process
function simulateImportProcess(cleansedDataId) {
    let progress = 0;
    const targetProgress = 100;
    const duration = 80;
    const frames = 100;
    const increment = targetProgress / frames;

    const interval = setInterval(() => {
        progress += increment;
        if (progress >= targetProgress) {
            clearInterval(interval);
            progress = targetProgress;
            updateProgressBar(progress);
            showDataSuccessModal();
        } else {
            updateProgressBar(progress);
        }
    }, duration / frames);
}

// Function to handle the save button click
function handleSaveButtonClick(cleansedDataId) {
    const fileInput = document.getElementById('file-upload');
    if (fileInput.files.length > 0) {
        showProgressBar();
        simulateImportProcess(cleansedDataId);
    }
}

// Function to show the Import Data Success Modal
function showDataSuccessModal() {
    const successModal = document.getElementById('DataSuccessModal');
    successModal.style.display = 'flex';
}

// Function to hide the Import Data Success Modal
function hideDataSuccessModal() {
    const successModal = document.getElementById('DataSuccessModal');
    successModal.style.display = 'none';
}

// Event listener for the close button
document.getElementById('close-modal-button').addEventListener('click', function() {
    hideDataSuccessModal();
});

// Function to enable/disable the Save button based on file selection
document.getElementById('file-upload').addEventListener('change', function() {
    const saveButton = document.getElementById('save-button');
    saveButton.disabled = this.files.length === 0;
});