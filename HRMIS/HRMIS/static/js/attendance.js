function openAttendanceEditModal(attendanceId) {
    var modal = document.getElementById("AttendanceEditModal");

    // Make AJAX request to fetch attendance details
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    // Populate modal with fetched data
                    populateAttendanceModal(response.data);
                    modal.style.display = "block";
                } else {
                    console.error('Error fetching attendance details:', response.error);
                }
            } else {
                console.error('Error fetching attendance details. Status:', xhr.status);
            }
        }
    };

    xhr.open("GET", `/hr_views/get_attendance_details/${attendanceId}/`);
    xhr.send();
}
function populateAttendanceModal(data) {
    document.getElementById("editEmployee").value = data.employee;
    document.getElementById("editDate").value = data.date;
    document.getElementById("editTimeIn").value = data.time_in;
    document.getElementById("editTimeOut").value = data.time_out;
    document.getElementById("editMinutesLate").value = data.minutes_late;
    document.getElementById("editUndertimeHours").value = data.undertime_hours;
    document.getElementById("editUndertimeMinutes").value = data.undertime_minutes;
    document.getElementById("editRemark").value = data.remark;
    document.getElementById("editExcelFile").value = data.excel_file;
    document.getElementById("editGeneratedDate").value = data.generated_date;  
}

function handleEditButtonClick() {
    var editEmployeeValue = document.getElementById("editEmployee").value;
    var editDateValue = document.getElementById("editDate").value;
    var editTimeInValue = document.getElementById("editTimeIn").value;
    var editTimeOutValue = document.getElementById("editTimeOut").value;
    var editUndertimeHoursValue = document.getElementById("editUndertimeHours").value;
    var editUndertimeMinutesValue = document.getElementById("editUndertimeMinutes").value;
    var editMinutesLateValue = document.getElementById("editMinutesLate").value;
    var editRemarkValue = document.getElementById("editRemark").value;
    var editExcelFileValue = document.getElementById("editExcelFile").value;
    var editGeneratedDateValue = document.getElementById("editGeneratedDate").value;

    // Prepare data to be sent in the request body
    var requestData = {
        employee: editEmployeeValue,
        date: editDateValue,
        timeIn: editTimeInValue,
        timeOut: editTimeOutValue,
        undertimeHours: editUndertimeHoursValue,
        undertimeMinutes: editUndertimeMinutesValue,
        minutesLate: editMinutesLateValue,
        remark: editRemarkValue,
        excelFile: editExcelFileValue,
        generatedDate: editGeneratedDateValue
        // Add other fields as needed
    };

    // Get the CSRF token from the cookie
    var csrfToken = getCookie('csrftoken');

    // Make an AJAX request to update the attendance data
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    // Show the success modal after successfully saving changes
                    document.getElementById('editSuccessModal').classList.remove('hidden');
                    // Close the edit modal
                    closeAttendanceEditModal();
                } else {
                    console.error('Error updating attendance details:', response.error);
                }
            } else {
                console.error('Error updating attendance details. Status:', xhr.status);
            }
        }
    };

    xhr.open("POST", "/hr_views/update_attendance/");
    
    // Include the CSRF token in the request headers
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    
    xhr.send(JSON.stringify(requestData));
}

function closeAttendanceEditModal() {
    var modal = document.getElementById("AttendanceEditModal");
    modal.style.display = "none";
}

function closeeditSuccessModal() {
    var successModal = document.getElementById("editSuccessModal");
    successModal.classList.add('hidden');
    location.reload();
}

// Function to open the modal
function openAddAttendanceModal() {
    document.getElementById('addAttendanceModal').style.display = 'block';
}

function closeAttendanceEditModal() {
    var modal = document.getElementById("AttendanceEditModal");
    modal.style.display = "none";
}

// Function to open the modal
function openAddAttendanceModal() {
    document.getElementById('addAttendanceModal').style.display = 'block';
}
  
// Function to close the modal
function closeAddAttendanceModal() {
    document.getElementById('addAttendanceModal').style.display = 'none';
}

function calculateMinutesLate() {
    const timeInInput = document.getElementById('time_in');
    const timeIn = new Date(`2000-01-01 ${timeInInput.value}`);

    const thresholdTime = new Date(`2000-01-01 08:00`);

    const timeDifference = timeIn - thresholdTime;
    const minutesLate = Math.max(0, Math.floor(timeDifference / (1000 * 60)));

    document.getElementById('minutes_late').value = minutesLate;
}

function saveAttendance() {
    // Collect form data
    var formData = {
        username: document.querySelector('input[name="username"]').value,
        date: document.querySelector('input[name="date"]').value,
        time_in: document.querySelector('input[name="time_in"]').value,
        time_out: document.querySelector('input[name="time_out"]').value,
        undertime_hours: document.querySelector('input[name="undertime_hours"]').value,
        undertime_minutes: document.querySelector('input[name="undertime_minutes"]').value,
        minutes_late: document.querySelector('input[name="minutes_late"]').value,
        existing_file: document.querySelector('select[name="existing_file"]').value,
        remark: document.querySelector('select[name="remark"]').value
    };

    // Construct the URL for the AJAX request
    var url = "/hr_views/add_attendance/" + formData.username + "/";

    // Send AJAX request to save attendance
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Handle success response
            console.log("Attendance saved successfully.");
            // Open the success modal
            closeAddAttendanceModal();
            openSuccessModal();
        } else {
            // Handle error response
            console.error("Failed to save attendance.");
        }
    };
    xhr.onerror = function() {
        // Handle network errors
        console.error("Network error occurred.");
    };
    xhr.send(JSON.stringify({formData: formData}));
}

function openSuccessModal() {
    var modal = document.getElementById("AddSuccessModal");
    modal.classList.remove("hidden");
}

function closeAddSuccessModal() {
    var modal = document.getElementById("AddSuccessModal");
    modal.classList.add("hidden");
    location.reload(); // Refresh the page
}

// Define variables for pagination
let currentPage = 1;
const totalPages = Math.ceil(document.querySelectorAll("table tbody tr").length / 13);
const prevPageBtn = document.getElementById("prevPageBtn");
const nextPageBtn = document.getElementById("nextPageBtn");

// Add blue-transparent class to the pagination buttons
prevPageBtn.classList.add("blue-transparent");
nextPageBtn.classList.add("blue-transparent");

// Change button text
prevPageBtn.textContent = "Prev";
nextPageBtn.textContent = "Next";

// Function to show the rows for the current page
function showRows() {
    const startIndex = (currentPage - 1) * 13;
    const endIndex = currentPage * 13;

    // Hide all rows
    document.querySelectorAll("table tbody tr").forEach(row => {
        row.style.display = "none";
    });


    // Show rows for the current page
    for (let i = startIndex; i < endIndex; i++) {
        if (i < document.querySelectorAll("table tbody tr").length) {
            document.querySelectorAll("table tbody tr")[i].style.display = "table-row";
        } else {
            break;
        }
    }
}

// Function to go to the previous page
function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        showRows();
    }
}

// Function to go to the next page
function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        showRows();
    }
}

// Initial pagination setup
showRows();