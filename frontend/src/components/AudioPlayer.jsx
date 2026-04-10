import React from 'react';
import { Play, Pause } from 'lucide-react';

const AudioPlayer = ({ audioUrl, autoPlay = true, onEnded }) => {
    const audioRef = React.useRef(null);
    const [isPlaying, setIsPlaying] = React.useState(autoPlay);

    React.useEffect(() => {
        if (audioRef.current && isPlaying) {
             audioRef.current.play().catch(e => console.error("Autoplay failed:", e));
        }
    }, [audioUrl, isPlaying]);

    if (!audioUrl) return null;

    return (
        <div className="flex items-center gap-4 bg-zinc-800/50 p-4 rounded-xl border border-zinc-700/50">
            <audio 
                ref={audioRef} 
                src={audioUrl} 
                onEnded={() => {
                    setIsPlaying(false);
                    if (onEnded) onEnded();
                }}
            />
            <button 
                onClick={() => setIsPlaying(!isPlaying)}
                className="w-12 h-12 bg-indigo-500 hover:bg-indigo-400 text-white rounded-full flex items-center justify-center transition-colors"
            >
                {isPlaying ? <Pause size={20} /> : <Play size={20} className="ml-1" />}
            </button>
            <div className="flex-1">
                <p className="text-sm font-medium text-zinc-300">AI Teacher Audio</p>
                <div className="h-1 bg-zinc-700 rounded-full mt-2 overflow-hidden relative">
                    <div className="absolute top-0 left-0 h-full bg-indigo-500/50 animate-pulse w-full"></div>
                </div>
            </div>
        </div>
    );
};

export default AudioPlayer;
