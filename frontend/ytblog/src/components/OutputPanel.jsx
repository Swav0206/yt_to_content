import { useState } from "react";

function renderMarkdown(text) {
  // A light client-side markdown renderer
  const lines = text.split("\n");
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("# ")) {
      elements.push(<h1 key={i}>{line.slice(2)}</h1>);
    } else if (line.startsWith("## ")) {
      elements.push(<h2 key={i}>{line.slice(3)}</h2>);
    } else if (line.startsWith("### ")) {
      elements.push(<h2 key={i} style={{ fontSize: '1.05rem' }}>{line.slice(4)}</h2>);
    } else if (line.startsWith("- ") || line.startsWith("* ")) {
      const items = [];
      while (i < lines.length && (lines[i].startsWith("- ") || lines[i].startsWith("* "))) {
        items.push(<li key={i}>{renderInline(lines[i].slice(2))}</li>);
        i++;
      }
      elements.push(<ul key={`ul-${i}`}>{items}</ul>);
      continue;
    } else if (/^\d+\. /.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(<li key={i}>{renderInline(lines[i].replace(/^\d+\. /, ""))}</li>);
        i++;
      }
      elements.push(<ol key={`ol-${i}`}>{items}</ol>);
      continue;
    } else if (line.startsWith("---") || line.startsWith("***")) {
      elements.push(<hr key={i} style={{ borderColor: 'rgba(255,255,255,0.15)', margin: '20px 0' }} />);
    } else if (line.trim() !== "") {
      elements.push(<p key={i}>{renderInline(line)}</p>);
    }
    i++;
  }
  return elements;
}

