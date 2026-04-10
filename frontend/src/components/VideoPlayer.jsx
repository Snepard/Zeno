import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Loader, ArrowLeft, Video as VideoIcon } from 'lucide-react';
import FloatingLines from './FloatingLines';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:4000/api';
const ASSET_BASE = import.meta.env.VITE_ASSET_BASE || 'http://127.0.0.1:4000';

function VideoPlayer() {
    const { lectureId } = useParams();
    const navigate = useNavigate();
    const [videoData, setVideoData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchVideoData = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get(`${API_BASE}/job/${lectureId}`, {
                    headers: token ? { Authorization: `Bearer ${token}` } : {}
                });
                if (response.data && response.data.result) {
                    setVideoData(response.data.result);
                } else {
                    alert("Video data missing from response.");
                }
            } catch (error) {
                console.error("Failed to fetch video:", error);
                alert("Could not load video.");
                navigate('/upload');
            } finally {
                setLoading(false);
            }
        };

        fetchVideoData();
    }, [lectureId, navigate]);

    if (loading) {
        return (
            <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center text-white relative">
                 <div className="absolute inset-0 z-0">
                    <FloatingLines enabledWaves={["middle"]} />
                </div>
                <div className="z-10 flex flex-col items-center">
                    <Loader className="w-12 h-12 animate-spin text-purple-500 mb-6" />
                    <span className="text-2xl font-bold tracking-widest text-slate-300">Summoning Final Video...</span>
                </div>
            </div>
        );
    }

    const videoUrl = videoData?.video_url;
    const finalSrc = videoUrl ? (videoUrl.startsWith('http') ? videoUrl : `${ASSET_BASE}${videoUrl}`) : null;

    return (
        <div className="min-h-screen bg-[#0a0a0f] flex flex-col relative">
            <div className="absolute inset-0 z-0 opacity-40">
                 <FloatingLines enabledWaves={["top"]} />
            </div>

            {/* Header */}
            <div className="z-10 p-6 flex items-center justify-between">
                <button
                    onClick={() => navigate('/upload')}
                    className="flex items-center gap-2 px-4 py-2 border border-white/20 bg-black/40 hover:bg-white/10 rounded-xl text-white backdrop-blur-md transition-all"
                >
                    <ArrowLeft className="w-5 h-5" /> Back to Dashboard
                </button>
                <div className="flex items-center gap-3 px-6 py-2 bg-purple-500/10 border border-purple-500/30 rounded-full text-purple-300 font-bold tracking-wider">
                    <VideoIcon className="w-5 h-5" /> Long Form Rendering
                </div>
            </div>

            {/* Content Body */}
            <div className="z-10 flex-1 flex items-center justify-center p-8">
                <div className="w-full max-w-6xl aspect-video bg-black rounded-3xl border border-white/10 shadow-[0_0_80px_rgba(168,85,247,0.2)] overflow-hidden flex items-center justify-center group relative">
                    {!finalSrc ? (
                        <div className="text-center text-white/60 p-8 flex flex-col items-center">
                            <VideoIcon className="w-16 h-16 text-slate-600 mb-4" />
                            <p className="text-xl">No structural video chunk rendered.</p>
                        </div>
                    ) : (
                        <video 
                            controls 
                            autoPlay 
                            className="w-full h-full object-contain"
                            src={finalSrc}
                        >
                            Your browser does not support the video tag.
                        </video>
                    )}
                </div>
            </div>
        </div>
    );
}

export default VideoPlayer;
