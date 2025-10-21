# Backend FastAPI - Sistema Cafetería

Este servicio implementa la API principal del sistema de comandas, stock y caja para la cafetería. Incluye autenticación JWT, RBAC y migraciones con Alembic.

## Requisitos

- Python 3.11
- [Poetry](https://python-poetry.org/) 1.7+

## Instalación

```bash
poetry install
```

## Variables de entorno

Crear un archivo `.env` en `backend/` con, al menos:

```
SECRET_KEY=super-secreto
DATABASE_URL=sqlite:///./cafeteria.db
SYNC_DATABASE_URL=sqlite:///./cafeteria.db
```

Para usar PostgreSQL en producción:

```
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/cafeteria
SYNC_DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/cafeteria
```

## Migraciones

```bash
poetry run alembic upgrade head
```

## Datos demo

```bash
poetry run python -m app.tasks.seed
```

## Servidor de desarrollo

```bash
poetry run uvicorn app.main:app --reload
```

Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

## Tests

```bash
poetry run pytest
```
