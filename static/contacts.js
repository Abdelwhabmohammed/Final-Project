document.addEventListener('DOMContentLoaded', function () {
    fetchContacts();

    function fetchContacts() {
        fetch('/contacts')
            .then(response => response.json())
            .then(data => {
                let tableBody = document.getElementById('contacttable');
                tableBody.innerHTML = '';

                data.forEach(contact => {
                    // Create an element 
                    let row = document.createElement('tr');

                    // Coloring the background based on the category
                    if (contact.category === 'family') {
                        row.style.backgroundColor = "lightskyblue";
                    } else if (contact.category === 'friends') {
                        row.style.backgroundColor = "lightseagreen";
                    } else {
                        row.style.backgroundColor = "lightslategrey";
                    }

                    // Create table elemnts and write the entered data inside it
                    row.innerHTML = `
                        <td>${contact.first_name}</td>
                        <td>${contact.second_name}</td>
                        <td>${contact.phone}</td>
                        <td>${contact.email}</td>
                        <td>${contact.category}</td>
                        <td><button class="delete-btn" data-id="${contact.id}">Delete</button></td>
                    `;
                    tableBody.appendChild(row);
                });

                // Activate the Delete button
                document.querySelectorAll('.delete-btn').forEach(button => {
                    button.addEventListener('click', function () {
                        let id = this.getAttribute('data-id');

                        fetch(`/contacts/${id}`, {
                            method: 'DELETE'
                        }).then(response => response.json())
                          .then(data => {
                              console.log(data.message);
                              
                              // Refresh the contact list
                              fetchContacts(); 
                          }).catch(error => console.error('Error:', error));
                    });
                });
            });
    }
});
