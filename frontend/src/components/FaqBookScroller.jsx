import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

const faqData = [
    {
        question: <>How does <span className="relative inline-block"><span className="absolute inset-0 bg-yellow-400/40 -rotate-2 rounded"></span><span className="relative">Zeno's AI</span></span> presentation generator work?</>,
        answer: <>Zeno uses advanced AI algorithms to analyze your <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600">PDF documents</span> and automatically creates professional visual lectures with smart slide layouts, virtual teachers, and engaging dual-host podcasts.</>
    },
    {
        question: <>What file formats does <span className="underline decoration-wavy decoration-cyan-500/60 underline-offset-4">Zeno accept?</span></>,
        answer: <>Currently, we specialize in high-fidelity extraction from <span className="relative inline-block px-1"><span className="absolute inset-0 bg-cyan-300/30 rotate-1 rounded"></span><span className="relative font-bold text-[#1e1e24]">PDF documents</span></span>. Ensure your PDFs have clear, extractable text for the best results.</>
    },
    {
        question: <>Is Zeno suitable for both <span className="relative inline-block"><span className="absolute inset-x-0 bottom-1 h-3 bg-yellow-400/50 -rotate-1 rounded"></span><span className="relative">teachers</span></span> and <span className="relative inline-block"><span className="absolute inset-x-0 bottom-1 h-3 bg-purple-400/40 rotate-1 rounded"></span><span className="relative">students</span></span>?</>,
        answer: <>Absolutely! Teachers can use it to create interactive materials and virtual lectures, while students can generate custom study guides or listen to podcast-style summaries of their course material.</>
    },
    {
        question: <>What's the difference between <span className="italic font-bold">visual lectures</span> and <span className="italic font-bold">podcasts</span>?</>,
        answer: <>Visual lectures create an interactive presentation deck guided by a 3D virtual teacher. Podcasts generate a <span className="relative inline-block px-1"><span className="absolute inset-0 bg-yellow-400/40 -rotate-[1deg] rounded"></span><span className="relative">conversational, audio-only experience</span></span> between two AI hosts discussing the subject matter.</>
    },
    {
        question: <>How <span className="relative inline-block px-1 w-max"><span className="absolute -inset-1 border-[3px] border-red-400/50 rounded-full rotate-2"></span><span className="relative">secure</span></span> is my educational data on Zeno?</>,
        answer: <>We prioritize your privacy and security. All uploaded documents and generated content are <span className="font-bold underline decoration-[3px] decoration-green-400/60 underline-offset-2">encrypted securely</span>. We never use your personal data or institutional materials to train our base AI models.</>
    }
];

const noiseSvg = `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.4'/%3E%3C/svg%3E")`;

const PageSide = ({ isBack, isCover, children }) => {
    return (
        <div 
            className="absolute inset-0 w-full h-full overflow-hidden"
            style={{
                backfaceVisibility: 'hidden',
                transform: isBack ? 'rotateY(180deg)' : 'rotateY(0deg)',
                backgroundColor: isCover ? '#4a2c34' : '#fdfbf7', // Dark Leather vs Paper
                borderTopRightRadius: isBack ? '0' : (isCover ? '8px' : '4px'),
                borderBottomRightRadius: isBack ? '0' : (isCover ? '8px' : '4px'),
                borderTopLeftRadius: isBack ? (isCover ? '8px' : '4px') : '0',
                borderBottomLeftRadius: isBack ? (isCover ? '8px' : '4px') : '0',
                boxShadow: isCover ? 'inset 0 0 30px rgba(0,0,0,0.8)' : 'inset 0 0 10px rgba(0,0,0,0.05)',
            }}
        >
            {/* Texture */}
            {isCover && (
                <div className="absolute inset-0 opacity-50 mix-blend-overlay pointer-events-none" style={{ backgroundImage: noiseSvg }}></div>
            )}
            {!isCover && (
                <div className="absolute inset-0 opacity-20 bg-[linear-gradient(transparent_95%,#cbd5e1_95%)] bg-[length:100%_1.8rem] pointer-events-none"></div>
            )}

            {/* Spine Hinge Shading */}
            <div className={`absolute top-0 bottom-0 w-[20px] pointer-events-none ${isBack ? 'right-0 bg-gradient-to-l' : 'left-0 bg-gradient-to-r'} ${isCover ? 'from-black/80 to-transparent' : 'from-black/10 to-transparent'}`}></div>

            {/* Content Container */}
            <div className={`relative z-10 w-full h-full ${isCover ? 'p-0' : 'p-6 md:p-10'} flex flex-col`}>
                {children}
            </div>
        </div>
    );
};

