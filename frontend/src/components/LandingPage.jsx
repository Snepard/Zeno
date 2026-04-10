import React, { useState } from 'react';
import Navbar from './Navbar';
import HowItWorksScroller from './HowItWorksScroller';
import Footer from './Footer';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { ReactLenis } from '@studio-freight/react-lenis';
import CardSwap, { Card } from './CardSwap';
import Particles from './Particles';
import AnimatedHero from './hero/AnimatedHero';
import { FaqBookScroller } from './FaqBookScroller';

// --- SVG Icons for Features ---
const FeatureIcon1 = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
    </svg>
);
const FeatureIcon2 = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
    </svg>
);
const FeatureIcon3 = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
    </svg>
);

// --- Components ---

const FeaturesSection = () => {
    const features = [
        { icon: <FeatureIcon1 />, title: 'Interactive Visual Lectures', description: 'Instantly convert PDFs into beautiful presentation slides accompanied by a virtual AI teacher explaining the concepts.' },
        { icon: <FeatureIcon3 />, title: 'Dual-Host Podcasts', description: 'Transform dry materials into an engaging, cinematic auditory experience featuring two AI hosts discussing the subject.' },
        { icon: <FeatureIcon2 />, title: 'Contextual Knowledge', description: 'Our algorithms intelligently parse and ingest your documents into contextual knowledge chunks for maximum synthesis accuracy.' },
    ];
    return (
        <section className="bg-transparent relative z-10 py-20 sm:py-24 overflow-hidden border-t border-white/5">
            <div className="container mx-auto px-6 max-w-6xl">
                <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-20">
                    {/* Left text component */}
                    <div className="lg:w-1/2 text-center lg:text-left">
                        <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-6 leading-tight">Everything You Need to <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-200">Ace Your Studies</span></h2>
                        <p className="text-xl text-gray-400 leading-relaxed">
                            Zeno combines advanced document processing with cutting-edge generative models to give you the ultimate learning advantage. Swap out dense materials for engaging multimedia formats instantly.
                        </p>
                    </div>

                    {/* Right CardSwap component */}
                    <div className="lg:w-1/2 w-full flex justify-center lg:justify-end mt-12 lg:mt-0 relative">
                        {/* Purple Glow Background behind cards */}
                        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-purple-600/40 rounded-full blur-[100px] pointer-events-none z-0"></div>

                        <div style={{ height: '500px', width: '100%', maxWidth: '500px', position: 'relative', zIndex: 10 }}>
                            <CardSwap
                                cardDistance={100}
                                verticalDistance={70}
                                delay={3000}
                                pauseOnHover={true}
                                width={320}
                                height={380}
                            >
                                {features.map((feature, index) => (
                                    <Card key={index} className="p-8 flex flex-col justify-between shadow-[0_20px_50px_rgba(0,0,0,0.5)] border border-white/10 group hover:border-purple-500/50 transition-colors duration-300 backdrop-blur-sm">
                                        <div>
                                            <div className="bg-gradient-to-br from-purple-600/80 to-indigo-600/80 rounded-2xl w-20 h-20 flex items-center justify-center mb-8 shadow-[0_0_20px_rgba(147,51,234,0.3)] border border-purple-400/30 group-hover:scale-105 transition-transform duration-300">
                                                {feature.icon}
                                            </div>
                                            <h3 className="text-2xl font-bold text-white mb-4 leading-snug">{feature.title}</h3>
                                            <p className="text-gray-300 leading-relaxed text-[15px]">{feature.description}</p>
                                        </div>
                                        <div className="text-purple-400 text-sm font-semibold tracking-wider mt-4 opacity-50 uppercase group-hover:opacity-100 transition-opacity">
                                            Feature 0{index + 1}
                                        </div>
                                    </Card>
                                ))}
                            </CardSwap>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};


// --- Main Landing Page Component ---

const LandingPage = () => {
    return (
        <ReactLenis root options={{ lerp: 0.05, duration: 1.5, smoothWheel: true }}>
            <div className="flex flex-col min-h-screen text-white font-sans selection:bg-purple-500/30 relative">
                <div className="fixed inset-0 z-0 bg-[#0B0A10]">
                    <Particles
                        particleColors={["#e3c5fc", "#a855f7", "#ffffff"]}
                        particleCount={200}
                        particleSpread={10}
                        speed={0.1}
                        particleBaseSize={100}
                        moveParticlesOnHover={false}
                        alphaParticles
                        disableRotation={false}
                        pixelRatio={1}
                    />
                </div>

                <Navbar />

                <div className="relative z-10 flex flex-col w-full">
                    <AnimatedHero />
                    <FeaturesSection />

                    <section className="relative">
                        <HowItWorksScroller />
                    </section>

                    <FaqBookScroller />
                </div>

                <div className="relative z-20 bg-[#0B0A10]">
                    <Footer />
                </div>
            </div>
        </ReactLenis>
    );
};

export default LandingPage;


