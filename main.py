"""
FastAPI backend for YouTube URL → Blog Post & LinkedIn Post generation.

Endpoints:
    POST /blog      - Generate a blog post from a YouTube video URL
    POST /linkedin  - Generate a LinkedIn post from a YouTube video URL
"""

import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils import get_transcript

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv(find_dotenv(), override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY is not set. Please add it to your .env file.")

# ---------------------------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="YT Content Generator API",
    description="Generates blog posts and LinkedIn posts from YouTube video URLs using Groq LLM.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# LLM initialization
# ---------------------------------------------------------------------------
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    groq_api_key=GROQ_API_KEY,
    temperature=0.7,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_TRANSCRIPT_CHARS = 60000  # Safe limit for Groq API payload and context window

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
BLOG_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are an expert content writer and blogger.

Below is the transcript of a YouTube video. Read it carefully and produce a 
well-structured, engaging **blog post** based on its content.

Guidelines:
- Start with a compelling title (use a markdown H1 heading)
- Write a short introduction paragraph that hooks the reader
- Organize the body with clear H2 subheadings for each main topic covered
- Use bullet points or numbered lists where appropriate
- End with a thoughtful conclusion / key takeaways section
- Write in a professional yet conversational tone
- Length: 600-900 words

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the full blog post now:""",
)

LINKEDIN_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a professional LinkedIn content creator who writes viral posts.

Below is the transcript of a YouTube video. Based on its content, craft a 
compelling **LinkedIn post**.

STRICT RULES:
- DO NOT use markdown headings (H1, H2, etc).
- Use line breaks and emojis for visual structure.
- Open with a strong hook sentence.
- Share 3-5 key insights in punchy paragraphs.
- Add relevant hashtags.
- THIS IS NOT A BLOG. Do not include a title. Just start with the hook.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the LinkedIn post now:""",
)

TWITTER_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a professional Twitter/X ghostwriter who creates viral, 
engaging threads and posts.

Below is the transcript of a YouTube video. Based on its content, craft a 
compelling **Twitter post or thread**.

Guidelines:
- If the content is short, write a single punchy tweet. If long, write a 3-5 tweet thread.
- Open with an attention-grabbing hook.
- Use bullet points or short sentences for readability.
- Add relevant emojis but keep it professional.
- End with a call to action or engaging question.
- Include 2-4 relevant hashtags.
- Ensure each tweet stays under the 280-character mental model (be concise).

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Twitter post/thread now:""",
)

YTSHORT_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are an expert YouTube Shorts scriptwriter and content summarizer.

Below is the transcript of a YouTube video. Based on its content, extract the most 
engaging, high-retention main points to create a compelling **YouTube Short script**.

STRICT GUIDELINES:
- Start with a highly engaging Hook (the first 3 seconds of the short).
- Extract 3-4 punchy, high-value main points from the video.
- Keep sentences short, fast-paced, and easy to speak.
- Add ideas for B-Roll or visual cues in brackets, e.g., [Show graphic of X].
- End with a strong Call to Action (CTA).
- DO NOT write a blog or article. This should look like a video script.
- Keep the total word count under 150 words.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the YouTube Short script now:""",
)

TED_TALK_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a world-class speech analyst and curator of "Ideas Worth Spreading."

Below is the transcript of a YouTube video. Your goal is to distill the core message into a 
compelling **TED Talk style summary**.

