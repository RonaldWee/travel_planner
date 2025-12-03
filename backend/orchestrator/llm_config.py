"""
LLM configuration for OpenRouter with CrewAI compatibility
"""
import os

def get_llm_for_crewai(api_key: str = None, use_claude: bool = False):
    """
    Get LLM configuration for OpenRouter that works with CrewAI

    Args:
        api_key: OpenRouter API key (if not provided, uses env var)
        use_claude: If True, try to use Claude (may cause provider errors)

    Returns:
        Model string that CrewAI/LiteLLM will use with OpenRouter
    """
    if api_key is None:
        api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OpenRouter API key required")

    # Set environment variables that CrewAI/LiteLLM will use
    # CRITICAL: These must be set for OpenRouter to work
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

    # Return model string with openrouter/ prefix
    # This tells LiteLLM (used by CrewAI) to route through OpenRouter
    if use_claude:
        return "openrouter/anthropic/claude-3.5-sonnet"
    else:
        return "openrouter/openai/gpt-4-turbo-preview"

def get_simple_llm(api_key: str = None):
    """
    Get a simpler LLM configuration that bypasses CrewAI's provider detection

    Uses gpt-4 model name to avoid Anthropic provider detection,
    but still routes through OpenRouter
    """
    if api_key is None:
        api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OpenRouter API key required")

    os.environ["OPENAI_API_KEY"] = api_key

    # Use openai/gpt-4-turbo through OpenRouter
    # This avoids the Anthropic provider detection issue
    llm = ChatOpenAI(
        model="openai/gpt-4-turbo-preview",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=4000,
        default_headers={
            "HTTP-Referer": os.getenv("SITE_URL", "http://localhost:8000"),
            "X-Title": os.getenv("APP_NAME", "Travel Planner")
        }
    )

    return llm
