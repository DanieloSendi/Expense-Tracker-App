# Expense-Tracker-App

An expense tracking application developed in Django.

## Features

- User authentication (register, login, logout)
- Expense management (add, edit, delete, view)
- Budget tracking with graphic alerts
- User profile management (username, email update, password change)
- Responsive UI/UX with Bootstrap
- CSV export of expenses
- Dockerized – Runs in a container for easy deployment
- CI/CD with GitHub Actions – Automated testing, Docker build, and deployment

## Installation & Setup

### Clone the repository

```bash
git clone https://github.com/DanieloSendi/Expense-Tracker-App.git
cd Expense-Tracker-App
```

### Create a virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin user (optional)
```

### Run the development server

```bash
python manage.py runserver
```

## Structure of the application

```bash
Expense-Tracker-App/
│── config/                       # Main Django settings & URLs
│── expenses/                     # Expense management module
│── users/                        # User authentication & profile management
│── templates/                    # HTML templates for frontend
│── static/                       # CSS, JavaScript, images
│── .env                          # Environment variables (not in repo)
│── requirements.txt              # Required Python packages
│── manage.py                     # Django entry point
│── Dockerfile                    # Docker configuration
│── .dockerignore                 # Files ignored in Docker builds
│── .github/workflows/django.yml  # CI/CD configuration
│── db.sqlite3                    # SQLite database file (local development)
│── README.md                     # Project documentation
│── LICENSE                       # License file for open-source usage
```

## Database models

The project contains three models in expenses app:

- **Category** - Stores predefined categories of expenses.
- **Expense** - Stores information about the user's expenses (amount, category, description, date).
- **Budget** - Stores user's monthly spending limit.

## Dashboard

Users can see:

- 📊 Total spent & balance
- 🟢 Green alert (under budget)
- 🟡 Yellow alert (near limit)
- 🔴 Red alert (over budget)

## Run with Docker

If you prefer running the application in a Docker container, use the following commands:

### Build and run locally

```bash
docker build -t expense-tracker .
docker run -p 8000:8000 --env SECRET_KEY=mysecretkey expense-tracker
```

### Run using the published Docker image from GitHub Container Registry

```bash
docker pull ghcr.io/danielosendi/expense-tracker-app:latest
docker run -p 8000:8000 ghcr.io/danielosendi/expense-tracker-app:latest
```

## CI/CD & Deployment

This project uses GitHub Actions for CI/CD automation:

- Build & Test – Every push to main triggers tests.
- Release – The app is containerized using Docker.
- Deploy – The latest image is deployed automatically.

## License

This project is licensed under the MIT License.