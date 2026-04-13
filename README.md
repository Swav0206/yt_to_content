 YouTube Multi-Platform Content Generator

An AI-powered web application that converts YouTube videos into **Blog Posts, LinkedIn Posts, and Twitter (X) Content** with **multilingual support**.

---

📌 Overview

This project automates content repurposing by extracting transcripts from YouTube videos and transforming them into platform-specific content using **Large Language Models (LLMs)**.

It helps content creators, marketers, and professionals save time by generating ready-to-publish content instantly.

---

✨ Features

* 🎥 Convert YouTube videos into:

  * ✍️ Blog posts (structured, long-form)
  * 💼 LinkedIn posts (professional & engaging)
  * 🐦 Twitter posts (short & catchy)
* 🌍 Multilingual content generation
* ⚡ Fast AI responses using Groq LLM
* 🧠 Smart prompt-based content generation
* 💻 Clean and responsive UI
* 🔐 Secure API key handling

---

🛠️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS

### Backend

* FastAPI (Python)
* LangChain
* Groq LLM API

### Other Tools

* YouTube Transcript API
* Python Dotenv

---

⚙️ How It Works

1. User enters a YouTube video URL
2. Backend extracts the transcript
3. AI model processes the transcript
4. Generates:

   * Blog content
   * LinkedIn post
   * Twitter post
5. Output is displayed on the frontend

---

🚀 Installation & Setup

🔹 Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
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
* Select content type
* Generate content instantly

---

🎯 Project Highlights

* 🔄 Multi-platform content generation
* 🌍 Multilingual support
* ⚡ Fast AI inference using Groq
* 🧩 Full-stack implementation (Frontend + Backend + AI)

---

🔮 Future Scope

* 📱 Instagram caption generation
* 🌐 More language support
* 📄 Export as PDF/Doc
* ☁️ Deployment (cloud hosting)

---

👨‍💻 Author

**Sweeti Rathore**

---

