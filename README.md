# 🤖 Autonomous AI Research Assistant

This project is a **Multi-Agent Research System** built using Python, LangChain, and Streamlit. It autonomously conducts deep research on any given topic by searching the web, scraping relevant articles, compiling a comprehensive report, and critiquing its own work to ensure high quality and accuracy.

## ✨ Features

- **🌐 Automated Web Search**: Uses the Tavily Search API to find the most relevant, up-to-date sources based on your topic.
- **📄 Intelligent Web Scraping**: Extracts text content directly from the identified URLs.
- **✍️ Report Generation Agent**: Uses Google's Gemini models to draft a well-structured research report summarizing the scraped findings.
- **🧠 Critic Agent**: Evaluates the generated report for clarity, accuracy, and formatting, providing constructive feedback.
- **🖥️ Streamlit UI**: A clean, responsive, and interactive graphical interface for initiating research and reviewing outputs organized in tabs.
- **💻 CLI Support**: Can also be executed seamlessly via the command line.

## 🛠️ Tech Stack

- **Framework**: [LangChain](https://www.langchain.com/) / LangGraph
- **LLM**: Google Gemini Models (`langchain-google-genai`)
- **Search Tool**: [Tavily Search API](https://tavily.com/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Language**: Python 3.10+

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have Python installed. You will also need API keys from:
- [Google Gemini API](https://aistudio.google.com/)
- [Tavily Search API](https://tavily.com/)

### 2. Installation Setup

Clone the repository or download the source code, then navigate to your project directory:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```
*(If you don't have a `requirements.txt` file yet, ensure you install: `pip install langchain langchain-google-genai streamlit python-dotenv tavily-python`)*

### 3. Environment Variables
Create a file named `.env` in the root of your project directory and add your API keys:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Running the Application

**Option A: Interactive UI (Recommended)**
Start the Streamlit dashboard:
```bash
streamlit run app.py
```

**Option B: Command Line Interface**
Run the pipeline directly in the terminal:
```bash
python pipeline.py
```

## 🏗️ Architecture / Pipeline Flow

1. **User Input:** Topic is provided via Streamlit or CLI.
2. **Search:** The pipeline fetches top results via Tavily.
3. **Scrape:** Raw text content is extracted directly from the web sources.
4. **Drafting:** The Report Agent synthesizes the scraped data into a Markdown report.
5. **Critique:** The Critic Agent reviews the draft and outputs an evaluation score and feedback.
6. **Output:** The UI displays the Final Report, Feedback, Scraped Data, and Sources cleanly to the user.

## ⚠️ Notes on API Limits
If you are using the free tier of the Gemini API, you may occasionally encounter a `429 RESOURCE_EXHAUSTED` or `limit: 0` error if you hit the strict token limit. The pipeline handles this by safely truncating the scraped content and adding synthetic pauses (`time.sleep()`) to help you respect free-tier constraints. 

## 📜 License
This project is open-source. Feel free to fork and modify!