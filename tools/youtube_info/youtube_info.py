"""
title: YouTube Video Info Extractor

author: newnol

author_url: https://newnol.io.vn

git_url: https://github.com/newnol/open-webui-tools

description: A tool that extracts title and full description from YouTube videos by accessing the ytInitialPlayerResponse JavaScript variable using Selenium.

requirements: selenium

version: 0.1.0

license: MIT
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional
import asyncio

from pydantic import BaseModel, Field


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


def _fetch_youtube_info_sync(url: str, headless: bool = True) -> Dict[str, Optional[str]]:
    """
    Core sync helper that uses Selenium to extract YouTube video info.
    
    :param url: YouTube video URL
    :param headless: Whether to run Chrome in headless mode
    :return: Dictionary with 'title' and 'description' keys
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Extract ytInitialPlayerResponse JavaScript variable
        # This contains all video metadata including full description
        player_data = driver.execute_script("return ytInitialPlayerResponse;")
        
        if not player_data:
            return {"title": None, "description": None}
        
        # Parse JSON data
        video_details = player_data.get('videoDetails', {})
        
        title = video_details.get('title')
        # shortDescription contains the full description text (not truncated)
        description = video_details.get('shortDescription')
        
        return {
            "title": title,
            "description": description
        }
        
    except Exception as e:
        raise RuntimeError(f"Failed to fetch YouTube info: {str(e)}")
    finally:
        if driver:
            driver.quit()


class Tools:
    class Valves(BaseModel):
        CITATION: bool = Field(
            default=True,
            description="True or false for citation (not used yet)."
        )

    class UserValves(BaseModel):
        HEADLESS_MODE: bool = Field(
            default=True,
            description="Run Chrome browser in headless mode (no GUI)."
        )

    def __init__(self):
        self.valves = self.Valves()
        self.citation = self.valves.CITATION

    async def get_youtube_info(
        self,
        url: str,
        __event_emitter__: Callable[[dict], Any] | None = None,
        __user__: dict = {},
    ) -> str:
        """
        Extracts title and full description from a YouTube video.
        
        This tool accesses the YouTube page using Selenium and extracts
        information from the ytInitialPlayerResponse JavaScript variable,
        which contains the complete video metadata including the full
        description text (not truncated like in the HTML).

        :param url: The YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
        :return: Formatted string containing title and description, or an error message.
        """
        emitter = EventEmitter(__event_emitter__)
        
        if "valves" not in __user__:
            __user__["valves"] = self.UserValves()
        
        try:
            await emitter.progress_update(f"Đang truy cập: {url}")
            
            # Validation
            if not url:
                raise ValueError("URL không được để trống")
            
            if "youtube.com" not in url and "youtu.be" not in url:
                raise ValueError("URL không hợp lệ. Vui lòng cung cấp URL YouTube hợp lệ.")
            
            # Get headless mode setting
            headless = __user__["valves"].HEADLESS_MODE
            
            await emitter.progress_update("Đang lấy thông tin video từ YouTube...")
            
            # Run blocking Selenium operations in a separate thread
            result = await asyncio.to_thread(
                _fetch_youtube_info_sync,
                url,
                headless
            )
            
            title = result.get("title")
            description = result.get("description")
            
            if not title:
                raise RuntimeError("Không thể lấy được title của video")
            
            # Format output
            output_lines = [
                "=" * 50,
                f"Title: {title}",
                "=" * 50,
            ]
            
            if description:
                output_lines.append("\nDescription (Full text từ biến JS):")
                output_lines.append("-" * 50)
                output_lines.append(description)
            else:
                output_lines.append("\nDescription: Không có mô tả")
            
            output_text = "\n".join(output_lines)
            
            await emitter.success_update("Đã lấy thông tin video thành công!")
            return output_text
            
        except Exception as e:
            error_message = f"Lỗi: {str(e)}"
            await emitter.error_update(error_message)
            return error_message


if __name__ == "__main__":
    # Simple CLI usage for quick testing
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python youtube_info.py <youtube_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    async def test():
        tools = Tools()
        result = await tools.get_youtube_info(url)
        print(result)
    
    asyncio.run(test())

