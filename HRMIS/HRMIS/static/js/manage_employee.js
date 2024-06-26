// TABLE TOGGLE 
function showTable(tableId) {
    const activeButton = document.getElementById('activeButton');
    const archiveButton = document.getElementById('archiveButton');
    const activeTable = document.getElementById('activeTable');
    const archiveTable = document.getElementById('archiveTable');

    if (tableId === 'activeTable') {
        activeTable.classList.remove('hidden');
        archiveTable.classList.add('hidden');
        activeButton.classList.add('bg-custom-blue');
        activeButton.classList.add('text-white');
        activeButton.classList.remove('bg-white');
        archiveButton.classList.add('bg-custom-bg');
        archiveButton.classList.remove('bg-custom-blue');
        archiveButton.classList.remove('text-white');
    } else if (tableId === 'archiveTable') {
        activeTable.classList.add('hidden');
        archiveTable.classList.remove('hidden');
        activeButton.classList.add('bg-custom-bg');
        activeButton.classList.remove('text-white');
        activeButton.classList.remove('bg-custom-blue');
        archiveButton.classList.add('bg-custom-blue');
        archiveButton.classList.add('text-white');
        archiveButton.classList.remove('bg-white');
    }
}
// OPEN ARCHIVE USER MODAL
function openArchiveModal(userId) {
    var archiveModal = document.getElementById('archiveModal');
    if (archiveModal) {
        archiveModal.style.display = 'block';

        var confirmArchiveButton = document.getElementById('confirmArchive');
        if (confirmArchiveButton) {
            confirmArchiveButton.setAttribute('data-user-id', userId);
            console.log(userId)
        }

        var overlay = document.getElementById('archiveModalOverlay');
        if (overlay) {
            overlay.addEventListener('click', closeArchiveModal);
        }
    }
}
// CLOSE ARCHIVE USER MODAL
function closeArchiveModal() {
    var archiveModal = document.getElementById('archiveModal');
    if (archiveModal) {
        archiveModal.style.display = 'none';
        var overlay = document.getElementById('archiveModalOverlay');
        if (overlay) {
            overlay.removeEventListener('click', closeArchiveModal);
        }
    }
}
// ARCHIVE USER
function archiveUser(userId) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/hr_views/archive_user/' + userId + '/');
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    var csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.onload = function () {
        if (xhr.status === 200) {
            closeArchiveModal();
            location.reload();
        } else {
            console.error('Error archiving user:', xhr.statusText);
        }
    };

    xhr.send(JSON.stringify({ archive: true }));
}
// ARCHIVE USER
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.archive-button').forEach(function (button) {
        button.addEventListener('click', function () {
            var userId = button.getAttribute('data-user-id');
            openArchiveModal(userId);
        });
    });

    var cancelArchiveButton = document.getElementById('cancelArchive');
    if (cancelArchiveButton) {
        cancelArchiveButton.addEventListener('click', function () {
            closeArchiveModal();
        });
    }

    var confirmArchiveButton = document.getElementById('confirmArchive');
    if (confirmArchiveButton) {
        confirmArchiveButton.addEventListener('click', function () {
            var userId = confirmArchiveButton.getAttribute('data-user-id');
            console.log('Clicked Confirm Archive. User ID:', userId);
            archiveUser(userId);
        });
    }
});

