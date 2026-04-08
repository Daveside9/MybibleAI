'use client';

import { useMemo } from 'react';

interface DateSelectorProps {
  selectedDate: string;
  onDateChange: (date: string) => void;
  daysToShow?: number;
}

export default function DateSelector({ 
  selectedDate, 
  onDateChange,
  daysToShow = 14 
}: DateSelectorProps) {
  // Generate date range from current date
  const availableDates = useMemo(() => {
    const dates = [];
    const today = new Date();
    
    for (let i = 0; i < daysToShow; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date.toISOString().split('T')[0]);
    }
    
    return dates;
  }, [daysToShow]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return {
      weekday: date.toLocaleDateString('en-US', { weekday: 'short' }),
      day: date.getDate(),
      month: date.toLocaleDateString('en-US', { month: 'short' }),
      year: date.getFullYear()
    };
  };

  const isToday = (dateString: string) => {
    const today = new Date().toISOString().split('T')[0];
    return dateString === today;
  };

  return (
    <div className="bg-navy-100 rounded-card p-4">
      <h3 className="text-text-primary font-semibold mb-3">Select Date</h3>
      
      {/* Horizontal scrollable date picker */}
      <div className="relative">
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-primary scrollbar-track-navy-200">
          {availableDates.map((date) => {
            const formatted = formatDate(date);
            const today = isToday(date);
            const selected = date === selectedDate;
            
            return (
              <button
                key={date}
                onClick={() => onDateChange(date)}
                className={`
                  flex-shrink-0 px-4 py-3 rounded-lg transition-all min-w-[80px]
                  ${selected
                    ? 'bg-primary text-white shadow-lg scale-105'
                    : today
                    ? 'bg-cyan/20 text-cyan border-2 border-cyan hover:bg-cyan/30'
                    : 'bg-navy-200 text-text-muted hover:bg-navy-300 hover:text-text-primary'
                  }
                `}
                aria-label={`Select ${formatted.weekday}, ${formatted.month} ${formatted.day}`}
                aria-pressed={selected}
              >
                {/* Weekday */}
                <div className={`text-xs font-medium ${selected ? 'text-white/90' : ''}`}>
                  {formatted.weekday}
                </div>
                
                {/* Day */}
                <div className={`text-lg font-bold my-1 ${selected ? 'text-white' : ''}`}>
                  {formatted.day}
                </div>
                
                {/* Month */}
                <div className={`text-xs ${selected ? 'text-white/90' : ''}`}>
                  {formatted.month}
                </div>
                
                {/* Today indicator */}
                {today && !selected && (
                  <div className="mt-1 w-1.5 h-1.5 bg-cyan rounded-full mx-auto"></div>
                )}
              </button>
            );
          })}
        </div>
        
        {/* Scroll indicators for mobile */}
        <div className="absolute right-0 top-0 bottom-2 w-8 bg-gradient-to-l from-navy-100 to-transparent pointer-events-none md:hidden"></div>
      </div>
      
      {/* Selected date display for screen readers */}
      <div className="sr-only" role="status" aria-live="polite">
        Selected date: {formatDate(selectedDate).weekday}, {formatDate(selectedDate).month} {formatDate(selectedDate).day}, {formatDate(selectedDate).year}
      </div>
    </div>
  );
}
