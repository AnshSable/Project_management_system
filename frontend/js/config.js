// API Configuration
// Auto-detect if running from integrated backend or standalone
const API_BASE_URL = window.location.origin; // This works for both local and deployed

const API_ENDPOINTS = {
    // Auth
    ADMIN_LOGIN: `${API_BASE_URL}/api/admin/login`,
    USER_SIGNUP: `${API_BASE_URL}/api/user/signup`,
    USER_LOGIN: `${API_BASE_URL}/api/user/login`,
    
    // Projects
    USER_PROJECTS: '/api/user/projects',
    ADMIN_PROJECTS: '/api/admin/projects',
    ADMIN_ADD_PROJECT: '/api/admin/add_project',
    ADMIN_PROJECT: (id) => `/api/admin/projects/${id}`,
    ADMIN_UPDATE_PROJECT: (id) => `/api/admin/projects/${id}`,
    ADMIN_DELETE_PROJECT: (id) => `/api/admin/projects/${id}`,
    
    // Clients
    USER_CLIENTS: '/api/user/clients',
    ADMIN_CLIENTS: '/api/admin/clients',
    ADMIN_ADD_CLIENT: '/api/admin/add_client',
    ADMIN_CLIENT: (id) => `/api/admin/clients/${id}`,
    ADMIN_UPDATE_CLIENT: (id) => `/api/admin/clients/${id}`,
    ADMIN_DELETE_CLIENT: (id) => `/api/admin/clients/${id}`,
    
    // Contact
    SUBMIT_CONTACT: '/api/contact',
    ADMIN_CONTACTS: '/api/admin/contacts',
    ADMIN_CONTACT: (id) => `/api/admin/contacts/${id}`,
    ADMIN_UPDATE_CONTACT: (id) => `/api/admin/contacts/${id}`,
    ADMIN_DELETE_CONTACT: (id) => `/api/admin/contacts/${id}`,
    
    // Subscription
    SUBSCRIBE: '/api/subscribe',
    UNSUBSCRIBE: '/api/unsubscribe',
    ADMIN_SUBSCRIPTIONS: '/api/admin/subscriptions',
    ADMIN_SUBSCRIPTION: (id) => `/api/admin/subscriptions/${id}`,
    ADMIN_UPDATE_SUBSCRIPTION: (id) => `/api/admin/subscriptions/${id}`,
    ADMIN_DELETE_SUBSCRIPTION: (id) => `/api/admin/subscriptions/${id}`
};

// Token Storage Keys
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_data';
const ROLE_KEY = 'user_role';
