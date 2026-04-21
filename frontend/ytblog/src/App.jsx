import { useState } from "react";
import Navbar from "./components/Navbar";
import UrlInput from "./components/UrlInput";
import LoadingState from "./components/LoadingState";
import OutputPanel from "./components/OutputPanel";
import { generateBlog, generateLinkedIn, generateTwitter, generateYTShort, generateTedTalk, generateInstagram, generateNewsletter, generateMedium } from "./api";

// Feature cards for the hero section
const FEATURES = [
  {
    icon: "M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 0 0 1.946-.806 3.42 3.42 0 0 1 4.438 0 3.42 3.42 0 0 0 1.946.806 3.42 3.42 0 0 1 3.138 3.138 3.42 3.42 0 0 0 .806 1.946 3.42 3.42 0 0 1 0 4.438 3.42 3.42 0 0 0-.806 1.946 3.42 3.42 0 0 1-3.138 3.138 3.42 3.42 0 0 0-1.946.806 3.42 3.42 0 0 1-4.438 0 3.42 3.42 0 0 0-1.946-.806 3.42 3.42 0 0 1-3.138-3.138 3.42 3.42 0 0 0-.806-1.946 3.42 3.42 0 0 1 0-4.438 3.42 3.42 0 0 0 .806-1.946 3.42 3.42 0 0 1 3.138-3.138z",
    title: "AI-Powered",
    desc: "Groq's LLaMA 3 model extracts meaning & generates structured content",
    color: "#a78bfa",
    bg: "rgba(139,92,246,0.08)",
  },
  {
    icon: "M13 10V3L4 14h7v7l9-11h-7z",
    title: "Lightning Fast",
    desc: "Groq's inference engine delivers results in seconds, not minutes",
    color: "#fbbf24",
    bg: "rgba(251,191,36,0.08)",
  },
  {
    icon: "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 0 1-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z",
    title: "Tri-Format",
    desc: "Get a long-form blog, a punchy LinkedIn post, or a viral Twitter thread",
    color: "#34d399",
    bg: "rgba(52,211,153,0.08)",
  },
];

