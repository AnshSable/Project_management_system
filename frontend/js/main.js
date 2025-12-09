// API Base URL - Update this to your backend URL
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const projectsContainer = document.getElementById('projects-container');
const clientsContainer = document.getElementById('clients-container');
const contactForm = document.getElementById('contact-form');
const newsletterForm = document.getElementById('newsletter-form');

// Load Projects from Backend
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const projects = await response.json();
        displayProjects(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        projectsContainer.innerHTML = `
            <div class="error-message">
                <p>Failed to load projects. Please try again later.</p>
                <button onclick="loadProjects()">Retry</button>
            </div>
        `;
    }
}

// Display Projects
function displayProjects(projects) {
    if (!projects || projects.length === 0) {
        projectsContainer.innerHTML = `
            <div class="no-projects">
                <p>No projects found. Add some from the admin panel!</p>
                <a href="admin.html" class="btn-primary">Go to Admin Panel</a>
            </div>
        `;
        return;
    }

    projectsContainer.innerHTML = projects.map(project => `
        <div class="project-card">
            <div class="project-image">
                <img src="${project.image_url || 'https://via.placeholder.com/300x200'}" alt="${project.name}">
            </div>
            <div class="project-content">
                <h3>${project.name}</h3>
                <p>${project.description.substring(0, 100)}...</p>
                <button class="read-more" onclick="showProjectDetails('${project._id}')">READ MORE</button>
            </div>
        </div>
    `).join('');
}

// Load Clients from Backend
async function loadClients() {
    try {
        const response = await fetch(`${API_BASE_URL}/clients`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const clients = await response.json();
        displayClients(clients);
    } catch (error) {
        console.error('Error loading clients:', error);
        clientsContainer.innerHTML = `
            <div class="error-message">
                <p>Failed to load clients. Please try again later.</p>
                <button onclick="loadClients()">Retry</button>
            </div>
        `;
    }
}

// Display Clients
function displayClients(clients) {
    if (!clients || clients.length === 0) {
        clientsContainer.innerHTML = `
            <div class="no-clients">
                <p>No clients found. Add some from the admin panel!</p>
                <a href="admin.html" class="btn-primary">Go to Admin Panel</a>
            </div>
        `;
        return;
    }

    clientsContainer.innerHTML = clients.map(client => `
        <div class="client-card">
            <div class="client-header">
                <div class="client-avatar">
                    <img src="${client.image_url || 'https://via.placeholder.com/60x60'}" alt="${client.name}">
                </div>
                <div class="client-info">
                    <h4>${client.name}</h4>
                    <p>${client.designation}</p>
                </div>
            </div>
            <div class="client-testimonial">
                <p>"${client.description.substring(0, 150)}..."</p>
            </div>
        </div>
    `).join('');
}

// Handle Contact Form Submission
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = contactForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    // Get form data
    const formData = {
        full_name: document.getElementById('fullName').value,
        email: document.getElementById('email').value,
        mobile: document.getElementById('mobile').value,
        city: document.getElementById('city').value
    };
    
    // Validation
    if (!formData.full_name || !formData.email || !formData.mobile || !formData.city) {
        showMessage('form-message', 'Please fill all fields', 'error');
        return;
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
        showMessage('form-message', 'Please enter a valid email address', 'error');
        return;
    }
    
    // Mobile validation (basic)
    if (formData.mobile.length < 10) {
        showMessage('form-message', 'Please enter a valid mobile number', 'error');
        return;
    }
    
    try {
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/contacts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showMessage('form-message', 'Thank you! We will contact you soon.', 'success');
            contactForm.reset();
        } else {
            const error = await response.json();
            showMessage('form-message', error.detail || 'Submission failed', 'error');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        showMessage('form-message', 'Network error. Please try again.', 'error');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

// Handle Newsletter Subscription
newsletterForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('newsletter-email').value;
    const submitBtn = newsletterForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showMessage('newsletter-message', 'Please enter a valid email address', 'error');
        return;
    }
    
    try {
        submitBtn.textContent = 'Subscribing...';
        submitBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/newsletter`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });
        
        if (response.ok) {
            showMessage('newsletter-message', 'Successfully subscribed!', 'success');
            newsletterForm.reset();
        } else {
            const error = await response.json();
            showMessage('newsletter-message', error.detail || 'Subscription failed', 'error');
        }
    } catch (error) {
        console.error('Error subscribing:', error);
        showMessage('newsletter-message', 'Network error. Please try again.', 'error');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

// Show Message Function
function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.style.color = type === 'success' ? 'green' : 'red';
    element.style.display = 'block';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Dummy function for READ MORE button
function showProjectDetails(projectId) {
    alert(`Project ID: ${projectId}\nThis is a dummy "Read More" button as per requirements.`);
}

// Mobile Menu Toggle
document.querySelector('.menu-toggle').addEventListener('click', () => {
    const navLinks = document.querySelector('.nav-links');
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    loadClients();
    
    // Handle responsive menu
    window.addEventListener('resize', () => {
        const navLinks = document.querySelector('.nav-links');
        if (window.innerWidth > 768) {
            navLinks.style.display = 'flex';
        } else {
            navLinks.style.display = 'none';
        }
    });
});