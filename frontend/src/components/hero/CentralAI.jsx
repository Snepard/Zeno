import React from 'react';
import { motion } from 'framer-motion';
import { BrainCircuit } from 'lucide-react';

const CentralAI = () => {
    return (
        <div className="relative flex items-center justify-center w-[300px] h-[300px] z-10 opacity-70">
            {/* Pulsing outer rings */}
            <motion.div
                className="absolute inset-0 rounded-full border border-indigo-500/20"
                animate={{ scale: [1, 1.4, 1], opacity: [0.2, 0, 0.2] }}
                transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
            />
            <motion.div
                className="absolute inset-6 rounded-full border border-purple-500/30"
                animate={{ scale: [1, 1.25, 1], opacity: [0.4, 0.1, 0.4] }}
                transition={{ duration: 3.5, repeat: Infinity, ease: 'easeInOut', delay: 0.5 }}
            />
            
            {/* Rotating dashed ring */}
            <motion.div
                className="absolute inset-12 rounded-full border-[1.5px] border-dashed border-cyan-500/40"
                animate={{ rotate: 360 }}
                transition={{ duration: 25, repeat: Infinity, ease: 'linear' }}
            />

            {/* Core Orb Container */}
            <motion.div 
                className="absolute inset-16 bg-gradient-to-br from-indigo-700/50 to-purple-900/50 backdrop-blur-md rounded-full shadow-[0_0_50px_rgba(79,70,229,0.6)] border border-white/20 flex items-center justify-center"
                animate={{ y: [0, -15, 0] }}
                transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
            >
                {/* Inner bright core */}
                <div className="absolute inset-2 bg-gradient-to-tr from-cyan-400/40 via-indigo-500/60 to-purple-500/40 rounded-full blur-md" />
                
                {/* Lucide Brain Icon representing the AI Core */}
                <BrainCircuit className="w-16 h-16 text-white z-10 drop-shadow-[0_0_15px_rgba(255,255,255,0.9)]" strokeWidth={1.5} />
            </motion.div>
        </div>
    );
};

export default CentralAI;
