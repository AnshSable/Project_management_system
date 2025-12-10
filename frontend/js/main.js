// Main Application Logic

// Toast Notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// Load Projects
async function loadProjects() {
    const projectsGrid = document.getElementById('projectsGrid');
    projectsGrid.innerHTML = '<div class="loading">Loading projects...</div>';
    
    try {
        let data;
        if (isAuthenticated()) {
            data = await apiRequest(API_ENDPOINTS.USER_PROJECTS);
        } else {
            // For non-authenticated users, show a message
            projectsGrid.innerHTML = `
                <div class="auth-required">
                    <i class="fas fa-lock"></i>
                    <h3>Login Required</h3>
                    <p>Please login to view projects</p>
                    <button class="btn btn-primary" onclick="showLoginModal()">Login</button>
                </div>
            `;
            return;
        }
        
        if (!data.projects || data.projects.length === 0) {
            projectsGrid.innerHTML = '<div class="empty-state">No projects available</div>';
            return;
        }
        
        projectsGrid.innerHTML = data.projects.map(project => `
            <div class="card project-card">
                <div class="card-image">
                    ${project.project_image ? 
                        `<img src="${project.project_image}" alt="${project.project_name}">` :
                        `<div class="placeholder-image"><i class="fas fa-project-diagram"></i></div>`
                    }
                </div>
                <div class="card-content">
                    <h3 class="card-title">${project.project_name}</h3>
                    <p class="card-description">${project.description || 'No description available'}</p>
                    <p class="card-date"><i class="far fa-calendar"></i> ${new Date(project.created_at).toLocaleDateString()}</p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
        projectsGrid.innerHTML = '<div class="error-state">Failed to load projects</div>';
    }
}

// Load Clients
async function loadClients() {
    const clientsGrid = document.getElementById('clientsGrid');
    clientsGrid.innerHTML = '<div class="loading">Loading clients...</div>';
    
    try {
        let data;
        if (isAuthenticated()) {
            data = await apiRequest(API_ENDPOINTS.USER_CLIENTS);
        } else {
            clientsGrid.innerHTML = `
                <div class="auth-required">
                    <i class="fas fa-lock"></i>
                    <h3>Login Required</h3>
                    <p>Please login to view clients</p>
                    <button class="btn btn-primary" onclick="showLoginModal()">Login</button>
                </div>
            `;
            return;
        }
        
        if (!data.clients || data.clients.length === 0) {
            clientsGrid.innerHTML = '<div class="empty-state">No clients available</div>';
            return;
        }
        
        clientsGrid.innerHTML = data.clients.map(client => `
            <div class="card client-card">
                <div class="card-image">
                    ${client.client_image ? 
                        `<img src="${client.client_image}" alt="${client.client_name}">` :
                        `<div class="placeholder-image"><i class="fas fa-user"></i></div>`
                    }
                </div>
                <div class="card-content">
                    <h3 class="card-title">${client.client_name}</h3>
                    ${client.designation ? `<p class="client-designation">${client.designation}</p>` : ''}
                    <p class="card-description">${client.description || 'No description available'}</p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading clients:', error);
        clientsGrid.innerHTML = '<div class="error-state">Failed to load clients</div>';
    }
}

// Contact Form
async function handleContactForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    try {
        await apiRequest(API_ENDPOINTS.SUBMIT_CONTACT, {
            method: 'POST',
            body: JSON.stringify(data),
            skipAuth: true
        });
        
        showToast('Thank you! Your message has been sent.', 'success');
        form.reset();
    } catch (error) {
        showToast(error.message || 'Failed to send message', 'error');
    }
}

// Newsletter Subscription
async function handleNewsletter(event) {
    event.preventDefault();
    const form = event.target;
    const email = form.querySelector('input[type="email"]').value;
    
    try {
        await apiRequest(API_ENDPOINTS.SUBSCRIBE, {
            method: 'POST',
            body: JSON.stringify({ email }),
            skipAuth: true
        });
        
        showToast('Successfully subscribed to newsletter!', 'success');
        form.reset();
    } catch (error) {
        showToast(error.message || 'Subscription failed', 'error');
    }
}

// Navigation
function scrollToProjects() {
    document.getElementById('projects').scrollIntoView({ behavior: 'smooth' });
}

function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.querySelector('.hamburger');
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
}

// Smooth Scrolling for Navigation Links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth' });
            
            // Update active link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Close mobile menu if open
            const navMenu = document.querySelector('.nav-menu');
            const hamburger = document.querySelector('.hamburger');
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });
});

// Intersection Observer for Scroll Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Initialize on Page Load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize auth UI
    updateUIForAuth();
    
    // Load content if authenticated
    if (isAuthenticated()) {
        loadProjects();
        loadClients();
    } else {
        // Show login prompt for projects and clients
        loadProjects();
        loadClients();
    }
    
    // Contact Form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
    
    // Newsletter Form
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletter);
    }
    
    // Observe sections for animations
    document.querySelectorAll('.section').forEach(section => {
        observer.observe(section);
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});

// Expose functions to global scope
window.showLoginModal = showLoginModal;
window.closeLoginModal = closeLoginModal;
window.showSignupModal = showSignupModal;
window.closeSignupModal = closeSignupModal;
window.logout = logout;
window.scrollToProjects = scrollToProjects;
window.toggleMenu = toggleMenu;
window.switchTab = switchTab;
