import './Dashboard.css';

const pedidos = [
  { id: 'PC-101', estado: 'pendiente', sala: 'Salón', demora: '02:15' },
  { id: 'PC-102', estado: 'en_curso', sala: 'Mostrador', demora: '05:40' },
  { id: 'PC-103', estado: 'listo', sala: 'Terraza', demora: '07:05' }
];

const estadoLabel: Record<string, string> = {
  pendiente: 'Pendiente',
  en_curso: 'En curso',
  listo: 'Listo'
};

export default function CocinaDashboard() {
  return (
    <section className="dashboard">
      <header>
        <h2>Tablero de Cocina (KDS)</h2>
        <p>Cola visual de comandas con estado y sala de origen.</p>
      </header>
      <div className="dashboard__grid">
        {pedidos.map((pedido) => (
          <article key={pedido.id} className="card">
            <h3>{pedido.id}</h3>
            <p>Estado: {estadoLabel[pedido.estado]}</p>
            <p>Origen: {pedido.sala}</p>
            <small>Tiempo en cola: {pedido.demora}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
