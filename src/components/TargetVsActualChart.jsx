import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TargetVsActualChart = ({ data }) => {
  // Filter out products with 0 targets and 0 actuals to keep chart clean
  const chartData = data.filter(item => item.targetQty > 0 || item.actualQty > 0);

  return (
    <div className="h-96 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
          <XAxis 
            dataKey="model" 
            angle={-45} 
            textAnchor="end" 
            interval={0} 
            tick={{ fontSize: 12, fill: '#6B7280' }} 
          />
          <YAxis tick={{ fill: '#6B7280' }} />
          <Tooltip 
            cursor={{ fill: '#F3F4F6' }}
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
          />
          <Legend wrapperStyle={{ top: 0, left: 20 }} />
          
          {/* Target Bar - Gray */}
          <Bar dataKey="targetQty" name="Target QTY" fill="#D1D5DB" radius={[4, 4, 0, 0]} />
          
          {/* Actual Bar - Afriipower Blue */}
          <Bar dataKey="actualQty" name="Actual QTY" fill="var(--color-afrii-lightblue)" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TargetVsActualChart;