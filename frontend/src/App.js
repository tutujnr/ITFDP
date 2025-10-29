import React, { useEffect, useState } from "react";

function App() {
  const [farmers, setFarmers] = useState([]);
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    fetch("/farmers")
      .then((r) => r.json())
      .then(setFarmers)
      .catch(() => setFarmers([]));

    fetch("/prices")
      .then((r) => r.json())
      .then(setPrices)
      .catch(() => setPrices([]));
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "Arial, sans-serif" }}>
      <h1>Integrated Tea Farmers — MVP</h1>

      <section style={{ marginBottom: 24 }}>
        <h2>Recent Mombasa Prices (KSH/kg)</h2>
        {prices.length === 0 ? <p>No prices yet.</p> : (
          <table border="1" cellPadding="6">
            <thead>
              <tr><th>Timestamp</th><th>Price</th><th>Source</th></tr>
            </thead>
            <tbody>
              {prices.map(p => (
                <tr key={p.id}>
                  <td>{new Date(p.timestamp).toLocaleString()}</td>
                  <td>{p.price_ksh_per_kg}</td>
                  <td>{p.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section>
        <h2>Farmers</h2>
        {farmers.length === 0 ? <p>No farmers yet.</p> : (
          <ul>
            {farmers.map(f => (<li key={f.id}>{f.name} — {f.phone || "no phone"}</li>))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;
