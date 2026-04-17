from agents import (
    build_search_agent,
    build_scrape_agent,
    chat_chain,
    critic_chain
)

def run_pipeline(topic: str) -> dict:
    state = {}

    print("\n" + "=" * 60)
    print("🔍 Starting Search Pipeline")
    print("=" * 60)

    # -----------------------------
    # STEP 1: SEARCH AGENT
    # -----------------------------
    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"Conduct a web search to gather information on the topic: {topic}"
            }
        ]
    })

    state['search_result'] = search_result['messages'][-1].content
    print("\n✅ Search Result:\n")
    print(state['search_result'][:500])


    # -----------------------------
    # STEP 2: SCRAPER AGENT
    # -----------------------------
    print("\n" + "=" * 60)
    print("🌐 Scraper Agent is extracting content")
    print("=" * 60)

    scrape_agent = build_scrape_agent()

    scraper_result = scrape_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Based on the search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper insights.\n\n"
                    f"Search Results:\n{state['search_result'][:800]}"
                )
            }
        ]
    })

    state['scrape_content'] = scraper_result['messages'][-1].content
    print("\n📄 Scraped Content:\n")
    print(state['scrape_content'][:500])


    # -----------------------------
    # STEP 3: REPORT GENERATION
    # -----------------------------
    print("\n" + "=" * 60)
    print("✍️ Generating Research Report")
    print("=" * 60)

    combined_research = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"SCRAPED CONTENT:\n{state['scrape_content']}"
    )

    state['report'] = chat_chain.invoke({
        "topic": topic,
        "research": combined_research
    })

    print("\n📊 Generated Report:\n")
    print(state['report'][:1000])


    # -----------------------------
    # STEP 4: CRITIC AGENT
    # -----------------------------
    print("\n" + "=" * 60)
    print("🧠 Critic Agent Evaluating Report")
    print("=" * 60)

    state['feedback'] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n📝 Critic Feedback:\n")
    print(state['feedback'])

    return state


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_pipeline(topic)