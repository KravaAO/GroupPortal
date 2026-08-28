![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)




**GroupPortal** is a collaborative web application built with Django designed to provide:
- Authenticated user profiles
- Forum for discussions
- Electronic gradebook
- Events & calendar
- Polling & voting systems
- Resources, announcements, gallery, portfolio

This README describes project goals, structure, and setup instructions.

## Table of Contents
1. [Features](#features)  
2. [Architecture](#architecture)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Contributing](#contributing)  
6. [License](#license)

## Features

**Authentication**
- Registration, login, roles (user/moderator/admin)

**Forum**
- Topics, posts, moderator controls

**Gradebook**
- View and manage grades

**Events & Calendar**
- Event creation and visualization

**Polls & Voting**
- Multi-step polls
- Voting with single responses

**Announcements & Materials**
- Management of materials and media

**Portfolio & Gallery**
- User portfolios and image/gallery submissions

##  Architecture

The backend is implemented with **Django** using multiple apps:
- `accounts`, `forum`, `grades`, `events`, `polls`, `votes`, `announcements`, `portfolio`
Each handles a separate feature set to support teamwork.

Frontend uses:
- HTML5, CSS3
- Bootstrap for responsive styling

## Installation

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GroupPortal
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   
   Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your settings (see [Environment Variables](#environment-variables) section)

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Visit http://localhost:8000

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# For production with PostgreSQL:
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=groupportal_db
# DATABASE_USER=your_db_user
# DATABASE_PASSWORD=your_db_password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432

# Static and Media Files
STATIC_URL=/static/
MEDIA_URL=/media/
```

**Important**: 
- Change `SECRET_KEY` for production (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` with your domain name

## Deployment

### Production Checklist

Before deploying to production:
- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate and set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Setup PostgreSQL database (recommended)
- [ ] Configure static files hosting
- [ ] Enable HTTPS/SSL
- [ ] Setup error monitoring (optional)

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set DATABASE_ENGINE=django.db.backends.postgresql
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku run python manage.py collectstatic --noinput
   ```

8. **Open your app**
   ```bash
   heroku open
   ```

### Railway / Render Deployment

1. Connect your GitHub repository
2. Set environment variables from `.env.example`
3. Add PostgreSQL database
4. Configure build command: `pip install -r requirements.txt`
5. Configure start command: `gunicorn gp.wsgi`
6. Deploy

### VPS Deployment (Ubuntu/Debian)

1. **Update system and install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```

2. **Clone repository**
   ```bash
   cd /var/www
   git clone <repository-url> groupportal
   cd groupportal
   ```

3. **Setup virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE groupportal_db;
   CREATE USER groupportal_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE groupportal_db TO groupportal_user;
   \q
   ```

5. **Setup environment variables**
   ```bash
   nano .env
   # Configure all required variables
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

7. **Setup Gunicorn service**
   ```bash
   sudo nano /etc/systemd/system/groupportal.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=GroupPortal Django App
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/groupportal
   Environment="PATH=/var/www/groupportal/venv/bin"
   ExecStart=/var/www/groupportal/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 gp.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

8. **Setup Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/groupportal
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /var/www/groupportal/staticfiles/;
       }

       location /media/ {
           alias /var/www/groupportal/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

9. **Enable and start services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/groupportal /etc/nginx/sites-enabled/
   sudo systemctl start groupportal
   sudo systemctl enable groupportal
   sudo systemctl restart nginx
   ```

## Usage

After installation, access the application at:
- Development: http://localhost:8000
- Production: https://your-domain.com

**Admin Panel**: `/admin`
- Login with superuser credentials

**Main Features**:
- Forum: `/forum`
- E-Diary: `/e_diary`
- Events Calendar: `/events`
- Voting System: `/vote`

## Project Structure

```
GroupPortal/
├── e_diary/           # Electronic gradebook app
├── event_calendar/    # Events and calendar app
├── forum/             # Forum discussion app
├── gallery/           # Gallery app
├── gp/                # Project settings
│   ├── settings.py    # Main settings
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI config
├── main/              # Main pages app
├── portfolio/         # Portfolio app
├── users/             # User management app
├── vote_system/       # Voting and polls app
├── manage.py          # Django CLI
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
├── Procfile           # Heroku deployment
└── runtime.txt        # Python version
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
