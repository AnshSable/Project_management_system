from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os
import base64
import io
from PIL import Image
import requests
import ssl
import certifi

# ==================== CONFIGURATION ====================

# MongoDB Configuration
MONGO_URL = "mongodb+srv://anshsable03_db_user:eSdogWFZz7rmmFUE@cluster0.ztejiue.mongodb.net/project_management_db?retryWrites=true&w=majority&appName=Cluster0"

# Initialize MongoDB client with SSL configuration
client = MongoClient(
    MONGO_URL,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000,
    connectTimeoutMS=30000,
    socketTimeoutMS=30000
)
db = client['project_management_db']

# Collections
admin_collection = db['admin_credentials']
users_collection = db['user_credentials']
projects_collection = db['projects']
clients_collection = db['clients']
contacts_collection = db['contacts']
subscriptions_collection = db['subscriptions']
counters_collection = db['counters']

# Repository root (parent of backend/) so static files can be served
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))

# Helper function for auto-increment IDs
def get_next_sequence_value(sequence_name: str) -> int:
    """Get next ID value for auto-increment"""
    sequence_doc = counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True,
        upsert=True
    )
    return sequence_doc.get("sequence_value", 1)

# Initialize counters if they don't exist
def init_counters():
    """Initialize counter values if not present"""
    for counter_name in ["project_id", "client_id", "contact_id", "subscription_id"]:
        if counters_collection.find_one({"_id": counter_name}) is None:
            counters_collection.insert_one({"_id": counter_name, "sequence_value": 0})

# Call init_counters on startup
init_counters()

