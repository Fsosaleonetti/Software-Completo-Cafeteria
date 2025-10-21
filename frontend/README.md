# Frontend React - Sistema de Cafetería

SPA construida con React + Vite en TypeScript. Sirve como base para las vistas por rol:

- **Mozo:** mapa de mesas, carga de pedidos, precuenta.
- **Cocina:** KDS en tiempo real y control de comandas.
- **Caja:** cobros, arqueos, múltiples medios de pago y propinas.
- **Administración:** gestión de catálogo, stock, clientes, proveedores e integraciones.

## Scripts

```bash
npm install
npm run dev       # desarrollo
npm run build     # build producción
npm run preview   # sirve la build
```

Configurar la variable `VITE_API_URL` para apuntar al backend (por defecto `http://localhost:8000/api`).

Los componentes actuales son maquetas funcionales y deben conectarse a los endpoints correspondientes.
