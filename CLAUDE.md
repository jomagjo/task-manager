# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Overview

MoreMe is a Django + PostgreSQL task manager: users create task lists (Daily/Weekly/Custom category), add tasks to them, search, dictate by voice, and manage status via a colored dropdown. Deployed on a GCP e2-micro VM at https://moreme.duckdns.org, behind Caddy (automatic HTTPS) in front of gunicorn, all via `docker compose --profile prod`.

## Design system

@design-system.md

## Project structure

- `config/` — Django settings, URLs, WSGI/ASGI
- `tasks/` — the app: models (`Task`, `TaskList`), views, forms, serializers (REST API), templates
- `templates/base.html` — shared layout/navbar/global CSS for every page
- `Dockerfile`, `docker-compose.yml`, `Caddyfile` — production deployment (the `prod` compose profile; local dev only runs `db` by default)

## Local development

```bash
docker compose up -d        # Postgres only
venv/bin/python manage.py runserver 127.0.0.1:8111
```

## Deploying a change

```bash
git push
ssh -i ~/.ssh/gcp_task_manager uchiha@35.255.84.113 "cd ~/task-manager && git pull && sudo docker compose --profile prod up -d --build web"
```

## Password reset

Deliberately not built as a self-service email flow — the signup form doesn't even collect an email address, so that would've been a bigger change (email required at signup, SMTP credentials, migrating existing accounts). Instead: a dedicated `admin` superuser account exists on the live site specifically for this. If a user forgets their password, an admin resets it directly via `/admin/` → Users → their account → set password. Don't propose building email-based reset unless the user asks for it again specifically.

## Known gotchas

- An editor hook auto-reformats templates after every write. It can split a Django `{% %}` tag's closing bracket onto its own line, which Django 3.2 silently mis-parses (no error, the tag just doesn't work). See `design-system.md` for the specific incident. After editing a template, re-fetch the rendered page rather than trusting a template-parse check alone.
- `Task` has no direct `user` field — ownership is derived through `task_list.user`. Don't reintroduce a redundant FK.
