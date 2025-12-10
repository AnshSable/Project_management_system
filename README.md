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
2025-12-10T10:41:37.173586045Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 98.8 MB/s eta 0:00:00
2025-12-10T10:41:37.177705981Z Downloading PyJWT-2.10.1-py3-none-any.whl (22 kB)
2025-12-10T10:41:37.187858925Z Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
2025-12-10T10:41:37.196425045Z Downloading python_dotenv-1.0.0-py3-none-any.whl (19 kB)
2025-12-10T10:41:37.203472893Z Downloading python_jose-3.5.0-py2.py3-none-any.whl (34 kB)
2025-12-10T10:41:37.210672894Z Downloading rsa-4.9.1-py3-none-any.whl (34 kB)
2025-12-10T10:41:37.217862116Z Downloading python_multipart-0.0.20-py3-none-any.whl (24 kB)
2025-12-10T10:41:37.225795138Z Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
2025-12-10T10:41:37.236025634Z Downloading requests-2.32.5-py3-none-any.whl (64 kB)
2025-12-10T10:41:37.243689849Z Downloading urllib3-2.6.1-py3-none-any.whl (131 kB)
2025-12-10T10:41:37.251966811Z Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
2025-12-10T10:41:37.259562423Z Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
2025-12-10T10:41:37.266403675Z Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
2025-12-10T10:41:37.273511334Z Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
2025-12-10T10:41:37.282709901Z Downloading uvicorn-0.38.0-py3-none-any.whl (68 kB)
2025-12-10T10:41:37.291684593Z Downloading werkzeug-3.0.1-py3-none-any.whl (226 kB)
2025-12-10T10:41:37.389473442Z Building wheels for collected packages: jose
2025-12-10T10:41:37.390417688Z   Building wheel for jose (pyproject.toml): started
2025-12-10T10:41:37.633518556Z   Building wheel for jose (pyproject.toml): finished with status 'done'
2025-12-10T10:41:37.634428342Z   Created wheel for jose: filename=jose-1.0.0-py3-none-any.whl size=8900 sha256=429b27685962baaad4b258584741c822500d93bb3f4470e468d5dfc61a779343
2025-12-10T10:41:37.634598536Z   Stored in directory: /opt/render/.cache/wheels/07/6e/e2/d6818308c2db8a78e5ee25938e141f615e6a4ce48de266b390
2025-12-10T10:41:37.636717396Z Successfully built jose
2025-12-10T10:41:37.748566768Z Installing collected packages: pytz, passlib, jose, urllib3, tzdata, typing_extensions, six, python-multipart, python-dotenv, PyJWT, pycparser, pyasn1, pillow, numpy, MarkupSafe, itsdangerous, idna, h11, et_xmlfile, dnspython, click, charset-normalizer, certifi, blinker, bcrypt, annotated-types, annotated-doc, Werkzeug, uvicorn, typing-inspection, rsa, requests, python-dateutil, pymongo, pydantic_core, openpyxl, Jinja2, email-validator, ecdsa, cffi, anyio, starlette, python-jose, pydantic, pandas, motor, Flask, cryptography, pydantic-settings, jwt, Flask-Cors, fastapi
2025-12-10T10:41:55.561636487Z 
2025-12-10T10:41:55.571361119Z Successfully installed Flask-3.0.0 Flask-Cors-4.0.0 Jinja2-3.1.6 MarkupSafe-3.0.3 PyJWT-2.10.1 Werkzeug-3.0.1 annotated-doc-0.0.4 annotated-types-0.7.0 anyio-4.12.0 bcrypt-4.0.1 blinker-1.9.0 certifi-2025.11.12 cffi-2.0.0 charset-normalizer-3.4.4 click-8.3.1 cryptography-46.0.3 dnspython-2.8.0 ecdsa-0.19.1 email-validator-2.3.0 et_xmlfile-2.0.0 fastapi-0.124.0 h11-0.16.0 idna-3.11 itsdangerous-2.2.0 jose-1.0.0 jwt-1.4.0 motor-3.7.1 numpy-2.3.5 openpyxl-3.1.5 pandas-2.3.3 passlib-1.7.4 pillow-12.0.0 pyasn1-0.6.1 pycparser-2.23 pydantic-2.12.5 pydantic-settings-2.12.0 pydantic_core-2.41.5 pymongo-4.15.5 python-dateutil-2.9.0.post0 python-dotenv-1.0.0 python-jose-3.5.0 python-multipart-0.0.20 pytz-2025.2 requests-2.32.5 rsa-4.9.1 six-1.17.0 starlette-0.50.0 typing-inspection-0.4.2 typing_extensions-4.15.0 tzdata-2025.2 urllib3-2.6.1 uvicorn-0.38.0
2025-12-10T10:41:55.684459647Z 
2025-12-10T10:41:55.684485787Z [notice] A new release of pip is available: 25.1.1 -> 25.3
2025-12-10T10:41:55.684491077Z [notice] To update, run: pip install --upgrade pip
2025-12-10T10:42:02.057751685Z ==> Uploading build...
2025-12-10T10:42:20.895955553Z ==> Uploaded in 14.7s. Compression took 4.1s
2025-12-10T10:42:20.992636681Z ==> Build successful 🎉
2025-12-10T10:42:30.436332532Z ==> Setting WEB_CONCURRENCY=1 by default, based on available CPUs in the instance
2025-12-10T10:42:30.60438526Z ==> Deploying...
2025-12-10T10:43:03.412811564Z ==> Running 'cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT'
2025-12-10T10:43:15.513761604Z INFO:     Started server process [57]
2025-12-10T10:43:15.513890797Z INFO:     Waiting for application startup.
2025-12-10T10:43:15.514142832Z INFO:     Application startup complete.
2025-12-10T10:43:15.514391418Z INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
2025-12-10T10:43:16.257428774Z INFO:     127.0.0.1:38478 - "HEAD / HTTP/1.1" 405 Method Not Allowed
2025-12-10T10:43:21.435451835Z ==> Your service is live 🎉
2025-12-10T10:43:21.630937417Z ==> 
2025-12-10T10:43:21.81975609Z ==> ///////////////////////////////////////////////////////////
2025-12-10T10:43:22.040158329Z ==> 
2025-12-10T10:43:22.231339402Z ==> Available at your primary URL https://project-management-system-svt3.onrender.com
2025-12-10T10:43:22.420814774Z ==> 
2025-12-10T10:43:22.613654207Z ==> ///////////////////////////////////////////////////////////
2025-12-10T10:43:25.549793087Z INFO:     35.230.45.39:0 - "GET / HTTP/1.1" 404 Not Found
2025-12-10T10:43:30.039216244Z INFO:     49.43.7.225:0 - "GET / HTTP/1.1" 404 Not Found
2025-12-10T10:43:30.210032336Z INFO:     49.43.7.225:0 - "GET /favicon.ico HTTP/1.1" 404 Not Found
2025-12-10T10:43:50.340313055Z INFO:     49.43.7.225:0 - "GET / HTTP/1.1" 404 Not Found
