import React, { useState, Suspense, useRef, useEffect } from 'react';
import axios from 'axios';
import { Upload, CheckCircle, Loader, PlayCircle, Mic2 } from 'lucide-react';
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom';
import Show from './components/Show';
import Podcast from './components/Podcast';
import VideoPlayer from './components/VideoPlayer';
import FloatingLines from './components/FloatingLines';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import LandingPage from './components/LandingPage';
import { DEMO_LECTURE_ID, MOCK_MODE } from './config/mock';

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

const MemoizedFloatingLines = React.memo(() => (
    <FloatingLines
        enabledWaves={["top", "middle", "bottom"]}
        lineCount={5}
        lineDistance={5}
        bendRadius={5}
        bendStrength={-0.5}
        interactive={true}
        parallax={true}
    />
));

function App() {
    const navigate = useNavigate();
    const progressIntervalRef = useRef(null);

    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("idle");
    const [ingestionData, setIngestionData] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [progress, setProgress] = useState(0);
    const [generationComplete, setGenerationComplete] = useState(false);
    const [completedJobId, setCompletedJobId] = useState(null);
    const [completedMode, setCompletedMode] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            axios.defaults.headers.common.Authorization = `Bearer ${token}`;
        }

        return () => {
            if (progressIntervalRef.current) {
                clearInterval(progressIntervalRef.current);
            }
        };
    }, []);

    const handleFileChange = (e) => {
        if (e.target.files?.length) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploadStatus("uploading");

        if (MOCK_MODE) {
            setTimeout(() => {
                setIngestionData({
                    pdf_url: `mock/${file.name || 'demo.pdf'}`,
                    status: 'complete',
                });
                setUploadStatus("success");
            }, 500);
            return;
        }

        const formData = new FormData();
        formData.append("pdf", file);

        try {
            const response = await axios.post(
                `${API_BASE}/generate/upload-pdf`,
                formData,
                { headers: { "Content-Type": "multipart/form-data" } }
            );

            setIngestionData(response.data);
            setUploadStatus("success");
        } catch (error) {
            console.error(error);
            setUploadStatus("error");
        }
    };

    const handleGenerate = async (mode = 'slides') => {
        setIsGenerating(true);
        setProgress(5);

        if (MOCK_MODE) {
            progressIntervalRef.current = setInterval(() => {
                setProgress((prev) => (prev >= 90 ? 90 : prev + 5));
            }, 1000);

            setTimeout(() => {
                clearInterval(progressIntervalRef.current);
                setProgress(100);
                setIsGenerating(false);
                setGenerationComplete(true);
                setCompletedJobId(DEMO_LECTURE_ID);
                setCompletedMode(mode);
            }, 2500);
            return;
        }

        try {
            const endpoint = mode === 'podcast' ? 'podcast' : mode === 'video' ? 'video' : 'ppt';
            const response = await axios.post(
                `${API_BASE}/generate/${endpoint}`,
                {
                    pdf_url: ingestionData?.pdf_url,
                    topic: file?.name || 'AI Lecture'
                },
                { timeout: 300000 }
            );

            const jobId = response.data.job_id || response.data.lecture_id;

            const token = localStorage.getItem('access_token');
            const pollInterval = setInterval(async () => {
                try {
                    const statusRes = await axios.get(`${API_BASE}/job/${jobId}`, {
                        headers: token ? { Authorization: `Bearer ${token}` } : {}
                    });
                    const job = statusRes.data;
                    
                    setProgress(job.progress || 10);

                    if (job.status === "completed") {
                        clearInterval(pollInterval);
                        setTimeout(() => {
                            setIsGenerating(false);
                            setGenerationComplete(true);
                            setCompletedJobId(jobId);
                            setCompletedMode(mode);
                        }, 500);
                    } else if (job.status === "failed") {
                        clearInterval(pollInterval);
                        setIsGenerating(false);
                        setProgress(0);
                        alert("Generation failed: " + (job.error || "Unknown backend error"));
                    }
                } catch (e) {
                    console.error("Polling error", e);
                }
            }, 2000);
            progressIntervalRef.current = pollInterval;

        } catch (error) {
            console.error("Generation dispatch failed:", error);
            setIsGenerating(false);
            setProgress(0);
            alert("Failed to initialize lecture generation. Please verify backend.");
        }
    };

    const UploadRoute = (
        <div className="h-screen w-full flex items-center justify-center p-6 lg:p-12 overflow-hidden bg-black text-white relative z-0">
            <div className="absolute inset-0 z-0 pointer-events-auto">
                <MemoizedFloatingLines />
            </div>

            <div className={`
                relative bg-white/5 backdrop-blur-2xl border border-white/10 rounded-[28px] shadow-[0_30px_80px_rgba(0,0,0,0.6)]
                transition-all duration-700 ease-[cubic-bezier(0.2,0.8,0.2,1)]
                flex flex-col md:flex-row overflow-hidden max-h-full
                ${uploadStatus === "success" ? "w-full max-w-5xl" : "w-full max-w-[480px]"}
            `}>
                <div className={`flex flex-col flex-shrink-0 transition-all duration-700 ease-[cubic-bezier(0.2,0.8,0.2,1)] p-8 sm:p-10 ${uploadStatus === "success" ? "w-full md:w-[480px] border-b md:border-b-0 md:border-r border-white/10 bg-black/20" : "w-full"}`}>
                    <div className="mb-8 text-center flex flex-col items-center">
                        <div className="relative mb-4">
                            <div className="h-[4.5rem] px-6 rounded-xl relative z-0 bg-white/10 border border-white/20 flex items-center justify-center">
                                <span className="text-3xl font-bold tracking-wide text-white">Zeno</span>
                            </div>
                            <div className="absolute inset-0 z-10 bg-purple-500/20 mix-blend-screen pointer-events-none rounded-xl blur-[12px] animate-pulse" />
                        </div>
                        <p className="text-slate-400 text-[15px] leading-relaxed text-center">
                            Upload your course material (PDF) to generate a beautifully interactive AI lecture.
                        </p>
                    </div>

                    <div className="flex-1 flex flex-col justify-center space-y-5">
                        <label className={`w-full group relative flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-2xl transition-all duration-300 cursor-pointer overflow-hidden ${
                            file ? 'border-purple-500/50 bg-purple-500/5' : 'border-white/10 hover:border-purple-400/50 hover:bg-white/5'
                        }`}>
                            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                            <Upload className={`w-8 h-8 mb-3 transition-colors duration-300 ${file ? 'text-purple-400' : 'text-slate-500 group-hover:text-purple-300'}`} />
                            <span className={`text-[15px] font-medium text-center truncate w-full px-4 transition-colors duration-300 ${file ? 'text-white' : 'text-slate-400 group-hover:text-slate-200'}`}>
                                {file ? file.name : "Click or drag to select PDF"}
                            </span>
                            <input
                                type="file"
                                accept=".pdf"
                                className="hidden"
                                onChange={handleFileChange}
                            />
                        </label>

                        <button
                            onClick={handleUpload}
                            disabled={!file || uploadStatus === "uploading" || uploadStatus === "success"}
                            className={`relative w-full py-4 rounded-xl font-bold text-[15px] tracking-wide transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-lg flex items-center justify-center gap-3 overflow-hidden
                            ${!file
                                ? "bg-white/5 text-slate-500 cursor-not-allowed border border-white/5"
                                : uploadStatus === "success"
                                ? "bg-green-500/20 text-green-300 border border-green-500/30 cursor-default"
                                : "bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white shadow-[0_0_40px_rgba(168,85,247,0.4)]"
                            }`}
                        >
                            {uploadStatus === "uploading" ? (
                                <>
                                    <Loader className="w-5 h-5 animate-spin" />
                                    Ingesting File...
                                </>
                            ) : uploadStatus === "success" ? (
                                <>
                                    <CheckCircle className="w-5 h-5" />
                                    Upload Complete
                                </>
                            ) : (
                                "Start Processing"
                            )}
                        </button>

                        {uploadStatus === "error" && (
                            <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-medium flex items-center justify-center gap-2 animate-fade-in-up">
                                <CheckCircle className="w-4 h-4" /> Failed to ingest. Check backend.
                            </div>
                        )}
                    </div>
                </div>

                <div className={`flex-1 flex flex-col transition-all duration-700 delay-150 ease-[cubic-bezier(0.2,0.8,0.2,1)] p-8 sm:p-10 ${uploadStatus === "success" ? "opacity-100 translate-x-0" : "opacity-0 translate-x-12 absolute inset-y-0 right-0 w-0 pointer-events-none"}`}>
                    {uploadStatus === "success" && ingestionData && (
                        <div className="h-full flex flex-col animate-fade-in custom-scrollbar overflow-y-auto">
                            <p className="text-slate-300 text-[15px] mb-8 leading-relaxed max-w-md">
                                Your material has been successfully uploaded as <span className="font-mono font-bold text-white px-1.5 py-0.5 rounded bg-white/10">{ingestionData.pdf_url || 'latest PDF'}</span>. You are now ready to generate your lecture.
                            </p>

                            <div className="flex-1 flex flex-col justify-center">
                                {isGenerating ? (
                                    <div className="w-full flex flex-col items-center justify-center gap-8 py-4">
                                        <div className="w-48 h-48 rounded-full bg-black/40 border-2 border-purple-500/30 overflow-hidden relative shadow-[0_0_50px_rgba(168,85,247,0.2)] flex items-center justify-center">
                                            <div className="absolute inset-0 rounded-full border-2 border-purple-400/50 animate-[spin_3s_linear_infinite]" style={{ borderTopColor: 'transparent' }} />
                                            <div className="absolute inset-4 rounded-full border border-purple-300/30 animate-[spin_5s_linear_infinite_reverse]" style={{ borderTopColor: 'transparent' }} />
                                            <span className="text-5xl select-none">🤖</span>
                                        </div>

                                        <div className="w-full max-w-xs">
                                            <div className="flex justify-between mb-3 text-[13px] font-bold text-purple-300 tracking-wide uppercase">
                                                <span>Synthesizing...</span>
                                                <span className="font-mono">{progress}%</span>
                                            </div>
                                            <div className="w-full bg-black/50 h-2 rounded-full overflow-hidden border border-white/5">
                                                <div
                                                    className="bg-gradient-to-r from-purple-500 to-pink-500 h-full transition-all duration-300 ease-out relative"
                                                    style={{ width: `${progress}%` }}
                                                >
                                                    <div className="absolute top-0 right-0 bottom-0 w-20 bg-gradient-to-r from-transparent to-white/50 animate-[translate-x_2s_linear_infinite]" />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ) : generationComplete ? (
                                    <div className="flex flex-col items-center justify-center h-full gap-6 animate-fade-in">
                                        <div className="w-20 h-20 bg-green-500/20 rounded-full flex items-center justify-center border-2 border-green-500/50 mb-2">
                                            <CheckCircle className="w-10 h-10 text-green-400" />
                                        </div>
                                        <h3 className="text-white text-2xl font-bold tracking-wide">Processing Complete</h3>
                                        <p className="text-slate-400 text-center max-w-sm mb-4">
                                            Your lecture has been fully generated natively with speech, transcription, and slides.
                                        </p>
                                        <button
                                            onClick={() => {
                                                if (completedMode === 'podcast') {
                                                    navigate(`/podcast/${completedJobId}`, { state: { initialMode: 'podcast' } });
                                                } else if (completedMode === 'video') {
                                                    navigate(`/video/${completedJobId}`);
                                                } else {
                                                    navigate(`/show/${completedJobId}`);
                                                }
                                            }}
                                            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-full text-[17px] font-bold transition-all hover:scale-105 shadow-[0_0_40px_rgba(168,85,247,0.4)] flex items-center gap-3 w-full max-w-sm justify-center"
                                        >
                                            <PlayCircle className="w-6 h-6" />
                                            Enter Classroom
                                        </button>
                                    </div>
                                ) : (
                                    <div className="flex flex-col gap-4 w-full">
                                        <h3 className="text-white text-lg font-semibold mb-2">Select Format:</h3>

                                        <button
                                            onClick={() => handleGenerate('slides')}
                                            className="group relative w-full p-5 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-purple-500/50 transition-all text-left flex items-start gap-4 overflow-hidden"
                                        >
                                            <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center shrink-0 border border-purple-500/30 group-hover:scale-110 transition-transform">
                                                <PlayCircle className="w-6 h-6 text-purple-300" />
                                            </div>
                                            <div>
                                                <h4 className="text-white font-bold text-[16px] mb-1 group-hover:text-purple-300 transition-colors">Visual Lecture (Slides)</h4>
                                                <p className="text-slate-400 text-[13px] leading-snug pr-4">Generates beautiful animated slides accompanied by a virtual AI teacher explaining the concepts.</p>
                                            </div>
                                        </button>

                                        <button
                                            onClick={() => handleGenerate('podcast')}
                                            className="group relative w-full p-5 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-pink-500/50 transition-all text-left flex items-start gap-4 overflow-hidden"
                                        >
                                            <div className="w-12 h-12 rounded-xl bg-pink-500/20 flex items-center justify-center shrink-0 border border-pink-500/30 group-hover:scale-110 transition-transform">
                                                <Mic2 className="w-6 h-6 text-pink-300" />
                                            </div>
                                            <div>
                                                <h4 className="text-white font-bold text-[16px] mb-1 group-hover:text-pink-300 transition-colors">Dual-Host Podcast</h4>
                                                <p className="text-slate-400 text-[13px] leading-snug pr-4">An engaging, cinematic auditory experience featuring two AI hosts discussing the material.</p>
                                            </div>
                                        </button>

                                        <button
                                            onClick={() => handleGenerate('video')}
                                            className="group relative w-full p-5 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-emerald-500/50 transition-all text-left flex items-start gap-4 overflow-hidden"
                                        >
                                            <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center shrink-0 border border-emerald-500/30 group-hover:scale-110 transition-transform">
                                                <PlayCircle className="w-6 h-6 text-emerald-300" />
                                            </div>
                                            <div>
                                                <h4 className="text-white font-bold text-[16px] mb-1 group-hover:text-emerald-300 transition-colors">Long-Form Video</h4>
                                                <p className="text-slate-400 text-[13px] leading-snug pr-4">Generates a fully autonomous, rendered animated video sequentially spanning 10-60+ minutes.</p>
                                            </div>
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );

    return (
        <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/upload" element={UploadRoute} />
            <Route path="/show/:lectureId" element={<Show />} />
            <Route path="/podcast/:lectureId" element={<Podcast />} />
            <Route path="/video/:lectureId" element={<VideoPlayer />} />
            <Route path="*" element={<Navigate to="/signin" replace />} />
        </Routes>
    );
}

export default App;
