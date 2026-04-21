export default function LoadingState({ mode }) {
  const isBlog = mode === "blog";
  const isTwitter = mode === "twitter";
  const isYTShort = mode === "ytshort";
  return (
    <div className="glass-card p-8 animate-fade-in">
      {/* Spinner + label */}
      <div className="flex flex-col items-center gap-6 mb-8">
        <div className="relative w-16 h-16">
          {/* Pulse rings */}
          <span className="absolute inset-0 rounded-full border-2 animate-ping"
            style={{ borderColor: 'rgba(255,255,255,0.5)', animationDuration: '1.2s' }} />
          <span className="absolute inset-0 rounded-full border-2 animate-ping"
            style={{ borderColor: 'rgba(255,255,255,0.3)', animationDuration: '1.8s' }} />
          {/* Core circle */}
          <div className="absolute inset-2 rounded-full flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05))' }}>
            <svg className="animate-spin-slow" width="22" height="22" viewBox="0 0 24 24" fill="none"
              stroke="#ffffff" strokeWidth="2.5">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
            </svg>
          </div>
        </div>
        <div className="text-center">
          <p className="text-white font-semibold text-lg">
            {isBlog ? "Crafting your blog post…" : isTwitter ? "Drafting your Twitter thread…" : isYTShort ? "Extracting Short points…" : "Writing your LinkedIn post…"}
          </p>
          <p className="text-gray-400 text-sm mt-1">
            Extracting transcript & generating with Groq AI
          </p>
        </div>
      </div>

      {/* Skeleton lines */}
      <div className="space-y-3">
        {isBlog ? (
          <>
            <div className="skeleton h-7 w-3/4" />
            <div className="skeleton h-4 w-full" />
            <div className="skeleton h-4 w-5/6" />
            <div className="skeleton h-4 w-4/5 mt-2" />
            <div className="skeleton h-5 w-1/2 mt-4" />
            <div className="skeleton h-4 w-full" />
            <div className="skeleton h-4 w-11/12" />
            <div className="skeleton h-4 w-3/4" />
          </>
        ) : (
          <>
            <div className="skeleton h-5 w-full" />
            <div className="skeleton h-4 w-5/6" />
            <div className="skeleton h-4 w-4/5" />
            <div className="skeleton h-4 w-3/5" />
            <div className="skeleton h-4 w-full mt-2" />
            <div className="skeleton h-4 w-2/3" />
          </>
        )}
      </div>
    </div>
  );
}
