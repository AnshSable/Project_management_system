# Project Management System - Frontend

A modern, responsive frontend application for the Project Management System with authentication, admin panel, and dynamic content management.

## 🎨 Features

### Public Features
- **Landing Page** with hero section and call-to-action
- **Projects Showcase** (requires login)
- **Clients Display** (requires login)
- **Contact Form** (public access)
- **Newsletter Subscription** (public access)
- Responsive design for mobile, tablet, and desktop

### Authentication
- **User Login/Signup** - Access projects and clients
- **Admin Login** - Full CRUD operations on all resources
- **JWT Token Management** - Secure, temporary storage in sessionStorage
- **Auto-logout** on token expiration (401 errors)
- **Role-based UI** - Different navigation for users vs admins

### Admin Panel
- **Dashboard** with statistics (total projects, clients, contacts, subscriptions)
- **Projects Management** - Create, Read, Update, Delete projects
- **Clients Management** - Full CRUD operations for clients
- **Contact Messages** - View, update status, delete messages
- **Subscriptions** - Manage newsletter subscriptions
- **Image Upload** with automatic cropping to 450x350 pixels
- **Real-time Updates** after every operation

## 📁 File Structure

```
frontend/
├── index.html              # Main landing page
├── admin.html              # Admin dashboard
├── css/
│   ├── style.css          # Main styles
│   └── admin.css          # Admin panel styles
└── js/
    ├── config.js          # API configuration
    ├── auth.js            # Authentication logic
    ├── main.js            # Main page functionality
    └── admin.js           # Admin panel functionality
```

## 🚀 Getting Started

### Prerequisites
- Backend API running on `http://localhost:8000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Setup

1. **Start the Backend Server**
   ```bash
   cd /path/to/Project_management_system
   uvicorn app:app --reload
   ```

2. **Open Frontend**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     python -m http.server 8080
     # Visit http://localhost:8080
     ```

### Default Admin Credentials
```
Username: admin
Password: admin123
```

## 🔐 Authentication Flow

### User Journey
1. Visit `index.html`
2. Click "Login" button
3. Choose "User" or "Admin" tab
4. Enter credentials
5. Token stored in sessionStorage
6. Access projects and clients (User)
7. Access admin panel (Admin)

### Token Storage
- **Storage Type**: sessionStorage (temporary, clears on browser close)
- **Token Expiry**: 10 hours (600 minutes)
- **Auto-refresh**: No (user must re-login after expiry)
- **Security**: Token sent as Bearer token in Authorization header

### Logout
- Clears all session data
- Redirects to main page
- Updates UI to show login button

## 🎯 Usage Guide

### For Users

#### View Projects and Clients
1. Login with user credentials
2. Projects and clients automatically load
3. View project images, descriptions, and dates
4. Browse client information

#### Submit Contact Form
1. Scroll to "Contact Us" section
2. Fill in: Name, Email, Phone (optional), Subject, Message
3. Click "Send Message"
4. No login required!

#### Subscribe to Newsletter
1. Scroll to newsletter section
2. Enter email address
3. Click "Subscribe"
4. Receive confirmation toast

### For Admins

#### Access Admin Panel
1. Login with admin credentials
2. Automatically redirected to `admin.html`
3. View dashboard with statistics

#### Manage Projects
1. Click "Projects" in sidebar
2. Click "Add Project" button
3. Fill form: Project Name*, Description, Image
4. Image automatically cropped to 450x350
5. Click "Save Project"
6. Edit: Click edit icon → Modify → Save
7. Delete: Click delete icon → Confirm

#### Manage Clients
1. Click "Clients" in sidebar
2. Click "Add Client" button
3. Fill form: Client Name*, Designation, Description, Image
4. Image automatically cropped to 450x350
5. Click "Save Client"
6. Edit/Delete similar to projects

#### Manage Contact Messages
1. Click "Contact Messages" in sidebar
2. View all submissions
3. Click "View" icon to see full message
4. Update status: Pending → Read → Responded
5. Delete unwanted messages

#### Manage Subscriptions
1. Click "Subscriptions" in sidebar
2. View all newsletter subscriptions
3. See active/unsubscribed status
4. Delete subscriptions if needed

