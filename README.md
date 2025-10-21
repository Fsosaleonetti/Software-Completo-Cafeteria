# Sistema Completo de Cafetería

Arquitectura base para el sistema integral de comandas, stock, caja y tienda online de una cafetería. El proyecto se organiza en un **monorepo** con backend FastAPI + SQLAlchemy/Alembic y frontend React + Vite.

## Estructura

```
backend/   -> API FastAPI con autenticación JWT, RBAC y migraciones Alembic
frontend/  -> SPA en React + Vite con dashboards por rol (Mozo, Cocina, Caja, Admin)
infrastructure/ -> espacio reservado para IaC/CI/CD
```

## Stack propuesto

- **Backend:** FastAPI, SQLAlchemy 2.0, Alembic, JWT (python-jose) y passlib.
- **Base de datos:** SQLite para desarrollo. Variables `DATABASE_URL` y `SYNC_DATABASE_URL` permiten apuntar a PostgreSQL en producción.
- **Frontend:** React 18 + Vite + React Router + TanStack Query.
- **Tiempo real:** FastAPI soporta WebSockets/SSE (pendiente de implementar en `/app/api/routes`).
- **Impresión local:** servicio planificado vía módulo externo (no incluido).
- **Integraciones:** Mercado Pago, WhatsApp Business y API pública previstas en la capa de servicios.

## Primeros pasos

1. Revisar `backend/README.md` y `frontend/package.json` para instalar dependencias.
2. Configurar `.env` en `backend/` con claves JWT, base de datos y proveedores.
3. Ejecutar migraciones Alembic y el script de `app.tasks.seed` para cargar datos demo.
4. Levantar `uvicorn` y `vite` para validar el flujo base.

## Roadmap funcional

- [x] Modelado inicial de entidades principales (usuarios, ventas, stock, cocina, caja).
- [x] Routers básicos (`/auth`, `/usuarios`, `/clientes`).
- [x] Seed demo para cuentas iniciales.
- [x] Dashboards estáticos por rol en frontend.
- [ ] Implementación completa de flujos de venta, cocina, caja y stock en API.
- [ ] Integración Mercado Pago/WhatsApp y Webhooks.
- [ ] Motor de impresión y servicio local Windows.
- [ ] Reportes, analíticas y exportación Excel.

## Documentación y manuales

- La API expone documentación interactiva en `/docs` (Swagger) una vez que el backend está en ejecución.
- Se recomienda complementar con diagramas de flujo y manual de usuario en futuras iteraciones.

## Licencia

Uso interno de la cafetería. Ajustar según necesidad.
