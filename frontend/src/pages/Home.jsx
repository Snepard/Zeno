import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Presentation, Mic, PlaySquare, ArrowRight } from 'lucide-react';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center justify-center p-8 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-purple-600/10 rounded-full blur-[100px] pointer-events-none"></div>
            
            <div className="max-w-4xl w-full z-10 flex flex-col items-center mt-20">
                <div className="px-4 py-1.5 mb-6 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-300 text-xs font-semibold tracking-wider uppercase">
                    AI Guruji Production v1.0
                </div>
                
                <h1 className="text-5xl md:text-7xl font-extrabold text-center tracking-tight mb-6">
                    Learn anything. <br/>
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">Instantly generated.</span>
                </h1>
                
                <p className="text-lg md:text-xl text-zinc-400 text-center max-w-2xl mb-12">
                    Enter any topic, concept, or document. Our AI Engine instantly renders a fully narrated presentation, a conversational podcast, or an interactive video lecture tightly coupled with a context-aware RAG Tutor.
                </p>

                <button 
                    onClick={() => navigate('/generate')}
                    className="group px-8 py-4 bg-white text-black rounded-full font-bold text-lg flex items-center gap-3 hover:scale-105 hover:bg-indigo-50 transition-all shadow-xl shadow-white/10"
                >
                    Start Generating <ArrowRight className="group-hover:translate-x-1 transition-transform" />
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-32 max-w-5xl w-full z-10 px-4">
                {[
                    { icon: Presentation, title: "Smart Presentations", desc: "Structured slides automatically generated and synced with Microsoft Edge TTS." },
                    { icon: Mic, title: "Podcast Generation", desc: "A naturally flowing 2-speaker conversational dialogue covering deep structural nuances." },
                    { icon: PlaySquare, title: "Avatar Lectures", desc: "Deploy your scripts seamlessly into a Wav2Lip ML generated virtual avatar lecturer explicitly." }
                ].map((Feature, idx) => (
                    <div key={idx} className="p-6 rounded-3xl bg-zinc-900/50 border border-zinc-800/50 backdrop-blur-sm hover:bg-zinc-800/50 transition-colors">
                        <div className="w-12 h-12 rounded-xl bg-zinc-800 flex items-center justify-center text-indigo-400 mb-4">
                            <Feature.icon size={24} />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">{Feature.title}</h3>
                        <p className="text-zinc-400 leading-relaxed text-sm">{Feature.desc}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
