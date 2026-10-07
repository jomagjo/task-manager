# Task Manager

A simple Django + PostgreSQL task manager. Add a task (title, description, due date, status) and view the list of all tasks.

## Setup

1. Copy the environment file and adjust if needed:

   ```bash
   cp .env.example .env
   ```

2. Start PostgreSQL:

   ```bash
   docker compose up -d
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. (Optional) Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the dev server:

   ```bash
   python manage.py runserver
   ```

7. Open http://127.0.0.1:8000/ to view the task list, or http://127.0.0.1:8000/add/ to add a task.

## Project Structure

- `config/` - Django project settings, URLs, WSGI/ASGI entry points
- `tasks/` - The task manager app (model, views, forms, templates, admin)
- `docker-compose.yml` - Local PostgreSQL container
