import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import { api } from '../api/endpoints';

const ChatBox = ({ jobId, currentSlide }) => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am AI Guruji. What questions do you have about this lecture?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    const handleSend = async () => {
        if (!input.trim() || !jobId) return;

        const userMsg = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setIsLoading(true);

        try {
            const res = await api.chat({
                user_id: "demo_user", // In production this comes from Auth
                job_id: jobId,
                question: userMsg,
                current_slide: currentSlide,
                mode: "doubt"
            });
            
            setMessages(prev => [...prev, { role: 'assistant', content: res.data.answer }]);
        } catch (err) {
            console.error("Chat error:", err);
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I am experiencing connection issues. Please try again." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-zinc-900 border border-zinc-800 rounded-2xl shadow-xl overflow-hidden relative">
            <div className="p-4 border-b border-zinc-800 bg-zinc-900/90 backdrop-blur top-0 z-10 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                        <Sparkles size={16} />
                    </div>
                    <h3 className="font-semibold text-white">Ask AI Guruji</h3>
                </div>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.map((m, i) => (
                    <div key={i} className={`flex gap-4 ${m.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === 'user' ? 'bg-zinc-700 text-white' : 'bg-indigo-600 text-white'}`}>
                            {m.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                        </div>
                        <div className={`px-4 py-3 rounded-2xl max-w-[80%] text-sm leading-relaxed ${m.role === 'user' ? 'bg-zinc-800 text-zinc-200 rounded-tr-sm' : 'bg-indigo-500/10 text-zinc-300 border border-indigo-500/20 rounded-tl-sm'}`}>
                            {m.content}
                        </div>
                    </div>
                ))}
                
                {isLoading && (
                    <div className="flex gap-4">
                        <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center shrink-0 text-white">
                            <Bot size={16} />
                        </div>
                        <div className="px-5 py-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 rounded-tl-sm flex items-center gap-1">
                            <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce"></div>
                            <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                            <div className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="p-4 bg-zinc-900 border-t border-zinc-800">
                <div className="relative flex items-center">
                    <input 
                        type="text" 
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Ask about this slide..."
                        className="w-full bg-zinc-800 text-white rounded-full pl-5 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 placeholder:text-zinc-500"
                        disabled={isLoading}
                    />
                    <button 
                        onClick={handleSend}
                        disabled={isLoading || !input.trim()}
                        className="absolute right-2 w-8 h-8 bg-indigo-600 hover:bg-indigo-500 disabled:bg-zinc-700 text-white rounded-full flex items-center justify-center transition-colors"
                    >
                        <Send size={14} className="ml-0.5" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatBox;
