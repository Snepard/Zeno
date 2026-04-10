import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const SlideViewer = ({ slides, currentIndex, onNext, onPrev }) => {
    if (!slides || slides.length === 0) return null;
    const slide = slides[currentIndex];

    return (
        <div className="w-full flex flex-col gap-6">
            <div className="aspect-video w-full bg-zinc-900 rounded-2xl border border-zinc-800 shadow-2xl overflow-hidden flex flex-col">
                <div className="h-2 bg-indigo-600 w-full"></div>
                <div className="flex-1 p-10 flex flex-col items-center justify-center text-center relative">
                    <h2 className="text-4xl font-bold text-white mb-8 leading-tight tracking-tight">{slide.title}</h2>
                    <p className="text-xl text-zinc-400 max-w-2xl leading-relaxed">
                        {slide.content}
                    </p>
                    
                    <div className="absolute bottom-6 left-6 flex gap-2">
                        {slide.keywords?.map((kw, idx) => (
                            <span key={idx} className="px-3 py-1 bg-zinc-800 text-indigo-400 text-xs font-mono rounded-full border border-zinc-700/50">
                                {kw}
                            </span>
                        ))}
                    </div>
                    <span className="absolute bottom-6 right-6 text-zinc-600 font-mono text-sm">
                        {currentIndex + 1} / {slides.length}
                    </span>
                </div>
            </div>

            <div className="flex justify-between items-center px-4">
                <button 
                    onClick={onPrev} 
                    disabled={currentIndex === 0}
                    className="flex items-center gap-2 px-6 py-3 bg-zinc-800 text-white rounded-xl hover:bg-zinc-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                    <ChevronLeft size={20}/> Previous
                </button>
                <div className="flex gap-2">
                   {slides.map((_, idx) => (
                       <div key={idx} className={`w-2 h-2 rounded-full transition-all ${idx === currentIndex ? 'bg-indigo-500 w-6' : 'bg-zinc-700'}`} />
                   ))}
                </div>
                <button 
                    onClick={onNext} 
                    disabled={currentIndex === slides.length - 1}
                    className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                    Next <ChevronRight size={20}/>
                </button>
            </div>
        </div>
    );
};

export default SlideViewer;
