import { useState, useEffect } from 'react';

// Define both API endpoints
const CASES_API_URL = 'http://localhost:8000/api/cases/';
const CLIENTS_API_URL = 'http://localhost:8000/api/clients/'; // Adjust this if your router path is different

export default function App() {
  // --- STATE: CASES ---
  const [cases, setCases] = useState([]);
  const [caseFormData, setCaseFormData] = useState({
    invoice_number: '',
    invoice_amount: '',
    invoice_date: '',
    due_date: '',
    client_id: ''
  });

  // --- STATE: CLIENTS ---
  const [clients, setClients] = useState([]);
  const [clientFormData, setClientFormData] = useState({
    client_name: '',
    company_name: '',
    city: '',
    contact_person: '',
    email: '',
    phone: ''
  });

  const [error, setError] = useState(null);

  // Fetch both sets of data when the page loads
  useEffect(() => {
    fetchCases();
    fetchClients();
  }, []);

  // --- FETCH FUNCTIONS ---
  const fetchCases = async () => {
    try {
      const response = await fetch(CASES_API_URL);
      if (!response.ok) throw new Error("Failed to fetch cases");
      const data = await response.json();
      setCases(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchClients = async () => {
    try {
      const response = await fetch(CLIENTS_API_URL);
      if (!response.ok) throw new Error("Failed to fetch clients");
      const data = await response.json();
      setClients(data);
    } catch (err) {
      setError(err.message);
    }
  };

  // --- SUBMIT FUNCTIONS ---
  const handleCaseSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(CASES_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(caseFormData),
      });

      if (!response.ok) throw new Error("Failed to create case");

      setCaseFormData({ invoice_number: '', invoice_amount: '', invoice_date: '', due_date: '', client_id: '' });
      fetchCases();
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleClientSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(CLIENTS_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(clientFormData),
      });

      if (!response.ok) throw new Error("Failed to create client");

      // Clear the form and refresh the table
      setClientFormData({ client_name: '', company_name: '', city: '', contact_person: '', email: '', phone: '' });
      fetchClients();
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
        Invoice Recovery Dashboard
      </h1>

      {error && <div style={{ color: 'red', marginBottom: '20px', padding: '10px', backgroundColor: '#ffe6e6', borderRadius: '5px' }}>Error: {error}</div>}

      <div style={{ display: 'flex', gap: '40px', marginTop: '30px' }}>

        {/* ========================================== */}
        {/* LEFT COLUMN: CLIENT MANAGEMENT             */}
        {/* ========================================== */}
        <div style={{ flex: 1 }}>
          <h2 style={{ color: '#333' }}>Client Management</h2>

          {/* CREATE CLIENT FORM */}
          <div style={{ border: '1px solid #ccc', padding: '20px', marginBottom: '30px', borderRadius: '8px', backgroundColor: '#fafafa' }}>
            <h3>Add New Client</h3>
            <form onSubmit={handleClientSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <input type="text" placeholder="Client Name" required
                value={clientFormData.client_name}
                onChange={(e) => setClientFormData({ ...clientFormData, client_name: e.target.value })}
              />
              <input type="text" placeholder="Company Name" required
                value={clientFormData.company_name}
                onChange={(e) => setClientFormData({ ...clientFormData, company_name: e.target.value })}
              />
              <input type="text" placeholder="City" required
                value={clientFormData.city}
                onChange={(e) => setClientFormData({ ...clientFormData, city: e.target.value })}
              />
              <input type="text" placeholder="Contact Person" required
                value={clientFormData.contact_person}
                onChange={(e) => setClientFormData({ ...clientFormData, contact_person: e.target.value })}
              />
              <input type="email" placeholder="Email" required
                value={clientFormData.email}
                onChange={(e) => setClientFormData({ ...clientFormData, email: e.target.value })}
              />
              <input type="tel" placeholder="Phone" required
                value={clientFormData.phone}
                onChange={(e) => setClientFormData({ ...clientFormData, phone: e.target.value })}
              />
              <button type="submit" style={{ padding: '8px', cursor: 'pointer', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
                Save Client
              </button>
            </form>
          </div>

          {/* CLIENT LIST DISPLAY */}
          <h3>Active Clients</h3>
          {clients.length === 0 ? (
            <p>No clients found.</p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', fontSize: '14px' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f4f4f4' }}>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>ID</th>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>Company</th>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>Contact</th>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>City</th>
                  </tr>
                </thead>
                <tbody>
                  {clients.map((c) => (
                    <tr key={c.id}>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{c.id}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{c.company_name}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{c.contact_person}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{c.city}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* ========================================== */}
        {/* RIGHT COLUMN: CASE MANAGEMENT              */}
        {/* ========================================== */}
        <div style={{ flex: 1 }}>
          <h2 style={{ color: '#333' }}>Case Management</h2>

          {/* CREATE CASE FORM */}
          <div style={{ border: '1px solid #ccc', padding: '20px', marginBottom: '30px', borderRadius: '8px', backgroundColor: '#fafafa' }}>
            <h3>Create New Case</h3>
            <form onSubmit={handleCaseSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <input type="text" placeholder="Invoice Number" required
                value={caseFormData.invoice_number}
                onChange={(e) => setCaseFormData({ ...caseFormData, invoice_number: e.target.value })}
              />
              <input type="number" step="0.01" placeholder="Amount" required
                value={caseFormData.invoice_amount}
                onChange={(e) => setCaseFormData({ ...caseFormData, invoice_amount: e.target.value })}
              />
              <input type="date" placeholder="Invoice Date" required
                value={caseFormData.invoice_date}
                onChange={(e) => setCaseFormData({ ...caseFormData, invoice_date: e.target.value })}
              />
              <input type="date" placeholder="Due Date" required
                value={caseFormData.due_date}
                onChange={(e) => setCaseFormData({ ...caseFormData, due_date: e.target.value })}
              />
              <input type="number" placeholder="Client ID" required
                value={caseFormData.client_id}
                onChange={(e) => setCaseFormData({ ...caseFormData, client_id: e.target.value })}
              />
              <button type="submit" style={{ padding: '8px', cursor: 'pointer', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}>
                Submit Case
              </button>
            </form>
          </div>

          {/* CASE LIST DISPLAY */}
          <h3>Active Cases</h3>
          {cases.length === 0 ? (
            <p>No cases found.</p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', fontSize: '14px' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f4f4f4' }}>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>Client ID</th>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>Invoice #</th>
                    <th style={{ padding: '8px', borderBottom: '2px solid #ddd' }}>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {cases.map((c) => (
                    <tr key={c.id}>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{c.client_id}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{c.invoice_number}</td>
                      <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>${c.invoice_amount}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}