//Open Unarchive Modal
function openUnarchiveModal(userId) {
    var unarchiveModal = document.getElementById('unarchiveModal');
    console.log('clicked button')
    if (unarchiveModal) {
        unarchiveModal.style.display = 'block';

        var confirmUnarchiveButton = document.getElementById('confirmUnarchive');
        if (confirmUnarchiveButton) {
           
            confirmUnarchiveButton.setAttribute('data-user-id', userId);
            confirmUnarchiveButton.onclick = function () {

                unarchiveUser(userId);
            };
        }

        var overlay = document.getElementById('unarchiveModalOverlay');
        if (overlay) {
            overlay.addEventListener('click', closeUnarchiveModal);
        }
    }
}
//Close Unarchive Modal
function closeUnarchiveModal() {
    var unarchiveModal = document.getElementById('unarchiveModal');
    if (unarchiveModal) {
        unarchiveModal.style.display = 'none';
        var overlay = document.getElementById('unarchiveModalOverlay');
        if (overlay) {
            overlay.removeEventListener('click', closeUnarchiveModal);
        }
    }
}
//Unarchive 
function unarchiveUser(userId) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/hr_views/unarchive_user/' + userId + '/');
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    var csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.onload = function () {
        if (xhr.status === 200) {
            closeUnarchiveModal();
            location.reload();
        } else {
            console.error('Error unarchiving user:', xhr.statusText);
        }
    };

    xhr.send(JSON.stringify({ unarchive: true }));
}

// EDIT MODAL JS
var currentUserId;
// OPEN EDIT MODAL
function openEditModal(userId) {
    console.log('Clicked for user ID:', userId);
    currentUserId = userId; 
    var xhr = new XMLHttpRequest(); 
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                try {
                    var responseData = JSON.parse(xhr.responseText);
                    if (responseData && responseData.username && responseData.name && responseData.role && responseData.salary_grade) {
                        
                        populateEditModal(responseData);

                        document.getElementById('editModal').classList.remove('hidden');
                    } else {
                        console.error('Error: User data properties are missing or undefined.');
                    }
                } catch (error) {
                    console.error('Error parsing JSON response:', error);
                }
            } else {
                console.error('Error fetching user details:', xhr.status);
            }
        }
    };
    xhr.open('GET', '/hr_views/edit_user/' + userId + '/');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');  
    xhr.send();
}

// SAVE EDIT MODAL
function saveChanges() {
    var userId = currentUserId;
  
    if (userId === undefined || userId === null) {
        console.error('Error: User ID is undefined or null.');
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/hr_views/save_user_changes/' + userId + '/');
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    var csrftoken = getCookie('csrftoken');  
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.onload = function () {
        if (xhr.status === 200) {
            var responseData = JSON.parse(xhr.responseText);
            if (responseData.success) {
                console.log('Changes saved successfully!');
                EditSuccessModal(); 
                closeEditModal(); 
                
            } else {
                console.error('Error saving changes:', responseData.errors);
            }
        } else {
            console.error('Error saving changes:', xhr.status);
        }
    };

    var formData = {
        username: document.getElementById('usernameInput').value,
        name: document.getElementById('nameInput').value,
        role: document.getElementById('roleInput').value,
        salary_grade: document.getElementById('salaryInput').value,
        cooperative_member: document.getElementById('cooperativeMemberInput').checked,
        category: document.getElementById('categoryInput').value,
    };
    console.log(formData);

    xhr.send(JSON.stringify(formData));
}


// Function to display the edit success modal
function EditSuccessModal() {
    document.getElementById('editSuccessModal').classList.remove('hidden');
}
// Function to close the edit success modal
function closeEditSuccessModal() {
    document.getElementById('editSuccessModal').classList.add('hidden');
    location.reload();
}

// Function to close the edit modal
function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
}
// POPULATE EDIT MODAL
function populateEditModal(userData) {
    if (userData) {
        document.getElementById('usernameInput').value = userData.username;
        document.getElementById('nameInput').value = userData.name;
        document.getElementById('roleInput').value = userData.role;
        document.getElementById('salaryInput').value = userData.salary_grade;
        document.getElementById('cooperativeMemberInput').checked = userData.cooperative_member;
        document.getElementById('categoryInput').value = userData.category;
    } else {
        console.error('Invalid user data received.');
    }
}
//NEW USER JS
// OPEN NEW USER MODAL
function openNewUserModal() {
    var newUserModal = document.getElementById('newUserModal');
    newUserModal.classList.remove('hidden');
}

// CLOSING NEW USER MODAL
function closeNewUserModal() {
    var newUserModal = document.getElementById('newUserModal');
    newUserModal.classList.add('hidden');
}

