// Use window.location to determine the correct API URL
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000'
    : 'http://localhost:5000';

function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.querySelectorAll('.tab-btn')[1].classList.remove('active');
}

function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
    document.querySelectorAll('.tab-btn')[0].classList.remove('active');
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('userName', data.user.name);
            window.location.href = 'pages/dashboard.html';
        } else {
            document.getElementById('loginMessage').textContent = data.message || 'Login failed';
            document.getElementById('loginMessage').className = 'message error';
        }
    } catch (error) {
        document.getElementById('loginMessage').textContent = 'Error connecting to server';
        document.getElementById('loginMessage').className = 'message error';
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('registerMessage').textContent = 'Registration successful! Please login.';
            document.getElementById('registerMessage').className = 'message success';
            setTimeout(() => showLogin(), 2000);
        } else {
            document.getElementById('registerMessage').textContent = data.message || 'Registration failed';
            document.getElementById('registerMessage').className = 'message error';
        }
    } catch (error) {
        document.getElementById('registerMessage').textContent = 'Error connecting to server';
        document.getElementById('registerMessage').className = 'message error';
    }
}

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '../index.html';
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userName');
    window.location.href = '../index.html';
}

function getAuthHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    };
}
