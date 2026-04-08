'use client';

import { useState } from 'react';

interface DatePickerProps {
  selectedDate: string;
  onDateChange: (date: string) => void;
}

export default function DatePicker({ selectedDate, onDateChange }: DatePickerProps) {
  const [isOpen, setIsOpen] = useState(false);

  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  const formatDate = (date: Date) => {
    return date.toISOString().split('T')[0];
  };

  const getDisplayDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const todayStr = formatDate(today);
    const tomorrowStr = formatDate(tomorrow);

    if (dateStr === todayStr) return 'Today';
    if (dateStr === tomorrowStr) return 'Tomorrow';
    
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const quickDates = [
    { label: 'Today', value: formatDate(today) },
    { label: 'Tomorrow', value: formatDate(tomorrow) },
    { label: 'Yesterday', value: formatDate(new Date(today.getTime() - 24 * 60 * 60 * 1000)) },
  ];

  return (
    <div className="relative">
      {/* Date Picker Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 bg-black/30 hover:bg-black/40 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/20 shadow-lg transition-all text-white"
      >
        <span className="text-sm">📅</span>
        <span className="font-semibold text-sm">{getDisplayDate(selectedDate)}</span>
        <span className={`text-xs transition-transform ${isOpen ? 'rotate-180' : ''}`}>▼</span>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown Content */}
          <div className="absolute top-full left-0 mt-2 bg-gray-900 backdrop-blur-md rounded-lg border border-white/20 shadow-2xl z-50 min-w-[200px]">
            {/* Quick Date Options */}
            <div className="p-2">
              <div className="text-xs font-semibold text-gray-400 mb-2 px-2">Quick Select</div>
              {quickDates.map((dateOption) => (
                <button
                  key={dateOption.value}
                  onClick={() => {
                    onDateChange(dateOption.value);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-all hover:bg-white/10 ${
                    selectedDate === dateOption.value 
                      ? 'bg-blue-600 text-white' 
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  {dateOption.label}
                </button>
              ))}
            </div>

            {/* Divider */}
            <div className="border-t border-white/10 my-2" />

            {/* Custom Date Picker */}
            <div className="p-2">
              <div className="text-xs font-semibold text-gray-400 mb-2 px-2">Custom Date</div>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => {
                  onDateChange(e.target.value);
                  setIsOpen(false);
                }}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white text-sm focus:border-blue-500 focus:outline-none"
              />
            </div>

            {/* Week Navigation */}
            <div className="p-2 border-t border-white/10">
              <div className="text-xs font-semibold text-gray-400 mb-2 px-2">This Week</div>
              <div className="grid grid-cols-7 gap-1">
                {Array.from({ length: 7 }, (_, i) => {
                  const date = new Date(today);
                  date.setDate(today.getDate() - today.getDay() + i);
                  const dateStr = formatDate(date);
                  const isSelected = selectedDate === dateStr;
                  const isToday = dateStr === formatDate(today);
                  
                  return (
                    <button
                      key={i}
                      onClick={() => {
                        onDateChange(dateStr);
                        setIsOpen(false);
                      }}
                      className={`p-2 text-xs rounded transition-all ${
                        isSelected 
                          ? 'bg-blue-600 text-white' 
                          : isToday
                          ? 'bg-green-600/20 text-green-400 hover:bg-green-600/30'
                          : 'text-gray-400 hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      <div className="font-semibold">
                        {date.toLocaleDateString('en-US', { weekday: 'short' })}
                      </div>
                      <div className="text-xs">
                        {date.getDate()}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}