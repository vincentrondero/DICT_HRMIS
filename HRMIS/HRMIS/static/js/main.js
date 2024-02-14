console.log ("1111", 1111);

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function openLogoutModal() {
    var logoutModal = document.getElementById('logoutModal');
    logoutModal.style.display = 'block';
} 

document.addEventListener('DOMContentLoaded', function () {
  var logoutModal = document.getElementById('logoutModal');
  var logoutButton = document.getElementById('logoutButton');
  var confirmLogout = document.getElementById('confirmLogout');
  var cancelLogout = document.getElementById('cancelLogout');

  if (logoutButton) {
    logoutButton.addEventListener('click', function () {
      logoutModal.style.display = 'block';
    });
  }

  if (confirmLogout) {
    confirmLogout.addEventListener('click', function () {
      var logoutUrl = logoutButton.getAttribute('data-logout-url');
      window.location.href = logoutUrl;
    });
  }

  if (cancelLogout) {
    cancelLogout.addEventListener('click', function () {
      logoutModal.style.display = 'none';
    });
  }

  window.onclick = function (event) {
    if (event.target == logoutModal) {
      logoutModal.style.display = 'none';
    }
  };
});