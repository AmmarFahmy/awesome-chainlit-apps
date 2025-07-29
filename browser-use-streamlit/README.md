# 🤖 Browser Use Agent 🚀

This application allows you to leverage AI agents to perform tasks in a web browser. It supports both OpenAI and Google Gemini LLMs. The agent navigates websites, extracts information, and follows instructions based on the given task.



## ✨ Features

*   **Task Execution in a Browser:** The agent uses a web browser to complete tasks, interacting with web pages like a human.
*   **LLM Powered:**  Utilizes either OpenAI's GPT models or Google's Gemini models to interpret tasks and plan actions.
*   **Step-by-Step History:** Provides a detailed history of the agent's actions, including goals, extracted content, and screenshots.
*   **Screenshot Support:** Displays screenshots of the browser at each step of the process, allowing you to visualize the agent's progress.

## 📋 Prerequisites

⚠️ **Important for Windows Users**: The `playwright` and `browser-use` packages have limited native Windows support. **Windows users must use WSL (Windows Subsystem for Linux)** to run this application.

### For Windows Users:
1. Install WSL2 if you haven't already:
   ```bash
   wsl --install
   ```
2. Open WSL terminal and proceed with the installation steps below.

### For Linux/macOS Users:
You can run the installation directly in your terminal.

## 🚀 Getting Started

1.  **Clone the GitHub Repository:** 
    ```bash
    git clone https://github.com/AmmarFahmy/awesome-chainlit-apps.git
    cd browser-use-streamlit
    ```

2.  **Set up Virtual Environment and Install Dependencies:**

    **For UV guys:**
    ```bash
    # Create virtual environment with Python 3.11
    uv venv --python 3.11
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install Python dependencies
    uv pip install -r requirements_chainlit.txt
    
    # Install Playwright browsers
    playwright install
    
    # Install Playwright system dependencies (Linux/WSL)
    playwright install-deps
    ```

    **Alternative using pip:**
    ```bash
    # Create virtual environment
    python3.11 -m venv .venv
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt  # or requirements_chainlit.txt for Chainlit
    
    # Install Playwright browsers
    playwright install
    
    # Install Playwright system dependencies
    playwright install-deps
    ```

## 🛠️ Usage

1.  **Configure API Keys:**
    
    **Create a `.env` file:**

    Add either:
    ```
    OPENAI_API_KEY=your_openai_key_here
    ```
    OR
    ```
    GOOGLE_API_KEY=your_google_key_here
    ```

2.  **Run the Chainlit App:**
    ```bash
    chainlit run app.py
    ```

3.  **Access the App:** 
    - The app will be available at `http://localhost:8000`
    - If using WSL, you can access it from your Windows browser at the same URL

4.  **Start Chatting:** Simply type your task in natural language, like "Search for the latest news about Tesla"

5.  **Real-time Updates:** Watch the agent work with live status updates, step-by-step progress, and screenshots


## 🧠 Built With

*   Python 3.11+
*   Playwright
*   browser-use
*   Streamlit / Chainlit
*   langchain
*   openai
*   uv (optional, for faster dependency management)

## 📄 License

This project is licensed under the MIT License.

## 🙌 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📩 Contact

For questions or suggestions, reach out via email or open an issue on GitHub.
