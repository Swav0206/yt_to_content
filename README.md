 YouTube Multi-Platform Content Generator

An AI-powered web application that converts YouTube videos into **Blog Posts, LinkedIn Posts, and Twitter (X) Content** with **multilingual support**.

---

📌 Overview

This project automates content repurposing by extracting transcripts from YouTube videos and transforming them into platform-specific content using **Large Language Models (LLMs)**.

It helps content creators, marketers, and professionals save time by generating ready-to-publish content instantly.

---

✨ Features

* 🎥 Convert YouTube videos into:
  * ✍️ **Blog Posts** (structured, long-form)
  * 💼 **LinkedIn Posts** (professional & engaging)
  * 🐦 **Twitter (X) Threads** (short & catchy)
  * 🎬 **TikTok Scripts** (high-energy & viral)
  * 👥 **Facebook Posts** (storytelling & community)
  * 📢 **YouTube Community Posts** (engagement-focused)
  * 📸 **Instagram Captions** (aesthetic & emojis)
  * 📧 **Email Newsletters** (personal & conversational)
  * 📝 **Medium Articles** (in-depth & intellectual)
  * 🧵 **Threads (Meta)** (conversational series)
  * 📌 **Pinterest Pins** (SEO-optimized titles & descriptions)
  * ❓ **Quora Answers** (authoritative & helpful)
  * 📊 **SEO & Summary Reports** (Keywords, Tags, & Executive Summary)
* 🌍 Multilingual content generation (12+ languages)
* ⚡ Ultra-fast inference using **Groq (LLaMA 3)**
* 🧠 Smart prompt engineering for each platform
* 💻 Premium Glassmorphic UI with dark mode
* 📥 **One-click Copy & Download** as .txt
* 🔐 Secure API key handling

---

🛠️ Tech Stack

### Frontend
* React (Vite)
* Tailwind CSS
* Framer Motion (for smooth animations)

### Backend
* FastAPI (Python)
* LangChain
* Groq LLM API (LLaMA-3-8B/70B)

### Other Tools
* YouTube Transcript API
* Python Dotenv

---

⚙️ How It Works

1. User enters a YouTube video URL
2. Backend extracts the transcript (tries English, then falls back to available)
3. AI model processes the transcript using platform-specific prompts
4. Generates optimized content for the selected platform
5. Output is rendered with markdown support and can be copied or saved

---

🚀 Installation & Setup

🔹 Clone the repository

```bash
git clone https://github.com/Swav0206/yt_to_content.git
cd yt_to_content
```

---

🔹 Backend Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Run backend:

```bash
uvicorn main:app --reload
```

---

🔹 Frontend Setup

```bash
cd frontend/ytblog
npm install
npm run dev
```

---

🌐 Usage

* Open frontend → `http://localhost:5173`
* Enter YouTube URL
* Select content type from the tab bar
* Generate content instantly
* Use "Save" to download as a text file

---

🎯 Project Highlights

* 🔄 **15+ Platform Formats**: The most comprehensive YouTube repurposing tool.
* 🌍 **Global Reach**: Generate content in Spanish, Hindi, French, and more.
* ⚡ **Performance**: Under 3 seconds generation time thanks to Groq.
* 🧩 **Full-stack**: Production-ready architecture.

---

🔮 Future Scope

* 🖼️ AI Image generation for Pinterest/Instagram (DALL-E/Stable Diffusion)
* ☁️ Cloud deployment (Vercel/Render)
* 🔐 User Authentication & History

---

👨‍💻 Author

**Sweeti Rathore**

---

