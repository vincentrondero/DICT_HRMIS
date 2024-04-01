function displayFileName() {
    var fileInput = document.getElementById('file-upload');
    var fileNameDisplay = document.getElementById('file-name-display');
    fileNameDisplay.textContent = fileInput.files[0].name;
}

function uploadProfilePicture() {
    var fileInput = document.getElementById('file-upload');
    var file = fileInput.files[0];
    var userIdString = document.getElementById('upload-btn').getAttribute('data-user-id');  
    console.log(userIdString)
    var userId = parseInt(userIdString);

    if (isNaN(userId)) {
        console.error('Invalid user ID:', userIdString);
        return;
    }

    var formData = new FormData();
    formData.append('profile_picture', file);
    formData.append('user_id', userId);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/employee_views/profile_view/');

    var csrfToken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.onload = function () {
        if (xhr.status == 200) {
            location.reload();
            cancelUpload();
            console.log('Upload successful');
        } else {
            console.error('Upload failed');
        }
    };

    xhr.send(formData);
}
function cancelUpload() {
    var modal = document.getElementById('profile-picture-modal');
    modal.classList.add('hidden');
}

function openUploadModal() {
    var modal = document.getElementById('profile-picture-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var fileUploadElement = document.getElementById('file-upload');
    var uploadBtnElement = document.getElementById('upload-btn');
    var openModalBtn = document.getElementById('open-modal-btn');

    if (fileUploadElement && uploadBtnElement && openModalBtn) {
        fileUploadElement.addEventListener('change', displayFileName);
        uploadBtnElement.addEventListener('click', uploadProfilePicture);
        openModalBtn.addEventListener('click', openUploadModal);
    }
});

function openPayrollModal() {
    var modal = document.getElementById("payrollModal");
    modal.style.display = "block";
}

function closePayrollModal() {
    var modal = document.getElementById("payrollModal");
    modal.style.display = "none";
}


function openPayslipDetailsModal(payslipId) {
    var payslipDetailsId = `payslipDetailsContent${payslipId}`;
    var selectedPayslipDetails = document.getElementById(payslipDetailsId);
    var payslipDetailsContainer = document.getElementById('payslipDetailsContainer');

    if (selectedPayslipDetails) {
        payslipDetailsContainer.innerHTML = selectedPayslipDetails.innerHTML;

        document.getElementById('payslipDetailsModal').style.display = 'block';
    } else {
        console.error('Payslip details element not found. ID:', payslipDetailsId);
    }
}



function goBackToMainModal() {
    document.getElementById('payslipDetailsModal').style.display = 'none';
    document.getElementById('payrollModal').style.display = 'block';
}

function closePayslipDetailsModal() {
    document.getElementById('payslipDetailsModal').style.display = 'none';
    document.getElementById('payrollModal').style.display = 'none';
}

function openAttendanceModal() {
    // Get the modal element
    var modal = document.getElementById("attendanceModal");
    
    // Show the modal
    modal.style.display = 'block';
    modal.style.remove = 'hidden';
}

function closeAttendanceModal() {
    // Get the modal element
    var modal = document.getElementById("attendanceModal");
    
    // Hide the modal
    modal.style.display = 'none';
}


