import React from 'react';

const NetworkBackground = () => {
    return (
        <div className="absolute inset-0 overflow-hidden pointer-events-none z-0 bg-[#0B0A10]">
            {/* Deep gradient background */}
            <div className="absolute inset-0 bg-gradient-to-b from-[#0B0A10] via-indigo-950/20 to-purple-900/10 mix-blend-screen" />
            
            {/* Soft subtle grid */}
            <div 
                className="absolute inset-0 opacity-[0.03]"
                style={{
                    backgroundImage: `linear-gradient(rgba(255, 255, 255, 0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.5) 1px, transparent 1px)`,
                    backgroundSize: '40px 40px'
                }}
            />

            {/* Glowing ambient orbs */}
            <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] mix-blend-screen animate-pulse" style={{ animationDuration: '8s' }} />
            <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-[150px] mix-blend-screen animate-pulse" style={{ animationDuration: '10s' }} />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-600/5 rounded-full blur-[100px] mix-blend-screen" />

            {/* Faint connecting lines abstraction using thin rotated divs or SVGs */}
            <svg className="absolute inset-0 w-full h-full opacity-[0.06]" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="networkPattern" x="0" y="0" width="200" height="200" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="2" fill="#fff" />
                        <circle cx="150" cy="80" r="1.5" fill="#fff" />
                        <circle cx="80" cy="160" r="2.5" fill="#fff" />
                        <line x1="20" y1="20" x2="150" y2="80" stroke="#fff" strokeWidth="0.5" />
                        <line x1="150" y1="80" x2="80" y2="160" stroke="#fff" strokeWidth="0.5" />
                        <line x1="80" y1="160" x2="20" y2="20" stroke="#fff" strokeWidth="0.5" />
                    </pattern>
                </defs>
                <rect x="0" y="0" width="100%" height="100%" fill="url(#networkPattern)" />
            </svg>
        </div>
    );
};

export default NetworkBackground;
