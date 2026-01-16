# ChatApp

Real-time chat application built with Django, deployed via Docker, and orchestrated in Kubernetes. Sample application used in the [DevOps Lab](https://github.com/Fahras23/Devops-lab).

## 🛠️ Technologies

| Layer | Tools |
|-------|-------|
| Backend | Django, Python |
| Database | SQLite (dev), PostgreSQL (prod) |
| Container | Docker, Docker Compose |
| Deployment | Kubernetes via Argo CD |

## 🎯 Purpose

Sample workload deployed through the DevOps Lab pipeline:
- **Local dev**: `docker-compose up`
- **Kubernetes**: Beta/Prod environments via GitOps
- **Integration**: Lives in DevOps Lab `Apps/chatapp/`

## 🚀 Quick Start (Local)

Setup local 

1. Clone & Virtual Environment
git clone https://github.com/Fahras23/ChatApp.git
cd ChatApp
python -m venv venv
source venv/bin/activate # Linux/Mac | Windows: venv\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt

3. Set Environment Variables
export REDIS_PORT=6379
export REDIS_HOST=localhost
export SECRET_KEY='your-super-secret-django-key-here'

4. Database & Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

5. Run Daphne Server or Docker compose
daphne -b 0.0.0.0 -p 8000 chatapp.asgi:application
setup redis on local machine or with docker container with access port on 6379
- Better alternative: docker compose up

6. Optional change to setup postgres database in settings