import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="h-full w-full flex items-center justify-center bg-[#F8FAFF]">
      <Loader2 className="h-10 w-10 animate-spin text-indigo-600" />
    </div>
  );
};

export default LoadingSpinner;
