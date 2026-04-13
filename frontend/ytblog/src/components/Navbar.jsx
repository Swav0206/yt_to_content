export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4"
      style={{ background: 'rgba(8, 11, 20, 0.85)', backdropFilter: 'blur(20px)', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
      <div className="flex items-center gap-3">
        {/* Logo icon */}
        <div className="w-8 h-8 rounded-lg flex items-center justify-center"
          style={{ background: 'linear-gradient(135deg, #7c3aed, #2563eb)' }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
          </svg>
        </div>
        <span className="font-bold text-lg" style={{ fontFamily: "'Outfit', sans-serif", letterSpacing: '-0.01em' }}>
          YT<span className="gradient-text">Creation</span>
        </span>
      </div>
      <div className="flex items-center gap-3">
        <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer"
          className="btn-ghost text-xs">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          API Docs
        </a>
      </div>
    </nav>
  );
}
