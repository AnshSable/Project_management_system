// Admin Panel JavaScript

// Check Authentication on Load
if (!isAuthenticated() || !isAdmin()) {
    window.location.href = '/';
}

// Display Admin Name
document.getElementById('adminName').textContent = getUserData().username;

// Toast Function
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// Section Navigation
document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = link.dataset.section;
        
        // Update active link
        document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Show section
        document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
        document.getElementById(section).classList.add('active');
        
        // Load data for section
        loadSectionData(section);
    });
});

// Load Section Data
function loadSectionData(section) {
    switch(section) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'projects':
            loadProjects();
            break;
        case 'clients':
            loadClients();
            break;
        case 'contacts':
            loadContacts();
            break;
        case 'subscriptions':
            loadSubscriptions();
            break;
    }
}

// Load Dashboard Stats
async function loadDashboard() {
    try {
        const [projects, clients, contacts, subscriptions] = await Promise.all([
            apiRequest(API_ENDPOINTS.ADMIN_PROJECTS),
            apiRequest(API_ENDPOINTS.ADMIN_CLIENTS),
            apiRequest(API_ENDPOINTS.ADMIN_CONTACTS),
            apiRequest(API_ENDPOINTS.ADMIN_SUBSCRIPTIONS)
        ]);
        
        document.getElementById('totalProjects').textContent = projects.projects?.length || 0;
        document.getElementById('totalClients').textContent = clients.clients?.length || 0;
        document.getElementById('totalContacts').textContent = contacts.contacts?.length || 0;
        document.getElementById('totalSubscriptions').textContent = 
            subscriptions.subscriptions?.filter(s => s.status === 'active').length || 0;
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// ===================================
// PROJECTS MANAGEMENT
// ===================================

async function loadProjects() {
    const container = document.getElementById('projectsTable');
    container.innerHTML = '<div class="loading">Loading projects...</div>';
    
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_PROJECTS);
        
        if (!data.projects || data.projects.length === 0) {
            container.innerHTML = '<div class="empty-state">No projects found</div>';
            return;
        }
        
        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Project Name</th>
                        <th>Description</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.projects.forEach(project => {
            html += `
                <tr>
                    <td>
                        ${project.project_image ? 
                            `<img src="${project.project_image}" alt="${project.project_name}" class="table-image">` :
                            '<div class="table-placeholder"><i class="fas fa-image"></i></div>'
                        }
                    </td>
                    <td><strong>${project.project_name}</strong></td>
                    <td>${project.description || 'N/A'}</td>
                    <td>${new Date(project.created_at).toLocaleDateString()}</td>
                    <td class="table-actions">
                        <button class="btn-icon btn-edit" onclick="editProject(${project.project_id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon btn-delete" onclick="deleteProject(${project.project_id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<div class="error-state">Failed to load projects</div>';
    }
}

function showProjectModal(project = null) {
    const modal = document.getElementById('projectModal');
    const form = document.getElementById('projectForm');
    
    if (project) {
        document.getElementById('projectModalTitle').textContent = 'Edit Project';
        document.getElementById('projectId').value = project.project_id;
        document.getElementById('projectName').value = project.project_name;
        document.getElementById('projectDescription').value = project.description || '';
        
        if (project.project_image) {
            document.getElementById('projectImagePreview').innerHTML = 
                `<img src="${project.project_image}" alt="Preview">`;
        }
    } else {
        document.getElementById('projectModalTitle').textContent = 'Add Project';
        form.reset();
        document.getElementById('projectImagePreview').innerHTML = '';
    }
    
    modal.classList.add('show');
}

function closeProjectModal() {
    document.getElementById('projectModal').classList.remove('show');
}

async function editProject(id) {
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_PROJECT(id));
        showProjectModal(data);
    } catch (error) {
        showToast('Failed to load project details', 'error');
    }
}

async function deleteProject(id) {
    if (!confirm('Are you sure you want to delete this project?')) return;
    
    try {
        await apiRequest(API_ENDPOINTS.ADMIN_PROJECT(id), { method: 'DELETE' });
        showToast('Project deleted successfully', 'success');
        loadProjects();
        loadDashboard();
    } catch (error) {
        showToast(error.message || 'Failed to delete project', 'error');
    }
}

// Project Form Submit
document.getElementById('projectForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('projectId').value;
    const name = document.getElementById('projectName').value;
    const description = document.getElementById('projectDescription').value;
    const imageFile = document.getElementById('projectImage').files[0];
    
    let imageBase64 = null;
    if (imageFile) {
        imageBase64 = await fileToBase64(imageFile);
    }
    
    const projectData = {
        project_name: name,
        description: description || null,
        project_image: imageBase64
    };
    
    try {
        if (id) {
            await apiRequest(API_ENDPOINTS.ADMIN_PROJECT(id), {
                method: 'PUT',
                body: JSON.stringify(projectData)
            });
            showToast('Project updated successfully', 'success');
        } else {
            await apiRequest(API_ENDPOINTS.ADMIN_PROJECTS, {
                method: 'POST',
                body: JSON.stringify(projectData)
            });
            showToast('Project created successfully', 'success');
        }
        
        closeProjectModal();
        loadProjects();
        loadDashboard();
    } catch (error) {
        showToast(error.message || 'Failed to save project', 'error');
    }
});

// Image Preview
document.getElementById('projectImage').addEventListener('change', function() {
    previewImage(this, 'projectImagePreview');
});

document.getElementById('clientImage').addEventListener('change', function() {
    previewImage(this, 'clientImagePreview');
});

function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// ===================================
// CLIENTS MANAGEMENT
// ===================================

async function loadClients() {
    const container = document.getElementById('clientsTable');
    container.innerHTML = '<div class="loading">Loading clients...</div>';
    
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_CLIENTS);
        
        if (!data.clients || data.clients.length === 0) {
            container.innerHTML = '<div class="empty-state">No clients found</div>';
            return;
        }
        
        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Client Name</th>
                        <th>Designation</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.clients.forEach(client => {
            html += `
                <tr>
                    <td>
                        ${client.client_image ? 
                            `<img src="${client.client_image}" alt="${client.client_name}" class="table-image">` :
                            '<div class="table-placeholder"><i class="fas fa-user"></i></div>'
                        }
                    </td>
                    <td><strong>${client.client_name}</strong></td>
                    <td>${client.designation || 'N/A'}</td>
                    <td>${client.description || 'N/A'}</td>
                    <td>${new Date(client.created_at).toLocaleDateString()}</td>
                    <td class="table-actions">
                        <button class="btn-icon btn-edit" onclick="editClient(${client.client_id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon btn-delete" onclick="deleteClient(${client.client_id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<div class="error-state">Failed to load clients</div>';
    }
}

function showClientModal(client = null) {
    const modal = document.getElementById('clientModal');
    const form = document.getElementById('clientForm');
    
    if (client) {
        document.getElementById('clientModalTitle').textContent = 'Edit Client';
        document.getElementById('clientId').value = client.client_id;
        document.getElementById('clientName').value = client.client_name;
        document.getElementById('clientDesignation').value = client.designation || '';
        document.getElementById('clientDescription').value = client.description || '';
        
        if (client.client_image) {
            document.getElementById('clientImagePreview').innerHTML = 
                `<img src="${client.client_image}" alt="Preview">`;
        }
    } else {
        document.getElementById('clientModalTitle').textContent = 'Add Client';
        form.reset();
        document.getElementById('clientImagePreview').innerHTML = '';
    }
    
    modal.classList.add('show');
}

function closeClientModal() {
    document.getElementById('clientModal').classList.remove('show');
}

async function editClient(id) {
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_CLIENT(id));
        showClientModal(data);
    } catch (error) {
        showToast('Failed to load client details', 'error');
    }
}

