const API_BASE = "http://localhost:8000";

export async function generateBlog(url, language = "English") {
  const res = await fetch(`${API_BASE}/blog`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json(); // { video_url, blog_post }
}

export async function generateLinkedIn(url, language = "English") {
  const res = await fetch(`${API_BASE}/linkedin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json(); // { video_url, linkedin_post }
}

export async function generateTwitter(url, language = "English") {
  const res = await fetch(`${API_BASE}/twitter`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json(); // { video_url, twitter_post }
}

export async function generateYTShort(url, language = "English") {
  const res = await fetch(`${API_BASE}/ytshort`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json(); // { video_url, ytshort_post }
}

export async function generateTedTalk(url, language = "English") {
  const res = await fetch(`${API_BASE}/tedtalk`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, language }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json(); // { video_url, tedtalk_post }
}
