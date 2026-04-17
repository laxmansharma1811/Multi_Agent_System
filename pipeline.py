from agents import build_search_agent, build_scrape_agent, chat_chain, critic_prompt

def run_pipeline(topic: str) -> dict:
    state = {}
    
    print("\n"+" ="*50)
    print("Starting search Pipeline")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "message": [("user", f"Conduct a web search to gather information on the topic: {topic}")]
        })
    state['search_result'] = search_result['message'][-1].content
    print("\n Search result: ", state['search_result'])
    
