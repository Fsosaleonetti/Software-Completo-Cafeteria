import './Dashboard.css';

const pagos = [
  { medio: 'Efectivo', monto: 25400, cantidad: 18 },
  { medio: 'Mercado Pago QR', monto: 18400, cantidad: 12 },
  { medio: 'Crédito', monto: 9800, cantidad: 4 }
];

export default function CajaDashboard() {
  const total = pagos.reduce((acc, pago) => acc + pago.monto, 0);

  return (
    <section className="dashboard">
      <header>
        <h2>Panel de Caja</h2>
        <p>Resumen de movimientos y medios de pago del turno en curso.</p>
        <strong>Total facturado: ARS {total.toLocaleString('es-AR')}</strong>
      </header>
      <div className="dashboard__grid">
        {pagos.map((pago) => (
          <article key={pago.medio} className="card">
            <h3>{pago.medio}</h3>
            <p>Monto: ARS {pago.monto.toLocaleString('es-AR')}</p>
            <small>Transacciones: {pago.cantidad}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
