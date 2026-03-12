import React from 'react';

const KpiCard = ({ title, value, target, type }) => {
  // Format numbers with commas
  const formattedValue = new Intl.NumberFormat('en-NG').format(value);
  
  // Determine color logic based on target achievement
  let textColorClass = "text-[var(--color-afrii-dark)]";
  if (target) {
    const percentAchieved = (value / target) * 100;
    if (percentAchieved >= 100) textColorClass = "text-[var(--color-afrii-green)]";
    else if (percentAchieved >= 70) textColorClass = "text-[var(--color-afrii-lightblue)]";
    else textColorClass = "text-[var(--color-afrii-orange)]";
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 flex flex-col justify-center items-start border-l-4 border-[var(--color-afrii-blue)]">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">{title}</h3>
      <div className={`text-3xl font-bold mt-2 ${textColorClass}`}>
        {type === 'revenue' ? `₦${formattedValue}` : formattedValue}
      </div>
      {target && (
        <p className="text-xs text-gray-400 mt-2">
          {((value / target) * 100).toFixed(1)}% of Target
        </p>
      )}
    </div>
  );
};

export default KpiCard;