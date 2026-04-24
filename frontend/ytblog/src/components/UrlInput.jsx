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
        style={{ background: "radial-gradient(circle, rgba(255,255,255,0.3), transparent)" }} />

      <div className="flex items-center justify-between mb-7 flex-wrap gap-4">
        {/* Mode toggle tabs */}
        <div className="flex flex-wrap gap-2">
          {[
            { id: "blog", label: "Blog Post", icon: "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z" },
            { id: "linkedin", label: "LinkedIn Post", icon: "M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z M4 6a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" },
            { id: "twitter", label: "Twitter Post", icon: "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" },
            { id: "ytshort", label: "YT Short", icon: "M10 16.5l6-4.5-6-4.5v9zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" },
            { id: "tedtalk", label: "TED Talk", icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" },
            { id: "instagram", label: "Instagram", icon: "M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2zm-.2 2A3.6 3.6 0 0 0 4 7.6v8.8C4 18.4 5.6 20 7.6 20h8.8a3.6 3.6 0 0 0 3.6-3.6V7.6C20 5.6 18.4 4 16.4 4H7.6zm9.65 1.5a1.25 1.25 0 0 1 1.25 1.25A1.25 1.25 0 0 1 17.25 8 1.25 1.25 0 0 1 16 6.75a1.25 1.25 0 0 1 1.25-1.25zM12 7a5 5 0 0 1 5 5 5 5 0 0 1-5 5 5 5 0 0 1-5-5 5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3z" },
            { id: "newsletter", label: "Newsletter", icon: "M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6zm-2 0l-8 5-8-5h16zm0 12H4V8l8 5 8-5v10z" },
            { id: "medium", label: "Medium", icon: "M2.75 3h18.5v18H2.75V3z" },
            { id: "threads", label: "Threads", icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 14.5c-2.48 0-4.5-2.02-4.5-4.5S9.52 7.5 12 7.5s4.5 2.02 4.5 4.5-2.02 4.5-4.5 4.5zM12 9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" },
            { id: "pinterest", label: "Pinterest", icon: "M12 2C6.48 2 2 6.48 2 12c0 4.27 2.66 7.9 6.43 9.35-.08-.8-.15-2.02.03-2.9.16-.78 1.05-4.44 1.05-4.44s-.27-.54-.27-1.33c0-1.25.72-2.18 1.63-2.18.77 0 1.14.58 1.14 1.27 0 .77-.49 1.93-.74 3-.21.87.43 1.58 1.28 1.58 1.54 0 2.73-1.62 2.73-3.96 0-2.07-1.49-3.51-3.61-3.51-2.45 0-3.89 1.84-3.89 3.73 0 .74.28 1.53.64 1.97.07.08.08.15.06.24-.07.28-.22.88-.25.99-.04.16-.14.2-.3.12-1.09-.51-1.77-2.1-1.77-3.38 0-2.75 2-5.27 5.75-5.27 3.02 0 5.37 2.15 5.37 5.03 0 3-.19 5.41-2.23 5.41-.43 0-.84-.22-.98-.48l-.27 1.03c-.1.38-.37.86-.55 1.16C10.51 21.6 11.24 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2z" },
            { id: "quora", label: "Quora", icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" },
            { id: "tiktok", label: "TikTok", icon: "M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.9-.32-1.98-.23-2.81.31-.75.42-1.24 1.16-1.35 1.99-.28 1.35.74 2.68 2.09 2.81 1.05.06 2.1-.59 2.55-1.54.22-.48.25-1.03.26-1.56.02-3.93 0-7.85.01-11.78z" },
            { id: "facebook", label: "Facebook", icon: "M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1V12h3v3h-3v6.95c5.05-.5 9-4.76 9-9.95z" },
            { id: "community", label: "Community", icon: "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" },
            { id: "summary", label: "Summary", icon: "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setMode(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border transition-all duration-200 ${mode === tab.id ? "tab-active" : "border-white/10 text-gray-400 hover:text-white hover:border-white/20 hover:bg-white/5"}`}
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
            className="input-field appearance-none py-2.5 pl-4 pr-10 text-sm font-medium text-gray-200 bg-white/5 focus:bg-white/10 border-white/10 hover:border-white/20 hover:text-white transition-all cursor-pointer rounded-xl h-auto"
            style={{ width: '160px' }}
          >
            <option value="English">🇬🇧 English</option>
            <option value="Spanish">🇪🇸 Spanish</option>
            <option value="French">🇫🇷 French</option>
            <option value="German">🇩🇪 German</option>
            <option value="Hindi">🇮🇳 Hindi</option>
            <option value="Mandarin Chinese">🇨🇳 Mandarin</option>
            <option value="Portuguese">🇵🇹 Portuguese</option>
            <option value="Italian">🇮🇹 Italian</option>
            <option value="Japanese">🇯🇵 Japanese</option>
            <option value="Korean">🇰🇷 Korean</option>
            <option value="Arabic">🇸🇦 Arabic</option>
            <option value="Russian">🇷🇺 Russian</option>
          </select>
          <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
               <polyline points="6 9 12 15 18 9" />
            </svg>
          </div>
        </div>
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit}>
        <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">
          YouTube URL
        </label>
        <div className="flex gap-3">
          <div className="flex-1 relative">
            {/* YT icon inside input */}
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white">
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
                Generate {mode === "blog" ? "Blog" : mode === "twitter" ? "Thread" : mode === "ytshort" ? "YT Short" : mode === "instagram" ? "Caption" : mode === "newsletter" ? "Newsletter" : mode === "medium" ? "Article" : "Post"}
              </>
            )}
          </button>
        </div>
        {urlError && (
          <p className="text-red-600 text-sm mt-2 flex items-center gap-1.5 animate-fade-in">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            {urlError}
          </p>
        )}
      </form>


    </div>
  );
}
