import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Generate from './pages/Generate';
import Viewer from './pages/Viewer';
import VideoPage from './pages/Video';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-zinc-950 font-sans antialiased text-zinc-100 flex flex-col">
        <Navbar />
        <main className="flex-1 flex flex-col">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/generate" element={<Generate />} />
            <Route path="/viewer/:jobId" element={<Viewer />} />
            <Route path="/video/:jobId" element={<VideoPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;