Guidelines:
- Start with the "Big Idea" (markdown H1)
- Identify 3 "Takeaway Pillars": The most educational or inspirational points.
- Use a narrative storytelling flow.
- Include a "Call to Thought": A final challenge for the audience.
- DO NOT write a blog post. No "In this video" intros. Keep it intellectual and inspiring.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the TED Talk summary now:""",
)

# ---------------------------------------------------------------------------
# LCEL Chains (Prompt | LLM | OutputParser)
# ---------------------------------------------------------------------------
output_parser = StrOutputParser()
blog_chain = BLOG_PROMPT | llm | output_parser
linkedin_chain = LINKEDIN_PROMPT | llm | output_parser
twitter_chain = TWITTER_PROMPT | llm | output_parser
ytshort_chain = YTSHORT_PROMPT | llm | output_parser
tedtalk_chain = TED_TALK_PROMPT | llm | output_parser

# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class URLRequest(BaseModel):
    url: str
    language: str = "English"

class BlogResponse(BaseModel):
    video_url: str
    blog_post: str

class LinkedInResponse(BaseModel):
    video_url: str
    linkedin_post: str

class TwitterResponse(BaseModel):
    video_url: str
    twitter_post: str

class YTShortResponse(BaseModel):
    video_url: str
    ytshort_post: str

class TedTalkResponse(BaseModel):
    video_url: str
    tedtalk_post: str

# ---------------------------------------------------------------------------
# Helper: fetch transcript with error handling
# ---------------------------------------------------------------------------
def fetch_transcript_safe(url: str) -> str:
    try:
        transcript = get_transcript(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while fetching transcript: {e}",
        )

    if not transcript or len(transcript.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail="Transcript is too short or empty to generate content.",
        )

    # Truncate if transcript is too long to avoid LLM context or API payload limits
    if len(transcript) > MAX_TRANSCRIPT_CHARS:
        half = MAX_TRANSCRIPT_CHARS // 2
        transcript = (
            transcript[:half]
            + "\n\n... [TRANSCRIPT TRUNCATED DUE TO LENGTH] ...\n\n"
            + transcript[-half:]
        )

    return transcript

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "YT Content Generator API is running."}


@app.post("/blog", response_model=BlogResponse, tags=["Content Generation"])
async def generate_blog(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a blog post.

    **Request body:**
    ```json
    { "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ```
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        blog_post = blog_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating blog post: {e}",
        )

    if not blog_post or not blog_post.strip():
        raise HTTPException(status_code=500, detail="Blog post generation returned empty content.")

    return BlogResponse(video_url=request.url, blog_post=blog_post.strip())


@app.post("/linkedin", response_model=LinkedInResponse, tags=["Content Generation"])
async def generate_linkedin(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a LinkedIn post.

    **Request body:**
    ```json
    { "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ```
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        linkedin_post = linkedin_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating LinkedIn post: {e}",
        )

    if not linkedin_post or not linkedin_post.strip():
        raise HTTPException(status_code=500, detail="LinkedIn post generation returned empty content.")

    return LinkedInResponse(video_url=request.url, linkedin_post=linkedin_post.strip())


@app.post("/twitter", response_model=TwitterResponse, tags=["Content Generation"])
async def generate_twitter(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a Twitter post.

    **Request body:**
    ```json
    { "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ```
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        twitter_post = twitter_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating Twitter post: {e}",
        )

    if not twitter_post or not twitter_post.strip():
        raise HTTPException(status_code=500, detail="Twitter post generation returned empty content.")

    return TwitterResponse(video_url=request.url, twitter_post=twitter_post.strip())

@app.post("/ytshort", response_model=YTShortResponse, tags=["Content Generation"])
async def generate_ytshort(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a YouTube Short script.

    **Request body:**
    ```json
    { "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
    ```
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        ytshort_post = ytshort_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating YT Short points: {e}",
        )

    if not ytshort_post or not ytshort_post.strip():
        raise HTTPException(status_code=500, detail="YT Short generation returned empty content.")

    return YTShortResponse(video_url=request.url, ytshort_post=ytshort_post.strip())

@app.post("/tedtalk", response_model=TedTalkResponse, tags=["Content Generation"])
async def generate_tedtalk(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a TED Talk style summary.
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        tedtalk_post = tedtalk_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating TED Talk summary: {e}",
        )

    if not tedtalk_post or not tedtalk_post.strip():
        raise HTTPException(status_code=500, detail="TED Talk generation returned empty content.")

    return TedTalkResponse(video_url=request.url, tedtalk_post=tedtalk_post.strip())
