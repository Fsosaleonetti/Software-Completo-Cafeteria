import './Dashboard.css';

const modulos = [
  {
    nombre: 'Productos y Recetas',
    descripcion: 'Gestioná listas de precios, recetas, favoritos y stock mínimo.'
  },
  {
    nombre: 'Reportes',
    descripcion: 'Ventas, gastos, propinas y mapas de calor exportables a Excel.'
  },
  {
    nombre: 'Integraciones',
    descripcion: 'Configuración de Mercado Pago, WhatsApp y Carta QR.'
  }
];

export default function AdminDashboard() {
  return (
    <section className="dashboard">
      <header>
        <h2>Panel Administrativo</h2>
        <p>Centro de control para usuarios, stock, proveedores e integraciones.</p>
      </header>
      <div className="dashboard__grid">
        {modulos.map((modulo) => (
          <article key={modulo.nombre} className="card">
            <h3>{modulo.nombre}</h3>
            <p>{modulo.descripcion}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
