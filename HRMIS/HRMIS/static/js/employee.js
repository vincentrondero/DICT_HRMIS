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

    $.ajax({
        url: '/employee_views/activated_payslip/',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            // Handle the received data and populate the modal
            if (data && data.payrolls && Array.isArray(data.payrolls) && data.payrolls.length > 0) {
                // Assuming you have a function to populate the modal
                populatePayrollModal(data.payrolls);
            } else {
                // Show the "NO DATA FOUND" modal
                showNoDataModal();
            }
        },        
        error: function(error) {
            // Handle the error case
            console.error('Error fetching activated payslips:', error);
            alert('Error fetching activated payslips. Please try again.');
        }
    });
}


function populatePayrollModal(payrolls) {
    var modal = $('#payrollModal');
    var payrollDetailsContainer = $('#payrollDetailsContainer');

    payrollDetailsContainer.empty();

    payrolls.forEach(function (payroll) {
        var payrollCard = $('<div>').addClass('payroll-card bg-white p-4 rounded-b-md shadow-md border-t-8 border-green-500');
        payrollCard.append($('<p>').addClass('font-bold').text('User: ' + payroll.user));
        payrollCard.append($('<p>').text('Monthly Salary: ' + payroll.monthly_salary));
        payrollCard.append($('<p>').text('Full Attendance Count: ' + payroll.full_attendance_count));
        payrollCard.append($('<p>').text('Half Attendance Count: ' + payroll.half_attendance_count));
        payrollCard.append($('<p>').text('Absent Attendance Count: ' + payroll.absent_attendance_count));
        payrollCard.append($('<p>').text('Date Range: ' + payroll.date_range));
        payrollCard.append($('<p>').text('Activated Date: ' + payroll.activated_date));
        payrollDetailsContainer.append(payrollCard);
    });

    modal.show();
}

function openPayrollModal() {
    $.ajax({
        url: '/employee_views/activated_payslip/',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            populatePayrollModal(data.payrolls);
        },        
        error: function(error) {
            console.error('Error fetching activated payslips:', error);
            alert('Error fetching activated payslips. Please try again.');
        }
    });
}


function closePayrollModal() {
    var modal = $('#payrollModal');
    modal.hide();
}