async function deleteClient(id) {
    if (!confirm('Are you sure you want to delete this client?')) return;
    
    try {
        await apiRequest(API_ENDPOINTS.ADMIN_CLIENT(id), { method: 'DELETE' });
        showToast('Client deleted successfully', 'success');
        loadClients();
        loadDashboard();
    } catch (error) {
        showToast(error.message || 'Failed to delete client', 'error');
    }
}

// Client Form Submit
document.getElementById('clientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('clientId').value;
    const name = document.getElementById('clientName').value;
    const designation = document.getElementById('clientDesignation').value;
    const description = document.getElementById('clientDescription').value;
    const imageFile = document.getElementById('clientImage').files[0];
    
    let imageBase64 = null;
    if (imageFile) {
        imageBase64 = await fileToBase64(imageFile);
    }
    
    const clientData = {
        client_name: name,
        designation: designation || null,
        description: description || null,
        client_image: imageBase64
    };
    
    try {
        if (id) {
            await apiRequest(API_ENDPOINTS.ADMIN_CLIENT(id), {
                method: 'PUT',
                body: JSON.stringify(clientData)
            });
            showToast('Client updated successfully', 'success');
        } else {
            await apiRequest(API_ENDPOINTS.ADMIN_CLIENTS, {
                method: 'POST',
                body: JSON.stringify(clientData)
            });
            showToast('Client created successfully', 'success');
        }
        
        closeClientModal();
        loadClients();
        loadDashboard();
    } catch (error) {
        showToast(error.message || 'Failed to save client', 'error');
    }
});

// ===================================
// CONTACTS MANAGEMENT
// ===================================

