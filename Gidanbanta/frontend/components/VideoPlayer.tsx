'use client';

import { useEffect, useRef, useState } from 'react';

interface VideoPlayerProps {
  streamUrl?: string;
  isLive?: boolean;
  title?: string;
}

export default function VideoPlayer({ streamUrl, isLive = false, title }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);


  useEffect(() => {
    const video = videoRef.current;
    if (!video || !streamUrl) return;

    setIsLoading(true);
    setHasError(false);

    // For HLS streams, we would typically use hls.js
    // For now, we'll use the native video element
    video.src = streamUrl;
    
    const handleLoadStart = () => setIsLoading(true);
    const handleCanPlay = () => {
      setIsLoading(false);
      setHasError(false);
    };
    const handleError = () => {
      setIsLoading(false);
      setHasError(true);
    };


    video.addEventListener('loadstart', handleLoadStart);
    video.addEventListener('canplay', handleCanPlay);
    video.addEventListener('error', handleError);


    return () => {
      video.removeEventListener('loadstart', handleLoadStart);
      video.removeEventListener('canplay', handleCanPlay);
      video.removeEventListener('error', handleError);

    };
  }, [streamUrl]);



  if (!streamUrl) {
    return (
      <div className="w-full aspect-video bg-gradient-to-br from-green-900 to-green-800 flex items-center justify-center border border-green-700 rounded-lg relative overflow-hidden">
        {/* Football field background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="w-full h-full bg-gradient-to-r from-green-600 to-green-700"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 border-2 border-white rounded-full"></div>
          <div className="absolute top-1/2 left-0 w-16 h-24 border-2 border-white border-l-0"></div>
          <div className="absolute top-1/2 right-0 w-16 h-24 border-2 border-white border-r-0"></div>
        </div>
        
        <div className="text-center text-white relative z-10">
          <div className="text-6xl mb-4 animate-bounce">⚽</div>
          <div className="text-xl mb-2 font-semibold">
            {isLive ? 'Live Football Match' : 'Football Match Stream'}
          </div>
          <div className="text-sm text-green-200 mb-4">
            {isLive ? 'Match is live - Stream will be available soon' : 'Stream not configured'}
          </div>
          {title && (
            <div className="bg-black/50 px-4 py-2 rounded-lg mb-4">
              <div className="text-lg font-bold">{title}</div>
            </div>
          )}
          {isLive && (
            <div className="flex items-center justify-center gap-2 text-red-400">
              <div className="w-3 h-3 bg-red-400 rounded-full animate-pulse"></div>
              <span className="text-sm font-semibold">🔴 LIVE MATCH</span>
            </div>
          )}
          <div className="mt-4 text-xs text-green-300">
            Real-time match data • Live chat available
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full aspect-video bg-black rounded-lg overflow-hidden border border-gray-700">
      <video
        ref={videoRef}
        className="w-full h-full object-cover"
        controls
        playsInline
        muted
        autoPlay={isLive}
      />
      
      {/* Loading Overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
          <div className="text-center text-white">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
            <div>Loading stream...</div>
          </div>
        </div>
      )}

      {/* Error Overlay */}
      {hasError && (
        <div className="absolute inset-0 bg-black/80 flex items-center justify-center">
          <div className="text-center text-white">
            <div className="text-4xl mb-4">⚠️</div>
            <div className="text-xl mb-2">Stream Error</div>
            <div className="text-sm text-gray-400 mb-4">
              Unable to load the stream. Please try refreshing the page.
            </div>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
            >
              Refresh Page
            </button>
          </div>
        </div>
      )}

      {/* Live Indicator */}
      {isLive && !isLoading && !hasError && (
        <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
          LIVE
        </div>
      )}

      {/* Title Overlay */}
      {title && !isLoading && !hasError && (
        <div className="absolute bottom-4 left-4 bg-black/70 text-white px-3 py-2 rounded-lg">
          <div className="text-sm font-semibold">{title}</div>
        </div>
      )}
    </div>
  );
}