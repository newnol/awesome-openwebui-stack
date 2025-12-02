"""
title: AutoTool Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.2.0
required_open_webui_version: 0.5.0
"""

from pydantic import BaseModel, Field
from typing import Callable, Awaitable, Any, Optional, Literal
import json
import re

# Updated imports
from open_webui.models.users import Users
from open_webui.models.tools import Tools
from open_webui.models.models import Models
from open_webui.utils.chat import generate_chat_completion  # Use the lightweight option
from open_webui.utils.misc import get_last_user_message


class Filter:
    class Valves(BaseModel):
        template: str = Field(
            default="""Tools: {{TOOLS}}
If a tool doesn't match the query, return an empty list []. Otherwise, return a list of matching tool IDs in the format ["tool_id"]. Select multiple tools if applicable. Only return the list. Do not return any other text only the list. Review the entire chat history to ensure the selected tool matches the context. If unsure, default to an empty list []. Use tools conservatively."""
        )
        status: bool = Field(default=False)
        pass

    def __init__(self):
        self.valves = self.Valves()
        pass

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __request__: Any,  # New requirement in version 0.5
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        messages = body["messages"]
        user_message = get_last_user_message(messages)

        if self.valves.status:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Finding the right tools...",
                        "done": False,
                    },
                }
            )

        all_tools = [
            {"id": tool.id, "description": tool.meta.description}
            for tool in Tools.get_tools()
        ]
        available_tool_ids = (
            __model__.get("info", {}).get("meta", {}).get("toolIds", [])
        )
        # Use set for O(1) lookup instead of O(n) list membership check
        available_tool_ids_set = set(available_tool_ids)
        available_tools = [
            tool for tool in all_tools if tool["id"] in available_tool_ids_set
        ]
        system_prompt = self.valves.template.replace("{{TOOLS}}", str(available_tools))
        # Optimize: take last 4 messages first, then reverse (more efficient than reversing entire list)
        recent_messages = messages[-4:] if len(messages) >= 4 else messages
        prompt = (
            "History:\n"
            + "\n".join(
                [
                    f"{message['role'].upper()}: \"\"\"{message['content']}\"\"\""
                    for message in reversed(recent_messages)
                ]
            )
            + f"\nQuery: {user_message}"
        )
        payload = {
            "model": body["model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

        try:
            user = Users.get_user_by_id(__user__["id"])
            # Updated to use the direct successor function
            response = await generate_chat_completion(
                request=__request__, form_data=payload, user=user
            )
            content = response["choices"][0]["message"]["content"]
            # Parse the function response
            if content is not None:
                print(f"content: {content}")
                # Extract JSON array pattern (non-greedy match)
                pattern = r"\[.*?\]"
                match = re.search(pattern, content)
                if match:
                    content = match.group(0)
                    # Try parsing as-is first (handles double quotes)
                    try:
                        result = json.loads(content)
                    except json.JSONDecodeError:
                        # If it fails, try replacing single quotes with double quotes
                        # This handles cases where LLM returns ['tool_id'] instead of ["tool_id"]
                        content = content.replace("'", '"')
                        try:
                            result = json.loads(content)
                        except json.JSONDecodeError:
                            # If still fails, return empty list as fallback
                            result = []
                else:
                    # Fallback: try to parse entire content as JSON
                    try:
                        result = json.loads(content.strip())
                    except json.JSONDecodeError:
                        result = []
                if isinstance(result, list) and len(result) > 0:
                    body["tool_ids"] = result
                    if self.valves.status:
                        await __event_emitter__(
                            {
                                "type": "status",
                                "data": {
                                    "description": f"Found matching tools: {', '.join(result)}",
                                    "done": True,
                                },
                            }
                        )
                else:
                    if self.valves.status:
                        await __event_emitter__(
                            {
                                "type": "status",
                                "data": {
                                    "description": "No matching tools found.",
                                    "done": True,
                                },
                            }
                        )
        except Exception as e:
            print(e)
            if self.valves.status:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Error processing request: {e}",
                            "done": True,
                        },
                    }
                )
            pass
        return body
