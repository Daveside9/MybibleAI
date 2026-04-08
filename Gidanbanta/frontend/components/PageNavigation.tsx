'use client';

import { useRouter } from 'next/navigation';
import { ArrowLeft, Home } from 'lucide-react';

interface PageNavigationProps {
  showBack?: boolean;
  showHome?: boolean;
  className?: string;
}

export default function PageNavigation({ 
  showBack = true, 
  showHome = true,
  className = '' 
}: PageNavigationProps) {
  const router = useRouter();

  return (
    <div className={`flex items-center gap-2 mb-4 ${className}`}>
      {showBack && (
        <button
          onClick={() => router.back()}
          className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors"
          aria-label="Go back"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>
      )}
      
      {showHome && (
        <button
          onClick={() => router.push('/dashboard')}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          aria-label="Go to home"
        >
          <Home className="w-4 h-4" />
          <span>Home</span>
        </button>
      )}
    </div>
  );
}
