import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

const steps = [
  {
    title: 'Upload Course PDF',
    description: 'Select your study material and securely upload it right into the platform.',
  },
  {
    title: 'Content Ingestion',
    description: 'Our backend breaks down your PDF into perfectly sized knowledge chunks.',
  },
  {
    title: 'AI Synthesis',
    description: 'The AI model synthesizes the chunks into interactive lectures or podcasts.',
  },
  {
    title: 'Start Learning',
    description: 'Immerse yourself in interactive slides or immersive auditory learning.',
  },
];

const Chunk = ({ x, y, r, scale, opacity, quad }) => {
  return (
    <motion.div 
      style={{ x, y, rotate: r, scale, opacity }} 
      className="absolute z-10"
    >
      <motion.div 
        animate={{ y: [0, quad === 'tl' || quad === 'bl' ? -5 : 5, 0] }} 
        transition={{ duration: 3.2, repeat: Infinity, ease: "easeInOut" }}
        className={`w-[48px] h-[64px] bg-white/95 backdrop-blur-sm border border-gray-200 overflow-hidden flex flex-col items-center justify-center shadow-2xl
          ${quad === 'tl' ? 'rounded-tl-lg shadow-[-20px_-20px_30px_rgba(34,211,238,0.3)] items-end justify-end p-2' : ''}
          ${quad === 'tr' ? 'rounded-tr-lg shadow-[20px_-20px_30px_rgba(34,211,238,0.3)] items-start justify-end p-2' : ''}
          ${quad === 'bl' ? 'rounded-bl-lg shadow-[-20px_20px_30px_rgba(34,211,238,0.3)] items-end justify-start p-2' : ''}
          ${quad === 'br' ? 'rounded-br-lg shadow-[20px_20px_30px_rgba(34,211,238,0.3)] items-start justify-start p-2' : ''}
        `}
      >
        <div className="w-[80%] h-[3px] bg-gray-400 rounded mb-1 opacity-60"></div>
        <div className="w-[60%] h-[3px] bg-gray-400 rounded mb-1 opacity-60"></div>
        <div className="w-[100%] h-[3px] bg-gray-400 rounded opacity-60"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/20 to-purple-500/10 mix-blend-overlay"></div>
      </motion.div>
    </motion.div>
  );
};

