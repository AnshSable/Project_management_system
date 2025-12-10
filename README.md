# Project Management System

A FastAPI-based project management system using Excel files for data storage (to be migrated to MongoDB Atlas later).

## Features

### Authentication & Authorization
- **JWT-based authentication** for secure API access
- **Role-based access control** (Admin vs User)
- **Token expiration** (60 minutes)

### Admin Panel
1. **Project Management**
   - View all current projects
   - Add new projects
   - Update existing projects
   - Delete projects

2. **Client Management**
   - View all clients
   - Add new clients
   - Update client information
   - Delete clients

### User Panel
- **Read-Only Access**
  - View all projects
  - View all clients
  - Cannot perform any CRUD operations

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Sample Data
```bash
python init_data.py
```

This will create:
- `data/admin_credentials.xlsx` - Admin login credentials
- `data/user_credentials.xlsx` - User login credentials
- `data/projects.xlsx` - Sample projects
- `data/clients.xlsx` - Sample clients

### 3. Run the Application
```bash
python app.py
```

The server will start at `http://localhost:8000`

You can also access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Managing Admin Accounts

Admin accounts cannot be created through the API. To add new admins:

### Option 1: Use the Admin Management Tool (Easiest)
```bash
python add_admin.py
```

This interactive script allows you to:
- Add new admin accounts
- List existing admins
- Automatically hash passwords

### Option 2: Modify init_data.py
Edit `init_data.py` to include new admin credentials and run:
```bash
python init_data.py
```

### Option 3: Manual Excel Entry
Directly edit `data/admin_credentials.xlsx` (requires password hashing)

## Sample Credentials

### Admin Login (Pre-configured)
- Username: `admin1` | Password: `admin123`
- Username: `admin2` | Password: `admin456`

**Note:** To add new admins, manually edit `data/admin_credentials.xlsx` or modify `init_data.py`

### User Login (Can self-register)
- Username: `user1` | Password: `user123`
- Username: `user2` | Password: `user456`

## API Endpoints

### Authentication (No token required)

**Note:** Admin accounts must be added manually to `data/admin_credentials.xlsx`. Use the `init_data.py` script or add entries directly to the Excel file.

#### Admin Login
```
POST /api/admin/login
Body: {
  "username": "string",
  "password": "string"
}
Response: {
  "access_token": "JWT token",
  "token_type": "bearer",
  "role": "admin"
}
```

#### User Signup
```
POST /api/user/signup
Body: {
  "username": "string",
  "password": "string",
  "email": "string"
}
```

#### User Login
```
POST /api/user/login
Body: {
  "username": "string",
  "password": "string"
}
Response: {
  "access_token": "JWT token",
  "token_type": "bearer",
  "role": "user"
}
```

### Project Management (Admin - Requires Admin Token)

**Note:** All admin endpoints require the JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

#### Get All Projects
```
GET /api/admin/projects
```

#### Add Project
```
POST /api/admin/add_project
Headers: Authorization: Bearer <admin_token>
Body: {
  "project_name": "string",
  "description": "string",
  "client_name": "string",
  "status": "Active|Completed",
  "start_date": "YYYY-MM-DD"
}
```

#### Update Project
```
PUT /api/admin/projects/<project_id>
Body: {
  "project_name": "string",
  "description": "string",
  "client_name": "string",
  "status": "Active|Completed",
  "start_date": "YYYY-MM-DD"
}
```

#### Delete Project
```
DELETE /api/admin/projects/<project_id>
```

### Client Management (Admin - Requires Admin Token)

#### Get All Clients
```
GET /api/admin/clients
```

#### Add Client
```
POST /api/admin/add_client
Headers: Authorization: Bearer <admin_token>
Body: {
  "client_name": "string",
  "email": "string",
  "phone": "string",
  "company": "string"
}
```

#### Update Client
```
PUT /api/admin/clients/<client_id>
Body: {
  "client_name": "string",
  "email": "string",
  "phone": "string",
  "company": "string"
}
```

#### Delete Client
```
DELETE /api/admin/clients/<client_id>
Headers: Authorization: Bearer <admin_token>
```

### User Endpoints (Read-Only - Requires User Token)

#### Get All Projects
```
GET /api/user/projects
Headers: Authorization: Bearer <user_token>
```

#### Get All Clients
```
GET /api/user/clients
Headers: Authorization: Bearer <user_token>
```

## Data Storage

Currently using Excel files stored in the `data/` directory:
- `admin_credentials.xlsx` - Admin users
- `user_credentials.xlsx` - Regular users
- `projects.xlsx` - Project information
- `clients.xlsx` - Client information

## Testing with Postman/cURL

### Step 1: Login

Example admin login request:
```bash
curl -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin1","password":"admin123"}'
```

**Save the `access_token` from the response!**

### Step 2: Use Token for Protected Endpoints

Example get projects (with token):
```bash
curl -X GET http://localhost:8000/api/admin/projects \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Example add project (with token):
```bash
curl -X POST http://localhost:8000/api/admin/add_project \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name":"New Project",
    "description":"Project description",
    "client_name":"John Doe",
    "status":"Active"
  }'
```

### Testing User Access (Read-Only)

```bash
# Login as user
curl -X POST http://localhost:8000/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"user123"}'

# View projects (with user token)
curl -X GET http://localhost:8000/api/user/projects \
  -H "Authorization: Bearer USER_TOKEN_HERE"

# Try to add project (will fail with 403 Forbidden)
curl -X POST http://localhost:8000/api/admin/add_project \
  -H "Authorization: Bearer USER_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"project_name":"Test","client_name":"John"}'
```

Or simply visit `http://localhost:8000/docs` for interactive API testing with Swagger UI.

## Important Notes

1. **JWT Tokens**: All protected endpoints require authentication
2. **Admin vs User**: Admins have full CRUD access, Users can only view
3. **Token Expiration**: Tokens expire after 60 minutes
4. **Swagger UI**: Use the "Authorize" button in Swagger UI to set your token
5. See `API_GUIDE.md` for detailed authentication documentation "description":"Project description",
    "client_name":"John Doe",
    "status":"Active"
  }'
```


==> Cloning from https://github.com/AnshSable/Project_management_system
==> Checking out commit 5d7d5052ea3edc359ccf45f870dd0ac54a60756c in branch main
==> Installing Python version 3.13.4...
==> Using Python version 3.13.4 (default)
==> Docs on specifying a Python version: https://render.com/docs/python-version
==> Using Poetry version 2.1.3 (default)
==> Docs on specifying a Poetry version: https://render.com/docs/poetry-version
==> Running build command ' pip install -r backend/requirements.txt'...
[notice] A new release of pip is available: 25.1.1 -> 25.3
[notice] To update, run: pip install --upgrade pip
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'backend/requirements.txt'
==> Build failed 😞
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
