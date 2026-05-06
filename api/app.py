import asyncio
import logging
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, query

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Claude SDK Agent")


class QueryRequest(BaseModel):
    prompt: str
    allowed_tools: Optional[List[str]] = ["Read", "Edit", "Glob"]
    permission_mode: Optional[str] = "acceptEdits"


class QueryResponse(BaseModel):
    response: str
    done: bool = True
    error: Optional[str] = None


async def run_agent(prompt: str, allowed_tools: List[str], permission_mode: str) -> tuple[str, Optional[str]]:
    output_lines: List[str] = []
    error_msg = None

    try:
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                allowed_tools=allowed_tools,
                permission_mode=permission_mode,
            ),
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        output_lines.append(block.text)
                        logger.info(f"Assistant: {block.text}")
                    elif hasattr(block, "name"):
                        output_lines.append(f"Tool: {block.name}")
                        logger.info(f"Tool used: {block.name}")
            elif isinstance(message, ResultMessage):
                output_lines.append(f"Done: {message.subtype}")
                logger.info(f"Result: {message.subtype}")
    except Exception as e:
        logger.error(f"Error during agent execution: {str(e)}", exc_info=True)
        error_msg = str(e)
        output_lines.append(f"Error: {str(e)}")

    return "\n".join(output_lines), error_msg


@app.get("/")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    logger.info(f"Query received: {request.prompt}")
    logger.info(f"Allowed tools: {request.allowed_tools}")
    
    response_text, error = await run_agent(
        prompt=request.prompt,
        allowed_tools=request.allowed_tools,
        permission_mode=request.permission_mode,
    )
    return QueryResponse(response=response_text, error=error)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

