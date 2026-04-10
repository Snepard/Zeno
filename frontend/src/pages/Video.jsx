import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useJobPolling } from '../hooks/useJobPolling';
import Loader from '../components/Loader';
import ChatBox from '../components/ChatBox';

const VideoPage = () => {
    const { jobId } = useParams();
    const { jobData, status, progress, error } = useJobPolling(jobId);
    const [mode, setMode] = useState('avatar'); // 'avatar' | 'lecture'

    if (error) {
        return (
            <div className="min-h-screen bg-zinc-950 flex items-center justify-center text-white">
                <div className="text-center p-8 bg-zinc-900 border border-red-500/20 rounded-2xl">
                    <h2 className="text-2xl font-bold text-red-400 mb-2">Video Rendering Faulted</h2>
                    <p className="text-zinc-400">{error}</p>
                </div>
            </div>
        );
    }

    if (!jobData || status !== 'completed') {
        return (
            <div className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center text-white">
                <Loader 
                    progress={progress} 
                    message={
                        progress < 40 ? "Generating Master Script..." :
                        progress < 80 ? "Rendering HW NVENC Graphics Nodes..." :
                        "Running ML Lipsync Sequence bounds..."
                    } 
                />
            </div>
        );
    }

    const { video_url, avatar_url, final_url } = jobData.result;
    
    // Choose correct URL explicitly routing dynamically accurately
    let activeUrl = "http://localhost:8000";
    if (mode === 'avatar' && final_url) {
         activeUrl += final_url;
    } else if (mode === 'avatar' && avatar_url) {
         activeUrl += avatar_url;
    } else {
         activeUrl += video_url;
    }

    return (
        <div className="min-h-[calc(100vh-73px)] bg-zinc-950 text-white flex flex-col md:flex-row gap-6 p-6">
            <div className="flex-1 flex flex-col gap-6">
                <div className="flex items-center justify-between pb-4 border-b border-zinc-800">
                    <h1 className="text-2xl font-bold">{jobData.result.topic || "AI Generated Video Masterclass"}</h1>
                    
                    <div className="flex bg-zinc-900 rounded-lg p-1 border border-zinc-800">
                        <button 
                            onClick={() => setMode('lecture')}
                            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${mode === 'lecture' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'}`}
                        >
                            Standard Lecture
                        </button>
                        <button 
                            onClick={() => setMode('avatar')}
                            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${mode === 'avatar' ? 'bg-indigo-600 text-white' : 'text-zinc-400 hover:text-white'}`}
                        >
                            AI Avatar Enabled
                        </button>
                    </div>
                </div>

                <div className="flex-1 bg-black rounded-2xl overflow-hidden border border-zinc-800 shadow-2xl relative flex items-center justify-center">
                    <video 
                        key={activeUrl}
                        src={activeUrl} 
                        controls 
                        autoPlay 
                        className="w-full h-full object-contain"
                    >
                        Your browser does not support standard video architectures natively.
                    </video>
                </div>
            </div>

            <div className="w-full md:w-[400px] shrink-0 h-[800px] md:h-auto">
                <ChatBox jobId={jobId} currentSlide={0} />
            </div>
        </div>
    );
};

export default VideoPage;