function renderInline(text) {
  // Bold: **text**
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

export default function OutputPanel({ result, mode, onReset }) {
  const [copied, setCopied] = useState(false);

  // Configuration for different modes to simplify scaling
  const MODE_CONFIG = {
    blog: {
      label: "Blog Post",
      content: result.blog_post,
      isProse: true,
      icon: "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
    },
    medium: {
      label: "Medium Article",
      content: result.medium_post,
      isProse: true,
      icon: "M2.75 3h18.5v18H2.75V3z"
    },
    twitter: {
      label: "Twitter Thread",
      content: result.twitter_post,
      isTwitter: true,
      icon: "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"
    },
    ytshort: {
      label: "YT Short Script",
      content: result.ytshort_post,
      isProse: true,
      icon: "M10 16.5l6-4.5-6-4.5v9zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
    },
    tedtalk: {
      label: "TED Talk Summary",
      content: result.tedtalk_post,
      isProse: true,
      icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
    },
    instagram: {
      label: "Instagram Caption",
      content: result.instagram_post,
      icon: "M7.8 2h8.4C19.4 2 22 4.6 22 7.8v8.4a5.8 5.8 0 0 1-5.8 5.8H7.8C4.6 22 2 19.4 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2zm-.2 2A3.6 3.6 0 0 0 4 7.6v8.8C4 18.4 5.6 20 7.6 20h8.8a3.6 3.6 0 0 0 3.6-3.6V7.6C20 5.6 18.4 4 16.4 4H7.6zm9.65 1.5a1.25 1.25 0 0 1 1.25 1.25A1.25 1.25 0 0 1 17.25 8 1.25 1.25 0 0 1 16 6.75a1.25 1.25 0 0 1 1.25-1.25zM12 7a5 5 0 0 1 5 5 5 5 0 0 1-5 5 5 5 0 0 1-5-5 5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3z"
    },
    newsletter: {
      label: "Email Newsletter",
      content: result.newsletter_post,
      isProse: true,
      icon: "M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6zm-2 0l-8 5-8-5h16zm0 12H4V8l8 5 8-5v10z"
    },
    threads: {
      label: "Threads Series",
      content: result.threads_post,
      icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 14.5c-2.48 0-4.5-2.02-4.5-4.5S9.52 7.5 12 7.5s4.5 2.02 4.5 4.5-2.02 4.5-4.5 4.5zM12 9c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"
    },
    pinterest: {
      label: "Pinterest Content",
      content: result.pinterest_post,
      isProse: true,
      icon: "M12 2C6.48 2 2 6.48 2 12c0 4.27 2.66 7.9 6.43 9.35-.08-.8-.15-2.02.03-2.9.16-.78 1.05-4.44 1.05-4.44s-.27-.54-.27-1.33c0-1.25.72-2.18 1.63-2.18.77 0 1.14.58 1.14 1.27 0 .77-.49 1.93-.74 3-.21.87.43 1.58 1.28 1.58 1.54 0 2.73-1.62 2.73-3.96 0-2.07-1.49-3.51-3.61-3.51-2.45 0-3.89 1.84-3.89 3.73 0 .74.28 1.53.64 1.97.07.08.08.15.06.24-.07.28-.22.88-.25.99-.04.16-.14.2-.3.12-1.09-.51-1.77-2.1-1.77-3.38 0-2.75 2-5.27 5.75-5.27 3.02 0 5.37 2.15 5.37 5.03 0 3-.19 5.41-2.23 5.41-.43 0-.84-.22-.98-.48l-.27 1.03c-.1.38-.37.86-.55 1.16C10.51 21.6 11.24 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2z"
    },
    quora: {
      label: "Quora Answer",
      content: result.quora_post,
      isProse: true,
      icon: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
    },
    tiktok: {
      label: "TikTok Script",
      content: result.tiktok_post,
      icon: "M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.9-.32-1.98-.23-2.81.31-.75.42-1.24 1.16-1.35 1.99-.28 1.35.74 2.68 2.09 2.81 1.05.06 2.1-.59 2.55-1.54.22-.48.25-1.03.26-1.56.02-3.93 0-7.85.01-11.78z"
    },
    facebook: {
      label: "Facebook Post",
      content: result.facebook_post,
      icon: "M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1V12h3v3h-3v6.95c5.05-.5 9-4.76 9-9.95z"
    },
    community: {
      label: "Community Post",
      content: result.community_post,
      icon: "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"
    },
    summary: {
      label: "SEO Summary",
      content: result.summary_post,
      isProse: true,
      icon: "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
    },
    linkedin: {
      label: "LinkedIn Post",
      content: result.linkedin_post,
      icon: "M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z M4 6a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"
    }
  };

  const currentConfig = MODE_CONFIG[mode] || MODE_CONFIG.linkedin;
  const { label, content, icon, isProse, isTwitter } = currentConfig;

  function handleCopy() {
    navigator.clipboard.writeText(content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  function handleDownload() {
    const element = document.createElement("a");
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = `${label.toLowerCase().replace(/\s+/g, '_')}_content.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }

  return (
    <div className="glass-card overflow-hidden animate-fade-in-up" id="output-panel">
      {/* Header bar */}
      <div className="flex items-center justify-between px-6 py-4"
        style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.03)' }}>
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #333, #111)', border: '1px solid rgba(255,255,255,0.2)' }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
              <path d={icon} />
            </svg>
          </div>
          <div>
            <p className="text-sm font-semibold text-white">
              {label}
            </p>
            <p className="text-xs text-gray-400 truncate max-w-xs" title={result.video_url}>
              {result.video_url}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {/* Copy button */}
          <button
            id="copy-btn"
            onClick={handleCopy}
            className="btn-ghost"
          >
            {copied ? (
              <>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#34d399" strokeWidth="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                <span style={{ color: '#34d399' }}>Copied!</span>
              </>
            ) : (
              <>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                </svg>
                Copy
              </>
            )}
          </button>
          {/* Download button */}
          <button
            id="download-btn"
            onClick={handleDownload}
            className="btn-ghost"
            title="Download as .txt"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4M7 10l5 5 5-5M12 15V3"/>
            </svg>
            Save
          </button>
          {/* Generate another */}
          <button
            id="generate-another-btn"
            onClick={onReset}
            className="btn-ghost"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-6.21"/>
            </svg>
            New
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 custom-scroll" style={{ maxHeight: '520px', overflowY: 'auto' }}>
        {isProse ? (
          <div className="prose-content">
            {renderMarkdown(content)}
          </div>
        ) : isTwitter ? (
          <div className="twitter-content whitespace-pre-wrap text-gray-200 leading-relaxed font-sans mt-2">
            {content}
          </div>
        ) : (
          <div className="linkedin-content whitespace-pre-wrap text-gray-200 leading-relaxed mt-2">
            {content}
          </div>
        )}
      </div>

      {/* Footer stats */}
      <div className="px-6 py-3 flex items-center gap-4"
        style={{ borderTop: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.03)' }}>
        <span className="text-xs text-gray-400 flex items-center gap-1">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-4H7l5-8v4h4l-5 8z"/>
          </svg>
          {content.split(/\s+/).length} words
        </span>
        <span className="text-xs text-gray-400 flex items-center gap-1">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/>
          </svg>
          {content.length} chars
        </span>
        <div className="ml-auto">
          <span className="text-xs px-2 py-1 rounded-full font-medium" style={{ background: 'rgba(255,255,255,0.1)', color: '#ffffff' }}>
            ✓ Generated by Groq AI
          </span>
        </div>
      </div>
    </div>
  );
}
