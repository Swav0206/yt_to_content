"""
Utility functions for extracting YouTube transcripts.
Compatible with youtube-transcript-api >= 1.0 (instance-based API).
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


def extract_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from a URL.
    Supports:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://www.youtube.com/embed/VIDEO_ID
      - https://www.youtube.com/shorts/VIDEO_ID
    """
    pattern = r"(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract a valid video ID from URL: {url}")


def get_transcript(youtube_url: str) -> str:
    """
    Fetch and return the full transcript of a YouTube video as a single string.
    Uses the new instance-based youtube-transcript-api >= 1.0 API.
    Tries English first, then falls back to any available language.
    """
    video_id = extract_video_id(youtube_url)

    # youtube-transcript-api >= 1.0 requires instantiation
    ytt_api = YouTubeTranscriptApi()

    try:
        # Try English first
        fetched = ytt_api.fetch(video_id, languages=["en"])
    except NoTranscriptFound:
        try:
            # Fallback: list all available transcripts and pick any
            transcript_list = ytt_api.list(video_id)
            available = list(transcript_list)
            if not available:
                raise ValueError("No transcripts available for this video.")
            fetched = available[0].fetch()
        except (NoTranscriptFound, TranscriptsDisabled) as e:
            raise ValueError(f"No transcript available for this video: {e}")
        except Exception as e:
            raise ValueError(f"Failed to fetch transcript: {e}")
    except TranscriptsDisabled:
        raise ValueError("Transcripts/captions are disabled for this video.")
    except VideoUnavailable:
        raise ValueError("This video is unavailable or private.")
    except Exception as e:
        if "blocking requests from your IP" in str(e):
            raise ValueError("YouTube is temporarily blocking automated requests from your network. Please wait a while before trying again, or use a different network/video.")
        raise ValueError(f"Failed to fetch transcript: {e}")

    # `fetched` is a FetchedTranscript iterable of snippet dicts with 'text' key
    full_text = " ".join(snippet.text for snippet in fetched)
    return full_text
