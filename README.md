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

2025-12-10T06:55:05.775355095Z ==> Cloning from https://github.com/AnshSable/Project_management_system
2025-12-10T06:55:06.76313351Z ==> Checking out commit f0c100441ebb48395ae871b36f00568b6fc6e99a in branch main
2025-12-10T06:55:10.581903653Z ==> Installing Python version 3.13.4...
2025-12-10T06:55:24.268587963Z ==> Using Python version 3.13.4 (default)
2025-12-10T06:55:24.293764614Z ==> Docs on specifying a Python version: https://render.com/docs/python-version
2025-12-10T06:55:28.640582428Z ==> Using Poetry version 2.1.3 (default)
2025-12-10T06:55:28.687218452Z ==> Docs on specifying a Poetry version: https://render.com/docs/poetry-version
2025-12-10T06:55:28.763809935Z ==> Running build command ' pip install -r backend/requirements.txt'...
2025-12-10T06:55:29.444955944Z Collecting annotated-doc==0.0.4 (from -r backend/requirements.txt (line 1))
2025-12-10T06:55:29.491403579Z   Downloading annotated_doc-0.0.4-py3-none-any.whl.metadata (6.6 kB)
2025-12-10T06:55:29.704171247Z Collecting annotated-types==0.7.0 (from -r backend/requirements.txt (line 2))
2025-12-10T06:55:29.710547386Z   Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
2025-12-10T06:55:29.832139351Z Collecting anyio==4.12.0 (from -r backend/requirements.txt (line 3))
2025-12-10T06:55:29.836432496Z   Downloading anyio-4.12.0-py3-none-any.whl.metadata (4.3 kB)
2025-12-10T06:55:29.96417959Z Collecting bcrypt==4.0.1 (from -r backend/requirements.txt (line 4))
2025-12-10T06:55:29.969240753Z   Downloading bcrypt-4.0.1-cp36-abi3-manylinux_2_28_x86_64.whl.metadata (9.0 kB)
2025-12-10T06:55:30.071780235Z Collecting blinker==1.9.0 (from -r backend/requirements.txt (line 5))
2025-12-10T06:55:30.075667529Z   Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
2025-12-10T06:55:30.194856994Z Collecting certifi==2025.11.12 (from -r backend/requirements.txt (line 6))
2025-12-10T06:55:30.2109625Z   Downloading certifi-2025.11.12-py3-none-any.whl.metadata (2.5 kB)
2025-12-10T06:55:30.432066285Z Collecting cffi==2.0.0 (from -r backend/requirements.txt (line 7))
2025-12-10T06:55:30.436234244Z   Downloading cffi-2.0.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.6 kB)
2025-12-10T06:55:30.821067913Z Collecting charset-normalizer==3.4.4 (from -r backend/requirements.txt (line 8))
2025-12-10T06:55:30.825100675Z   Downloading charset_normalizer-3.4.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (37 kB)
2025-12-10T06:55:31.048674804Z Collecting click==8.3.1 (from -r backend/requirements.txt (line 9))
2025-12-10T06:55:31.057544498Z   Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
2025-12-10T06:55:31.615609296Z Collecting cryptography==46.0.3 (from -r backend/requirements.txt (line 10))
2025-12-10T06:55:31.619318172Z   Downloading cryptography-46.0.3-cp311-abi3-manylinux_2_34_x86_64.whl.metadata (5.7 kB)
2025-12-10T06:55:31.778207203Z Collecting dnspython==2.8.0 (from -r backend/requirements.txt (line 11))
2025-12-10T06:55:31.781810214Z   Downloading dnspython-2.8.0-py3-none-any.whl.metadata (5.7 kB)
2025-12-10T06:55:31.915908725Z Collecting ecdsa==0.19.1 (from -r backend/requirements.txt (line 12))
2025-12-10T06:55:31.919675783Z   Downloading ecdsa-0.19.1-py2.py3-none-any.whl.metadata (29 kB)
2025-12-10T06:55:32.083047429Z Collecting email-validator==2.3.0 (from -r backend/requirements.txt (line 13))
2025-12-10T06:55:32.08726412Z   Downloading email_validator-2.3.0-py3-none-any.whl.metadata (26 kB)
2025-12-10T06:55:32.22335413Z Collecting et_xmlfile==2.0.0 (from -r backend/requirements.txt (line 14))
2025-12-10T06:55:32.227648475Z   Downloading et_xmlfile-2.0.0-py3-none-any.whl.metadata (2.7 kB)
2025-12-10T06:55:32.345140125Z Collecting fastapi==0.124.0 (from -r backend/requirements.txt (line 15))
2025-12-10T06:55:32.354711094Z   Downloading fastapi-0.124.0-py3-none-any.whl.metadata (30 kB)
2025-12-10T06:55:32.401724317Z Collecting Flask==3.0.0 (from -r backend/requirements.txt (line 16))
2025-12-10T06:55:32.406617642Z   Downloading flask-3.0.0-py3-none-any.whl.metadata (3.6 kB)
2025-12-10T06:55:32.440721038Z Collecting Flask-Cors==4.0.0 (from -r backend/requirements.txt (line 17))
2025-12-10T06:55:32.445379331Z   Downloading Flask_Cors-4.0.0-py2.py3-none-any.whl.metadata (5.4 kB)
2025-12-10T06:55:32.469600103Z Collecting h11==0.16.0 (from -r backend/requirements.txt (line 18))
2025-12-10T06:55:32.47453783Z   Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
2025-12-10T06:55:32.504426526Z Collecting idna==3.11 (from -r backend/requirements.txt (line 19))
2025-12-10T06:55:32.512783384Z   Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
2025-12-10T06:55:32.538597836Z Collecting itsdangerous==2.2.0 (from -r backend/requirements.txt (line 20))
2025-12-10T06:55:32.544216848Z   Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
2025-12-10T06:55:32.569896923Z Collecting Jinja2==3.1.6 (from -r backend/requirements.txt (line 21))
2025-12-10T06:55:32.573197848Z   Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
2025-12-10T06:55:32.596937976Z Collecting jose==1.0.0 (from -r backend/requirements.txt (line 22))
2025-12-10T06:55:32.602192279Z   Downloading jose-1.0.0.tar.gz (9.2 kB)
2025-12-10T06:55:32.617445012Z   Installing build dependencies: started
2025-12-10T06:55:33.66169658Z   Installing build dependencies: finished with status 'done'
2025-12-10T06:55:33.662751133Z   Getting requirements to build wheel: started
2025-12-10T06:55:34.136604956Z   Getting requirements to build wheel: finished with status 'done'
2025-12-10T06:55:34.137901051Z   Preparing metadata (pyproject.toml): started
2025-12-10T06:55:34.482154338Z   Preparing metadata (pyproject.toml): finished with status 'done'
2025-12-10T06:55:34.678900734Z Collecting jwt==1.4.0 (from -r backend/requirements.txt (line 23))
2025-12-10T06:55:34.722013171Z   Downloading jwt-1.4.0-py3-none-any.whl.metadata (3.9 kB)
2025-12-10T06:55:35.238475306Z Collecting MarkupSafe==3.0.3 (from -r backend/requirements.txt (line 24))
2025-12-10T06:55:35.243764581Z   Downloading markupsafe-3.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
2025-12-10T06:55:35.551512881Z Collecting motor==3.7.1 (from -r backend/requirements.txt (line 25))
2025-12-10T06:55:35.558438637Z   Downloading motor-3.7.1-py3-none-any.whl.metadata (21 kB)
2025-12-10T06:55:36.199077066Z Collecting numpy==2.3.5 (from -r backend/requirements.txt (line 26))
2025-12-10T06:55:36.204236374Z   Downloading numpy-2.3.5-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (62 kB)
2025-12-10T06:55:36.460803603Z Collecting openpyxl==3.1.5 (from -r backend/requirements.txt (line 27))
2025-12-10T06:55:36.465892757Z   Downloading openpyxl-3.1.5-py2.py3-none-any.whl.metadata (2.5 kB)
2025-12-10T06:55:36.69555179Z Collecting pandas==2.3.3 (from -r backend/requirements.txt (line 28))
2025-12-10T06:55:36.711135359Z   Downloading pandas-2.3.3-cp313-cp313-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (91 kB)
2025-12-10T06:55:36.955168891Z Collecting passlib==1.7.4 (from -r backend/requirements.txt (line 29))
2025-12-10T06:55:36.959632114Z   Downloading passlib-1.7.4-py2.py3-none-any.whl.metadata (1.7 kB)
2025-12-10T06:55:37.554498752Z Collecting pillow==12.0.0 (from -r backend/requirements.txt (line 30))
2025-12-10T06:55:37.562424868Z   Downloading pillow-12.0.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (8.8 kB)
2025-12-10T06:55:37.863605889Z Collecting pyasn1==0.6.1 (from -r backend/requirements.txt (line 31))
2025-12-10T06:55:37.868846191Z   Downloading pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
2025-12-10T06:55:38.113846491Z Collecting pycparser==2.23 (from -r backend/requirements.txt (line 32))
2025-12-10T06:55:38.117589048Z   Downloading pycparser-2.23-py3-none-any.whl.metadata (993 bytes)
2025-12-10T06:55:38.515299809Z Collecting pydantic==2.12.5 (from -r backend/requirements.txt (line 33))
2025-12-10T06:55:38.520335111Z   Downloading pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)
2025-12-10T06:55:38.780013915Z Collecting pydantic-settings==2.12.0 (from -r backend/requirements.txt (line 34))
2025-12-10T06:55:38.790005725Z   Downloading pydantic_settings-2.12.0-py3-none-any.whl.metadata (3.4 kB)
2025-12-10T06:55:39.762101607Z Collecting pydantic_core==2.41.5 (from -r backend/requirements.txt (line 35))
2025-12-10T06:55:39.7677446Z   Downloading pydantic_core-2.41.5-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
2025-12-10T06:55:40.016043164Z Collecting PyJWT==2.10.1 (from -r backend/requirements.txt (line 36))
2025-12-10T06:55:40.020424463Z   Downloading PyJWT-2.10.1-py3-none-any.whl.metadata (4.0 kB)
2025-12-10T06:55:40.539756649Z Collecting pymongo==4.15.5 (from -r backend/requirements.txt (line 37))
2025-12-10T06:55:40.545854054Z   Downloading pymongo-4.15.5-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (22 kB)
2025-12-10T06:55:40.718191477Z Collecting python-dateutil==2.9.0.post0 (from -r backend/requirements.txt (line 38))
2025-12-10T06:55:40.721914543Z   Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
2025-12-10T06:55:40.962094621Z Collecting python-dotenv==1.0.0 (from -r backend/requirements.txt (line 39))
2025-12-10T06:55:40.965955844Z   Downloading python_dotenv-1.0.0-py3-none-any.whl.metadata (21 kB)
2025-12-10T06:55:41.242117413Z Collecting python-jose==3.5.0 (from -r backend/requirements.txt (line 40))
2025-12-10T06:55:41.247747274Z   Downloading python_jose-3.5.0-py2.py3-none-any.whl.metadata (5.5 kB)
2025-12-10T06:55:41.500571315Z Collecting python-multipart==0.0.20 (from -r backend/requirements.txt (line 41))
2025-12-10T06:55:41.504712232Z   Downloading python_multipart-0.0.20-py3-none-any.whl.metadata (1.8 kB)
2025-12-10T06:55:41.891721026Z Collecting pytz==2025.2 (from -r backend/requirements.txt (line 42))
2025-12-10T06:55:41.895560129Z   Downloading pytz-2025.2-py2.py3-none-any.whl.metadata (22 kB)
2025-12-10T06:55:42.198257374Z Collecting requests==2.32.5 (from -r backend/requirements.txt (line 43))
2025-12-10T06:55:42.205185691Z   Downloading requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
2025-12-10T06:55:42.459520767Z Collecting rsa==4.9.1 (from -r backend/requirements.txt (line 44))
2025-12-10T06:55:42.464214202Z   Downloading rsa-4.9.1-py3-none-any.whl.metadata (5.6 kB)
2025-12-10T06:55:42.612665669Z Collecting six==1.17.0 (from -r backend/requirements.txt (line 45))
2025-12-10T06:55:42.617008617Z   Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
2025-12-10T06:55:42.756718767Z Collecting starlette==0.50.0 (from -r backend/requirements.txt (line 46))
2025-12-10T06:55:42.756740128Z   Downloading starlette-0.50.0-py3-none-any.whl.metadata (6.3 kB)
2025-12-10T06:55:42.945741665Z Collecting typing-inspection==0.4.2 (from -r backend/requirements.txt (line 47))
2025-12-10T06:55:42.950853581Z   Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
2025-12-10T06:55:43.325531098Z Collecting typing_extensions==4.15.0 (from -r backend/requirements.txt (line 48))
2025-12-10T06:55:43.329341469Z   Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
2025-12-10T06:55:43.778047789Z Collecting tzdata==2025.2 (from -r backend/requirements.txt (line 49))
2025-12-10T06:55:43.782104112Z   Downloading tzdata-2025.2-py2.py3-none-any.whl.metadata (1.4 kB)
2025-12-10T06:55:44.517018213Z Collecting urllib3==2.6.1 (from -r backend/requirements.txt (line 50))
2025-12-10T06:55:44.521251955Z   Downloading urllib3-2.6.1-py3-none-any.whl.metadata (6.6 kB)
2025-12-10T06:55:45.10055768Z Collecting uvicorn==0.38.0 (from -r backend/requirements.txt (line 51))
2025-12-10T06:55:45.104919638Z   Downloading uvicorn-0.38.0-py3-none-any.whl.metadata (6.8 kB)
2025-12-10T06:55:45.295537285Z Collecting Werkzeug==3.0.1 (from -r backend/requirements.txt (line 52))
2025-12-10T06:55:45.306162467Z   Downloading werkzeug-3.0.1-py3-none-any.whl.metadata (4.1 kB)
2025-12-10T06:55:45.607587398Z Downloading annotated_doc-0.0.4-py3-none-any.whl (5.3 kB)
2025-12-10T06:55:45.771373773Z Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
2025-12-10T06:55:45.908578578Z Downloading anyio-4.12.0-py3-none-any.whl (113 kB)
2025-12-10T06:55:45.92520926Z Downloading bcrypt-4.0.1-cp36-abi3-manylinux_2_28_x86_64.whl (593 kB)
2025-12-10T06:55:45.948223011Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 593.7/593.7 kB 17.8 MB/s eta 0:00:00
2025-12-10T06:55:45.953086334Z Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
2025-12-10T06:55:45.96759359Z Downloading certifi-2025.11.12-py3-none-any.whl (159 kB)
2025-12-10T06:55:45.980436643Z Downloading cffi-2.0.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (219 kB)
2025-12-10T06:55:46.001035634Z Downloading charset_normalizer-3.4.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (153 kB)
2025-12-10T06:55:46.016200152Z Downloading click-8.3.1-py3-none-any.whl (108 kB)
2025-12-10T06:55:46.031277087Z Downloading cryptography-46.0.3-cp311-abi3-manylinux_2_34_x86_64.whl (4.5 MB)
2025-12-10T06:55:46.115232327Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 53.0 MB/s eta 0:00:00
2025-12-10T06:55:46.119908131Z Downloading dnspython-2.8.0-py3-none-any.whl (331 kB)
2025-12-10T06:55:46.142701281Z Downloading ecdsa-0.19.1-py2.py3-none-any.whl (150 kB)
2025-12-10T06:55:46.161498162Z Downloading email_validator-2.3.0-py3-none-any.whl (35 kB)
2025-12-10T06:55:46.176782597Z Downloading et_xmlfile-2.0.0-py3-none-any.whl (18 kB)
2025-12-10T06:55:46.195207748Z Downloading fastapi-0.124.0-py3-none-any.whl (112 kB)
2025-12-10T06:55:46.214147836Z Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)
2025-12-10T06:55:46.241227481Z Downloading starlette-0.50.0-py3-none-any.whl (74 kB)
2025-12-10T06:55:46.256890765Z Downloading flask-3.0.0-py3-none-any.whl (99 kB)
2025-12-10T06:55:46.277308276Z Downloading Flask_Cors-4.0.0-py2.py3-none-any.whl (14 kB)
2025-12-10T06:55:46.318335429Z Downloading h11-0.16.0-py3-none-any.whl (37 kB)
2025-12-10T06:55:46.337597612Z Downloading idna-3.11-py3-none-any.whl (71 kB)
2025-12-10T06:55:46.354297438Z Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
2025-12-10T06:55:46.369341031Z Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
2025-12-10T06:55:46.390748282Z Downloading jwt-1.4.0-py3-none-any.whl (18 kB)
2025-12-10T06:55:46.403772503Z Downloading markupsafe-3.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
2025-12-10T06:55:46.418375944Z Downloading motor-3.7.1-py3-none-any.whl (74 kB)
2025-12-10T06:55:46.436708461Z Downloading pymongo-4.15.5-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (2.0 MB)
2025-12-10T06:55:46.461996147Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 77.9 MB/s eta 0:00:00
2025-12-10T06:55:46.468314403Z Downloading numpy-2.3.5-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.6 MB)
2025-12-10T06:55:46.613785411Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.6/16.6 MB 114.9 MB/s eta 0:00:00
2025-12-10T06:55:46.618299347Z Downloading openpyxl-3.1.5-py2.py3-none-any.whl (250 kB)
2025-12-10T06:55:46.629124798Z Downloading pandas-2.3.3-cp313-cp313-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.3 MB)
2025-12-10T06:55:46.755795736Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.3/12.3 MB 101.4 MB/s eta 0:00:00
2025-12-10T06:55:46.760344603Z Downloading passlib-1.7.4-py2.py3-none-any.whl (525 kB)
2025-12-10T06:55:46.771160805Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 525.6/525.6 kB 36.2 MB/s eta 0:00:00
2025-12-10T06:55:46.775558695Z Downloading pillow-12.0.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (7.0 MB)
2025-12-10T06:55:46.823734695Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.0/7.0 MB 152.3 MB/s eta 0:00:00
2025-12-10T06:55:46.827510554Z Downloading pyasn1-0.6.1-py3-none-any.whl (83 kB)
2025-12-10T06:55:46.836334645Z Downloading pycparser-2.23-py3-none-any.whl (118 kB)
2025-12-10T06:55:46.845191689Z Downloading pydantic_settings-2.12.0-py3-none-any.whl (51 kB)
2025-12-10T06:55:46.857936236Z Downloading pydantic_core-2.41.5-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
2025-12-10T06:55:46.878854413Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 102.5 MB/s eta 0:00:00
2025-12-10T06:55:46.883148048Z Downloading PyJWT-2.10.1-py3-none-any.whl (22 kB)
2025-12-10T06:55:46.891572299Z Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
2025-12-10T06:55:46.902294166Z Downloading python_dotenv-1.0.0-py3-none-any.whl (19 kB)
2025-12-10T06:55:46.910204801Z Downloading python_jose-3.5.0-py2.py3-none-any.whl (34 kB)
2025-12-10T06:55:46.918244834Z Downloading rsa-4.9.1-py3-none-any.whl (34 kB)
2025-12-10T06:55:46.92636107Z Downloading python_multipart-0.0.20-py3-none-any.whl (24 kB)
2025-12-10T06:55:46.93456396Z Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
2025-12-10T06:55:46.947036564Z Downloading requests-2.32.5-py3-none-any.whl (64 kB)
2025-12-10T06:55:46.956599753Z Downloading urllib3-2.6.1-py3-none-any.whl (131 kB)
2025-12-10T06:55:46.968413584Z Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
2025-12-10T06:55:46.977291038Z Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
2025-12-10T06:55:46.985712499Z Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
2025-12-10T06:55:46.994386503Z Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
2025-12-10T06:55:47.005174923Z Downloading uvicorn-0.38.0-py3-none-any.whl (68 kB)
2025-12-10T06:55:47.015004475Z Downloading werkzeug-3.0.1-py3-none-any.whl (226 kB)
2025-12-10T06:55:47.126617999Z Building wheels for collected packages: jose
2025-12-10T06:55:47.127616759Z   Building wheel for jose (pyproject.toml): started
2025-12-10T06:55:47.398040448Z   Building wheel for jose (pyproject.toml): finished with status 'done'
2025-12-10T06:55:47.399206167Z   Created wheel for jose: filename=jose-1.0.0-py3-none-any.whl size=8900 sha256=dce4a8880f64322a2ea7def7cd781a7afae5c46dcf12088fba4576f2b7759cd3
2025-12-10T06:55:47.399476251Z   Stored in directory: /opt/render/.cache/wheels/07/6e/e2/d6818308c2db8a78e5ee25938e141f615e6a4ce48de266b390
2025-12-10T06:55:47.402300442Z Successfully built jose
2025-12-10T06:55:47.53538542Z Installing collected packages: pytz, passlib, jose, urllib3, tzdata, typing_extensions, six, python-multipart, python-dotenv, PyJWT, pycparser, pyasn1, pillow, numpy, MarkupSafe, itsdangerous, idna, h11, et_xmlfile, dnspython, click, charset-normalizer, certifi, blinker, bcrypt, annotated-types, annotated-doc, Werkzeug, uvicorn, typing-inspection, rsa, requests, python-dateutil, pymongo, pydantic_core, openpyxl, Jinja2, email-validator, ecdsa, cffi, anyio, starlette, python-jose, pydantic, pandas, motor, Flask, cryptography, pydantic-settings, jwt, Flask-Cors, fastapi
2025-12-10T06:56:08.217431864Z 
2025-12-10T06:56:08.223602472Z Successfully installed Flask-3.0.0 Flask-Cors-4.0.0 Jinja2-3.1.6 MarkupSafe-3.0.3 PyJWT-2.10.1 Werkzeug-3.0.1 annotated-doc-0.0.4 annotated-types-0.7.0 anyio-4.12.0 bcrypt-4.0.1 blinker-1.9.0 certifi-2025.11.12 cffi-2.0.0 charset-normalizer-3.4.4 click-8.3.1 cryptography-46.0.3 dnspython-2.8.0 ecdsa-0.19.1 email-validator-2.3.0 et_xmlfile-2.0.0 fastapi-0.124.0 h11-0.16.0 idna-3.11 itsdangerous-2.2.0 jose-1.0.0 jwt-1.4.0 motor-3.7.1 numpy-2.3.5 openpyxl-3.1.5 pandas-2.3.3 passlib-1.7.4 pillow-12.0.0 pyasn1-0.6.1 pycparser-2.23 pydantic-2.12.5 pydantic-settings-2.12.0 pydantic_core-2.41.5 pymongo-4.15.5 python-dateutil-2.9.0.post0 python-dotenv-1.0.0 python-jose-3.5.0 python-multipart-0.0.20 pytz-2025.2 requests-2.32.5 rsa-4.9.1 six-1.17.0 starlette-0.50.0 typing-inspection-0.4.2 typing_extensions-4.15.0 tzdata-2025.2 urllib3-2.6.1 uvicorn-0.38.0
2025-12-10T06:56:08.317097278Z 
2025-12-10T06:56:08.317119699Z [notice] A new release of pip is available: 25.1.1 -> 25.3
2025-12-10T06:56:08.31712433Z [notice] To update, run: pip install --upgrade pip
2025-12-10T06:56:15.619266967Z ==> Uploading build...
2025-12-10T06:56:38.366311431Z ==> Setting WEB_CONCURRENCY=1 by default, based on available CPUs in the instance
2025-12-10T06:56:38.535734039Z ==> Deploying...
2025-12-10T06:56:34.648112063Z ==> Uploaded in 11.5s. Compression took 7.5s
2025-12-10T06:56:34.751702621Z ==> Build successful 🎉
2025-12-10T06:57:13.520383851Z ==> Running 'cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT'
2025-12-10T06:57:15.136632267Z ERROR:    Error loading ASGI app. Could not import module "main".
2025-12-10T06:57:16.745520459Z ==> Exited with status 1
2025-12-10T06:57:16.916371137Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
2025-12-10T06:57:21.669142468Z ==> Running 'cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT'
