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
    document.getElementById("editRemark").value = data.remark;
    document.getElementById("editExcelFile").value = data.excel_file;
    document.getElementById("editGeneratedDate").value = data.generated_date;  
}


function handleEditButtonClick() {
    var editEmployeeValue = document.getElementById("editEmployee").value;
    var editDateValue = document.getElementById("editDate").value;
    var editTimeInValue = document.getElementById("editTimeIn").value;
    var editTimeOutValue = document.getElementById("editTimeOut").value;
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
                    location.reload();
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