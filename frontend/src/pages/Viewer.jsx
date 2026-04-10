import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useJobPolling } from '../hooks/useJobPolling';
import Loader from '../components/Loader';
import SlideViewer from '../components/SlideViewer';
import AudioPlayer from '../components/AudioPlayer';
import ChatBox from '../components/ChatBox';

const Viewer = () => {
    const { jobId } = useParams();
    const { jobData, status, progress, error } = useJobPolling(jobId);
    const [currentIdx, setCurrentIdx] = useState(0);

    // Block completely rendering states dynamically accurately tracking limits.
    if (error) {
        return (
            <div className="min-h-screen bg-zinc-950 flex items-center justify-center text-white">
                <div className="text-center p-8 bg-zinc-900 border border-red-500/20 rounded-2xl">
                    <h2 className="text-2xl font-bold text-red-400 mb-2">Generation Faulted</h2>
                    <p className="text-zinc-400">{error}</p>
                </div>
            </div>
        );
    }

    if (!jobData || (status !== 'completed' && (!jobData.result || !jobData.result.script))) {
        return (
            <div className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center text-white">
                <Loader progress={progress} message="AI LLMs & Audio mapping engines are rendering your content..." />
            </div>
        );
    }

    const script = jobData.result.script;
    const slides = script.slides || script.dialogue; // Support both structures dynamically

    return (
        <div className="min-h-[calc(100vh-73px)] bg-zinc-950 text-white flex flex-col md:flex-row gap-6 p-6">
            <div className="flex-1 flex flex-col gap-6">
                
                <div className="flex items-center justify-between pb-4 border-b border-zinc-800">
                    <h1 className="text-2xl font-bold">{jobData.result.topic || script.topic}</h1>
                    {status !== 'completed' && (
                        <div className="flex items-center gap-3 px-4 py-1.5 bg-indigo-500/10 rounded-full border border-indigo-500/20 text-sm font-medium text-indigo-300">
                            <div className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse"></div>
                            Processing Audio ({progress}%)
                        </div>
                    )}
                </div>

                <div className="flex-1 flex flex-col">
                    <SlideViewer 
                        slides={slides} 
                        currentIndex={currentIdx} 
                        onNext={() => setCurrentIdx(prev => Math.min(prev + 1, slides.length - 1))}
                        onPrev={() => setCurrentIdx(prev => Math.max(prev - 1, 0))}
                    />
                </div>

                {/* Progressive Audio Execution Native Hook */}
                {slides[currentIdx]?.audio_url && (
                    <div className="mt-auto">
                        <AudioPlayer 
                            key={`audio-${currentIdx}`}
                            audioUrl={`http://localhost:8000${slides[currentIdx].audio_url}`} 
                            onEnded={() => {
                                // Optional auto-advance globally safely preventing overflow bounds
                                if (currentIdx < slides.length - 1) {
                                    setCurrentIdx(prev => prev + 1);
                                }
                            }}
                        />
                    </div>
                )}
            </div>

            <div className="w-full md:w-[400px] shrink-0 h-[800px] md:h-auto">
                <ChatBox 
                    jobId={jobId} 
                    currentSlide={slides[currentIdx]?.slide_no || currentIdx} 
                />
            </div>
        </div>
    );
};

export default Viewer;