// SAVING NEW USER
function saveNewUser() {
    const username = document.getElementById('newUsernameInput').value;
    const password = document.getElementById('newPasswordInput').value;
    const name = document.getElementById('newNameInput').value;
    const role = document.getElementById('newRoleInput').value;
    const salary_grade = document.getElementById('newSalaryInput').value;
    const cooperative_member = document.getElementById('newCooperativeMemberInput').checked;
    const category = document.getElementById('newCategoryInput').value;

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('name', name);
    formData.append('role', role);
    formData.append('salary_grade', salary_grade);
    formData.append('cooperative_member', cooperative_member);
    formData.append('category', category);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/hr_views/create_user/');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); 
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log('New user saved successfully!');
                displaySuccessModal(); // Display the success modal
                closeNewUserModal(); // Close the new user modal
                
            } else {
                console.error('Error saving new user:', xhr.responseText);
            }
        }
    };
    xhr.send(formData);
}

// Function to display the success modal
function displaySuccessModal() {
    document.getElementById('newUserSuccessModal').classList.remove('hidden');
}

// Function to close the success modal
function closeNewUserSuccessModal() {
    document.getElementById('newUserSuccessModal').classList.add('hidden');
    location.reload();
}

function showActiveSearch() {
    const activeSearchForm = document.getElementById('activeSearchForm');
    const archiveSearchForm = document.getElementById('archiveSearchForm');

    if (activeSearchForm && archiveSearchForm) {
        activeSearchForm.style.display = 'block';
        archiveSearchForm.style.display = 'none';
    }
}

function showArchiveSearch() {
    const activeSearchForm = document.getElementById('activeSearchForm');
    const archiveSearchForm = document.getElementById('archiveSearchForm');

    if (activeSearchForm && archiveSearchForm) {
        archiveSearchForm.style.display = 'block';
        activeSearchForm.style.display = 'none';
    }
}


function search() {
    const searchText = document.getElementById('simple-search').value.toLowerCase(); 
    const tableRows = document.querySelectorAll('#activeTable tbody tr'); 
    let found = false;

    tableRows.forEach(row => {
        const name = row.querySelector('td:nth-child(1)').textContent.toLowerCase(); 
        const id = row.querySelector('td:nth-child(2)').textContent.toLowerCase(); 
        if (searchText === '' || name.includes(searchText) || id.includes(searchText)) {
            row.style.display = 'table-row';
            found = true; 
        } else {
            row.style.display = 'none'; 
        }
    });

    const errorMessageRow = document.getElementById('noResultsMessage');
    errorMessageRow.style.display = found ? 'none' : 'table-row';
}

function searchArchive() {
    const searchText = document.getElementById('archive-search').value.toLowerCase(); 
    const tableRows = document.querySelectorAll('#archiveTable tbody tr'); 
    let found = false;

    tableRows.forEach(row => {
        const name = row.querySelector('td:nth-child(1)').textContent.toLowerCase(); 
        const id = row.querySelector('td:nth-child(2)').textContent.toLowerCase(); 
        if (searchText === '' || name.includes(searchText) || id.includes(searchText)) {
            row.style.display = 'table-row'; 
            found = true; 
        } else {
            row.style.display = 'none'; 
        }
    });

    const errorMessageRow = document.getElementById('archivedResultsMessage');
    errorMessageRow.style.display = found ? 'none' : 'table-row';
}
document.addEventListener('DOMContentLoaded', function() {
    const simpleSearchInput = document.getElementById('simple-search');
    const archiveSearchInput = document.getElementById('archive-search');
    const activeButton = document.getElementById('activeButton');
    const archiveButton = document.getElementById('archiveButton');

    if (simpleSearchInput) {
        simpleSearchInput.addEventListener('input', search);
    }

    if (archiveSearchInput) {
        archiveSearchInput.addEventListener('input', searchArchive);
    }

    if (activeButton) {
        activeButton.addEventListener('click', showActiveSearch);
    }

    if (archiveButton) {
        archiveButton.addEventListener('click', showArchiveSearch);
    }

    showActiveSearch();
});