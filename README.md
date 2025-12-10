A modern, responsive full-stack web application built for the Flipr Placement Drive. This application features a landing page for showcasing projects and client testimonials, along with a comprehensive admin panel for content management.

MONGO_URL=mongodb+srv://anshsable03_db_user:eSdogWFZz7rmmFUE@cluster0.ztejiue.mongodb.net/sample_db?appName=Cluster0

📋 Table of Contents
Features

Tech Stack

Project Structure

Installation

Environment Variables

API Documentation

Deployment

Screenshots

Contributing

License

✨ Features
🏠 Landing Page
Projects Showcase: Dynamic display of projects with images, descriptions, and names

Client Testimonials: Showcase happy clients with images, designations, and feedback

Contact Form: Fully functional contact form with validation

Newsletter Subscription: Email subscription system for updates

Responsive Design: Mobile-friendly interface with modern UI/UX

👨‍💼 Admin Panel
Project Management: CRUD operations for projects with image upload

Client Management: Add and manage client testimonials

Contact Management: View all contact form submissions

Newsletter Management: Monitor newsletter subscriptions

Image Processing: Automatic image cropping and optimization

🔧 Backend Features
RESTful API: Complete API with proper HTTP methods

Database Integration: MongoDB Atlas with efficient data modeling

Image Processing: Automatic image resizing and cropping (450x350 ratio)

CORS Enabled: Secure cross-origin resource sharing

Input Validation: Comprehensive data validation using Pydantic

Error Handling: Graceful error handling and meaningful responses

🛠 Tech Stack
Backend
Python 3.10+: Core programming language

FastAPI: Modern, fast web framework for building APIs

MongoDB Atlas: Cloud database service for data persistence

Pydantic: Data validation and settings management

Pillow (PIL): Image processing and manipulation

Uvicorn: ASGI server for running FastAPI applications

Frontend
HTML5: Semantic markup structure

CSS3: Modern styling with Flexbox and Grid

JavaScript (ES6+): Dynamic functionality and API integration

Font Awesome: Icon library for enhanced UI

Development & Deployment
Git: Version control

MongoDB Atlas: Cloud database hosting

Render/Vercel/Heroku: Deployment platforms (compatible)

📁 Project Structure
text
flipr-assignment/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # MongoDB connection and configuration
│   ├── models.py            # Pydantic data models
│   ├── requirements.txt     # Python dependencies
│   ├── .env                # Environment variables
│   ├── uploads/            # Image upload directory
│   ├── routers/            # API route modules
│   │   ├── projects.py
│   │   ├── clients.py
│   │   ├── contacts.py
│   │   └── newsletter.py
│   └── utils/
│       └── image_processor.py
├── frontend/
│   ├── index.html          # Landing page
│   ├── admin.html          # Admin panel
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       ├── main.js         # Landing page JavaScript
│       └── admin.js        # Admin panel JavaScript
└── README.md              # This file
🚀 Installation
Prerequisites
Python 3.10 or higher

MongoDB Atlas account (free tier)

Git

Step 1: Clone the Repository
bash
git clone <repository-url>
cd flipr-assignment
Step 2: Backend Setup
bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment variables file
cp .env.example .env
# Edit .env with your MongoDB Atlas credentials
Step 3: Frontend Setup
bash
# Navigate to frontend directory
cd ../frontend

# No build process required - static files are ready to use
# Update API_BASE_URL in js/main.js and js/admin.js if needed
Step 4: Run the Application
Backend Server:

bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Frontend:

Open frontend/index.html in your browser

Or use a local server:

bash
cd frontend
python -m http.server 3000
The application will be available at:

Frontend: http://localhost:3000 or http://localhost:8000

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs

🔐 Environment Variables
Create a .env file in the backend directory:

env
# MongoDB Atlas Connection
MONGO_URL=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/<database_name>?retryWrites=true&w=majority

# Optional: Local MongoDB
# MONGO_URL=mongodb://localhost:27017/flipr_db
📚 API Documentation
FastAPI automatically generates interactive API documentation:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Available Endpoints
Method	Endpoint	Description	Access
GET	/api/projects	Get all projects	Public
POST	/api/projects	Create new project	Admin
DELETE	/api/projects/{id}	Delete project	Admin
GET	/api/clients	Get all clients	Public
POST	/api/clients	Create new client	Admin
GET	/api/contacts	Get contact submissions	Admin
POST	/api/contacts	Submit contact form	Public
GET	/api/newsletter	Get newsletter subscriptions	Admin
POST	/api/newsletter	Subscribe to newsletter	Public
🚢 Deployment
Backend Deployment (Render)
Push code to GitHub repository

Create a new Web Service on Render

Connect your GitHub repository

Set build command: pip install -r requirements.txt

Set start command: uvicorn main:app --host 0.0.0.0 --port 10000

Add environment variables (MONGO_URL)

Frontend Deployment (Vercel/Netlify)
Push frontend code to GitHub

Import project on Vercel/Netlify

Configure build settings (none required for static files)

Update API_BASE_URL in JavaScript files to point to deployed backend

Database (MongoDB Atlas)
Create free cluster on MongoDB Atlas

Create database user with read/write permissions

Add IP whitelist (0.0.0.0/0 for development)

Get connection string and update environment variables

📸 Screenshots
Landing Page
https://via.placeholder.com/800x450/4a6cf7/ffffff?text=Flipr+Landing+Page

Projects Section
https://via.placeholder.com/800x450/6a11cb/ffffff?text=Projects+Showcase

Admin Panel
https://via.placeholder.com/800x450/2d8cff/ffffff?text=Admin+Dashboard

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is created for the Flipr Placement Drive. All rights reserved.

✍️ Author
Your Name

GitHub: @yourusername

LinkedIn: Your Name

🙏 Acknowledgments
Flipr for the opportunity and challenging assignment

FastAPI and MongoDB teams for excellent documentation

All open-source libraries used in this project

