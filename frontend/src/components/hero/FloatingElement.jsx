import React from 'react';
import { motion, useTransform, useSpring } from 'framer-motion';

const FloatingElement = ({ children, x, y, mouseX, mouseY, depth = 1, delay = 0, className = "" }) => {
    // Parallax movement ranges based on depth
    // Depth > 0 means it moves closer/faster relative to the mouse
    const movementX = useTransform(mouseX, [0, 1], [-25 * depth, 25 * depth]);
    const movementY = useTransform(mouseY, [0, 1], [-25 * depth, 25 * depth]);

    // Apply spring physics for smoother parallax tracking, so it doesn't snap instantly but drifts
    const springX = useSpring(movementX, { stiffness: 40, damping: 20 });
    const springY = useSpring(movementY, { stiffness: 40, damping: 20 });

    return (
        <motion.div
            style={{ 
                left: x, 
                top: y, 
                x: springX, 
                y: springY 
            }}
            className={`absolute z-10 ${className}`}
        >
            {/* Continuous floating animation separate from mouse parallax */}
            <motion.div
                animate={{ y: [0, -15, 0], rotate: [0, 3, -3, 0] }}
                transition={{ 
                    duration: 6 + (delay * 0.5), 
                    repeat: Infinity, 
                    ease: "easeInOut",
                    delay: delay
                }}
                className="group cursor-pointer flex flex-col items-center gap-2"
                style={{ perspective: 1000 }}
            >
                <div className="relative flex items-center justify-center p-3 sm:p-4 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.3)] hover:bg-white/10 hover:border-white/20 transition-all duration-300 group-hover:scale-105 group-hover:-translate-y-2 group-hover:shadow-[0_15px_40px_rgba(147,51,234,0.4)]">
                    {children}
                </div>
            </motion.div>
        </motion.div>
    );
};

export default FloatingElement;
