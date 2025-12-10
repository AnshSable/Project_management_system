// API Configuration
// Auto-detect if running from integrated backend or standalone
const API_BASE_URL = window.location.origin;

const API_ENDPOINTS = {
    // Auth
    ADMIN_LOGIN: `${API_BASE_URL}/api/admin/login`,
    USER_SIGNUP: `${API_BASE_URL}/api/user/signup`,
    USER_LOGIN: `${API_BASE_URL}/api/user/login`,
    
    // Projects
    USER_PROJECTS: `${API_BASE_URL}/api/user/projects`,
    ADMIN_PROJECTS: `${API_BASE_URL}/api/admin/projects`,
    ADMIN_ADD_PROJECT: `${API_BASE_URL}/api/admin/add_project`,
    ADMIN_PROJECT: (id) => `${API_BASE_URL}/api/admin/projects/${id}`,
    ADMIN_UPDATE_PROJECT: (id) => `${API_BASE_URL}/api/admin/projects/${id}`,
    ADMIN_DELETE_PROJECT: (id) => `${API_BASE_URL}/api/admin/projects/${id}`,
    
    // Clients
    USER_CLIENTS: `${API_BASE_URL}/api/user/clients`,
    ADMIN_CLIENTS: `${API_BASE_URL}/api/admin/clients`,
    ADMIN_ADD_CLIENT: `${API_BASE_URL}/api/admin/add_client`,
    ADMIN_CLIENT: (id) => `${API_BASE_URL}/api/admin/clients/${id}`,
    ADMIN_UPDATE_CLIENT: (id) => `${API_BASE_URL}/api/admin/clients/${id}`,
    ADMIN_DELETE_CLIENT: (id) => `${API_BASE_URL}/api/admin/clients/${id}`,
    
    // Contact
    SUBMIT_CONTACT: `${API_BASE_URL}/api/contact`,
    ADMIN_CONTACTS: `${API_BASE_URL}/api/admin/contacts`,
    ADMIN_CONTACT: (id) => `${API_BASE_URL}/api/admin/contacts/${id}`,
    ADMIN_UPDATE_CONTACT: (id) => `${API_BASE_URL}/api/admin/contacts/${id}`,
    ADMIN_DELETE_CONTACT: (id) => `${API_BASE_URL}/api/admin/contacts/${id}`,
    
    // Subscription
    SUBSCRIBE: `${API_BASE_URL}/api/subscribe`,
    UNSUBSCRIBE: `${API_BASE_URL}/api/unsubscribe`,
    ADMIN_SUBSCRIPTIONS: `${API_BASE_URL}/api/admin/subscriptions`,
    ADMIN_SUBSCRIPTION: (id) => `${API_BASE_URL}/api/admin/subscriptions/${id}`,
    ADMIN_UPDATE_SUBSCRIPTION: (id) => `${API_BASE_URL}/api/admin/subscriptions/${id}`,
    ADMIN_DELETE_SUBSCRIPTION: (id) => `${API_BASE_URL}/api/admin/subscriptions/${id}`
};

// Token Storage Keys
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_data';
const ROLE_KEY = 'user_role';
