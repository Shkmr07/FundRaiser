const url = 'http://127.0.0.1:8000/fundraiser/';

document.getElementById('login').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    const username = document.getElementById('logInp').value;
    const password = document.getElementById('logPass').value;
    console.log('Submit button clicked');

    try {
        const res = await fetch(`${url}login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'username': username,
                'password': password
            }),
            credentials: 'include' // Important for cross-origin cookies
        });

        console.log('Response Status:', res.status);

        if (!res.ok) {
            const errorData = await res.json();
            console.log('Response Data:', errorData);
            throw new Error(errorData.message || 'Login failed');
        }

        const data = await res.json();
        console.log('Login Successful:', data);

        // Assuming the token is part of the response body
        const { token } = data;

        // Store the token in localStorage
        localStorage.setItem('token', token);
        localStorage.setItem('username', username)
        window.location.href = './index.html'; // Change to your desired page
        alert('Login Successful')

        // Use a delay to ensure proper execution
        // setTimeout(() => {
        // }, 100); // 100ms delay

    } catch (error) {
        console.error('Error during login:', error);
        alert(`Error: ${error.message}`);
    }
});