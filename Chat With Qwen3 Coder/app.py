import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_chat_model(api_key: str) -> ChatOpenAI:
    """Initialize and return ChatOpenAI model with OpenRouter configuration."""
    return ChatOpenAI(
        model="qwen/qwen3-coder",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        streaming=True
    )


@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    # Initialize message history with system message
    cl.user_session.set("messages", [
        SystemMessage(content="You are a helpful AI assistant.")
    ])

    # Check if API key is available from environment
    env_api_key = os.getenv("OPENROUTER_API_KEY")

    # Only send a message if no API key is found (to avoid conflicts with readme/starters)
    if not env_api_key:
        await cl.Message(
            content="⚠️ **No API Key Detected**\n\n"
            "Please add `OPENROUTER_API_KEY=your_key` to a `.env` file to get started."
        ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming user messages."""

    # Get API key from settings or environment variable
    settings = cl.user_session.get("settings", {})
    api_key = settings.get("openrouter_api_key") or os.getenv(
        "OPENROUTER_API_KEY")

    if not api_key:
        await cl.Message(
            content="❌ **OpenRouter API Key Required**\n\n"
            "Please set your OpenRouter API key in a `.env` file as `OPENROUTER_API_KEY`."
        ).send()
        return

    # Get message history
    messages = cl.user_session.get("messages", [])

    # Add user message to history
    messages.append(HumanMessage(content=message.content))

    try:
        # Initialize chat model
        chat = get_chat_model(api_key)

        # Create a message placeholder for streaming
        msg = cl.Message(content="")
        await msg.send()

        # Get AI response with streaming
        response = await chat.ainvoke(messages)

        # Update the message with the complete response
        msg.content = response.content
        await msg.update()

        # Add AI response to history
        messages.append(AIMessage(content=response.content))

        # Update message history in session
        cl.user_session.set("messages", messages)

    except Exception as e:
        await cl.Message(
            content=f"❌ **Error occurred**: {str(e)}\n\n"
            "Please check your API key and try again."
        ).send()


@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates."""
    cl.user_session.set("settings", settings)

    # If API key is provided, send confirmation
    if settings.get("openrouter_api_key"):
        await cl.Message(
            content="✅ **API Key Updated**\n\nYou can now start chatting!"
        ).send()

# Settings configuration


@cl.set_starters
async def set_starters():
    """Set starter messages for the chat."""
    return [
        cl.Starter(
            label="Hello! 👋",
            message="Hello! Can you help me with some coding questions?",
            icon="/public/idea.svg",
        ),
        cl.Starter(
            label="Code Review 🔍",
            message="Can you review this code and suggest improvements?\n\n```python\n# Paste your code here\ndef example_function():\n    pass\n```",
            icon="/public/learn.svg",
        ),
        cl.Starter(
            label="Debug Help 🐛",
            message="I'm having trouble with my code. Can you help me debug this error?\n\n**Error message:**\n[Paste error message here]\n\n**Code:**\n```python\n# Paste problematic code here\n```",
            icon="/public/terminal.svg",
        ),
        cl.Starter(
            label="Best Practices 📚",
            message="What are the best practices for writing clean, maintainable code in [language/framework]? Specifically for [describe your context or specific area of interest]?",
            icon="/public/write.svg",
        ),
    ]
