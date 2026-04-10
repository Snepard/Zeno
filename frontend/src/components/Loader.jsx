import React from 'react';

const Loader = ({ progress, message }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4 w-full h-full min-h-[300px]">
      <div className="relative w-20 h-20">
        <div className="absolute inset-0 border-4 border-zinc-800 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-indigo-500 rounded-full animate-spin border-t-transparent"></div>
      </div>
      <h3 className="text-xl font-medium text-white">{message || "Generating..."}</h3>
      <div className="w-64 h-2 bg-zinc-800 rounded-full overflow-hidden">
        <div 
            className="h-full bg-indigo-500 transition-all duration-500" 
            style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="text-zinc-400 font-mono text-sm">{progress}%</p>
    </div>
  );
};

export default Loader;
