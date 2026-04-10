import React, { useRef, Suspense } from 'react';
import { motion, useMotionValue, useScroll, useTransform } from 'framer-motion';
import { Link } from 'react-router-dom';
import NetworkBackground from './NetworkBackground';
import CentralAI from './CentralAI';
import FloatingElement from './FloatingElement';
import { FileText, BarChart3, MessageSquareText, Layers, Network, BookOpen } from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import { Environment, Float } from '@react-three/drei';
import { Ziva } from '../Ziva';

const AnimatedHero = () => {
    const containerRef = useRef(null);
    const mouseX = useMotionValue(0.5); // 0 to 1
    const mouseY = useMotionValue(0.5);

    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end start"]
    });

    const yText = useTransform(scrollYProgress, [0, 1], [0, 300]);
    const opacityText = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

    const yZiva = useTransform(scrollYProgress, [0, 1], [0, 150]);
    const opacityZiva = useTransform(scrollYProgress, [0, 0.9], [1, 0]);

    const yBg = useTransform(scrollYProgress, [0, 1], [0, 200]);
    const opacityBg = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

    const handleMouseMove = (e) => {
        if (!containerRef.current) return;
        const rect = containerRef.current.getBoundingClientRect();

        // Calculate normalized mouse position (0 to 1)
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;

        mouseX.set(x);
        mouseY.set(y);
    };

    return (
        <div
            ref={containerRef}
            onMouseMove={handleMouseMove}
            onMouseLeave={() => { mouseX.set(0.5); mouseY.set(0.5); }}
            className="relative w-full h-screen min-h-[800px] flex overflow-hidden"
        >
            <NetworkBackground />

            <div className="flex w-full h-full relative z-20">
                {/* Central Element & Floating Orbit - Spans entire screen behind text and Ziva */}
                <motion.div
                    style={{ y: yBg, opacity: opacityBg, willChange: 'transform, opacity' }}
                    className="absolute inset-0 flex items-center justify-center z-10 pointer-events-none"
                >
                    <div className="relative w-full h-full max-w-[1600px] flex items-center justify-center">

                        {/* Slowly gliding Central AI Core */}
                        <motion.div
                            className="absolute"
                            animate={{
                                x: [0, 80, -60, 100, -80, 0],
                                y: [0, -70, 50, 40, -90, 0],
                            }}
                            transition={{
                                duration: 45,
                                ease: "easeInOut",
                                repeat: Infinity,
                            }}
                        >
                            <CentralAI />
                        </motion.div>

                        {/* Floating Elements Collection */}
                        <div className="absolute inset-0 pointer-events-auto">
                            {/* Top Left */}
                            <FloatingElement x="16%" y="15%" depth={1.2} delay={0} mouseX={mouseX} mouseY={mouseY} className="hidden sm:block">
                                <FileText className="w-8 h-8 text-cyan-400" />
                                <span className="text-xs font-semibold text-cyan-200 mt-1 hidden lg:block">Materials</span>
                            </FloatingElement>

                            {/* Mid Left */}
                            <FloatingElement x="10%" y="45%" depth={2.2} delay={1} mouseX={mouseX} mouseY={mouseY}>
                                <BarChart3 className="w-10 h-10 text-purple-400" />
                            </FloatingElement>

                            {/* Bottom Left */}
                            <FloatingElement x="24%" y="75%" depth={0.8} delay={2} mouseX={mouseX} mouseY={mouseY}>
                                <Network className="w-6 h-6 text-indigo-300" />
                            </FloatingElement>

                            {/* Top Right */}
                            <FloatingElement x="80%" y="12%" depth={1.5} delay={0.5} mouseX={mouseX} mouseY={mouseY}>
                                <MessageSquareText className="w-9 h-9 text-purple-300" />
                                <span className="text-xs font-semibold text-purple-200 mt-1 hidden lg:block">AI Tutor</span>
                            </FloatingElement>

                            {/* Mid Right */}
                            <FloatingElement x="86%" y="45%" depth={2.5} delay={1.5} mouseX={mouseX} mouseY={mouseY} className="hidden sm:block">
                                <Layers className="w-7 h-7 text-indigo-400" />
                            </FloatingElement>

                            {/* Bottom Right */}
                            <FloatingElement x="76%" y="72%" depth={1.1} delay={2.5} mouseX={mouseX} mouseY={mouseY}>
                                <BookOpen className="w-8 h-8 text-cyan-300" />
                                <span className="text-xs font-semibold text-cyan-100 mt-1 hidden lg:block">Flashcards</span>
                            </FloatingElement>
                        </div>
                    </div>
                </motion.div>

                {/* Main Foreground Layout */}
                <div className="w-full h-full flex relative z-20 container mx-auto">
                    {/* Left Side - Text Content */}
                    <div className="w-full lg:w-[60%] relative flex flex-col items-center justify-center px-6 pointer-events-none mt-[-2%] mix-blend-plus-lighter text-center lg:translate-x-28 xl:translate-x-48 transition-transform">
                        <motion.div
                            style={{ y: yText, opacity: opacityText, willChange: 'transform, opacity' }}
                            className="w-full flex flex-col items-center justify-center"
                        >
                            <motion.h1
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.8, ease: "easeOut" }}
                                className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-white tracking-tight mb-6 leading-tight max-w-2xl drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]"
                            >
                                Study Smarter. Score Higher.{' '}
                                <span className="relative inline-block mt-2 md:mt-0 xl:mt-2">
                                    <span className="relative z-10 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-200">
                                        With Zeno
                                    </span>
                                    <motion.div
                                        initial={{ scaleX: 0 }}
                                        animate={{ scaleX: 1 }}
                                        transition={{ duration: 0.8, delay: 0.5, ease: "easeOut" }}
                                        className="absolute -bottom-1 left-0 right-0 h-2.5 bg-purple-600/40 blur-sm -z-10 origin-left"
                                    />
                                </span>
                            </motion.h1>

                            <motion.p
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ duration: 0.8, delay: 0.3 }}
                                className="text-lg lg:text-xl text-indigo-100/70 max-w-xl mb-10 font-medium drop-shadow-md"
                            >
                                Upload your course material to generate beautifully interactive visual lectures or engaging dual-host podcasts instantly.
                            </motion.p>

                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.5, delay: 0.5 }}
                                className="z-30 relative pointer-events-auto"
                            >
                                <Link to="/upload">
                                    <button className="bg-white/10 backdrop-blur-md text-white font-bold py-3.5 px-8 rounded-full text-lg hover:bg-white/20 transition-all transform hover:scale-105 duration-300 shadow-[0_0_20px_rgba(147,51,234,0.4)] hover:shadow-[0_0_30px_rgba(147,51,234,0.7)] border border-white/30 flex items-center justify-center gap-3 group">
                                        Start Generating
                                        <motion.span
                                            className="group-hover:translate-x-1 transition-transform"
                                        >
                                            →
                                        </motion.span>
                                    </button>
                                </Link>
                            </motion.div>
                        </motion.div>
                    </div>

                    {/* Right Side - Ziva 3D Model */}
                    <div className="hidden lg:flex w-[40%] relative z-30 h-full pointer-events-none items-center justify-center lg:-translate-x-24 xl:-translate-x-40 transition-transform">
                        <motion.div
                            style={{ y: yZiva, opacity: opacityZiva, willChange: 'transform, opacity' }}
                            className="w-full h-full flex items-center justify-center"
                        >
                            <Canvas
                                camera={{ position: [-0.8, 0.5, 4], fov: 45 }}
                                className="w-full h-[90%]"
                                frameloop="demand"
                                shadows
                            >
                                <Suspense fallback={null}>
                                    <ambientLight intensity={0.4} />
                                    <spotLight position={[5, 10, 5]} angle={0.4} penumbra={1} intensity={1.0} castShadow />
                                    <pointLight position={[-5, 5, -5]} intensity={0.3} color="#blue" />
                                    {/* Ziva wrapped in Float to simulate subtle anti-gravity hovering */}
                                    <Float speed={1.5} rotationIntensity={0.1} floatIntensity={0.5} floatingRange={[-0.1, 0.1]}>
                                        <Ziva
                                            position={[0, -1.18, 0]}
                                            scale={1.2}
                                            rotation={[0, -Math.PI / 8, 0]}
                                            overrideAnim="greeting"
                                        />
                                    </Float>
                                    <Environment preset="city" />
                                </Suspense>
                            </Canvas>
                        </motion.div>
                    </div>
                </div>
            </div>

            {/* Bottom fading scroll gradient */}
            <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#0B0A10] to-transparent z-40 pointer-events-none" />
        </div>
    );
};

export default AnimatedHero;
