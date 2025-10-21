import { ReactNode } from 'react';
import { Link } from 'react-router-dom';

import './AppLayout.css';

const menuLinks = [
  { path: '/mozo', label: 'Mozo' },
  { path: '/cocina', label: 'Cocina' },
  { path: '/caja', label: 'Caja' },
  { path: '/admin', label: 'Administración' }
];

interface Props {
  children: ReactNode;
}

export function AppLayout({ children }: Props) {
  return (
    <div className="layout">
      <aside className="layout__sidebar">
        <h1 className="layout__title">Cafetería POS</h1>
        <nav>
          <ul>
            {menuLinks.map((item) => (
              <li key={item.path}>
                <Link to={item.path}>{item.label}</Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <main className="layout__main">{children}</main>
    </div>
  );
}