const STEPS = [
  { num: "01", text: "Paste any YouTube video URL" },
  { num: "02", text: "Choose Blog or LinkedIn format" },
  { num: "03", text: "Hit Generate and copy your content" },
];

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [currentMode, setCurrentMode] = useState("blog");

  const handleGenerate = async (url, mode, language) => {
    setIsLoading(true);
    setError("");
    setResult(null);
    setCurrentMode(mode);

    try {
      const data = mode === "blog"
        ? await generateBlog(url, language)
        : mode === "twitter"
        ? await generateTwitter(url, language)
        : mode === "ytshort"
        ? await generateYTShort(url, language)
        : mode === "tedtalk"
        ? await generateTedTalk(url, language)
        : mode === "instagram"
        ? await generateInstagram(url, language)
        : mode === "newsletter"
        ? await generateNewsletter(url, language)
        : mode === "medium"
        ? await generateMedium(url, language)
        : await generateLinkedIn(url, language);
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong generating your content.");
    } finally {
      setIsLoading(false);
    }
  };

  function handleReset() {
    setResult(null);
    setError("");
  }

  return (
    <div className="min-h-screen relative" style={{ background: '#000000' }}>
      {/* Atmospheric Background glow (softened for professional look) */}
      <div className="orb w-96 h-96 -top-20 -left-20 opacity-30"
        style={{ background: 'radial-gradient(circle, rgba(255,255,255,0.1), transparent 70%)', animationDelay: '0s' }} />
      <div className="orb w-80 h-80 top-1/3 -right-20 opacity-30"
        style={{ background: 'radial-gradient(circle, rgba(255,255,255,0.05), transparent 70%)', animationDelay: '-3s' }} />
      <div className="orb w-72 h-72 bottom-20 left-1/4 opacity-20"
        style={{ background: 'radial-gradient(circle, rgba(255,255,255,0.08), transparent 70%)', animationDelay: '-5s' }} />

      <Navbar />

      <main className="relative z-10 max-w-4xl mx-auto px-4 pt-32 pb-20">

        {/* ── Hero ── */}
        <section className="text-center mb-14 animate-fade-in-up">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full mb-6"
            style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}>
            <span className="w-2 h-2 rounded-full bg-white animate-pulse" />
            <span className="text-xs font-semibold text-gray-300 tracking-wide uppercase">AI Content Suite</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-black leading-tight mb-5 text-white"
            style={{ fontFamily: "'Outfit', sans-serif", letterSpacing: '-0.04em' }}>
            Repurpose YouTube into
            <br />
            <span className="gradient-text">Ready-to-Publish Assets</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-xl mx-auto leading-relaxed">
            Paste a link and instantly get a polished <strong className="text-white font-medium">multi-format campaign</strong> — zero editing required.
          </p>
        </section>

        {/* ── Input Card ── */}
        <section className="mb-10">
          <UrlInput onGenerate={handleGenerate} isLoading={isLoading} />
        </section>

        {/* ── Error ── */}
        {error && !isLoading && (
          <div className="glass-card p-5 mb-8 flex items-start gap-4 animate-fade-in"
            style={{ borderColor: 'rgba(239,68,68,0.5)', background: 'rgba(239,68,68,0.1)' }}>
            <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{ background: 'rgba(239,68,68,0.2)' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#ef4444">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
              </svg>
            </div>
            <div>
              <p className="font-semibold text-red-500 text-sm">Generation Failed</p>
              <p className="text-red-400 text-sm mt-1">{error}</p>
            </div>
            <button onClick={() => setError("")} className="ml-auto text-gray-500 hover:text-white transition-colors">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        )}

        {/* ── Loading ── */}
        {isLoading && (
          <section className="mb-10">
            <LoadingState mode={currentMode} />
          </section>
        )}

        {/* ── Output ── */}
        {result && !isLoading && (
          <section className="mb-14">
            <OutputPanel result={result} mode={currentMode} onReset={handleReset} />
          </section>
        )}

        {/* ── Features ── */}
        {!result && !isLoading && (
          <>
            <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12 animate-fade-in-up delay-200">
              {FEATURES.map((f) => (
                <div key={f.title} className="glass-card p-5 group hover:scale-[1.02] transition-transform duration-200">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
                    style={{ background: 'rgba(255,255,255,0.1)' }}>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                      stroke="#ffffff" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <path d={f.icon} />
                    </svg>
                  </div>
                  <p className="font-semibold text-white text-sm mb-1">{f.title}</p>
                  <p className="text-gray-400 text-xs leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </section>

            {/* How it works */}
            <section className="glass-card p-6 animate-fade-in-up delay-300">
              <h2 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-5">How it works</h2>
              <div className="flex flex-col md:flex-row gap-4">
                {STEPS.map((step, idx) => (
                  <div key={step.num} className="flex items-center gap-4 flex-1">
                    <div className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-black text-sm"
                      style={{ background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: '#ffffff' }}>
                      {step.num}
                    </div>
                    <p className="text-gray-300 text-sm">{step.text}</p>
                    {idx < STEPS.length - 1 && (
                      <svg className="hidden md:block animate-bounce-x flex-shrink-0" width="16" height="16"
                        viewBox="0 0 24 24" fill="none" stroke="#737373" strokeWidth="2">
                        <line x1="5" y1="12" x2="19" y2="12"/>
                        <polyline points="12 5 19 12 12 19"/>
                      </svg>
                    )}
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 text-center pb-8">
        <p className="text-xs text-gray-500">
          Built with <span className="text-gray-300">FastAPI</span> · <span className="text-gray-300">LangChain</span> · <span className="text-gray-300">Groq</span> · <span className="text-gray-300">React</span>
        </p>
      </footer>
    </div>
  );
}
