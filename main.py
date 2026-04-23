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

INSTAGRAM_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are an expert Instagram content creator who writes highly engaging captions.

Below is the transcript of a YouTube video. Based on its content, craft a 
compelling **Instagram caption**.

STRICT RULES:
- Start with an attention-grabbing hook in the first line.
- Use spacing and line breaks to make it highly readable.
- Extract 2-3 key takeaways or fascinating points from the transcript.
- Add relevant emojis to break up text and add visual interest.
- Include a clear Call to Action (e.g., "Save this post for later", "Link in bio", or a question).
- End with 5-10 relevant hashtags.
- THIS IS NOT A BLOG. Do not include a title. Just write the caption.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Instagram caption now:""",
)

NEWSLETTER_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a professional email marketer and newsletter author.

Below is the transcript of a YouTube video. Based on its content, write an 
engaging, high-value **Email Newsletter**.

Guidelines:
- Create a catchy, intriguing Subject Line at the top.
- Open with a friendly, personal greeting and hook.
- Structure the body of the email clearly, using brief paragraphs and bullet points for readability.
- Share the core value, insights, or story from the video.
- Write in a conversational, relatable tone as if writing to a friend.
- Include a clear Call to Action (e.g., "Reply to this email", "Watch the full video here").
- Sign off cleanly.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Email Newsletter now:""",
)

MEDIUM_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a top Medium.com writer who creates in-depth, thought-provoking articles.

Below is the transcript of a YouTube video. Read it carefully and produce a 
well-structured, engaging **Medium article** based on its content.

Guidelines:
- Start with a compelling title (use a markdown H1 heading) and an optional subtitle (H2).
- Write a strong hook that draws the reader in emotionally or intellectually.
- Organize the body with clear, evocative H2 subheadings.
- Weave a narrative rather than just summarizing; add insightful commentary based on the provided facts.
- Use formatting (bolding, italics, blockquotes) to highlight key points.
- Conclude with a strong, lingering thought or takeaway.
- Length: 800-1200 words if possible given the transcript length.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the full Medium article now:""",
)

THREADS_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a professional Threads (Instagram) ghostwriter who creates viral, 
conversational, and high-engagement threads.

Below is the transcript of a YouTube video. Based on its content, craft a 
compelling **Threads series**.

Guidelines:
- Start with a strong, relatable hook that stops the scroll.
- Use a conversational, "friends-chatting" tone (less formal than LinkedIn/Twitter).
- Break the content into 5-8 short, punchy posts.
- Use emojis naturally to convey emotion.
- Include a "What do you think?" style question at the end to spark comments.
- Keep it concise and mobile-friendly.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Threads series now:""",
)

PINTEREST_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a Pinterest marketing expert and SEO specialist.

Below is the transcript of a YouTube video. Based on its content, create a 
**Pinterest Pin Title and Description**.

Guidelines:
- Create 3 distinct Pin Titles (attention-grabbing and keyword-rich).
- Write an SEO-optimized Pin Description (up to 500 characters) that explains the value.
- Use natural language but include high-search-volume keywords from the transcript.
- Include a clear call to action (e.g., "Click to watch the full tutorial").
- Add 5-10 relevant hashtags.
- Suggest 3 ideas for "Text Overlay" to be used on the Pin image.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Pinterest content now:""",
)

QUORA_PROMPT = PromptTemplate(
    input_variables=["transcript", "language"],
    template="""You are a top-voted Quora contributor known for providing helpful, 
detailed, and authoritative answers.

Below is the transcript of a YouTube video. Based on its content, write a 
**Quora-style answer** to a hypothetical relevant question.

Guidelines:
- Start by stating a common question this video answers.
- Provide a detailed, well-structured answer based on the facts in the transcript.
- Use a helpful, educational, and slightly personal tone.
- Use bolding for key points and bullet points for readability.
- Conclude with a helpful summary or "Final Tip".
- DO NOT just summarize; provide value as if you are answering a real person.

---
TRANSCRIPT:
{transcript}
---

CRUCIAL RULE: Write the entire response in {language}.

Generate the Quora answer now:""",
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
