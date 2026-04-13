import { useState } from "react";

const YT_REGEX = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|shorts\/|embed\/)|youtu\.be\/).+/;

function isValidYouTubeUrl(url) {
  return YT_REGEX.test(url.trim());
}

export default function UrlInput({ onGenerate, isLoading }) {
  const [url, setUrl] = useState("");
  const [mode, setMode] = useState("blog"); // "blog" | "linkedin" | "twitter"
  const [language, setLanguage] = useState("English");
  const [urlError, setUrlError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!url.trim()) {
      setUrlError("Please paste a YouTube URL");
      return;
    }
    if (!isValidYouTubeUrl(url)) {
      setUrlError("This doesn't look like a valid YouTube URL");
      return;
    }
    setUrlError("");
    onGenerate(url.trim(), mode, language);
  }

  return (
    <div className="glass-card-strong relative overflow-hidden p-8 animate-fade-in-up">
      {/* Subtle glow inside card */}
      <div className="absolute -top-20 -right-20 w-60 h-60 orb opacity-20"
        style={{ background: mode === "blog" ? "radial-gradient(circle, #7c3aed, transparent)" : "radial-gradient(circle, #2563eb, transparent)" }} />

      <div className="flex items-center justify-between mb-7 flex-wrap gap-4">
        {/* Mode toggle tabs */}
        <div className="flex gap-2">
          {[
            { id: "blog", label: "Blog Post", icon: "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z" },
            { id: "linkedin", label: "LinkedIn Post", icon: "M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z M4 6a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" },
            { id: "twitter", label: "Twitter Post", icon: "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setMode(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border transition-all duration-200 ${mode === tab.id ? "tab-active" : "border-white/10 text-slate-400 hover:text-slate-200 hover:border-white/20"}`}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d={tab.icon} />
              </svg>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Language selector */}
        <div className="relative">
          <select 
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            disabled={isLoading}
            className="input-field appearance-none py-2.5 pl-4 pr-10 text-sm font-medium text-slate-300 bg-black/20 focus:bg-black/40 border-white/10 hover:border-white/20 hover:text-slate-200 transition-all cursor-pointer rounded-xl h-auto"
            style={{ width: '160px' }}
          >
            <option value="English">🇬🇧 English</option>
            <option value="Spanish">🇪🇸 Spanish</option>
            <option value="French">🇫🇷 French</option>
            <option value="German">🇩🇪 German</option>
            <option value="Hindi">🇮🇳 Hindi</option>
            <option value="Mandarin Chinese">🇨🇳 Mandarin</option>
          </select>
          <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
               <polyline points="6 9 12 15 18 9" />
            </svg>
          </div>
        </div>
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit}>
        <label className="block text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">
          YouTube URL
        </label>
        <div className="flex gap-3">
          <div className="flex-1 relative">
            {/* YT icon inside input */}
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-red-500">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21.8 8.001a2.75 2.75 0 0 0-1.935-1.951C18.2 5.6 12 5.6 12 5.6s-6.2 0-7.865.45A2.75 2.75 0 0 0 2.2 8.001 28.8 28.8 0 0 0 1.75 12a28.8 28.8 0 0 0 .45 3.999 2.75 2.75 0 0 0 1.935 1.951C5.8 18.4 12 18.4 12 18.4s6.2 0 7.865-.45a2.75 2.75 0 0 0 1.935-1.951A28.8 28.8 0 0 0 22.25 12a28.8 28.8 0 0 0-.45-3.999zM9.75 15.02V8.98L15.5 12l-5.75 3.02z"/>
              </svg>
            </div>
            <input
              id="yt-url-input"
              type="url"
              value={url}
              onChange={(e) => { setUrl(e.target.value); setUrlError(""); }}
              placeholder="https://www.youtube.com/watch?v=..."
              className="input-field"
              style={{ paddingLeft: '48px' }}
              disabled={isLoading}
            />
          </div>
          <button
            id="generate-btn"
            type="submit"
            className="btn-primary"
            disabled={isLoading}
            style={{ whiteSpace: 'nowrap', minWidth: '156px' }}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin-slow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                </svg>
                Generating…
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                Generate {mode === "blog" ? "Blog" : mode === "twitter" ? "Thread" : "Post"}
              </>
            )}
          </button>
        </div>
        {urlError && (
          <p className="text-red-400 text-sm mt-2 flex items-center gap-1.5 animate-fade-in">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            {urlError}
          </p>
        )}
      </form>

      {/* Examples */}
      <div className="mt-5 flex items-center gap-2 flex-wrap">
        <span className="text-xs text-slate-500">Try:</span>
        {[
          { label: "YT Short", url: "https://www.youtube.com/shorts/DnPTHuqBEa8" },
          { label: "TED Talk", url: "https://www.youtube.com/watch?v=8S0FDjFBj8o" },
        ].map(ex => (
          <button
            key={ex.label}
            onClick={() => { setUrl(ex.url); setUrlError(""); onGenerate(ex.url, mode, language); }}
            className="text-xs px-3 py-1 rounded-lg border border-white/10 text-slate-400 hover:text-slate-200 hover:border-violet-500/40 transition-all duration-200"
            disabled={isLoading}
          >
            {ex.label}
          </button>
        ))}
      </div>
    </div>
  );
}
