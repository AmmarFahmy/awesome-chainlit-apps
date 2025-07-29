# 🚀 Chat With Qwen3 Coder

This is a Chainlit web application that allows you to chat with the `qwen/qwen3-coder` model, powered by [OpenRouter](https://openrouter.ai/models).

## ✨ Features

- Interactive chat interface built with Chainlit.
- Powered by the `qwen/qwen3-coder` model via OpenRouter.
- Secure API key management through settings.
- Starter prompts for common coding scenarios.
- Real-time streaming responses.
- Clean, modern UI with message history.

## 🛠️ Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.7+
- An [OpenRouter](https://openrouter.ai/) account and API key.
- (Optional) [UV](https://docs.astral.sh/uv/) for faster package management

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/AmmarFahmy/awesome-chainlit-apps.git
    cd "Chat With Qwen3 Coder"
    ```

2.  **Install dependencies (choose one method):**

    **Option A: Using UV (Recommended - Faster):**
    
    ```bash
    # Install UV if you haven't already
    # On macOS and Linux:
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # On Windows:
    # powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    # Create virtual environment
    uv venv
    
    # Activate virtual environment
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    # source .venv/bin/activate
    
    # Install dependencies
    uv pip install -r requirements.txt
    ```
    
    **Option B: Using Pip (Traditional):**
    
    ```bash
    # Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

4.  **Set up your OpenRouter API key (choose one option):**
    
    Create a `.env` file in the project directory:
    ```bash
    OPENROUTER_API_KEY=your_openrouter_api_key_here
    ```


## 🏃‍♀️ Usage

1.  **Run the Chainlit application (make sure virtual environment is activated):**

    ```bash
    chainlit run app.py
    ```

2.  Open your web browser and navigate to the local URL provided by Chainlit (usually `http://localhost:8000`).


3.  Use the starter prompts or type your own coding questions to get help from the AI assistant.
