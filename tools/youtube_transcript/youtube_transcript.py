"""
title: Youtube Transcript Provider (youtube-transcript-api)

author: newnol

author_url: https://newnol.io.vn

git_url: https://github.com/newnol/open-webui-tools

description: A tool that returns the full YouTube transcript (using youtube-transcript-api) for a given YouTube URL or video ID.

requirements: youtube-transcript-api

version: 0.1.0

license: MIT
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional
import re
import asyncio

from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


YOUTUBE_ID_REGEX = re.compile(
    r"(?:v=|youtu\.be/|youtube\.com/embed/|shorts/)([A-Za-z0-9_-]{11})"
)


class EventEmitter:
    def __init__(self, event_emitter: Callable[[dict], Any] | None = None):
        self.event_emitter = event_emitter

    async def progress_update(self, description: str) -> None:
        await self.emit(description)

    async def error_update(self, description: str) -> None:
        await self.emit(description, "error", True)

    async def success_update(self, description: str) -> None:
        await self.emit(description, "success", True)

    async def emit(
        self,
        description: str = "Unknown State",
        status: str = "in_progress",
        done: bool = False,
    ) -> None:
        if self.event_emitter:
            await self.event_emitter(
                {
                    "type": "status",
                    "data": {
                        "status": status,
                        "description": description,
                        "done": done,
                    },
                }
            )


def extract_video_id(url_or_id: str) -> str:
    """
    Extract a YouTube video ID from a full URL or return the input if it already
    looks like a bare 11-character ID.
    """
    candidate = url_or_id.strip()
    if len(candidate) == 11 and re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
        return candidate

    match = YOUTUBE_ID_REGEX.search(candidate)
    if not match:
        raise ValueError("Could not extract video ID from the provided URL/ID.")
    return match.group(1)


def _fetch_youtube_transcript_structured(
    url_or_id: str,
    language: str = "vi",
    fallback_languages: Optional[List[str]] = None,
) -> Dict[str, object]:
    """
    Core sync helper that talks to youtube-transcript-api and returns a structured dict.
    """
    if fallback_languages is None:
        # Try preferred language, then English as a common fallback.
        fallback_languages = [language, "en"]
    else:
        # Ensure preferred language is first in the list.
        if language not in fallback_languages:
            fallback_languages = [language] + fallback_languages

    video_id = extract_video_id(url_or_id)

    last_error: Optional[Exception] = None
    transcript_data = None
    used_language = None

    # According to the official docs:
    #   ytt_api = YouTubeTranscriptApi()
    #   ytt_api.fetch(video_id)
    # See: https://github.com/jdepoix/youtube-transcript-api
    ytt_api = YouTubeTranscriptApi()

    for lang in fallback_languages:
        try:
            # In the current library version, .fetch returns a list of
            # FetchedTranscriptSnippet objects (not plain dicts).
            transcript_data = ytt_api.fetch(video_id, languages=[lang])
            used_language = lang
            break
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            last_error = e
            continue

    if transcript_data is None:
        msg = "Transcript not found for this video."
        if last_error is not None:
            msg += f" Reason: {last_error}"
        raise RuntimeError(msg)

    # Normalize to list[dict] for easier use in Open WebUI / JSON.
    segments = []
    for snippet in transcript_data:
        # FetchedTranscriptSnippet has attributes: text, start, duration
        segments.append(
            {
                "start": getattr(snippet, "start", None),
                "duration": getattr(snippet, "duration", None),
                "text": getattr(snippet, "text", ""),
            }
        )

    full_text = "\n".join(seg["text"] for seg in segments if seg["text"])

    return {
        "video_id": video_id,
        "language": used_language,
        "segments": segments,
        "full_text": full_text,
    }


class Tools:
    class Valves(BaseModel):
        CITATION: bool = Field(
            default=True, description="True or false for citation (not used yet)."
        )

    class UserValves(BaseModel):
        TRANSCRIPT_LANGUAGE: str = Field(
            default="vi,en",
            description="Comma-separated list of languages from highest priority to lowest.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.citation = self.valves.CITATION

    async def get_youtube_transcript(
        self,
        url: str,
        __event_emitter__: Callable[[dict], Any] | None = None,
        __user__: dict = {},
    ) -> str:
        """
        Provides the full transcript of a YouTube video.

        Only use if the user supplied a valid YouTube URL or video ID.

        :param url: The URL or ID of the YouTube video.
        :return: The full transcript text of the YouTube video, or an error message.
        """
        emitter = EventEmitter(__event_emitter__)

        if "valves" not in __user__:
            __user__["valves"] = self.UserValves()

        try:
            await emitter.progress_update(f"Validating URL/ID: {url}")

            if not url:
                raise ValueError("Invalid YouTube URL/ID (empty).")
            elif "dQw4w9WgXcQ" in url:
                raise ValueError("Rick Roll URL provided... is that what you want?")

            # Parse user language preferences
            languages = [
                item.strip()
                for item in __user__["valves"].TRANSCRIPT_LANGUAGE.split(",")
                if item.strip()
            ]
            if not languages:
                languages = ["vi", "en"]

            await emitter.progress_update(
                f"Fetching transcript (preferred languages: {', '.join(languages)})"
            )

            # Run blocking HTTP call in a separate thread to avoid blocking event loop.
            data = await asyncio.to_thread(
                _fetch_youtube_transcript_structured,
                url,
                languages[0],
                languages,
            )

            transcript_text = data.get("full_text", "")
            if not transcript_text:
                raise RuntimeError("Transcript is empty.")

            await emitter.success_update("Transcript retrieved successfully!")
            return transcript_text

        except Exception as e:
            error_message = f"Error: {str(e)}"
            await emitter.error_update(error_message)
            return error_message


if __name__ == "__main__":
    # Simple CLI usage for quick testing:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Fetch YouTube transcript.")
    parser.add_argument("url_or_id", help="YouTube URL or video ID")
    parser.add_argument(
        "--language",
        "-l",
        default="vi",
        help="Preferred language code (default: vi)",
    )
    args = parser.parse_args()

    result = _fetch_youtube_transcript_structured(args.url_or_id, language=args.language)
    print(json.dumps(result, ensure_ascii=False, indent=2))

