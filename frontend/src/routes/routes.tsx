import { lazy } from 'react';

import type { ComponentType } from 'react';

interface RouteConfig {
  path: string;
  component: ComponentType;
}

export const routes: RouteConfig[] = [
  {
    path: '/mozo',
    component: lazy(() => import('../pages/MozoDashboard'))
  },
  {
    path: '/cocina',
    component: lazy(() => import('../pages/CocinaDashboard'))
  },
  {
    path: '/caja',
    component: lazy(() => import('../pages/CajaDashboard'))
  },
  {
    path: '/admin',
    component: lazy(() => import('../pages/AdminDashboard'))
  }
];
