import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    options = ClaudeAgentOptions(
        cwd=project_root,  # Project root with .claude/skills/
        setting_sources=["user", "project"],  # Load Skills from filesystem
        allowed_tools=["Skill", "Read", "Write", "Bash"],  # Enable Skill tool
    )

    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=options,
    ):
        print(message)


asyncio.run(main())
