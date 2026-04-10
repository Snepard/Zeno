import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/endpoints';
import { Presentation, Mic, PlaySquare, Loader2 } from 'lucide-react';

const Generate = () => {
    const navigate = useNavigate();
    const [topic, setTopic] = useState('');
    const [type, setType] = useState('ppt'); // ppt, podcast, video
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGenerate = async (e) => {
        e.preventDefault();
        if (!topic.trim()) return;
        
        setLoading(true);
        setError('');

        try {
            // Note: If type is video, we technically hit ppt then the worker continues to video
            const endpoint = (type === 'podcast') ? api.generatePodcast : api.generatePPT;
            
            const res = await endpoint({ topic });
            const jobId = res.data.job_id;
            
            // Redirect cleanly natively bypassing hangs
            if (type === 'video') {
                navigate(`/video/${jobId}`);
            } else {
                navigate(`/viewer/${jobId}`);
            }
            
        } catch (err) {
            setError(err.response?.data?.detail || "Failed to initiate generation sequence securely.");
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-zinc-950 flex flex-col items-center py-20 px-4 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-indigo-600/5 rounded-full blur-[120px] pointer-events-none"></div>

            <div className="max-w-2xl w-full">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-extrabold text-white mb-4 tracking-tight">Create a new Masterclass</h1>
                    <p className="text-zinc-400 text-lg">Define your topic and our ML architecture will synthesize the entire pipeline end-to-end natively.</p>
                </div>

                <form onSubmit={handleGenerate} className="p-8 rounded-3xl bg-zinc-900 border border-zinc-800 shadow-2xl relative z-10">
                    <div className="mb-8">
                        <label className="block text-sm font-semibold text-zinc-300 mb-3">What do you want to learn?</label>
                        <textarea 
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="e.g. The intricate mechanisms behind Python's Global Interpreter Lock (GIL)..."
                            className="w-full bg-zinc-950 border border-zinc-800 rounded-xl p-4 text-white placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 resize-none h-32"
                            disabled={loading}
                        />
                    </div>

                    <div className="mb-10">
                        <label className="block text-sm font-semibold text-zinc-300 mb-4">Output Format Architecture</label>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {[
                                { id: 'ppt', icon: Presentation, title: "Interactive PPT" },
                                { id: 'podcast', icon: Mic, title: "Podcast Audio" },
                                { id: 'video', icon: PlaySquare, title: "Video + Avatar" }
                            ].map(opt => (
                                <div 
                                    key={opt.id}
                                    onClick={() => !loading && setType(opt.id)}
                                    className={`flex flex-col items-center p-4 rounded-xl border-2 cursor-pointer transition-all ${type === opt.id ? 'border-indigo-500 bg-indigo-500/10' : 'border-zinc-800 bg-zinc-950 hover:border-zinc-700'}`}
                                >
                                    <opt.icon size={28} className={type === opt.id ? 'text-indigo-400 mb-2' : 'text-zinc-500 mb-2'} />
                                    <span className={`font-medium ${type === opt.id ? 'text-white' : 'text-zinc-400'}`}>{opt.title}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-sm">
                            {error}
                        </div>
                    )}

                    <button 
                        type="submit"
                        disabled={loading || !topic.trim()}
                        className="w-full py-4 bg-white text-black font-bold rounded-xl flex items-center justify-center gap-2 hover:bg-zinc-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        {loading ? (
                            <><Loader2 size={20} className="animate-spin" /> Synthesizing Pipeline...</>
                        ) : (
                            "Launch Generation Engine"
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Generate;