# JWT Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# FastAPI app
app = FastAPI(title="Project Management System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== HELPER FUNCTIONS ====================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def crop_image_to_ratio(image_data: str, target_width: int = 450, target_height: int = 350) -> str:
    """
    Crop and resize image to target dimensions (450x350).
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
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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

# ==================== PYDANTIC MODELS ====================

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
    status: Optional[str] = None

class SubscriptionCreate(BaseModel):
    email: EmailStr

class SubscriptionUpdate(BaseModel):
    email: Optional[EmailStr] = None
    status: Optional[str] = None

# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main frontend page"""
    try:
        index_path = os.path.join(REPO_ROOT, "frontend", "index.html")
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend not found")

@app.get("/admin", response_class=HTMLResponse)
async def serve_admin():
    """Serve the admin panel page"""
    try:
        admin_path = os.path.join(REPO_ROOT, "frontend", "admin.html")
        with open(admin_path, "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Admin page not found")

@app.get("/css/{file_path:path}")
async def serve_css(file_path: str):
    """Serve CSS files"""
    file_location = os.path.join(REPO_ROOT, "frontend", "css", file_path)
    if os.path.exists(file_location):
        return FileResponse(file_location, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/js/{file_path:path}")
async def serve_js(file_path: str):
    """Serve JavaScript files"""
    file_location = os.path.join(REPO_ROOT, "frontend", "js", file_path)
    if os.path.exists(file_location):
        return FileResponse(file_location, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript file not found")

# ==================== AUTH ROUTES ====================

@app.post("/api/admin/login")
async def admin_login(user: UserLogin):
    try:
        admin_user = admin_collection.find_one({"username": user.username})
        
        if not admin_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if verify_password(user.password, admin_user['password']):
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
        # Check if username already exists
        if users_collection.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = hash_password(user.password)
        
        new_user = {
            'username': user.username,
            'password': hashed_password,
            'email': user.email,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        users_collection.insert_one(new_user)
        
        return {"message": "User registered successfully", "username": user.username}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/login")
async def user_login(user: UserLogin):
    try:
        user_doc = users_collection.find_one({"username": user.username})
        
        if not user_doc:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if verify_password(user.password, user_doc['password']):
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
        projects = list(projects_collection.find({}, {"_id": 0}))
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/projects/{project_id}")
async def get_project_admin(project_id: int, current_user: dict = Depends(verify_admin)):
    try:
        project = projects_collection.find_one({"project_id": project_id}, {"_id": 0})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/projects", status_code=status.HTTP_201_CREATED)
async def add_project(project: ProjectCreate, current_user: dict = Depends(verify_admin)):
    try:
        project_id = get_next_sequence_value("project_id")
        
        # Crop image to 450x350 if provided
        cropped_image = crop_image_to_ratio(project.project_image) if project.project_image else ""
        
        new_project = {
            'project_id': project_id,
            'project_name': project.project_name,
            'project_image': cropped_image,
            'description': project.description,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        projects_collection.insert_one(new_project)
        
        return {"message": "Project added successfully", "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/projects/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate, current_user: dict = Depends(verify_admin)):
    try:
        # Check if project exists
        if not projects_collection.find_one({"project_id": project_id}):
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Build update data
        update_data = project.dict(exclude_unset=True)
        
        # Crop image if being updated
        if 'project_image' in update_data and update_data['project_image']:
            update_data['project_image'] = crop_image_to_ratio(update_data['project_image'])
        
        if update_data:
            projects_collection.update_one(
                {"project_id": project_id},
                {"$set": update_data}
            )
        
        return {"message": "Project updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/projects/{project_id}")
async def delete_project(project_id: int, current_user: dict = Depends(verify_admin)):
    try:
        result = projects_collection.delete_one({"project_id": project_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CLIENT ROUTES (ADMIN) ====================

@app.get("/api/admin/clients")
async def get_all_clients_admin(current_user: dict = Depends(verify_admin)):
    try:
        clients = list(clients_collection.find({}, {"_id": 0}))
        return {"clients": clients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/clients/{client_id}")
async def get_client_admin(client_id: int, current_user: dict = Depends(verify_admin)):
    try:
        client = clients_collection.find_one({"client_id": client_id}, {"_id": 0})
        
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return client
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/clients", status_code=status.HTTP_201_CREATED)
async def add_client(client: ClientCreate, current_user: dict = Depends(verify_admin)):
    try:
        client_id = get_next_sequence_value("client_id")
        
        # Crop image to 450x350 if provided
        cropped_image = crop_image_to_ratio(client.client_image) if client.client_image else ""
        
        new_client = {
            'client_id': client_id,
            'client_name': client.client_name,
            'client_image': cropped_image,
            'description': client.description,
            'designation': client.designation,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        clients_collection.insert_one(new_client)
        
        return {"message": "Client added successfully", "client_id": client_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/clients/{client_id}")
async def update_client(client_id: int, client: ClientUpdate, current_user: dict = Depends(verify_admin)):
    try:
        # Check if client exists
        if not clients_collection.find_one({"client_id": client_id}):
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Build update data
        update_data = client.dict(exclude_unset=True)
        
        # Crop image if being updated
        if 'client_image' in update_data and update_data['client_image']:
            update_data['client_image'] = crop_image_to_ratio(update_data['client_image'])
        
        if update_data:
            clients_collection.update_one(
                {"client_id": client_id},
                {"$set": update_data}
            )
        
        return {"message": "Client updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/clients/{client_id}")
async def delete_client(client_id: int, current_user: dict = Depends(verify_admin)):
    try:
        result = clients_collection.delete_one({"client_id": client_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return {"message": "Client deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== USER ROUTES (READ-ONLY) ====================

@app.get("/api/user/projects")
async def get_all_projects_user(current_user: dict = Depends(verify_user)):
    try:
        projects = list(projects_collection.find({}, {"_id": 0}))
        return {"projects": projects, "user": current_user["username"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/clients")
async def get_all_clients_user(current_user: dict = Depends(verify_user)):
    try:
        clients = list(clients_collection.find({}, {"_id": 0}))
        return {"clients": clients, "user": current_user["username"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CONTACT FORM ROUTES ====================

@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
async def submit_contact_form(contact: ContactForm):
    """Public endpoint - Anyone can submit contact form (no auth required)"""
    try:
        contact_id = get_next_sequence_value("contact_id")
        
        new_contact = {
            'contact_id': contact_id,
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'subject': contact.subject,
            'message': contact.message,
            'status': 'pending',
            'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        contacts_collection.insert_one(new_contact)
        
        return {"message": "Contact form submitted successfully", "contact_id": contact_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/contacts")
async def get_all_contacts(current_user: dict = Depends(verify_admin)):
    """Admin only - View all contact form submissions"""
    try:
        contacts = list(contacts_collection.find({}, {"_id": 0}))
        return {"contacts": contacts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/contacts/{contact_id}")
async def get_contact(contact_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - View specific contact"""
    try:
        contact = contacts_collection.find_one({"contact_id": contact_id}, {"_id": 0})
        
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return {"contact": contact}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactUpdate, current_user: dict = Depends(verify_admin)):
    """Admin only - Update contact (mainly for status updates)"""
    try:
        # Check if contact exists
        if not contacts_collection.find_one({"contact_id": contact_id}):
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Build update data
        update_data = contact.dict(exclude_unset=True)
        
        if update_data:
            contacts_collection.update_one(
                {"contact_id": contact_id},
                {"$set": update_data}
            )
        
        return {"message": "Contact updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/contacts/{contact_id}")
async def delete_contact(contact_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - Delete contact"""
    try:
        result = contacts_collection.delete_one({"contact_id": contact_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found")
        
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
        # Check if email already exists
        existing = subscriptions_collection.find_one({"email": subscription.email})
        
        if existing:
            if existing['status'] == 'active':
                raise HTTPException(status_code=400, detail="Email already subscribed")
            else:
                # Reactivate subscription
                subscriptions_collection.update_one(
                    {"email": subscription.email},
                    {"$set": {
                        "status": "active",
                        "subscribed_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }}
                )
                return {"message": "Subscription reactivated successfully"}
        
        subscription_id = get_next_sequence_value("subscription_id")
        
        new_subscription = {
            'subscription_id': subscription_id,
            'email': subscription.email,
            'status': 'active',
            'subscribed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        subscriptions_collection.insert_one(new_subscription)
        
        return {"message": "Subscribed successfully", "subscription_id": subscription_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/unsubscribe", status_code=status.HTTP_200_OK)
async def unsubscribe_newsletter(subscription: SubscriptionCreate):
    """Public endpoint - Anyone can unsubscribe (no auth required)"""
    try:
        existing = subscriptions_collection.find_one({"email": subscription.email})
        
        if not existing:
            raise HTTPException(status_code=404, detail="Email not found in subscriptions")
        
        # Update status to unsubscribed
        subscriptions_collection.update_one(
            {"email": subscription.email},
            {"$set": {"status": "unsubscribed"}}
        )
        
        return {"message": "Unsubscribed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/subscriptions")
async def get_all_subscriptions(current_user: dict = Depends(verify_admin)):
    """Admin only - View all subscriptions"""
    try:
        subscriptions = list(subscriptions_collection.find({}, {"_id": 0}))
        return {"subscriptions": subscriptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/subscriptions/{subscription_id}")
async def get_subscription(subscription_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - View specific subscription"""
    try:
        subscription = subscriptions_collection.find_one({"subscription_id": subscription_id}, {"_id": 0})
        
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        return {"subscription": subscription}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/subscriptions/{subscription_id}")
async def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, current_user: dict = Depends(verify_admin)):
    """Admin only - Update subscription"""
    try:
        # Check if subscription exists
        if not subscriptions_collection.find_one({"subscription_id": subscription_id}):
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        # Build update data
        update_data = subscription.dict(exclude_unset=True)
        
        if update_data:
            subscriptions_collection.update_one(
                {"subscription_id": subscription_id},
                {"$set": update_data}
            )
        
        return {"message": "Subscription updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/subscriptions/{subscription_id}")
async def delete_subscription(subscription_id: int, current_user: dict = Depends(verify_admin)):
    """Admin only - Delete subscription"""
    try:
        result = subscriptions_collection.delete_one({"subscription_id": subscription_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        return {"message": "Subscription deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MAIN ====================

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)