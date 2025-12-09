// API Base URL - Same as main.js
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const navLinks = document.querySelectorAll('.nav-link');
const adminSections = document.querySelectorAll('.admin-section');
const adminMessage = document.getElementById('admin-message');

// Navigation
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active nav link
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Show corresponding section
        const sectionId = link.getAttribute('data-section');
        adminSections.forEach(section => {
            section.classList.remove('active');
            if (section.id === `${sectionId}-section`) {
                section.classList.add('active');
            }
        });
        
        // Load data for the section
        switch(sectionId) {
            case 'projects':
                loadProjectsForAdmin();
                break;
            case 'clients':
                loadClientsForAdmin();
                break;
            case 'contacts':
                loadContacts();
                break;
            case 'newsletter':
                loadNewsletterSubscriptions();
                break;
        }
    });
});

// Show/Hide Forms
document.getElementById('add-project-btn')?.addEventListener('click', () => {
    document.getElementById('project-form').classList.add('active');
});

document.getElementById('cancel-project')?.addEventListener('click', () => {
    document.getElementById('project-form').classList.remove('active');
    document.getElementById('add-project-form').reset();
});

document.getElementById('add-client-btn')?.addEventListener('click', () => {
    document.getElementById('client-form').classList.add('active');
});

document.getElementById('cancel-client')?.addEventListener('click', () => {
    document.getElementById('client-form').classList.remove('active');
    document.getElementById('add-client-form').reset();
});

// Load Projects for Admin
async function loadProjectsForAdmin() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        const projects = await response.json();
        displayProjectsTable(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        showMessage('Failed to load projects', 'error');
    }
}

// Display Projects in Table
function displayProjectsTable(projects) {
    const tbody = document.getElementById('projects-table-body');
    
    if (!projects || projects.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px;">
                    No projects found. Add your first project!
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = projects.map(project => `
        <tr>
            <td>
                <img src="${project.image_url || 'https://via.placeholder.com/50'}" 
                     alt="${project.name}" 
                     style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;">
            </td>
            <td>${project.name}</td>
            <td>${project.description.substring(0, 50)}...</td>
            <td>${new Date(project.created_at).toLocaleDateString()}</td>
            <td>
                <button class="action-btn delete-btn" onclick="deleteProject('${project._id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        </tr>
    `).join('');
}

// Add Project
document.getElementById('add-project-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showMessage('Project added successfully!', 'success');
            form.reset();
            document.getElementById('project-form').classList.remove('active');
            loadProjectsForAdmin();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Failed to add project', 'error');
        }
    } catch (error) {
        console.error('Error adding project:', error);
        showMessage('Network error. Please try again.', 'error');
    }
});

// Delete Project
async function deleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Project deleted successfully!', 'success');
            loadProjectsForAdmin();
        } else {
            showMessage('Failed to delete project', 'error');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

// Load Clients for Admin
async function loadClientsForAdmin() {
    try {
        const response = await fetch(`${API_BASE_URL}/clients`);
        const clients = await response.json();
        displayClientsTable(clients);
    } catch (error) {
        console.error('Error loading clients:', error);
        showMessage('Failed to load clients', 'error');
    }
}

// Display Clients in Table
function displayClientsTable(clients) {
    const tbody = document.getElementById('clients-table-body');
    
    if (!clients || clients.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 40px;">
                    No clients found. Add your first client!
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = clients.map(client => `
        <tr>
            <td>
                <img src="${client.image_url || 'https://via.placeholder.com/50'}" 
                     alt="${client.name}" 
                     style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">
            </td>
            <td>${client.name}</td>
            <td>${client.designation}</td>
            <td>${client.description.substring(0, 50)}...</td>
            <td>${new Date(client.created_at).toLocaleDateString()}</td>
            <td>
                <button class="action-btn delete-btn" onclick="deleteClient('${client._id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        </tr>
    `).join('');
}

// Add Client
document.getElementById('add-client-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`${API_BASE_URL}/clients`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showMessage('Client added successfully!', 'success');
            form.reset();
            document.getElementById('client-form').classList.remove('active');
            loadClientsForAdmin();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Failed to add client', 'error');
        }
    } catch (error) {
        console.error('Error adding client:', error);
        showMessage('Network error. Please try again.', 'error');
    }
});

// Delete Client
async function deleteClient(clientId) {
    if (!confirm('Are you sure you want to delete this client?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/clients/${clientId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Client deleted successfully!', 'success');
            loadClientsForAdmin();
        } else {
            showMessage('Failed to delete client', 'error');
        }
    } catch (error) {
        console.error('Error deleting client:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

// Load Contacts
async function loadContacts() {
    try {
        const response = await fetch(`${API_BASE_URL}/contacts`);
        const contacts = await response.json();
        displayContactsTable(contacts);
    } catch (error) {
        console.error('Error loading contacts:', error);
        showMessage('Failed to load contacts', 'error');
    }
}

// Display Contacts in Table
function displayContactsTable(contacts) {
    const tbody = document.getElementById('contacts-table-body');
    
    if (!contacts || contacts.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px;">
                    No contact submissions yet.
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = contacts.map(contact => `
        <tr>
            <td>${contact.full_name}</td>
            <td>${contact.email}</td>
            <td>${contact.mobile}</td>
            <td>${contact.city}</td>
            <td>${new Date(contact.created_at).toLocaleString()}</td>
        </tr>
    `).join('');
}

// Load Newsletter Subscriptions
async function loadNewsletterSubscriptions() {
    try {
        const response = await fetch(`${API_BASE_URL}/newsletter`);
        const subscriptions = await response.json();
        displayNewsletterTable(subscriptions);
    } catch (error) {
        console.error('Error loading newsletter:', error);
        showMessage('Failed to load newsletter subscriptions', 'error');
    }
}

// Display Newsletter in Table
function displayNewsletterTable(subscriptions) {
    const tbody = document.getElementById('newsletter-table-body');
    
    if (!subscriptions || subscriptions.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="2" style="text-align: center; padding: 40px;">
                    No newsletter subscriptions yet.
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = subscriptions.map(sub => `
        <tr>
            <td>${sub.email}</td>
            <td>${new Date(sub.created_at).toLocaleString()}</td>
        </tr>
    `).join('');
}

// Show Message Function
function showMessage(text, type) {
    adminMessage.textContent = text;
    adminMessage.className = `message ${type}`;
    adminMessage.style.display = 'block';
    
    setTimeout(() => {
        adminMessage.style.display = 'none';
    }, 5000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Load initial data for active section
    loadProjectsForAdmin();
});