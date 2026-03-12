import React, { useState, useEffect } from 'react';
import axios from 'axios';
import KpiCard from './components/KpiCard';
import TargetVsActualChart from './components/TargetVsActualChart';

function App() {
  const [kpis, setKpis] = useState({ targetRevenue: 0, actualRevenue: 0, targetQty: 0, actualQty: 0 });
  const [products, setProducts] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState('2026-03-01');

  // Hardcoded rep_id for Mercy, can be dynamic later
  const repId = 1; 

  useEffect(() => {
    const fetchData = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const kpiRes = await axios.get(`${API_URL}/api/kpis/${repId}?month=${selectedMonth}`);
        setKpis(kpiRes.data);

        const prodRes = await axios.get(`${API_URL}/api/products/${repId}?month=${selectedMonth}`);
        setProducts(prodRes.data);
      } catch (error) {
        console.error("Error fetching data", error);
      }
    };
    fetchData();
  }, [selectedMonth]);

  return (
    <div className="min-h-screen bg-[var(--color-afrii-gray)] p-8 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-8 bg-[var(--color-afrii-blue)] text-white p-4 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold tracking-wider">AFRIIPOWER INTERNAL DASHBOARD</h1>
        <select 
          className="bg-white text-[var(--color-afrii-dark)] p-2 rounded-md font-semibold"
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
        >
          <option value="2026-01-01">January 2026</option>
          <option value="2026-02-01">February 2026</option>
          <option value="2026-03-01">March 2026</option>
        </select>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <KpiCard title="Target Revenue (₦)" value={kpis.targetRevenue} type="neutral" />
        <KpiCard title="Actual Revenue (₦)" value={kpis.actualRevenue} target={kpis.targetRevenue} type="revenue" />
        <KpiCard title="Target Units" value={kpis.targetQty} type="neutral" />
        <KpiCard title="Units Sold" value={kpis.actualQty} target={kpis.targetQty} type="qty" />
      </div>

      {/* Charts Section */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-[var(--color-afrii-blue)] mb-4">Product Performance: Target vs Actual (Units)</h2>
        <TargetVsActualChart data={products} />
      </div>

    </div>
  );
}

export default App;