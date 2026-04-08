'use client';

import { useState } from 'react';

interface CouponNavigatorProps {
  onCouponSelect: (couponType: string) => void;
}

export default function CouponNavigator({ onCouponSelect }: CouponNavigatorProps) {
  const [selectedCoupon, setSelectedCoupon] = useState<string>('today');

  const handleCouponClick = (couponType: string) => {
    console.log('Coupon clicked:', couponType);
    setSelectedCoupon(couponType);
    onCouponSelect(couponType);
  };

  return (
    <div className="bg-gradient-to-b from-gray-800 to-gray-900 rounded-lg overflow-hidden border border-gray-700 shadow-xl">
      {/* DAILY COUPONS Section */}
      <div className="bg-gradient-to-r from-gray-700 to-gray-800 px-4 py-3 border-b border-gray-600">
        <h2 className="text-white font-bold text-base tracking-wide">DAILY COUPONS</h2>
      </div>
      
      <div className="border-b border-gray-700">
        <button
          onClick={() => handleCouponClick('today')}
          className={`w-full px-4 py-3 text-left flex items-center justify-between transition-all ${
            selectedCoupon === 'today'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Today's matches</span>
          {selectedCoupon === 'today' && (
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
          )}
        </button>
        
        <button
          onClick={() => handleCouponClick('tomorrow')}
          className={`w-full px-4 py-3 text-left flex items-center justify-between transition-all border-t border-gray-700/50 ${
            selectedCoupon === 'tomorrow'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Tomorrow's matches</span>
          {selectedCoupon === 'tomorrow' && (
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
          )}
        </button>
      </div>

      {/* POPULAR COUPONS Section */}
      <div className="bg-gradient-to-r from-gray-700 to-gray-800 px-4 py-3 border-b border-gray-600 mt-2">
        <h2 className="text-white font-bold text-base tracking-wide">POPULAR COUPONS</h2>
      </div>
      
      <div>
        <button
          onClick={() => handleCouponClick('popular-today')}
          className={`w-full px-4 py-3 text-left transition-all ${
            selectedCoupon === 'popular-today'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Today's matches</span>
        </button>
        
        <button
          onClick={() => handleCouponClick('european')}
          className={`w-full px-4 py-3 text-left transition-all border-t border-gray-700/50 ${
            selectedCoupon === 'european'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Top European Leagues</span>
        </button>
        
        <button
          onClick={() => handleCouponClick('international-clubs')}
          className={`w-full px-4 py-3 text-left transition-all border-t border-gray-700/50 ${
            selectedCoupon === 'international-clubs'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Top International Clubs Leagues</span>
        </button>
        
        <button
          onClick={() => handleCouponClick('top-leagues')}
          className={`w-full px-4 py-3 text-left transition-all border-t border-gray-700/50 ${
            selectedCoupon === 'top-leagues'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Top Leagues</span>
        </button>
        
        <button
          onClick={() => handleCouponClick('american')}
          className={`w-full px-4 py-3 text-left transition-all border-t border-gray-700/50 ${
            selectedCoupon === 'american'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">American Leagues</span>
        </button>
        
        <button
          onClick={() => handleCouponClick('top-international')}
          className={`w-full px-4 py-3 text-left transition-all border-t border-gray-700/50 ${
            selectedCoupon === 'top-international'
              ? 'bg-gray-700/50 text-white'
              : 'text-gray-300 hover:bg-gray-800/50 hover:text-white'
          }`}
        >
          <span className="text-base">Top International</span>
        </button>
      </div>
    </div>
  );
}
