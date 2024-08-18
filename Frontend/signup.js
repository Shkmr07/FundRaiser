const url = 'http://127.0.0.1:8000/fundraiser/';

document.getElementById('signup').addEventListener('submit', async (event) => {
    event.preventDefault();

    const first_name = document.getElementById('fname').value;
    const last_name = document.getElementById('lname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('pass').value;
    const username = document.getElementById('user').value;

    try {
        const res = await fetch(`${url}register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'first_name': first_name,
                'last_name': last_name,
                'username' : username,
                'email': email,
                'password': password
            })
        });

        if (!res.ok) {
            // If the response status is not OK (e.g., 4xx or 5xx status), throw an error
            const errorData = await res.json();
            throw new Error(errorData.message || 'Something went wrong with the signup process.');
        }

        const data = await res.json();
        // alert('Signup Successful');
        window.location.href = './login.html';
        // Optionally redirect to another page after successful signup
        // window.location.href = './login.html';

    } catch (error) {
        console.error('Error during signup:', error);
        alert(`Error: ${error.message}`);
    }

});
