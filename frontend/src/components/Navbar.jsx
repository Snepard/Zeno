import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, History, Github } from 'lucide-react';

const Navbar = () => {
    return (
        <nav className="w-full px-8 py-5 flex items-center justify-between border-b border-zinc-800/50 bg-zinc-900/50 backdrop-blur-md sticky top-0 z-50">
            <Link to="/" className="flex items-center gap-2 group">
                <div className="w-8 h-8 rounded bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
                    <Sparkles size={16} className="text-white" />
                </div>
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
                    AI Guruji
                </span>
            </Link>
            
            <div className="flex items-center gap-6">
                <Link to="/generate" className="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Generate</Link>
                <div className="w-px h-4 bg-zinc-800"></div>
                <button className="flex items-center gap-2 px-4 py-2 bg-white text-black text-sm font-semibold rounded-full hover:bg-zinc-200 transition-colors">
                    Get Started
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
