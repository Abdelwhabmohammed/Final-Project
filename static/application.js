document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('contactForm').addEventListener('submit', function (event) {
        event.preventDefault();

        let firstName = document.getElementById('firstname').value.trim();
        let phone = document.getElementById('phone').value.trim();
        let email = document.getElementById('email').value.trim();

        // Check that the user has already entered data
        if (!firstName || !phone) {
            showMessage('First Name and Phone Number are required', 'error');
            return;
        }

        // Ensure that phone number is > 10
        if (phone.length < 10) {
            showMessage('Phone Number is too short', 'error');
            return;
        }

        // check that the entered email is correct
        if (email && !validateEmail(email)) {
            showMessage('Invalid email format', 'error');
            return;
        }

        // After that assigning data to a dict
        let formData = {
            first_name: firstName,
            second_name: document.getElementById('secondname').value.trim(),
            phone: phone,
            email: email,
            category: document.getElementById('category').value
        };

        fetch('/contacts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then(response => response.json())
          .then(data => {
              if (data.status === "error") {
                  // Display error message
                  showMessage(data.message, 'error'); 
              } else {
                  // Display success message
                  showMessage(data.message, 'success'); 
                  
                  // Refresh the contact list
                  fetchContacts(); 
              }
        }).catch(error => console.error('Error:', error));
    });
});
// Make a showMessage function to use insteead of flash message as it requirs refreshing the page 
function showMessage(message, type) {
    // Create a div to put it inside
    let messageElement = document.createElement('div');
    
    // Showing the wanted message in the created element
    messageElement.textContent = message;

    // Styling message passed on its type(success or error)
    messageElement.className = `flash-message ${type}`;
    document.body.appendChild(messageElement);
    
    // Remove the message after a few seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}

// Create a ValidateEmail function to ensure that the enterd email is correct
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}
