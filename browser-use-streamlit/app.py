import chainlit as cl
import os
import asyncio
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image
import io
import base64
import tempfile
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    # Check if API keys are available from environment
    env_openai_key = os.getenv("OPENAI_API_KEY")
    env_google_key = os.getenv("GOOGLE_API_KEY")

    # Only send a message if no API key is found (to avoid conflicts with readme/starters)
    if not env_openai_key and not env_google_key:
        await cl.Message(
            content="⚠️ **No API Key Detected**\n\n"
            "Please configure an API key using one of these methods:\n\n"
            "**Method 1 - Environment File (.env):**\n"
            "Create a `.env` file in the project root with:\n"
            "```\n"
            "OPENAI_API_KEY=your_openai_key\n"
            "# OR\n"
            "GOOGLE_API_KEY=your_google_key\n"
            "```\n\n"
            "**Method 2 - Settings Panel:**\n"
            "Click the ⚙️ settings icon in the bottom left and add your API key.\n\n"
            "**Get API Keys:**\n"
            "- OpenAI: https://platform.openai.com/api-keys\n"
            "- Google AI: https://aistudio.google.com/app/apikey"
        ).send()


@cl.on_settings_update
async def setup_agent(settings):
    """Update settings when user changes them."""
    cl.user_session.set("settings", settings)


async def get_llm_from_settings():
    """Get the appropriate LLM based on user settings."""
    settings = cl.user_session.get("settings", {})

    openai_api_key = settings.get(
        "openai_api_key") or os.getenv("OPENAI_API_KEY")
    google_api_key = settings.get(
        "google_api_key") or os.getenv("GOOGLE_API_KEY")

    if openai_api_key:
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=openai_api_key
        ), "OpenAI GPT-4o-mini"
    elif google_api_key:
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=google_api_key
        ), "Google Gemini 2.0 Flash"
    else:
        return None, None


async def save_screenshot_as_temp_file(screenshot_base64: str) -> str:
    """Convert base64 screenshot to temporary file and return path."""
    try:
        img_bytes = base64.b64decode(screenshot_base64)
        img = Image.open(io.BytesIO(img_bytes))

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            img.save(tmp_file.name, "PNG")
            return tmp_file.name
    except Exception as e:
        cl.logger.error(f"Error saving screenshot: {e}")
        return None


async def run_browser_agent(task: str, llm, llm_name: str):
    """Run the browser agent with real-time updates."""

    # Send initial status
    status_msg = await cl.Message(
        content=f"🚀 **Starting Browser Agent** ({llm_name})\n\n"
        f"**Task:** {task}\n\n"
        "Initializing browser..."
    ).send()

    config = BrowserConfig(headless=True)
    browser = Browser(config=config)
    agent = Agent(task=task, llm=llm, browser=browser, generate_gif=False)

    try:
        # Start the agent
        status_msg.content = f"🚀 **Starting Browser Agent** ({llm_name})\n\n" \
            f"**Task:** {task}\n\n" \
            "🔄 Agent is running..."
        await status_msg.update()

        result = await agent.run()

        # Send completion status
        await cl.Message(
            content=f"✅ **Task Completed Successfully** ({llm_name})\n\n"
            f"**Task:** {task}\n"
            f"**Total Steps:** {len(result.history)}\n\n"
            "📋 **Step-by-step results:**"
        ).send()

        # Process each step and send individually
        for i, action in enumerate(result.history):
            step_num = i + 1
            step_content = f"### 📍 Step {step_num}\n\n"

            step = action.model_output.current_state

            if step.next_goal is not None:
                step_content += f"**🎯 Goal:** {step.next_goal}\n\n"

            if action.result and len(action.result) > 0 and action.result[0].extracted_content is not None:
                content = action.result[0].extracted_content
                # Truncate long content
                if len(content) > 500:
                    content = content[:500] + "..."
                step_content += f"**📄 Extracted Content:**\n```\n{content}\n```"

            # Handle screenshot
            screenshot_elements = []
            try:
                if result.history[i].state.screenshot:
                    screenshot_path = await save_screenshot_as_temp_file(result.history[i].state.screenshot)
                    if screenshot_path:
                        screenshot_elements.append(cl.Image(
                            path=screenshot_path,
                            name=f"step_{step_num}_screenshot",
                            display="inline",
                            size="large"
                        ))
                        step_content += f"\n\n**📷 Screenshot:** Captured"

                        # Send step message with screenshot
                        await cl.Message(
                            content=step_content,
                            elements=screenshot_elements
                        ).send()

                        # Clean up temp file
                        try:
                            os.unlink(screenshot_path)
                        except:
                            pass
                    else:
                        step_content += f"\n\n**📷 Screenshot:** Failed to process"
                        await cl.Message(content=step_content).send()
                else:
                    step_content += f"\n\n**📷 Screenshot:** Not available"
                    await cl.Message(content=step_content).send()

            except Exception as e:
                step_content += f"\n\n**📷 Screenshot:** Error ({str(e)})"
                await cl.Message(content=step_content).send()

        # Update final status
        status_msg.content = f"🎉 **Browser automation completed!** The agent successfully executed {len(result.history)} steps."
        await status_msg.update()

    except Exception as e:
        error_msg = f"❌ **Error occurred during browser automation:**\n\n```\n{str(e)}\n```"
        status_msg.content = error_msg
        await status_msg.update()
        await cl.Message(
            content="Please check your task description and try again. Make sure the task is clear and specific."
        ).send()
    finally:
        await browser.close()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming user messages."""

    # Get LLM from settings
    llm, llm_name = await get_llm_from_settings()

    if not llm:
        await cl.Message(
            content="⚠️ **API Key Required**\n\n"
            "Please configure an API key using one of these methods:\n\n"
            "**Method 1 - Environment File (.env):**\n"
            "Create a `.env` file in the project root with:\n"
            "```\n"
            "OPENAI_API_KEY=your_openai_key\n"
            "# OR\n"
            "GOOGLE_API_KEY=your_google_key\n"
            "```\n\n"
            "**Method 2 - Settings Panel:**\n"
            "Click the ⚙️ settings icon in the bottom left and add your API key.\n\n"
            "**Get API Keys:**\n"
            "- OpenAI: https://platform.openai.com/api-keys\n"
            "- Google AI: https://aistudio.google.com/app/apikey"
        ).send()
        return

    # Get the task from user message
    task = message.content.strip()

    if not task:
        await cl.Message(
            content="Please provide a specific task for the browser agent to perform."
        ).send()
        return

    # Run the browser agent
    await run_browser_agent(task, llm, llm_name)


# Settings configuration
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Research Company Information",
            message="Search for the latest 5 news and activities about Tesla",
            icon="/public/search.svg",
        ),
        cl.Starter(
            label="Extract Product Details",
            message="Go to amazon.com and find details about the latest iPhone",
            icon="/public/shopping.svg",
        ),
        cl.Starter(
            label="Check Website Status",
            message="Visit github.com and check if it's working properly",
            icon="/public/monitor.svg",
        ),
        cl.Starter(
            label="Social Media Research",
            message="Find the top 5 latest posts about Genrative AI on Twitter/X",
            icon="/public/twitter.svg",
        ),
    ]


if __name__ == "__main__":
    cl.run()
