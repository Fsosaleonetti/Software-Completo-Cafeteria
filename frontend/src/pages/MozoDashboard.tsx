import './Dashboard.css';

const mesas = [
  { sala: 'Salón', numero: '1', estado: 'Ocupada', mozo: 'Mozo Demo' },
  { sala: 'Salón', numero: '2', estado: 'Libre', mozo: 'Mozo Demo' },
  { sala: 'Terraza', numero: '3', estado: 'Cuenta solicitada', mozo: 'Mozo Demo' }
];

export default function MozoDashboard() {
  return (
    <section className="dashboard">
      <header>
        <h2>Gestión de Mesas</h2>
        <p>Visualización rápida de ocupación, con acceso a pedidos, precuenta e impresión.</p>
      </header>
      <div className="dashboard__grid">
        {mesas.map((mesa) => (
          <article key={`${mesa.sala}-${mesa.numero}`} className="card">
            <h3>
              {mesa.sala} · Mesa {mesa.numero}
            </h3>
            <p>Estado: {mesa.estado}</p>
            <small>Asignada a: {mesa.mozo}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
