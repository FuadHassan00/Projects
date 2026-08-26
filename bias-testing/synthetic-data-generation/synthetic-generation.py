"""
Generate synthetic data for testing purposes
"""

def initialize_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI

    model = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",  # Gemini 3.0+ is the default model
        temperature=1.0,  # Gemini 3.0+ defaults to 1.0
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return model