## 🎨 Design Features

### Color Scheme
- **Primary**: Indigo (#6366f1)
- **Secondary**: Pink (#ec4899)
- **Accent**: Teal (#14b8a6)
- **Success**: Green (#10b981)
- **Error**: Red (#ef4444)

### Typography
- **Headings**: Poppins
- **Body**: Inter
- **Fallback**: System fonts

### Responsive Breakpoints
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

### Animations
- Fade-in on scroll
- Floating cards in hero section
- Hover effects on cards and buttons
- Smooth page transitions
- Toast slide-in notifications

## 🔧 Customization

### Change API URL
Edit `frontend/js/config.js`:
```javascript
const API_BASE_URL = 'http://your-api-url:port';
```

### Modify Colors
Edit `frontend/css/style.css`:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    /* ... more colors */
}
```

### Update Logo/Branding
Edit `frontend/index.html` and `frontend/admin.html`:
```html
<a href="/" class="nav-brand">Your Brand Name</a>
```

## 📱 Mobile Responsiveness

### Features
- Hamburger menu for mobile navigation
- Stacked grid layouts on small screens
- Touch-friendly buttons and forms
- Optimized font sizes
- Collapsible admin sidebar

### Testing
Test on various devices:
- iPhone (Safari)
- Android (Chrome)
- Tablet (iPad)
- Desktop (all major browsers)

## 🐛 Troubleshooting

### Projects/Clients Not Loading
**Problem**: "Login Required" message appears
**Solution**: Click "Login" button and authenticate

### Image Upload Not Working
**Problem**: Images not displaying after upload
**Solution**: Backend automatically crops to 450x350 and returns base64

### Token Expired
**Problem**: 401 errors after some time
**Solution**: Re-login (token expires after 10 hours)

### Admin Panel Not Accessible
**Problem**: Redirected to index.html
**Solution**: Login with admin credentials, not user credentials

### CORS Errors
**Problem**: Network errors in console
**Solution**: Ensure backend CORS is properly configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔒 Security Notes

### Best Practices Implemented
- ✅ JWT tokens in sessionStorage (temporary)
- ✅ Bearer token authentication
- ✅ Automatic logout on 401
- ✅ Password fields masked
- ✅ Admin-only routes protected
- ✅ Form validation

### Security Considerations
- sessionStorage clears when browser closes
- Tokens not stored in localStorage (persistent)
- HTTPS recommended for production
- Input sanitization on backend
- No sensitive data in frontend code

## 🚀 Production Deployment

### Steps
1. **Update API URL** in `config.js`
2. **Enable HTTPS** for secure token transmission
3. **Minify CSS/JS** for faster loading
4. **Optimize Images** before upload
5. **Set Proper CORS** on backend
6. **Use CDN** for Font Awesome

### Recommended Hosting
- **Static Hosting**: Netlify, Vercel, GitHub Pages
- **Server**: Nginx, Apache
- **CDN**: Cloudflare

## 📊 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ Internet Explorer: Not supported

## 📝 API Integration

All API calls use the `apiRequest()` function from `auth.js`:

```javascript
// Automatic token injection
const data = await apiRequest('/api/user/projects');

// With options
const data = await apiRequest('/api/admin/projects', {
    method: 'POST',
    body: JSON.stringify(projectData)
});

// Skip authentication (public endpoints)
const data = await apiRequest('/api/contact', {
    method: 'POST',
    body: JSON.stringify(contactData),
    skipAuth: true
});
```

## 🎯 Future Enhancements

- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Advanced search and filters
- [ ] Bulk operations in admin panel
- [ ] Export data to Excel/PDF
- [ ] Real-time notifications with WebSockets
- [ ] Image gallery for projects
- [ ] Client testimonials section
- [ ] Blog/News section

## 📞 Support

For issues or questions:
- Check backend API documentation
- Review console errors in browser DevTools
- Verify network requests in Network tab
- Ensure backend is running on port 8000

## 📄 License

Part of the Project Management System. See main repository for license details.

---

**Built with** ❤️ using vanilla JavaScript, HTML5, and CSS3
