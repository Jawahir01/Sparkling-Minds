
// Function to display and hide alert messages.
setTimeout(function () {
    let messagesDj = document.getElementById('messages-notes');
    if (messagesDj) {
        messagesDj.style.display = 'none';
    }
}, 2500);

// check if the user has checked the confirmation checkbox before submitting the form.
// function validateForm() {
//     const confCheckbox = document.getElementById('confirm');
//     if (!confCheckbox.checked) {
//         alert('Please confirm your informations before proceeding.');
//         return false;
//     }

//     return true;
// }

const dropdownElementList = document.querySelectorAll('.dropdown-toggle')
const dropdownList = [...dropdownElementList].map(dropdownToggleEl => new bootstrap.Dropdown(dropdownToggleEl))