from agents import (
    build_scrape_agent,
    chat_chain,
    critic_chain
)

from tavily import TavilyClient
import os
import time
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# -----------------------------
# Retry Wrapper (IMPORTANT)
# -----------------------------
def safe_invoke(chain, payload, retries=3):
    for i in range(retries):
        try:
            return chain.invoke(payload)
        except Exception as e:
            print(f"⚠️ Retry {i+1}/{retries} due to: {e}")
            time.sleep(2)
    raise Exception("❌ Failed after retries")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline(topic: str) -> dict:
    state = {}

    print("\n" + "=" * 60)
    print("🔍 Starting Research Pipeline")
    print("=" * 60)

    # -----------------------------
    # STEP 1: DIRECT TAVILY SEARCH
    # -----------------------------
    print("\n🌐 Fetching search results from Tavily...\n")

    results = tavily.search(query=topic, max_results=5)

    urls = [r["url"] for r in results["results"]]
    state["urls"] = urls

    print("✅ URLs Found:")
    for url in urls:
        print(url)

    # -----------------------------
    # STEP 2: SCRAPE MULTIPLE URLS
    # -----------------------------
    print("\n" + "=" * 60)
    print("📄 Scraping content from URLs")
    print("=" * 60)

    # We don't need a LangChain Agent just to execute a Python tool directly
    from tools import scrape_url
    all_content = []

    for url in urls:
        print(f"\n🔗 Scraping: {url}")
        
        try:
            # Call the tool directly instead of using an LLM to decide to use the tool
            content = scrape_url.invoke(url)
            all_content.append(f"Source: {url}\n{content}\n")
        except Exception as e:
            print(f"⚠️ Failed to scrape {url}: {e}")

    state["scrape_content"] = "\n\n".join(all_content)

    # -----------------------------
    # STEP 3: REPORT GENERATION
    # -----------------------------
    print("\n" + "=" * 60)
    print("✍️ Generating Research Report")
    print("=" * 60)

    # Cut down the scraped content drastically to save on tokens
    # Google's free tier token per minute limit gets destroyed if we pass 5 full webpages
    truncated_content = state["scrape_content"][:1000] # Super strict limiting to ~2.5k tokens max

    print("⏳ Waiting 30 seconds before report generation to reset token count...")
    time.sleep(30)

    state["report"] = safe_invoke(chat_chain, {
        "topic": topic,
        "research": truncated_content
    })

    print("\n📊 REPORT:\n")
    print(state["report"][:1000])

    # -----------------------------
    # STEP 4: CRITIC
    # -----------------------------
    print("\n" + "=" * 60)
    print("🧠 Evaluating Report")
    print("=" * 60)

    print("⏳ Waiting 15 seconds before evaluation...")
    time.sleep(15)

    state["feedback"] = safe_invoke(critic_chain, {
        "report": state["report"]
    })

    print("\n📝 CRITIQUE:\n")
    print(state["feedback"])

    return state


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_pipeline(topic)