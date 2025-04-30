document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let form = event.target;
    let valid = true;

    // Get input elements
    let firstName = document.getElementById('first-name');
    let lastName = document.getElementById('last-name');
    let username = document.getElementById('username');
    let email = document.getElementById('email');
    let password = document.getElementById('password');

    // Validate each input
    if (firstName.value.trim() === '') {
        firstName.classList.add('error');
        valid = false;
    } else {
        firstName.classList.remove('error');
        firstName.classList.add('success');
    }

    if (lastName.value.trim() === '') {
        lastName.classList.add('error');
        valid = false;
    } else {
        lastName.classList.remove('error');
        lastName.classList.add('success');
    }

    if (username.value.trim() === '') {
        username.classList.add('error');
        valid = false;
    } else {
        username.classList.remove('error');
        username.classList.add('success');
    }

    if (email.value.trim() === '' || !validateEmail(email.value)) {
        email.classList.add('error');
        valid = false;
    } else {
        email.classList.remove('error');
        email.classList.add('success');
    }

    if (password.value.length < 6) {
        password.classList.add('error');
        valid = false;
    } else {
        password.classList.remove('error');
        password.classList.add('success');
    }

    // If form is valid, simulate successful form submission
    if (valid) {
        alert('Account created successfully!');
        form.reset(); // Reset the form after success
    } else {
        alert('Please fill in all fields correctly!');
    }
});

function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}