const BookPage = ({ rotateMap, zIndexRight, zIndexLeft, frontContent, backContent, isCoverFront, isCoverBack }) => {
    const dynamicZ = useTransform(rotateMap, [-180, -90, -89.9, 0], [zIndexLeft, zIndexLeft, zIndexRight, zIndexRight]);

    return (
        <motion.div
            style={{
                rotateY: rotateMap,
                zIndex: dynamicZ,
                transformStyle: 'preserve-3d'
            }}
            className="absolute inset-y-0 left-0 w-full origin-left"
        >
            <PageSide isBack={false} isCover={isCoverFront}>{frontContent}</PageSide>
            <PageSide isBack={true} isCover={isCoverBack}>{backContent}</PageSide>
        </motion.div>
    );
};

const CoverArt = () => (
    <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-[#4a2c34] to-[#2a171d]">
        <div className="border-[2px] border-[#ffd7a0]/40 rounded-lg p-6 flex flex-col items-center justify-center w-[85%] h-[90%] shadow-[inset_0_0_20px_rgba(0,0,0,0.5)] bg-[#4a2c34]/20">
            <span className="text-transparent bg-clip-text bg-gradient-to-b from-[#ffedc2] to-[#cda562] text-7xl mb-4 font-serif relative drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">
                ?
            </span>
            <h2 className="font-black uppercase items-center flex flex-col text-center drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">
                <span className="text-[#ffd7a0] text-xl tracking-[0.4em] mb-6 opacity-90">ZENO</span>
                <span className="text-transparent bg-clip-text bg-gradient-to-b from-[#ffedc2] to-[#cda562] text-4xl md:text-5xl leading-relaxed tracking-widest px-2">FAQs</span>
            </h2>
        </div>
    </div>
);

const BackCoverArt = () => (
    <div className="w-full h-full bg-gradient-to-bl from-[#4a2c34] to-[#2a171d] flex items-end justify-center pb-12">
         <span className="text-[#ffd7a0]/60 font-black tracking-widest drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] text-lg">ZENO.AI</span>
    </div>
);

const FaqPageContent = ({ index }) => {
    const faq = faqData[index];
    if (!faq) return null;
    return (
        <div className="flex flex-col h-full w-full">
            <h4 className="text-xl md:text-2xl font-black text-[#1e1e24] mb-4 leading-snug drop-shadow-sm font-sans tracking-tight">
                {faq.question}
            </h4>
            <p className="text-[#4a4a55] text-[13px] md:text-[15px] leading-relaxed mb-auto font-medium">
                {faq.answer}
            </p>
            <div className="flex justify-between items-center text-xs text-gray-500 font-bold border-t-2 border-gray-200 pt-4 mt-4 uppercase tracking-wider">
                <span>Zeno FAQ</span>
                <span>Page {index + 1}</span>
            </div>
        </div>
    );
};

const OutroContent = () => (
    <div className="flex flex-col h-full w-full items-center justify-center text-center">
        <h4 className="text-2xl md:text-3xl font-black text-[#1e1e24] mb-4 leading-tight drop-shadow-sm">
            Ready to <br/> transform your material?
        </h4>
        <p className="text-[#4a4a55] text-sm md:text-base leading-relaxed font-medium">
            Start using Zeno today to convert stagnant PDFs into highly interactive cinematic learning experiences.
        </p>
    </div>
);

export const FaqBookScroller = () => {
    const containerRef = useRef(null);
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start end", "end start"]
    });

    // Book X translation to center the spine organically
    // -50% means moving left by half the wrapper's width (which puts the origin-left spine in the exact center)
    const bookX = useTransform(scrollYProgress,
        [0.0, 0.24, 0.33, 0.72, 0.79, 1.0],
        ["0%", "0%", "50%", "50%", "0%", "0%"]
    );

    // Dynamic rotation for all 4 pages
    // The book waits until 0.25 (after it has safely locked into its sticky container).
    // The book closes fully by 0.79 (right before it starts un-sticking and scrolling out of view at 0.80)
    const rotateCover = useTransform(scrollYProgress, [0.25, 0.33, 0.74, 0.79], [0, -180, -180, 0]);
    const rotatePage1 = useTransform(scrollYProgress, [0.40, 0.48, 0.73, 0.78], [0, -180, -180, 0]);
    const rotatePage2 = useTransform(scrollYProgress, [0.55, 0.63, 0.72, 0.77], [0, -180, -180, 0]);
    const rotateBack  = useTransform(scrollYProgress, [0, 1], [0, 0]);

    return (
        <section ref={containerRef} className="relative h-[400vh] bg-transparent text-white pt-20">
            <div className="sticky top-0 h-screen w-full flex items-center justify-center overflow-hidden" style={{ perspective: '2000px' }}>
                

                <motion.div 
                    style={{ x: bookX, rotateX: 5, rotateZ: -1, transformStyle: 'preserve-3d' }} 
                    className="relative w-[80vw] max-w-[350px] aspect-[1/1.4] z-10 flex justify-center"
                >
                    {/* The physical spine binding */}
                    <div className="absolute inset-y-0 left-[-15px] w-[30px] bg-gradient-to-r from-[#201015] via-[#4a2c34] to-[#251319] rounded-full shadow-[0_0_20px_rgba(0,0,0,0.8)] z-0 hidden md:block"></div>

                    {/* Book Pages Container. Notice the wrapper is just to hold origin logic */}
                    <div className="relative w-full h-full" style={{ transformStyle: 'preserve-3d' }}>
                        
                        {/* 1. FRONT COVER */}
                        <BookPage 
                            rotateMap={rotateCover} 
                            zIndexRight={4}
                            zIndexLeft={1}
                            isCoverFront={true} 
                            isCoverBack={false}
                            frontContent={<CoverArt />}
                            backContent={<FaqPageContent index={0} />}
                        />

                        {/* 2. INNER PAGE 1 */}
                        <BookPage 
                            rotateMap={rotatePage1} 
                            zIndexRight={3}
                            zIndexLeft={2}
                            isCoverFront={false} 
                            isCoverBack={false}
                            frontContent={<FaqPageContent index={1} />}
                            backContent={<FaqPageContent index={2} />}
                        />

                        {/* 3. INNER PAGE 2 */}
                        <BookPage 
                            rotateMap={rotatePage2} 
                            zIndexRight={2}
                            zIndexLeft={3}
                            isCoverFront={false} 
                            isCoverBack={false}
                            frontContent={<FaqPageContent index={3} />}
                            backContent={<FaqPageContent index={4} />}
                        />

                        {/* 4. BACK COVER AND OUTRO */}
                        <BookPage 
                            rotateMap={rotateBack} 
                            zIndexRight={1}
                            zIndexLeft={4}
                            isCoverFront={false} 
                            isCoverBack={true}
                            frontContent={<OutroContent />}
                            backContent={<BackCoverArt />}
                        />
                        
                    </div>
                </motion.div>
            </div>
        </section>
    );
};
