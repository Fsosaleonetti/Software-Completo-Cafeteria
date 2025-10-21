import { Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';

import { AppLayout } from './layouts/AppLayout';
import { routes } from './routes/routes';

function App() {
  return (
    <AppLayout>
      <Suspense fallback={<div>Cargando...</div>}>
        <Routes>
          {routes.map((route) => (
            <Route key={route.path} path={route.path} element={<route.component />} />
          ))}
          <Route path="*" element={<div>Seleccione un módulo</div>} />
        </Routes>
      </Suspense>
    </AppLayout>
  );
}

export default App;
