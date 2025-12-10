// Authentication and Token Management

// Token Storage
function setToken(token) {
    sessionStorage.setItem(TOKEN_KEY, token);
}

function getToken() {
    return sessionStorage.getItem(TOKEN_KEY);
}

function removeToken() {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    sessionStorage.removeItem(ROLE_KEY);
}

function setUserData(username, role) {
    sessionStorage.setItem(USER_KEY, username);
    sessionStorage.setItem(ROLE_KEY, role);
}

function getUserData() {
    return {
        username: sessionStorage.getItem(USER_KEY),
        role: sessionStorage.getItem(ROLE_KEY)
    };
}

function isAuthenticated() {
    return getToken() !== null;
}

function isAdmin() {
    return getUserData().role === 'admin';
}

// API Request Helper with Token
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const config = { ...options, headers };
    try {
        // endpoint is already full URL from config.js!
        const response = await fetch(endpoint, config);
        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                removeToken();
                updateUIForAuth();
                showToast('Session expired. Please login again.', 'error');
            }
            throw new Error(data.detail || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Login Functions
let currentLoginType = 'user';

function switchTab(type) {
    currentLoginType = type;
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
}

async function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const password = form.password.value;

    try {
        const endpoint = currentLoginType === 'admin' ? API_ENDPOINTS.ADMIN_LOGIN : API_ENDPOINTS.USER_LOGIN;
        const data = await apiRequest(endpoint, {
            method: 'POST',
            body: JSON.stringify({ username, password }),
            skipAuth: true
        });

        setToken(data.access_token);
        setUserData(username, currentLoginType);

        showToast(`Welcome back, ${username}!`, 'success');
        closeLoginModal();
        updateUIForAuth();

        if (currentLoginType === 'admin') {
            setTimeout(() => {
                window.location.href = '/admin';
            }, 1000);
        } else {
            loadProjects();
            loadClients();
        }
    } catch (error) {
        showToast(error.message || 'Login failed', 'error');
    }
}

async function handleSignup(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const email = form.email.value;
    const password = form.password.value;

    try {
        await apiRequest(API_ENDPOINTS.USER_SIGNUP, {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
            skipAuth: true
        });

        showToast('Account created successfully! Please login.', 'success');
        closeSignupModal();
        showLoginModal();
    } catch (error) {
        showToast(error.message || 'Signup failed', 'error');
    }
}

function logout() {
    removeToken();
    updateUIForAuth();
    showToast('Logged out successfully', 'success');
    window.location.href = '/';
}

// UI Updates Based on Auth State
function updateUIForAuth() {
    const authButtons = document.getElementById('authButtons');
    const userMenu = document.getElementById('userMenu');
    const adminMenu = document.getElementById('adminMenu');
    const userName = document.getElementById('userName');

    if (isAuthenticated()) {
        const userData = getUserData();
        authButtons.style.display = 'none';

        if (isAdmin()) {
            adminMenu.style.display = 'flex';
            if (userMenu) userMenu.style.display = 'none';
        } else {
            userMenu.style.display = 'flex';
            if (userName) userName.textContent = userData.username;
            if (adminMenu) adminMenu.style.display = 'none';
        }
    } else {
        authButtons.style.display = 'flex';
        if (userMenu) userMenu.style.display = 'none';
        if (adminMenu) adminMenu.style.display = 'none';
    }
}

// Modal Functions
function showLoginModal() {
    closeSignupModal();
    document.getElementById('loginModal').style.display = 'block';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function showSignupModal() {
    closeLoginModal();
    document.getElementById('signupModal').style.display = 'block';
}

function closeSignupModal() {
    document.getElementById('signupModal').style.display = 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        const loginModal = document.getElementById('loginModal');
        const signupModal = document.getElementById('signupModal');
        if (event.target == loginModal) {
            closeLoginModal();
        }
        if (event.target == signupModal) {
            closeSignupModal();
        }
    };

    updateUIForAuth();
});