const HowItWorksScroller = () => {
  const containerRef = useRef(null);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  // Text Opacities (Synced purely with exact animation holds)
  const o1 = useTransform(scrollYProgress, [0, 0.2, 0.23, 0.25], [1, 1, 0.3, 0.3]);
  const o2 = useTransform(scrollYProgress, [0.2, 0.25, 0.32, 0.40], [0.3, 1, 1, 0.3]);
  const o3 = useTransform(scrollYProgress, [0.32, 0.40, 0.58, 0.65], [0.3, 1, 1, 0.3]);
  const o4 = useTransform(scrollYProgress, [0.58, 0.65, 1], [0.3, 1, 1]);
  const textOpacities = [o1, o2, o3, o4];

  // The active line will stall securely while animations resolve
  const progressLineHeight = useTransform(
     scrollYProgress, 
     [0.0, 0.20, 0.25, 0.32, 0.40, 0.58, 0.65, 1.0], 
     ["0%", "0%", "33.3%", "33.3%", "66.6%", "66.6%", "100%", "100%"]
  );

  // --- SCENE 1: UPLOAD ---
  // PDF waits at (-180, -100) until the cursor grabs it at 0.08, then they move to the laptop center (0, -10)
  const pdfX = useTransform(scrollYProgress, [0, 0.08, 0.2], [-180, -180, 0]);
  const pdfY = useTransform(scrollYProgress, [0, 0.08, 0.2], [-100, -100, -10]);
  const pdfScale = useTransform(scrollYProgress, [0, 0.08, 0.2], [1, 1, 0.4]);
  const pdfOpacity = useTransform(scrollYProgress, [0, 0.05, 0.18, 0.2], [0, 1, 1, 0]);
  const pdfRotate = useTransform(scrollYProgress, [0, 0.08, 0.2], [-10, -10, 0]);

  // Cursor flies in from bottom, lands exactly on PDF at 0.08 (with +20 offset), and firmly moves it into laptop
  const cursorX = useTransform(scrollYProgress, [0, 0.08, 0.2], [-250, -160, 20]);
  const cursorY = useTransform(scrollYProgress, [0, 0.08, 0.2], [150, -80, 10]);
  const cursorOpacity = useTransform(scrollYProgress, [0, 0.05, 0.18, 0.2], [0, 1, 1, 0]);
  const cursorScale = useTransform(scrollYProgress, [0, 0.06, 0.08, 0.2], [1.5, 1.2, 0.8, 0.8]);
  
  const laptopScale = useTransform(scrollYProgress, [0, 0.2, 0.25, 0.3], [0.8, 1, 3.5, 3.5]); 
  const laptopY = useTransform(scrollYProgress, [0, 0.2, 0.25, 0.3], [100, 0, 50, 50]);
  const laptopOpacity = useTransform(scrollYProgress, [0, 0.25, 0.28, 0.3], [1, 1, 0, 0]);

  // --- SCENE 2: INGESTION ---
  const vPdfScale = useTransform(scrollYProgress, [0.22, 0.25, 0.28], [0.5, 1.2, 1.5]);
  const vPdfOpacity = useTransform(scrollYProgress, [0.22, 0.25, 0.279, 0.28], [0, 1, 1, 0]);

  const flashOpacity = useTransform(scrollYProgress, [0.27, 0.28, 0.32], [0, 1, 0]);
  const flashScale = useTransform(scrollYProgress, [0.27, 0.32], [0, 10]);

  const chunkScaleDynamic = useTransform(scrollYProgress, [0.28, 0.35], [1.5, 1.2]);
  const chunkOpacity = useTransform(scrollYProgress, [0.27, 0.28, 0.45, 0.48], [0, 1, 1, 0]);

  const c1X = useTransform(scrollYProgress, [0.28, 0.35], [-24, -200]);
  const c1Y = useTransform(scrollYProgress, [0.28, 0.35], [-32, -140]);
  const c1R = useTransform(scrollYProgress, [0.28, 0.45], [0, -65]);

  const c2X = useTransform(scrollYProgress, [0.28, 0.35], [24, 200]);
  const c2Y = useTransform(scrollYProgress, [0.28, 0.35], [-32, -100]);
  const c2R = useTransform(scrollYProgress, [0.28, 0.45], [0, 75]);

  const c3X = useTransform(scrollYProgress, [0.28, 0.35], [-24, -180]);
  const c3Y = useTransform(scrollYProgress, [0.28, 0.35], [32, 150]);
  const c3R = useTransform(scrollYProgress, [0.28, 0.45], [0, -45]);

  const c4X = useTransform(scrollYProgress, [0.28, 0.35], [24, 180]);
  const c4Y = useTransform(scrollYProgress, [0.28, 0.35], [32, 170]);
  const c4R = useTransform(scrollYProgress, [0.28, 0.45], [0, 105]);

  const beamY = useTransform(scrollYProgress, [0.35, 0.45], [-280, 280]);
  const beamOpacity = useTransform(scrollYProgress, [0.34, 0.36, 0.46, 0.47], [0, 1, 1, 0]);

  // --- SCENE 3: AI SYNTHESIS ---
  const coreScale = useTransform(scrollYProgress, [0.45, 0.52], [0, 1]);
  const coreOpacity = useTransform(scrollYProgress, [0.45, 0.5, 0.62, 0.68], [0, 1, 1, 0]);
  const cardsOpacity = useTransform(scrollYProgress, [0.52, 0.58], [0, 1]);
  const wrapperOrbitScale = useTransform(scrollYProgress, [0.5, 0.6, 0.65, 0.72], [0, 1, 1, 0.85]);
  
  // --- SCENE 4: LEARNING EXPERIENCE ---
  const studentScale = useTransform(scrollYProgress, [0.65, 0.72], [0.4, 1]);
  const studentY = useTransform(scrollYProgress, [0.65, 0.72], [80, 0]);
  const studentOpacity = useTransform(scrollYProgress, [0.65, 0.72], [0, 1]);

  const orbitRotation = useTransform(scrollYProgress, [0.68, 1], [0, 180]);
  const counterOrbitRotation = useTransform(scrollYProgress, [0.68, 1], [0, -180]);

  return (
    <div ref={containerRef} className="relative h-[400vh] bg-transparent text-white">
      <div className="sticky top-0 h-screen w-full flex items-center justify-center overflow-hidden">
        
        {/* Background Glow */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0B0A10]/50 to-transparent pointer-events-none z-0"></div>

        <div className="container mx-auto px-6 max-w-7xl relative z-10 w-full h-full flex flex-col md:flex-row items-center pt-24 pb-12">
          
          {/* Left Text Sequence */}
          <div className="w-full md:w-[45%] h-full flex flex-col justify-center relative">
            
            <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-12 leading-tight ml-0 md:ml-16 drop-shadow-lg">
               The Journey of <br/> <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-200">Your Document</span>
            </h2>

            {/* Flex container enforcing fixed height to reliably calculate timeline percentages */}
            <div className="flex flex-col h-[500px] w-full max-w-md ml-0 md:ml-16 relative">
              
              {/* Progress Line Track Container (Exactly 3x 125px = 375px spanning node 1 to node 4 perfectly) */}
              <div className="absolute left-[-35px] top-[36px] h-[375px] w-[2px] hidden md:block z-0">
                 {/* Active Progress Line */}
                 <motion.div 
                    style={{ height: progressLineHeight }} 
                    className="w-full bg-gradient-to-b from-purple-400 to-purple-200 shadow-[0_0_15px_rgba(168,85,247,0.8)] origin-top rounded-full"
                 ></motion.div>
              </div>

              {steps.map((step, index) => (
                <div 
                  key={index} 
                  className="relative flex-1 flex flex-col justify-start transition-all duration-300"
                >
                  <div className="flex items-center mb-3">
                    {/* Permanently Opaque Desktop Sphere Wrapper */}
                    <div className="absolute -left-[54px] top-4 flex h-10 w-10 items-center justify-center rounded-full bg-[#0a0a0f] border-2 border-slate-700 z-10 hidden md:flex">
                      <motion.span style={{ opacity: textOpacities[index] }} className="text-cyan-300 font-bold shadow-[0_0_20px_rgba(34,211,238,0.3)]">
                        {index + 1}
                      </motion.span>
                    </div>
                    
                    {/* Permanently Opaque Mobile Sphere Wrapper */}
                    <div className="flex md:hidden h-8 w-8 items-center justify-center rounded-full bg-[#0a0a0f] border border-cyan-400/50 z-10 mr-3 text-sm">
                      <motion.span style={{ opacity: textOpacities[index] }} className="text-cyan-300 font-bold shadow-[0_0_15px_rgba(34,211,238,0.3)]">
                        {index + 1}
                      </motion.span>
                    </div>
                    
                    <motion.h3 style={{ opacity: textOpacities[index] }} className="text-xl md:text-2xl font-bold text-white tracking-wide">
                      {step.title}
                    </motion.h3>
                  </div>
                  <motion.p style={{ opacity: textOpacities[index] }} className="text-[15px] text-gray-400 leading-relaxed max-w-[320px]">
                    {step.description}
                  </motion.p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Animation Sandbox */}
          <div className="w-full md:w-[55%] h-[60vh] md:h-full relative flex items-center justify-center perspective-[1000px]">
            {/* The Stage */}
            <div className="relative w-full max-w-[500px] aspect-square flex items-center justify-center transform-style-3d">
              
              {/* SCENE 1: Laptop */}
              <motion.div style={{ scale: laptopScale, y: laptopY, opacity: laptopOpacity }} className="absolute z-10 flex flex-col items-center">
                <motion.div animate={{ y: [0, -6, 0] }} transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }} className="flex flex-col items-center">
                  <div className="w-64 h-40 bg-[#0f0e15] border-[6px] border-[#25252d] rounded-t-xl rounded-b shadow-[0_20px_50px_rgba(0,0,0,0.8)] relative overflow-hidden flex items-center justify-center perspective-[500px]">
                     <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-cyan-600/20 to-transparent"></div>
                     <div className="w-20 h-20 rounded-full bg-cyan-500/30 blur-2xl"></div>
                     <div className="absolute top-2 left-2 flex gap-1">
                        <div className="w-1.5 h-1.5 rounded-full bg-red-400"></div>
                        <div className="w-1.5 h-1.5 rounded-full bg-yellow-400"></div>
                        <div className="w-1.5 h-1.5 rounded-full bg-green-400"></div>
                     </div>
                     <div className="absolute top-6 inset-x-4 bottom-4 bg-white/5 border border-white/10 rounded overflow-hidden p-2 flex flex-col gap-1.5">
                        <div className="w-1/3 h-2 bg-white/10 rounded"></div>
                        <div className="w-full h-8 bg-white/5 rounded"></div>
                        <div className="w-3/4 h-2 bg-white/10 rounded"></div>
                     </div>
                  </div>
                  <div className="w-72 h-4 bg-[#4a4a55] rounded-b-xl relative flex justify-center shadow-2xl">
                     <div className="absolute w-12 h-1 bg-gray-400 rounded-b-xl"></div>
                  </div>
                </motion.div>
              </motion.div>

              {/* SCENE 1: External PDF */}
              <motion.div 
                style={{ x: pdfX, y: pdfY, scale: pdfScale, opacity: pdfOpacity, rotate: pdfRotate }} 
                className="absolute z-20 pointer-events-none"
              >
                <motion.div animate={{ y: [0, -4, 0] }} transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut" }} className="w-24 h-32 bg-white/95 backdrop-blur-sm border border-gray-200 rounded-lg shadow-[0_30px_60px_rgba(0,0,0,0.5)] flex flex-col items-center p-3">
                   <div className="w-10 h-12 bg-red-500 rounded text-sm font-black tracking-wider flex items-center justify-center text-white mb-3 shadow-[0_4px_10px_rgba(239,68,68,0.5)]">PDF</div>
                <div className="w-full h-[3px] bg-gray-300 rounded mb-1.5"></div>
                <div className="w-3/4 h-[3px] bg-gray-300 rounded mb-1.5 self-start"></div>
                <div className="w-full h-[3px] bg-gray-300 rounded mb-1.5"></div>
                <div className="w-5/6 h-[3px] bg-gray-300 rounded self-start"></div>
              </motion.div>
              </motion.div>

              {/* SCENE 1: Cursor */}
              <motion.div 
                style={{ x: cursorX, y: cursorY, opacity: cursorOpacity, scale: cursorScale }} 
                className="absolute z-30"
              >
                <svg width="40" height="40" viewBox="0 0 24 24" fill="white" className="drop-shadow-[0_10px_10px_rgba(0,0,0,0.5)] text-[#1f2937] origin-top-left">
                  <path d="M10.5 4.5A2.5 2.5 0 0 1 13 7v3.54a1.5 1.5 0 0 1 3 0V11a2.5 2.5 0 0 1 5 0v3.5a8.5 8.5 0 1 1-17 0V7a2.5 2.5 0 0 1 2.5-2.5h0zM8 7v7.5a6.5 6.5 0 1 0 13 0V11a.5.5 0 0 0-1 0v3.54a1.5 1.5 0 0 1-3 0V7.5a.5.5 0 0 0-1 0v3.54a1.5 1.5 0 0 1-3 0V7a.5.5 0 0 0-1 0v3.54a1.5 1.5 0 0 1-3 0V7a.5.5 0 0 0-1 0h0z" stroke="currentColor" strokeWidth="1"/>
                </svg>
              </motion.div>

              {/* SCENE 2: Virtual PDF (inside laptop) */}
              <motion.div 
                style={{ scale: vPdfScale, opacity: vPdfOpacity }} 
                className="absolute z-20 pointer-events-none"
              >
                <motion.div animate={{ y: [0, -4, 0] }} transition={{ duration: 3.2, repeat: Infinity, ease: "easeInOut" }} className="w-[96px] h-[128px] bg-white border border-gray-200 rounded-lg shadow-[0_30px_60px_rgba(0,0,0,0.5)] flex flex-col items-center p-3">
                   <div className="w-12 h-14 bg-red-500 rounded text-sm font-black tracking-wider flex items-center justify-center text-white mb-3 shadow-[0_4px_10px_rgba(239,68,68,0.5)]">PDF</div>
                <div className="w-full h-[4px] bg-gray-300 rounded mb-2"></div>
                <div className="w-3/4 h-[4px] bg-gray-300 rounded mb-2 self-start"></div>
                <div className="w-full h-[4px] bg-gray-300 rounded mb-2"></div>
                <div className="w-5/6 h-[4px] bg-gray-300 rounded self-start"></div>
              </motion.div>
              </motion.div>

              {/* SCENE 2: Fragmentation Burst Flash */}
              <motion.div style={{ opacity: flashOpacity, scale: flashScale }} className="absolute z-30 w-32 h-32 bg-cyan-200 rounded-full mix-blend-screen blur-2xl pointer-events-none"></motion.div>

              {/* SCENE 2: Chunks (The Burst) */}
              <Chunk x={c1X} y={c1Y} r={c1R} scale={chunkScaleDynamic} opacity={chunkOpacity} quad="tl" />
              <Chunk x={c2X} y={c2Y} r={c2R} scale={chunkScaleDynamic} opacity={chunkOpacity} quad="tr" />
              <Chunk x={c3X} y={c3Y} r={c3R} scale={chunkScaleDynamic} opacity={chunkOpacity} quad="bl" />
              <Chunk x={c4X} y={c4Y} r={c4R} scale={chunkScaleDynamic} opacity={chunkOpacity} quad="br" />

              {/* SCENE 3: Realistic Scanner Beam */}
              <motion.div style={{ y: beamY, opacity: beamOpacity }} className="absolute z-40 w-[160%] h-[250px] left-[-30%] pointer-events-none flex flex-col justify-end">
                 {/* Main volumetric light body (fades sharply at top and edges, dense at bottom) */}
                 <div className="absolute bottom-0 w-full h-full bg-[radial-gradient(ellipse_at_bottom,rgba(34,211,238,0.12),transparent_70%)] mix-blend-screen"></div>
                 
                 {/* Secondary core color shift (purple tint in the center) */}
                 <div className="absolute bottom-[2px] w-full h-[120px] bg-[radial-gradient(ellipse_at_bottom,rgba(168,85,247,0.25),transparent_60%)] mix-blend-screen"></div>
                 
                 {/* The Laser Origin Line */}
                 <div className="relative w-full flex justify-center items-center">
                    {/* Broad cyan ambient ground flare */}
                    <div className="absolute w-[100%] h-[4px] bg-cyan-500 blur-[15px] opacity-80"></div>
                    {/* Dense purple/cyan optical flare core */}
                    <div className="absolute w-[80%] h-[2px] bg-purple-400 blur-[4px] opacity-90"></div>
                    {/* Pure white cutting laser */}
                    <div className="relative w-[65%] h-[1px] bg-white brightness-150 shadow-[0_0_10px_2px_rgba(34,211,238,0.9),0_0_20px_5px_rgba(168,85,247,0.7)] rounded-full"></div>
                 </div>
              </motion.div>

              {/* SCENE 3: AI Core Sphere */}
              <motion.div style={{ scale: coreScale, opacity: coreOpacity }} className="absolute z-10 flex items-center justify-center pointer-events-none">
                 <motion.div animate={{ y: [0, -8, 0] }} transition={{ duration: 4.8, repeat: Infinity, ease: "easeInOut" }} className="relative w-40 h-40 bg-white rounded-full shadow-[0_0_80px_#a855f7,inset_0_0_20px_#fff,0_0_120px_#22d3ee] flex items-center justify-center">
                     {/* Orbiting wireframe nets */}
                     <motion.div animate={{ rotateX: 60, rotateZ: 360 }} transition={{ rotateZ: { repeat: Infinity, duration: 8, ease: "linear" } }} className="absolute w-[160%] h-[160%] border-[2px] border-cyan-400/40 rounded-full" />
                     <motion.div animate={{ rotateX: 60, rotateY: 45, rotateZ: -360 }} transition={{ rotateZ: { repeat: Infinity, duration: 12, ease: "linear" } }} className="absolute w-[160%] h-[160%] border-[2px] border-purple-400/40 rounded-full" />
                     <motion.div animate={{ rotateZ: 360 }} transition={{ repeat: Infinity, duration: 20, ease: "linear" }} className="absolute w-[140%] h-[140%] border border-white/20 rounded-[40%_60%_70%_30%] mix-blend-overlay" />

                     {/* Glowing Particles */}
                     <div className="absolute -top-10 left-10 w-2 h-2 bg-white rounded-full animate-ping shadow-[0_0_10px_white]"></div>
                     <div className="absolute bottom-5 -right-8 w-1 h-1 bg-white rounded-full animate-ping shadow-[0_0_10px_white]"></div>
                     <div className="absolute top-1/2 -left-12 w-2 h-2 bg-cyan-200 rounded-full animate-ping shadow-[0_0_10px_cyan]" style={{ animationDelay: '0.4s' }}></div>

                     {/* AI Badge Center */}
                     <div className="relative z-20 w-[72px] h-[72px] bg-[#0f0e15]/70 backdrop-blur-lg rounded-2xl border-[3px] border-[#22d3ee] shadow-[0_0_30px_rgba(34,211,238,0.8),inset_0_0_15px_rgba(34,211,238,0.5)] flex items-center justify-center">
                         <span className="text-3xl tracking-wider font-black text-white drop-shadow-[0_0_15px_rgba(34,211,238,1)]">AI</span>
                     </div>
                 </motion.div>
              </motion.div>

              {/* SCENE 4: Student (Minimalist, Clean Edition) */}
              <motion.div style={{ scale: studentScale, y: studentY, opacity: studentOpacity }} className="absolute z-10 flex flex-col items-center justify-end w-full h-[360px] pb-[10px] drop-shadow-[0_15px_30px_rgba(0,0,0,0.5)] pointer-events-none">
                  
                  {/* Clean Desk Container */ }
                  <div className="absolute bottom-0 w-[500px] h-4 bg-slate-800 rounded-full shadow-[0_10px_20px_rgba(0,0,0,0.6)] z-0 overflow-hidden flex justify-center border-t border-slate-600"></div>

                  <div className="relative flex flex-col items-center z-10 w-full">
                     {/* Subtle Breathing/Studying Animation Wrapper */}
                     <motion.div 
                        animate={{ y: [0, -4, 0] }} 
                        transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }}
                        className="relative flex flex-col items-center w-full transform -translate-y-2"
                     >
                         {/* Head / Hair */}
                         <div className="relative z-20 w-28 h-32">
                            {/* Back Hair */}
                            <div className="absolute inset-x-0 top-0 bottom-0 bg-[#1e293b] rounded-t-[60px] rounded-b-xl shadow-inner z-10"></div>
                            
                            {/* Face */}
                            <div className="absolute top-6 left-4 right-4 bottom-8 bg-[#fde68a] rounded-[35px] overflow-hidden shadow-[inset_0_-5px_10px_rgba(0,0,0,0.2)] z-20">
                               {/* Soft Screen Reflection */}
                               <div className="absolute bottom-0 inset-x-0 h-1/2 bg-white/20 blur-md"></div>
                            </div>
                            
                            {/* Bangs */}
                            <div className="absolute -top-1 -left-1 -right-1 h-14 bg-[#1e293b] rounded-t-[60px] rounded-b-[20px] shadow-[0_4px_6px_rgba(0,0,0,0.2)] z-20"></div>
                            <div className="absolute top-10 right-0 w-8 h-12 bg-[#1e293b] rounded-bl-[15px] rounded-br-[10px] z-20"></div>
                            
                            {/* Clean Modern Headphones */}
                            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 w-[116px] h-[70px] border-t-[8px] border-[#94a3b8] rounded-t-full z-30 drop-shadow-sm"></div>
                            <div className="absolute top-10 -left-4 w-7 h-14 bg-[#334155] border-2 border-[#475569] rounded-full z-30 shadow-md"></div>
                            <div className="absolute top-10 -right-4 w-7 h-14 bg-[#334155] border-2 border-[#475569] rounded-full z-30 shadow-md"></div>
                         </div>
                         
                         {/* Neck */}
                         <div className="relative z-10 w-8 h-10 bg-[#f59e0b] -mt-2 rounded-b-xl shadow-[inset_0_-8px_10px_rgba(0,0,0,0.3)]"></div>

                         {/* Minimalist Sweater Torso */}
                         <div className="relative z-10 w-44 h-40 bg-[#4f46e5] rounded-t-[55px] rounded-b-xl overflow-hidden shadow-lg flex justify-center -mt-6">
                            {/* Shirt Collar */}
                            <div className="absolute top-0 w-12 h-14 bg-[#f8fafc] rounded-b-full shadow-[inset_0_10px_10px_rgba(0,0,0,0.2)]"></div>
                            <div className="absolute top-0 w-16 h-8 border-b-[4px] border-indigo-300 rounded-b-full"></div>
                            
                            {/* Relaxed Arms */}
                            <div className="absolute top-12 -left-3 w-16 h-40 bg-[#3730a3] rounded-full rotate-[12deg] shadow-[-2px_0_10px_rgba(0,0,0,0.2)]"></div>
                            <div className="absolute top-12 -right-3 w-16 h-40 bg-[#3730a3] rounded-full -rotate-[12deg] shadow-[2px_0_10px_rgba(0,0,0,0.2)]"></div>
                         </div>
                     </motion.div>
                     
                     {/* Clean Modern Hardware Set */}
                     <div className="absolute bottom-3 z-40 w-full flex flex-col items-center pointer-events-none" style={{ perspective: '800px' }}>
                        
                        {/* Sleek Glass Display Panel */}
                        <div className="relative z-50 w-56 h-32 bg-white/5 backdrop-blur-md rounded-xl border border-white/20 transform -rotateX-[5deg] origin-bottom mb-[-10px] flex items-center justify-center p-2 shadow-[0_-10px_30px_rgba(255,255,255,0.05)]">
                           {/* Interface Data */}
                           <div className="w-full h-full border border-white/10 rounded-lg flex flex-col gap-2 p-3 bg-slate-900/40">
                              <div className="w-1/2 h-2 bg-white/50 rounded"></div>
                              <div className="w-full flex-1 flex items-end gap-2 opacity-70">
                                 <div className="flex-1 h-[30%] bg-indigo-400 rounded-t"></div>
                                 <div className="flex-1 h-[60%] bg-indigo-400 rounded-t"></div>
                                 <div className="flex-1 h-[80%] bg-indigo-400 rounded-t"></div>
                                 <div className="flex-1 h-[50%] bg-purple-400 rounded-t"></div>
                                 <div className="flex-1 h-[70%] bg-purple-400 rounded-t"></div>
                              </div>
                           </div>
                        </div>

                        {/* Minimalist Base/Keyboard */}
                        <div className="w-[300px] h-16 bg-[#1e293b] border-t-2 border-slate-500 rounded-b-2xl rounded-t-sm shadow-[0_-5px_15px_rgba(0,0,0,0.5)] flex justify-center items-start transform rotateX-[45deg] origin-bottom p-2 relative z-40">
                           <div className="w-52 h-[80%] border border-slate-600 rounded bg-[#0f172a] opacity-80 flex justify-center items-center p-1">
                               <div className="w-full h-full bg-slate-700/50 rounded-sm"></div>
                           </div>
                        </div>
                     </div>
                  </div>
              </motion.div>

              {/* SCENE 3 & 4: Cards Orbit wrapper */}
              <motion.div style={{ scale: wrapperOrbitScale, rotate: orbitRotation, opacity: cardsOpacity }} className="absolute z-20 w-[490px] h-[490px] md:w-[620px] md:h-[620px] flex items-center justify-center pointer-events-none">
                  {/* PPT Card */}
                  <div className="absolute left-0 transform -translate-x-1/2">
                     <motion.div style={{ rotate: counterOrbitRotation }}>
                        <motion.div animate={{ y: [0, -5, 0] }} transition={{ duration: 3.8, repeat: Infinity, ease: "easeInOut" }} className="w-36 h-28 md:w-44 md:h-32 bg-[#1e1e24]/80 backdrop-blur-2xl border border-white/10 rounded-2xl shadow-[0_20px_40px_rgba(0,0,0,0.6)] p-3 md:p-4 flex flex-col justify-between overflow-hidden relative">
                           <div className="absolute -right-4 -top-4 w-20 h-20 bg-cyan-500/20 blur-2xl rounded-full"></div>
                           <div className="flex items-center gap-3 mb-2 relative z-10">
                               <div className="w-5 h-5 md:w-6 md:h-6 rounded-full bg-gradient-to-tr from-purple-400 to-purple-300 flex items-center justify-center border border-white/20">
                                 <div className="w-2 h-2 bg-white rounded-full"></div>
                               </div>
                               <div className="space-y-1.5 flex-1">
                                  <div className="w-full bg-white/20 rounded h-1.5"></div>
                                  <div className="w-2/3 bg-white/10 rounded h-1.5"></div>
                               </div>
                           </div>
                           <div className="w-full h-10 md:h-12 bg-white/5 border border-white/10 rounded-lg relative z-10 flex gap-1 p-1">
                               <div className="w-1/2 h-full bg-indigo-500/20 rounded"></div>
                               <div className="w-1/2 h-full bg-cyan-500/20 rounded"></div>
                           </div>
                        </motion.div>
                     </motion.div>
                  </div>
                  
                  {/* Podcast Card */}
                  <div className="absolute right-0 transform translate-x-1/2">
                     <motion.div style={{ rotate: counterOrbitRotation }}>
                        <motion.div animate={{ y: [0, 5, 0] }} transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut" }} className="w-36 h-28 md:w-44 md:h-32 bg-[#141419]/90 backdrop-blur-2xl border border-cyan-500/30 rounded-2xl shadow-[0_20px_40px_rgba(0,0,0,0.6)] p-3 md:p-4 flex flex-col items-center justify-between relative overflow-hidden">
                           <div className="absolute -left-4 -bottom-4 w-20 h-20 bg-indigo-500/20 blur-2xl rounded-full"></div>
                           <div className="w-full flex justify-between items-center relative z-10 opacity-70">
                              <div className="text-[9px] md:text-[10px] font-bold text-gray-400">EP 1: YOUR PDF</div>
                              <div className="w-3 h-3 md:w-4 md:h-4 rounded-full bg-indigo-500 flex items-center justify-center pl-0.5">
                                 <div className="w-0 h-0 border-t-[2px] md:border-t-[3px] border-t-transparent border-l-[3px] md:border-l-[4px] border-l-white border-b-[2px] md:border-b-[3px] border-b-transparent"></div>
                              </div>
                           </div>
                           <div className="flex gap-1.5 items-end h-6 md:h-8 relative z-10">
                               <div className="w-1 md:w-1.5 h-2 md:h-3 bg-cyan-400 rounded-t animate-[bounce_1s_infinite]"></div>
                               <div className="w-1 md:w-1.5 h-6 md:h-8 bg-purple-400 rounded-t animate-[bounce_1.2s_infinite]"></div>
                               <div className="w-1 md:w-1.5 h-4 md:h-5 bg-cyan-400 rounded-t animate-[bounce_0.8s_infinite]"></div>
                               <div className="w-1 md:w-1.5 h-5 md:h-7 bg-purple-400 rounded-t animate-[bounce_1.1s_infinite]"></div>
                               <div className="w-1 md:w-1.5 h-3 md:h-4 bg-cyan-400 rounded-t animate-[bounce_0.9s_infinite]"></div>
                           </div>
                           <div className="flex relative z-10 w-full justify-center mt-1 md:mt-2">
                              <div className="w-6 h-6 md:w-7 md:h-7 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 border-2 border-[#141419] z-20 flex items-center justify-center"><div className="w-1.5 h-1.5 md:w-2 md:h-2 bg-[#0B0A10] rounded-full"></div></div>
                              <div className="w-6 h-6 md:w-7 md:h-7 rounded-full bg-gradient-to-br from-purple-300 to-purple-500 border-2 border-[#141419] z-10 -ml-2 flex items-center justify-center"><div className="w-1.5 h-1.5 md:w-2 md:h-2 bg-[#0B0A10] rounded-full"></div></div>
                           </div>
                        </motion.div>
                     </motion.div>
                  </div>
              </motion.div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowItWorksScroller;
