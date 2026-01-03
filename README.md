#  Videoflix – Backend Description


## ![Features Icon](assets/icons/logoheader.png) Description
Videoflix is a video streaming platform inspired by Netflix. We use djangorestframework_simplejwt for authentication with JWTs. User registration is handled via a RegisterView that requires an email address, password, and password confirmation; the account is only activated after successful email verification.

After logging in, the user receives an access token and a refresh token to securely renew the session. In addition, there is a password reset feature that allows users to reset their password via a link sent by email.

Videos are uploaded through the admin panel and are automatically converted into three different resolutions. Depending on the screen resolution, the optimal video size is delivered to avoid unnecessary bandwidth usage and to ensure efficient playback.

The backend runs in Docker containers and uses PostgreSQL as the database. FFMPEG is used for video transcoding and thumbnail generation, while time-consuming tasks are processed asynchronously using Django RQ with Redis.

A caching layer based on django-redis improves performance, configuration is managed securely via dotenv, static files are served using WhiteNoise, and in production the application runs efficiently with Gunicorn.

Frontend repository: [Videoflix Frontend](https://github.com/Pinguinrakete/videoflix_fontend)


## ![Features Icon](assets/icons/gear.png) Features

### **User Authentication**: <br>
**JWT-Based Authentication**<br>
**User Registration with Email Verification**<br>
**Login & Token Management**<br>
**Token Refresh & Logout**<br>
**Password Reset via Email**<br>
<br>

### **Video**:<br>
**Video Upload via Admin Panel**<br>
**Automatic Video Transcoding**<br>
**Adaptive Video Delivery**<br>
**Thumbnail Generation**<br>
**Asynchronous Processing**<br>
**Performance Optimization**<br>


## ![Tech Stack Icon](assets/icons/stack.png) Tech Stack
• Python 3.11  
• Django 5.2.8  
• Django REST Framework 3.16.1  
• Docker and Docker Compose  
• FFMPEG - Video encoder  
• JWT-Authentifizierung  |    Secure login with JSON Web Tokens  
• PosgreSQL              |    Database  


## ![Tech Stack Icon](assets/icons/folder.png) Project Structure
VIDEOFLIX-BACKEND/  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── assets/  &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;# Static project assets (images, files, etc.)  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp; |── icons/ &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Icon files used by the application  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── image/ &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;# Image files used by the application   
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── auth_app/  &nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django app handling authentication features  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── api/    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── managers.py  &emsp;&emsp;&emsp;&nbsp;&emsp;# Email-based Django user manager  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── permissions.py  &emsp;&emsp;&nbsp;&emsp;# Owner permission and cookie JWT  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── serializers.py  &emsp;&emsp;&emsp;&nbsp;&emsp;# validates, converts, and represents data  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── urls.py &nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# API URL routes for authentication  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;└──  views.py  &nbsp;&nbsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;#  Complete JWT-based auth workflow  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── test_models.py &emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Tests for authentication functionality   
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── core/  &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Main project configuration module  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;├── settings.py  &nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django project settings (config, installed apps, etc.)  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;└── urls.py  &emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;# Root URL routing for the whole project  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── content_app/  &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;# Django app handling videos and related features  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── api/    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── permissions.py  &emsp;&emsp;&emsp;&nbsp;# Owner permission and cookie JWT  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── serializer.py   &nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;# Serializers for video-related models  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── signals.py &emsp;&emsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;# Video processing via Django signals  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── tasks.py &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# FFmpeg video resolution conversion functions  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;├── urls.py  &nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# API URL routes for quiz features  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&emsp;&emsp;&emsp;└──  views.py   &nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;# Authenticated DRF HLS video streaming    
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── admin.py   &nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;# Admin panel configuration for video model  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── apps.py  &nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;# Django app configuration  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;├── models.py     &nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Database models for videos  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│   &emsp;&emsp;&nbsp;&nbsp;└── test_models.py    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Tests for video functionality  
&emsp;&emsp;&nbsp;&emsp;&nbsp;│  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── env.template   &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Template file for environment variables  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── backend.Dockerfile  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# Builds Python app with dependencies, entrypoint   
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── backend.entrypoint.sh  &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;# Initialize and start the backend server    
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── docker-compose.yml  &emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;# Defines and runs multi-container Docker services  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── manage.py  &nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Django CLI management script  
&emsp;&emsp;&nbsp;&emsp;&nbsp;├── readme.md  &nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# Project documentation and setup guide  
&emsp;&emsp;&nbsp;&emsp;&nbsp;└── requirements.txt  &emsp;&nbsp;&nbsp;&nbsp;&emsp;&emsp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&emsp;# Python dependencies for the project  

# ![Installation Icon](assets/icons/installation.png) Installation
### 1. Install Python 3.11 or higher
Installed from https://www.python.org/downloads/<br>
### 2. FFMPEG - Video encoder
### Windows 10/11
&nbsp;&nbsp;Download the latest FFmpeg build: https://ffmpeg.org/download.html <br>
&nbsp;&nbsp;Windows builds (usually from gyan.dev or BtbN).
<br><br>
&nbsp;&nbsp;Unpack the ZIP file, e.g., to C:\ffmpeg<br>
&nbsp;&nbsp;Go to the bin folder → ffmpeg.exe is located there. <br>
&nbsp;&nbsp;Add the bin path to the environment variables:<br>
&nbsp;&nbsp;&nbsp;•&nbsp;Right-click on 'This PC' → 'Properties' → 'Advanced system settings'.<br>
&nbsp;&nbsp;&nbsp;•&nbsp;Click 'Environment Variables...' → add the entry C:\ffmpeg\bin to the Path.

### Linux
```bash
sudo apt update
sudo apt install ffmpeg 
```
### Mac OS
```bash
brew install ffmpeg 
```

### 3. Docker and Docker Compose  
Installed from https://docs.docker.com/get-started/get-docker/<br>

### 4. Clone the repository:
```bash
create a folder "videoflix_backend"
open the folder in VSCode
open the console
git clone https://github.com/Pinguinrakete/videoflix_backend.git .
```   

### 5. Generate a secret key
### Windows 10/11
```bash
Generate a SCRET_KEY, please open the PowerShell:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
### LINUX / MAC OS 
```bash
Generate a SCRET_KEY, please open the bash:
python3 -c 'import secrets, string; chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"; print("".join(secrets.choice(chars) for _ in range(50)))'
```
### 5. Configure the .env file

Please rename the file .env.template to .env and adjust all necessary environment variables.   
The Secret Key from step 5 should be entered here.  
The admin user will be created automatically when the container is built, based on the values defined in the .env file.

### 6. Starting the Docker container
First, build and start the Docker container.
```bash
docker-compose up --build
```
When restarting
```bash
docker-compose up
```
Remove all containers if needed
```bash
docker-compose down -v 
```

### 7. Access to Backend and Admin Panel
You can reach the backend at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin

## ![API Endpoints Icon](assets/icons//api.png) API Endpoint Documentation
### ![Authentication Icon](assets/icons/authentication.png) Authentication 

| Method | Endpoint                               | Description                                              |
|--------|----------------------------------------|----------------------------------------------------------|
| POST   | /api/auth/register/                    | Registers a new user                                     |
| GET    |`/api/activate/<uidb64>/`               | Activates the user account using the token sent by email |
| POST   | /api/auth/login/                       | Confirms identity and returns JWT tokens                 |
| POST   | /api/auth/logout/                      | Logs user out and clears session data                    |
| POST   | /api/auth/token/refresh/               | Refreshes expired authentication tokens for users        |
| POST   | /api/passwort_reset/                   | Sends a password reset link to the user’s email          |
| POST   |`/api/passwort_confirm/<uidb64>/<token>`| Confirms the password change using the email token       |

### ![Quiz Icon](assets/icons/quiz.png) Video
| Method | Endpoint                                                  | Description                                                           |            
|--------|-----------------------------------------------------------|-----------------------------------------------------------------------|
| GET    | /api/video/                                               | Returns a list of all available videos                                |
| GET    |`/api/video/<int:movie_id>/<str:resolution>/index.m3u8`    | Returns the HLS master playlist for a selected film and resolution.   |
| GET    |`/api/video/<int:movie_id>/<str:resolution>/<str:segment>/`| Returns a single HLS video segment for a selected film and resolution |


### ![Quiz Icon](assets/icons/quiz.png) 8. License
The license is under the MIT License.