function populatePayrollModal(payrolls) {
    var modal = $('#payrollModal');
    var payrollDetailsContainer = $('#payrollDetailsContainer');

    payrollDetailsContainer.empty();

    if (payrolls && Array.isArray(payrolls) && payrolls.length > 0) {
        payrolls.forEach(function (payroll) {
            var payrollCard = $('<div>').addClass('payroll-card bg-white p-4 rounded-b-md shadow-md border-t-8 border-green-500');
            payrollCard.append($('<p>').addClass('font-bold').text('User: ' + payroll.user));
            payrollCard.append($('<p>').text('Monthly Salary: ' + payroll.monthly_salary));
            payrollCard.append($('<p>').text('Full Attendance Count: ' + payroll.full_attendance_count));
            payrollCard.append($('<p>').text('Half Attendance Count: ' + payroll.half_attendance_count));
            payrollCard.append($('<p>').text('Absent Attendance Count: ' + payroll.absent_attendance_count));
            payrollCard.append($('<p>').text('Date Range: ' + payroll.date_range));
            payrollCard.append($('<p>').text('Activated Date: ' + payroll.activated_date));
            payrollDetailsContainer.append(payrollCard);
        });
    } else {
        var noDataContent = `
            <div class="text-center">
                <div  class="text-center"  style="justify-content: center; align-items: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" data-name="Layer 1" width="250" height="250" viewBox="0 0 709.53268 558.59384" xmlns:xlink="http://www.w3.org/1999/xlink"><rect x="0.27492" y="0.36501" width="643.86162" height="412.35762" fill="#e6e6e6"/><rect x="18.68599" y="52.08494" width="607.03947" height="336.24257" fill="#fff"/><rect width="643.86163" height="27.3536" fill="#4885d1"/><circle cx="20.327" cy="13.98461" r="5.06978" fill="#fff"/><circle cx="39.57061" cy="13.98461" r="5.06978" fill="#fff"/><circle cx="58.81422" cy="13.98461" r="5.06978" fill="#fff"/><rect x="73.84385" y="86.97284" width="155.98055" height="266.46677" fill="#e6e6e6"/><rect x="256.7496" y="86.97284" width="129.9838" height="73.34799" fill="#4885d1"/><rect x="256.7496" y="180.74686" width="129.9838" height="78.91873" fill="#e6e6e6"/><rect x="256.7496" y="280.09161" width="129.9838" height="73.34799" fill="#e6e6e6"/><rect x="414.58707" y="86.97284" width="155.98056" height="116.12476" fill="#e6e6e6"/><rect x="414.58707" y="237.31485" width="155.98056" height="116.12476" fill="#e6e6e6"/><path d="M755.71223,382.14309v-25a33.5,33.5,0,1,1,67,0v25a4.50508,4.50508,0,0,1-4.5,4.5h-58A4.50508,4.50508,0,0,1,755.71223,382.14309Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><polygon points="593.514 536.786 581.698 540.056 563.462 496.038 580.901 491.212 593.514 536.786" fill="#ffb8b8"/><path d="M819.38459,708.28158h23.64387a0,0,0,0,1,0,0v14.88687a0,0,0,0,1,0,0H804.49773a0,0,0,0,1,0,0v0A14.88686,14.88686,0,0,1,819.38459,708.28158Z" transform="translate(-406.29299 74.94457) rotate(-15.46951)" fill="#2f2e41"/><polygon points="470.328 545.875 458.068 545.875 452.235 498.587 470.33 498.587 470.328 545.875" fill="#ffb8b8"/><path d="M449.31065,542.37161h23.64387a0,0,0,0,1,0,0v14.88687a0,0,0,0,1,0,0H434.42379a0,0,0,0,1,0,0v0A14.88686,14.88686,0,0,1,449.31065,542.37161Z" fill="#2f2e41"/><path d="M700.77825,452.301a10.0558,10.0558,0,0,0,15.392.91737l32.59018,14.65807L745.796,449.54488l-30.4937-11.10914a10.11028,10.11028,0,0,0-14.524,13.86524Z" transform="translate(-245.23366 -170.70308)" fill="#ffb8b8"/><path d="M768.49246,562.53911c-10.23925,0-20.83911-1.52539-29.74878-6.06152a38.41551,38.41551,0,0,1-19.70874-23.56543c-4.64233-14.69922,1.21094-29.14014,6.87134-43.105,3.50757-8.65381,6.82056-16.82715,7.68018-24.88379l.30029-2.86036c1.33887-12.84765,2.49512-23.94335,8.897-28.105,3.31836-2.15722,7.77979-2.28027,13.64063-.377l55.04492,17.88135-2.02393,104.49023-.33447.11182C808.82279,556.16118,789.41824,562.53911,768.49246,562.53911Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><path d="M755.46218,401.05127s27-8,48-5c0,0-12,66-8,88s-69.5,8.5-54.5-12.5l5-25s-10-10-1-22Z" transform="translate(-245.23366 -170.70308)" fill="#4885d1"/><path d="M742.18192,560.55815l-33.27637-6.23926,11.61768-89.40673c.78125-2.4961,18.77807-59.14307,26.95166-62.208a139.51716,139.51716,0,0,1,18.16626-5.04688l1.18383-.23681-6.67236,10.00879-26.56445,63.65429Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><path d="M724.84329,705.62163l-42.99487-7.16553,24.12817-98.52392,35.90332-134.73731.35425,2.39258c.02808.17822,3.38208,17.77978,53.15064,9.96973l.43774-.06836.12085.42627,60.1521,212.53759-48.99048,8.165L762.42215,543.55083Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><path d="M784.43558,577.2896l.02685-.75635c.03-.83984,2.988-84.37256,2-117.96729-.99145-33.709,9.92188-62.90087,10.03223-63.19189l.08887-.23438.24121-.06933c14.11963-4.03369,26.3689,8.00537,26.491,8.12744l.17211.17188-4.02124,33.17626,17.21607,120.64161Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><circle cx="537.09466" cy="190.79701" r="24.56103" fill="#ffb8b8"/><path d="M747.78694,359.14309a26.53,26.53,0,0,1,26.5-26.5h5.00024a26.52977,26.52977,0,0,1,26.49976,26.5v.5H795.22029l-3.604-10.09179-.7207,10.09179h-5.46094l-1.81836-5.09179-.36377,5.09179H747.78694Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><path d="M779.91118,389.45438a4.43341,4.43341,0,0,1-.3523-4.707c5.29859-10.07813,12.71729-28.7002,2.87012-40.18457l-.70776-.8252h28.5874V386.6575l-25.96948,4.582a4.59632,4.59632,0,0,1-.79639.07032A4.48193,4.48193,0,0,1,779.91118,389.45438Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><path d="M664.81368,212.24945a135.01972,135.01972,0,1,0,7.65509,199.4028L838.08687,551.4a12.44209,12.44209,0,0,0,16.06592-19.00287l-.01831-.01544L688.51631,392.63391A135.02729,135.02729,0,0,0,664.81368,212.24945ZM654.13692,379.17712a101.15765,101.15765,0,1,1-12.0766-142.54788l.00006,0A101.15764,101.15764,0,0,1,654.13692,379.17712Z" transform="translate(-245.23366 -170.70308)" fill="#3f3d56"/><path d="M511.589,391.25375a101.16315,101.16315,0,0,1-17.16559-135.989q-2.90121,2.92177-5.60938,6.1199A101.15767,101.15767,0,1,0,643.43849,391.85605q2.702-3.20224,5.089-6.559A101.163,101.163,0,0,1,511.589,391.25375Z" transform="translate(-245.23366 -170.70308)" opacity="0.3" style="isolation:isolate"/><path d="M790.214,495.239a10.05578,10.05578,0,0,0,12.42386-9.13254l34.433-9.55748L823.074,464.34553l-30.55233,10.94686A10.11027,10.11027,0,0,0,790.214,495.239Z" transform="translate(-245.23366 -170.70308)" fill="#ffb8b8"/><path d="M804.52567,490.18022,802.43021,470.274l28.76245-15.86914-18.75244-22.70019L815.5,406.20512l7.61987-3.26562.23707.30469c3.593,4.62011,35.10522,45.28076,35.10522,50.30713,0,5.16259-6.02856,20.32324-14.27637,24.44726-7.95581,3.978-37.83081,11.70947-39.09863,12.03711Z" transform="translate(-245.23366 -170.70308)" fill="#2f2e41"/><path d="M953.76634,729.29692h-381a1,1,0,1,1,0-2h381a1,1,0,0,1,0,2Z" transform="translate(-245.23366 -170.70308)" fill="#ccc"/></svg>
                </div>
                <p class="text-lg mt-2">NO DATA FOUND</p>
            </div>`;
        payrollDetailsContainer.html(noDataContent);
        payrollDetailsContainer.removeClass('grid grid-cols-3 gap-4');
    }
    modal.show();
}

