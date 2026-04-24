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

TIKTOK_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a viral TikTok scriptwriter.
    
Below is the transcript of a YouTube video. Based on its content, craft a 
compelling, high-energy **TikTok script**.

STRICT RULES:
- Start with a massive hook (0-3 seconds) to stop the scroll.
- Use fast-paced, punchy dialogue or narration.
- Include visual cues in brackets, e.g., [Fast cut to X], [Zoom in on face].
- Add trending audio/vibe suggestions.
- End with a clear, quick CTA (e.g., "Follow for part 2").
- Keep it under 60 seconds of spoken time (roughly 120-150 words).

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the TikTok script now:""",
)

FACEBOOK_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a social media manager for Facebook.
    
Below is the transcript of a YouTube video. Based on its content, craft an 
engaging **Facebook post**.

Guidelines:
- Write a slightly longer, more storytelling-focused post compared to Twitter.
- Use a friendly, community-oriented tone.
- Highlight 3 interesting facts or stories from the transcript.
- Use emojis naturally to add personality.
- End with a question to encourage comments and shares.
- Include 3-5 relevant hashtags.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Facebook post now:""",
)

COMMUNITY_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a YouTube Channel Manager specializing in Community Tab engagement.
    
Below is the transcript of a YouTube video. Based on its content, craft a 
compelling **YouTube Community Post**.

Guidelines:
- Create an "Inside Scoop" or "Did you know?" style post.
- Summarize the most surprising or valuable part of the video in 2-3 short paragraphs.
- Use a casual, direct tone as if speaking to subscribers.
- Encourage a specific action (e.g., "Vote in the poll below", "Check out the full video").
- End with an engaging question.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the YouTube Community Post now:""",
)

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are an expert SEO specialist and content summarizer.
    
Below is the transcript of a YouTube video. Based on its content, produce a 
**Summary & SEO Keyword report**.

STRICT STRUCTURE:
1. **The Core Message** (1 sentence summary)
2. **Executive Summary** (A detailed 150-200 word summary of the main arguments)
3. **5 Key Takeaways** (Bullet points)
4. **Primary SEO Keyword** (The most relevant high-volume search term)
5. **10 Secondary SEO Keywords** (Comma-separated list)
6. **Suggested Video Tags** (Optimized for YouTube search)

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Summary & Keywords now:""",
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
instagram_chain = INSTAGRAM_PROMPT | llm | output_parser
newsletter_chain = NEWSLETTER_PROMPT | llm | output_parser
medium_chain = MEDIUM_PROMPT | llm | output_parser
threads_chain = THREADS_PROMPT | llm | output_parser
pinterest_chain = PINTEREST_PROMPT | llm | output_parser
quora_chain = QUORA_PROMPT | llm | output_parser
tiktok_chain = TIKTOK_PROMPT | llm | output_parser
facebook_chain = FACEBOOK_PROMPT | llm | output_parser
community_chain = COMMUNITY_PROMPT | llm | output_parser
summary_chain = SUMMARY_PROMPT | llm | output_parser

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

class InstagramResponse(BaseModel):
    video_url: str
    instagram_post: str

class NewsletterResponse(BaseModel):
    video_url: str
    newsletter_post: str

class MediumResponse(BaseModel):
    video_url: str
    medium_post: str

class ThreadsResponse(BaseModel):
    video_url: str
    threads_post: str

class PinterestResponse(BaseModel):
    video_url: str
    pinterest_post: str

class QuoraResponse(BaseModel):
    video_url: str
    quora_post: str

class TikTokResponse(BaseModel):
    video_url: str
    tiktok_post: str

class FacebookResponse(BaseModel):
    video_url: str
    facebook_post: str

class CommunityResponse(BaseModel):
    video_url: str
    community_post: str

class SummaryResponse(BaseModel):
    video_url: str
    summary_post: str

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


@app.post("/instagram", response_model=InstagramResponse, tags=["Content Generation"])
async def generate_instagram(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate an Instagram caption.
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        instagram_post = instagram_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating Instagram caption: {e}",
        )

    if not instagram_post or not instagram_post.strip():
        raise HTTPException(status_code=500, detail="Instagram caption generation returned empty content.")

    return InstagramResponse(video_url=request.url, instagram_post=instagram_post.strip())


@app.post("/newsletter", response_model=NewsletterResponse, tags=["Content Generation"])
async def generate_newsletter(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate an Email Newsletter.
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        newsletter_post = newsletter_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating Email Newsletter: {e}",
        )

    if not newsletter_post or not newsletter_post.strip():
        raise HTTPException(status_code=500, detail="Email Newsletter generation returned empty content.")

    return NewsletterResponse(video_url=request.url, newsletter_post=newsletter_post.strip())


@app.post("/medium", response_model=MediumResponse, tags=["Content Generation"])
async def generate_medium(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a Medium article.
    """
    transcript = fetch_transcript_safe(request.url)

    try:
        medium_post = medium_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM error while generating Medium article: {e}",
        )

    if not medium_post or not medium_post.strip():
        raise HTTPException(status_code=500, detail="Medium article generation returned empty content.")

    return MediumResponse(video_url=request.url, medium_post=medium_post.strip())


@app.post("/threads", response_model=ThreadsResponse, tags=["Content Generation"])
async def generate_threads(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a Threads series.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        threads_post = threads_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating Threads: {e}")
    return ThreadsResponse(video_url=request.url, threads_post=threads_post.strip())


@app.post("/pinterest", response_model=PinterestResponse, tags=["Content Generation"])
async def generate_pinterest(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate Pinterest content.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        pinterest_post = pinterest_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating Pinterest: {e}")
    return PinterestResponse(video_url=request.url, pinterest_post=pinterest_post.strip())


@app.post("/quora", response_model=QuoraResponse, tags=["Content Generation"])
async def generate_quora(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a Quora answer.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        quora_post = quora_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating Quora answer: {e}")
    return QuoraResponse(video_url=request.url, quora_post=quora_post.strip())


@app.post("/tiktok", response_model=TikTokResponse, tags=["Content Generation"])
async def generate_tiktok(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a TikTok script.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        tiktok_post = tiktok_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating TikTok: {e}")
    return TikTokResponse(video_url=request.url, tiktok_post=tiktok_post.strip())


@app.post("/facebook", response_model=FacebookResponse, tags=["Content Generation"])
async def generate_facebook(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a Facebook post.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        facebook_post = facebook_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating Facebook: {e}")
    return FacebookResponse(video_url=request.url, facebook_post=facebook_post.strip())


@app.post("/community", response_model=CommunityResponse, tags=["Content Generation"])
async def generate_community(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate a YouTube Community post.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        community_post = community_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating Community Post: {e}")
    return CommunityResponse(video_url=request.url, community_post=community_post.strip())


@app.post("/summary", response_model=SummaryResponse, tags=["Content Generation"])
async def generate_summary(request: URLRequest):
    """
    Given a YouTube video URL, extract its transcript and generate an SEO Summary report.
    """
    transcript = fetch_transcript_safe(request.url)
    try:
        summary_post = summary_chain.invoke({"transcript": transcript, "language": request.language})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error while generating Summary: {e}")
    return SummaryResponse(video_url=request.url, summary_post=summary_post.strip())