async function loadContacts() {
    const container = document.getElementById('contactsTable');
    container.innerHTML = '<div class="loading">Loading contacts...</div>';
    
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_CONTACTS);
        
        if (!data.contacts || data.contacts.length === 0) {
            container.innerHTML = '<div class="empty-state">No contact messages found</div>';
            return;
        }
        
        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Subject</th>
                        <th>Status</th>
                        <th>Submitted</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.contacts.forEach(contact => {
            const statusClass = contact.status === 'pending' ? 'status-pending' : 
                               contact.status === 'read' ? 'status-read' : 'status-responded';
            
            html += `
                <tr>
                    <td><strong>${contact.name}</strong></td>
                    <td>${contact.email}</td>
                    <td>${contact.subject}</td>
                    <td><span class="status-badge ${statusClass}">${contact.status}</span></td>
                    <td>${new Date(contact.submitted_at).toLocaleString()}</td>
                    <td class="table-actions">
                        <button class="btn-icon btn-view" onclick="viewContact(${contact.contact_id})" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn-icon btn-delete" onclick="deleteContact(${contact.contact_id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<div class="error-state">Failed to load contacts</div>';
    }
}

async function viewContact(id) {
    try {
        const contact = await apiRequest(API_ENDPOINTS.ADMIN_CONTACT(id));
        
        const html = `
            <div class="contact-detail">
                <div class="detail-row">
                    <strong>Name:</strong>
                    <span>${contact.name}</span>
                </div>
                <div class="detail-row">
                    <strong>Email:</strong>
                    <span>${contact.email}</span>
                </div>
                <div class="detail-row">
                    <strong>Phone:</strong>
                    <span>${contact.phone || 'N/A'}</span>
                </div>
                <div class="detail-row">
                    <strong>Subject:</strong>
                    <span>${contact.subject}</span>
                </div>
                <div class="detail-row">
                    <strong>Message:</strong>
                    <p>${contact.message}</p>
                </div>
                <div class="detail-row">
                    <strong>Status:</strong>
                    <select class="form-select" id="contactStatus">
                        <option value="pending" ${contact.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="read" ${contact.status === 'read' ? 'selected' : ''}>Read</option>
                        <option value="responded" ${contact.status === 'responded' ? 'selected' : ''}>Responded</option>
                    </select>
                    <button class="btn btn-primary btn-small" onclick="updateContactStatus(${contact.contact_id})">
                        Update Status
                    </button>
                </div>
                <div class="detail-row">
                    <strong>Submitted:</strong>
                    <span>${new Date(contact.submitted_at).toLocaleString()}</span>
                </div>
            </div>
        `;
        
        document.getElementById('contactDetails').innerHTML = html;
        document.getElementById('contactModal').classList.add('show');
    } catch (error) {
        showToast('Failed to load contact details', 'error');
    }
}

function closeContactModal() {
    document.getElementById('contactModal').classList.remove('show');
}

async function updateContactStatus(id) {
    const status = document.getElementById('contactStatus').value;
    
    try {
        await apiRequest(API_ENDPOINTS.ADMIN_CONTACT(id), {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
        showToast('Contact status updated', 'success');
        closeContactModal();
        loadContacts();
    } catch (error) {
        showToast(error.message || 'Failed to update status', 'error');
    }
}

async function deleteContact(id) {
    if (!confirm('Are you sure you want to delete this contact message?')) return;
    
    try {
        await apiRequest(API_ENDPOINTS.ADMIN_CONTACT(id), { method: 'DELETE' });
        showToast('Contact deleted successfully', 'success');
        loadContacts();
        loadDashboard();
    } catch (error) {
        showToast(error.message || 'Failed to delete contact', 'error');
    }
}

// ===================================
// SUBSCRIPTIONS MANAGEMENT
// ===================================

async function loadSubscriptions() {
    const container = document.getElementById('subscriptionsTable');
    container.innerHTML = '<div class="loading">Loading subscriptions...</div>';
    
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_SUBSCRIPTIONS);
        
        if (!data.subscriptions || data.subscriptions.length === 0) {
            container.innerHTML = '<div class="empty-state">No subscriptions found</div>';
            return;
        }
        
        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Email</th>
                        <th>Status</th>
                        <th>Subscribed</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.subscriptions.forEach(sub => {
            const statusClass = sub.status === 'active' ? 'status-active' : 'status-unsubscribed';
            
            html += `
                <tr>
                    <td><strong>${sub.email}</strong></td>
                    <td><span class="status-badge ${statusClass}">${sub.status}</span></td>
                    <td>${new Date(sub.subscribed_at).toLocaleString()}</td>
                    <td class="table-actions">
                        <button class="btn-icon btn-delete" onclick="deleteSubscription(${sub.subscription_id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<div class="error-state">Failed to load subscriptions</div>';
    }
}

async function deleteSubscription(id) {
    if (!confirm('Are you sure you want to delete this subscription?')) return;
    
    try {
        await apiRequest(API_ENDPOINTS.ADMIN_SUBSCRIPTION(id), { method: 'DELETE' });
        showToast('Subscription deleted successfully', 'success');
        loadSubscriptions();
        loadDashboard();
    } catch (error) {
        showToast(error.message || 'Failed to delete subscription', 'error');
    }
}

// Initialize Dashboard on Load
loadDashboard();
