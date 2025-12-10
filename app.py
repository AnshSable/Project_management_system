from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import pandas as pd
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
import jwt  # Changed from jose import
from PIL import Image
import io
import base64
import requests

app = FastAPI(title="Project Management System")

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Excel file paths
ADMIN_CREDS_FILE = 'data/admin_credentials.xlsx'
USER_CREDS_FILE = 'data/user_credentials.xlsx'
PROJECTS_FILE = 'data/projects.xlsx'
CLIENTS_FILE = 'data/clients.xlsx'
CONTACTS_FILE = 'data/contacts.xlsx'
SUBSCRIPTIONS_FILE = 'data/subscriptions.xlsx'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Helper functions
def read_excel(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return pd.DataFrame()

def write_excel(df, file_path):
    df.to_excel(file_path, index=False)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def crop_image_to_ratio(image_data: str, target_width: int = 450, target_height: int = 350) -> str:
    """
    Crop/resize image to specific dimensions (450x350).
    Accepts base64 encoded image or URL.
    Returns base64 encoded image string.
    """
    try:
        # If empty or None, return as is
        if not image_data or image_data.strip() == "":
            return image_data
        
        # Check if it's a URL
        if image_data.startswith(('http://', 'https://')):
            response = requests.get(image_data, timeout=10)
            image = Image.open(io.BytesIO(response.content))
        # Check if it's base64
        elif image_data.startswith('data:image'):
            # Extract base64 data
            base64_data = image_data.split(',')[1] if ',' in image_data else image_data
            image_bytes = base64.b64decode(base64_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            # Try to decode as base64 without data URI prefix
            try:
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            except:
                # If it's not a valid image format, return as is
                return image_data
        
        # Convert to RGB if necessary (handles PNG with transparency)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calculate aspect ratio
        original_width, original_height = image.size
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        
        # Crop to target ratio first (center crop)
        if original_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(original_height * target_ratio)
            left = (original_width - new_width) // 2
            image = image.crop((left, 0, left + new_width, original_height))
        elif original_ratio < target_ratio:
            # Image is taller, crop height
            new_height = int(original_width / target_ratio)
            top = (original_height - new_height) // 2
            image = image.crop((0, top, original_width, top + new_height))
        
        # Resize to target dimensions
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{img_str}"
    
    except Exception as e:
        # If processing fails, return original data
        print(f"Image processing error: {str(e)}")
        return image_data

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency to verify admin role
async def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_data = verify_token(token)
    if user_data["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_data

# Dependency to verify any authenticated user
async def verify_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_data = verify_token(token)
    return user_data

# Pydantic models
class UserSignup(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class ProjectCreate(BaseModel):
    project_name: str
    project_image: Optional[str] = ""
    description: Optional[str] = ""

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    project_image: Optional[str] = None
    description: Optional[str] = None

class ClientCreate(BaseModel):
    client_name: str
    client_image: Optional[str] = ""
    description: Optional[str] = ""
    designation: Optional[str] = ""

class ClientUpdate(BaseModel):
    client_name: Optional[str] = None
    client_image: Optional[str] = None
    description: Optional[str] = None
    designation: Optional[str] = None

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = ""
    subject: str
    message: str

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None  # pending, read, responded

class SubscriptionCreate(BaseModel):
    email: EmailStr

class SubscriptionUpdate(BaseModel):
    email: Optional[EmailStr] = None
    status: Optional[str] = None  # active, unsubscribed

# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main frontend page"""
    try:
        with open("frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend not found")

@app.get("/admin", response_class=HTMLResponse)
async def serve_admin():
    """Serve the admin panel page"""
    try:
        with open("frontend/admin.html", "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Admin page not found")

@app.get("/css/{file_path:path}")
async def serve_css(file_path: str):
    """Serve CSS files"""
    file_location = f"frontend/css/{file_path}"
    if os.path.exists(file_location):
        return FileResponse(file_location, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/js/{file_path:path}")
async def serve_js(file_path: str):
    """Serve JavaScript files"""
    file_location = f"frontend/js/{file_path}"
    if os.path.exists(file_location):
        return FileResponse(file_location, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")

# ==================== AUTH ROUTES ====================

# Note: Admin signup is disabled. Admins must be added manually to the admin_credentials.xlsx file

@app.post("/api/admin/login")
async def admin_login(user: UserLogin):
    try:
        df = read_excel(ADMIN_CREDS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user_row = df[df['username'] == user.username]
        
        if user_row.empty:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        stored_password = user_row.iloc[0]['password']
        if verify_password(user.password, stored_password):
            # Create JWT token
            access_token = create_access_token(
                data={"sub": user.username, "role": "admin"}
            )
            return {
                "message": "Login successful",
                "username": user.username,
                "role": "admin",
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserSignup):
    try:
        df = read_excel(USER_CREDS_FILE)
        
        if not df.empty and user.username in df['username'].values:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = hash_password(user.password)
        
        new_user = pd.DataFrame({
            'username': [user.username],
            'password': [hashed_password],
            'email': [user.email],
            'created_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        df = pd.concat([df, new_user], ignore_index=True)
        write_excel(df, USER_CREDS_FILE)
        
        return {"message": "User registered successfully", "username": user.username}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/login")
async def user_login(user: UserLogin):
    try:
        df = read_excel(USER_CREDS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user_row = df[df['username'] == user.username]
        
        if user_row.empty:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        stored_password = user_row.iloc[0]['password']
        if verify_password(user.password, stored_password):
            # Create JWT token
            access_token = create_access_token(
                data={"sub": user.username, "role": "user"}
            )
            return {
                "message": "Login successful",
                "username": user.username,
                "role": "user",
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== PROJECT ROUTES (ADMIN) ====================

@app.get("/api/admin/projects")
async def get_all_projects_admin(current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(PROJECTS_FILE)
        if df.empty:
            return {"projects": []}
        
        # Replace NaN with None for JSON serialization
        df = df.fillna("")
        projects = df.to_dict('records')
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/projects/{project_id}")
async def get_project_admin(project_id: int, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(PROJECTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_row = df[df['project_id'] == project_id]
        
        if project_row.empty:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Replace NaN with empty string for JSON serialization
        project_row = project_row.fillna("")
        project = project_row.to_dict('records')[0]
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/add_project", status_code=status.HTTP_201_CREATED)
async def add_project(project: ProjectCreate, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(PROJECTS_FILE)
        
        if df.empty:
            project_id = 1
        else:
            project_id = int(df['project_id'].max() + 1)
        
        # Crop image to 450x350 if provided
        cropped_image = crop_image_to_ratio(project.project_image) if project.project_image else ""
        
        new_project = pd.DataFrame({
            'project_id': [project_id],
            'project_name': [project.project_name],
            'project_image': [cropped_image],
            'description': [project.description],
            'created_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        df = pd.concat([df, new_project], ignore_index=True)
        write_excel(df, PROJECTS_FILE)
        
        return {"message": "Project added successfully", "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/projects/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(PROJECTS_FILE)
        if df.empty:
            raise HTTPException(status_code=404, detail="Project not found")
        project_index = df[df['project_id'] == project_id].index
        if project_index.empty:
            raise HTTPException(status_code=404, detail="Project not found")
        # Dynamically update only provided fields
        update_data = project.dict(exclude_unset=True)
        # Crop image if being updated
        if 'project_image' in update_data and update_data['project_image']:
            update_data['project_image'] = crop_image_to_ratio(update_data['project_image'])
        for field, value in update_data.items():
            df.at[project_index[0], field] = value
        write_excel(df, PROJECTS_FILE)
        return {"message": "Project updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/projects/{project_id}")
async def delete_project(project_id: int, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(PROJECTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Project not found")
        
        original_len = len(df)
        df = df[df['project_id'] != project_id]
        
        if len(df) == original_len:
            raise HTTPException(status_code=404, detail="Project not found")
        
        write_excel(df, PROJECTS_FILE)
        
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CLIENT ROUTES (ADMIN) ====================

@app.get("/api/admin/clients")
async def get_all_clients_admin(current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(CLIENTS_FILE)
        if df.empty:
            return {"clients": []}
        
        # Replace NaN with empty string for JSON serialization
        df = df.fillna("")
        clients = df.to_dict('records')
        return {"clients": clients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/clients/{client_id}")
async def get_client_admin(client_id: int, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(CLIENTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Client not found")
        
        client_row = df[df['client_id'] == client_id]
        
        if client_row.empty:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Replace NaN with empty string for JSON serialization
        client_row = client_row.fillna("")
        client = client_row.to_dict('records')[0]
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/add_client", status_code=status.HTTP_201_CREATED)
async def add_client(client: ClientCreate, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(CLIENTS_FILE)
        
        if df.empty:
            client_id = 1
        else:
            client_id = int(df['client_id'].max() + 1)
        
        # Crop image to 450x350 if provided
        cropped_image = crop_image_to_ratio(client.client_image) if client.client_image else ""
        
        new_client = pd.DataFrame({
            'client_id': [client_id],
            'client_name': [client.client_name],
            'client_image': [cropped_image],
            'description': [client.description],
            'designation': [client.designation],
            'created_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        df = pd.concat([df, new_client], ignore_index=True)
        write_excel(df, CLIENTS_FILE)
        
        return {"message": "Client added successfully", "client_id": client_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/clients/{client_id}")
async def update_client(client_id: int, client: ClientUpdate, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(CLIENTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Client not found")
        
        client_index = df[df['client_id'] == client_id].index
        
        if client_index.empty:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Dynamically update only provided fields
        update_data = client.dict(exclude_unset=True)
        # Crop image if being updated
        if 'client_image' in update_data and update_data['client_image']:
            update_data['client_image'] = crop_image_to_ratio(update_data['client_image'])
        for field, value in update_data.items():
            df.at[client_index[0], field] = value
        
        write_excel(df, CLIENTS_FILE)
        
        return {"message": "Client updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/clients/{client_id}")
async def delete_client(client_id: int, current_user: dict = Depends(verify_admin)):
    try:
        df = read_excel(CLIENTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Client not found")
        
        original_len = len(df)
        df = df[df['client_id'] != client_id]
        
        if len(df) == original_len:
            raise HTTPException(status_code=404, detail="Client not found")
        
        write_excel(df, CLIENTS_FILE)
        
        return {"message": "Client deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== USER ROUTES (READ-ONLY) ====================

@app.get("/api/user/projects")
async def get_all_projects_user(current_user: dict = Depends(verify_user)):
    try:
        df = read_excel(PROJECTS_FILE)
        if df.empty:
            return {"projects": []}
        
        # Replace NaN with empty string for JSON serialization
        df = df.fillna("")
        projects = df.to_dict('records')
        return {"projects": projects, "user": current_user["username"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/clients")
async def get_all_clients_user(current_user: dict = Depends(verify_user)):
    try:
        df = read_excel(CLIENTS_FILE)
        if df.empty:
            return {"clients": []}
        
        # Replace NaN with empty string for JSON serialization
        df = df.fillna("")
        clients = df.to_dict('records')
        return {"clients": clients, "user": current_user["username"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CONTACT FORM ROUTES ====================

@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
async def submit_contact_form(contact: ContactForm):
    """Public endpoint - Anyone can submit contact form (no auth required)"""
    try:
        df = read_excel(CONTACTS_FILE)
        
        if df.empty:
            contact_id = 1
        else:
            contact_id = int(df['contact_id'].max() + 1)
        
        new_contact = pd.DataFrame({
            'contact_id': [contact_id],
            'name': [contact.name],
            'email': [contact.email],
            'phone': [contact.phone],
            'subject': [contact.subject],
            'message': [contact.message],
            'status': ['pending'],
            'submitted_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        df = pd.concat([df, new_contact], ignore_index=True)
        write_excel(df, CONTACTS_FILE)
        
        return {"message": "Contact form submitted successfully", "contact_id": contact_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/contacts")
async def get_all_contacts(current_user: dict = Depends(verify_admin)):
    """Admin only - View all contact form submissions"""
    try:
        df = read_excel(CONTACTS_FILE)
        if df.empty:
            return {"contacts": []}
        
        # Replace NaN with empty string for JSON serialization
        df = df.fillna("")
        contacts = df.to_dict('records')
        return {"contacts": contacts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/contacts/{contact_id}")
async def get_contact(contact_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - View specific contact"""
    try:
        df = read_excel(CONTACTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        contact_row = df[df['contact_id'] == contact_id]
        
        if contact_row.empty:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Replace NaN with empty string for JSON serialization
        contact_row = contact_row.fillna("")
        contact = contact_row.to_dict('records')[0]
        return {"contact": contact}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactUpdate, current_user: dict = Depends(verify_admin)):
    """Admin only - Update contact (mainly for status updates)"""
    try:
        df = read_excel(CONTACTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        contact_index = df[df['contact_id'] == contact_id].index
        
        if contact_index.empty:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Update only the fields that are provided (not None)
        update_data = contact.dict(exclude_unset=True)
        for field, value in update_data.items():
            df.at[contact_index[0], field] = value
        
        write_excel(df, CONTACTS_FILE)
        
        return {"message": "Contact updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/contacts/{contact_id}")
async def delete_contact(contact_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - Delete contact"""
    try:
        df = read_excel(CONTACTS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        original_len = len(df)
        df = df[df['contact_id'] != contact_id]
        
        if len(df) == original_len:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        write_excel(df, CONTACTS_FILE)
        
        return {"message": "Contact deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== SUBSCRIPTION ROUTES ====================

@app.post("/api/subscribe", status_code=status.HTTP_201_CREATED)
async def subscribe_newsletter(subscription: SubscriptionCreate):
    """Public endpoint - Anyone can subscribe (no auth required)"""
    try:
        df = read_excel(SUBSCRIPTIONS_FILE)
        
        # Check if email already exists
        if not df.empty and subscription.email in df['email'].values:
            # Check if already active
            existing = df[df['email'] == subscription.email].iloc[0]
            if existing['status'] == 'active':
                raise HTTPException(status_code=400, detail="Email already subscribed")
            else:
                # Reactivate subscription
                df.loc[df['email'] == subscription.email, 'status'] = 'active'
                df.loc[df['email'] == subscription.email, 'subscribed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                write_excel(df, SUBSCRIPTIONS_FILE)
                return {"message": "Subscription reactivated successfully"}
        
        if df.empty:
            subscription_id = 1
        else:
            subscription_id = int(df['subscription_id'].max() + 1)
        
        new_subscription = pd.DataFrame({
            'subscription_id': [subscription_id],
            'email': [subscription.email],
            'status': ['active'],
            'subscribed_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        df = pd.concat([df, new_subscription], ignore_index=True)
        write_excel(df, SUBSCRIPTIONS_FILE)
        
        return {"message": "Subscribed successfully", "subscription_id": subscription_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/unsubscribe", status_code=status.HTTP_200_OK)
async def unsubscribe_newsletter(subscription: SubscriptionCreate):
    """Public endpoint - Anyone can unsubscribe (no auth required)"""
    try:
        df = read_excel(SUBSCRIPTIONS_FILE)
        
        if df.empty or subscription.email not in df['email'].values:
            raise HTTPException(status_code=404, detail="Email not found in subscriptions")
        
        # Update status to unsubscribed
        df.loc[df['email'] == subscription.email, 'status'] = 'unsubscribed'
        write_excel(df, SUBSCRIPTIONS_FILE)
        
        return {"message": "Unsubscribed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/subscriptions")
async def get_all_subscriptions(current_user: dict = Depends(verify_admin)):
    """Admin only - View all subscriptions"""
    try:
        df = read_excel(SUBSCRIPTIONS_FILE)
        if df.empty:
            return {"subscriptions": []}
        
        # Replace NaN with empty string for JSON serialization
        df = df.fillna("")
        subscriptions = df.to_dict('records')
        return {"subscriptions": subscriptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/subscriptions/{subscription_id}")
async def get_subscription(subscription_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - View specific subscription"""
    try:
        df = read_excel(SUBSCRIPTIONS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        subscription_row = df[df['subscription_id'] == subscription_id]
        
        if subscription_row.empty:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        # Replace NaN with empty string for JSON serialization
        subscription_row = subscription_row.fillna("")
        subscription = subscription_row.to_dict('records')[0]
        return {"subscription": subscription}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/subscriptions/{subscription_id}")
async def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, current_user: dict = Depends(verify_admin)):
    """Admin only - Update subscription"""
    try:
        df = read_excel(SUBSCRIPTIONS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        subscription_index = df[df['subscription_id'] == subscription_id].index
        
        if subscription_index.empty:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        # Update only the fields that are provided (not None)
        update_data = subscription.dict(exclude_unset=True)
        for field, value in update_data.items():
            df.at[subscription_index[0], field] = value
        
        write_excel(df, SUBSCRIPTIONS_FILE)
        
        return {"message": "Subscription updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/subscriptions/{subscription_id}")
async def delete_subscription(subscription_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - Delete subscription"""
    try:
        df = read_excel(SUBSCRIPTIONS_FILE)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        original_len = len(df)
        df = df[df['subscription_id'] != subscription_id]
        
        if len(df) == original_len:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        write_excel(df, SUBSCRIPTIONS_FILE)
        
        return {"message": "Subscription deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MAIN ====================

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

