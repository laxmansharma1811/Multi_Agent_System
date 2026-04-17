import streamlit as st
from pipeline import run_pipeline
import io
try:
    from fpdf import FPDF
except ImportError:
    st.error("Please install fpdf2 to enable PDF downloads: `pip install fpdf2`")

def generate_pdf(text, title):
    """Utility function to convert pure text/markdown to a PDF byte stream."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Adding a Unicode font or falling back to simple latin-1 encoding
    # We replace unsupported unicode characters since default FPDF fonts don't support all emojis/symbols
    pdf.set_font("Helvetica", size=16, style="B")
    pdf.multi_cell(0, 10, txt=title.encode("latin-1", "replace").decode("latin-1"), align="C")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=12)
    # clean up known markdown elements slightly for text format, encode to handle emojis safely
    clean_text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 8, txt=clean_text)
    
    return pdf.output()

# Configure the Streamlit page
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make the UI look more polished
st.markdown("""
<style>
    .report-container {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #333;
        margin-top: 1rem;
    }
    .stButton>button {
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    .topic-header {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🤖 Autonomous AI Research Assistant")
st.markdown("""
Welcome to the multi-agent research tool. Enter any topic below, and our autonomous agents will:
1. 🌐 **Search** the web for the most relevant and up-to-date sources.
2. 📄 **Scrape** the content from those sources.
3. ✍️ **Draft** a comprehensive research report.
4. 🧠 **Critique** the report to ensure high quality and accuracy.
""")

# Sidebar for extra info
with st.sidebar:
    st.header("Dashboard Information")
    st.info("""
    **Powered by:**
    - LangChain / LangGraph
    - Tavily Search API
    - Streamlit
    """)
    st.markdown("---")
    st.markdown("💡 *Tip: Try searching for complex technological advancements, market analyses, or historical events.*")

# Main Input Section
st.markdown("### Kickoff Research")
topic = st.text_input(
    "What would you like to research today?", 
    placeholder="e.g., The impact of Generative AI on graphic design in 2024...",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    start_btn = st.button("🚀 Start Autonomous Research", type="primary")

# Execution logic
if start_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before starting the research.")
    else:
        # Use st.status to show progress
        with st.status(f"Running Multi-Agent Pipeline for: '{topic}'...", expanded=True) as status:
            try:
                st.write("🔍 Searching the web (Tavily)...")
                st.write("📄 Scraping extracted URLs...")
                st.write("✍️ Drafting the initial report...")
                st.write("🧠 Critic agent is reviewing the draft...")
                
                # Call our main pipeline
                results = run_pipeline(topic)
                
                status.update(label="✅ Research Completed Successfully!", state="complete", expanded=False)
            except Exception as e:
                status.update(label="❌ Pipeline Error", state="error", expanded=False)
                st.error(f"An error occurred during execution: {str(e)}")
                st.stop()

        # Displaying Results in Tabs for a clean UI
        st.divider()
        st.markdown(f"<h3 class='topic-header'>Results for: {topic}</h3>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📑 Final Report", "📝 Critic Feedback", "🔗 Sources Used", "📊 Raw Scraped Data"])

        with tab1:
            st.markdown("### Research Report")
            # Wrap report in custom container
            st.markdown("<div class='report-container'>", unsafe_allow_html=True)
            report_text = results.get("report", "*No report generated.*")
            st.markdown(report_text)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Simple line break
            st.write("")
            
            # Option to download report as PDF
            try:
                pdf_bytes = generate_pdf(text=report_text, title=f"AI Research Report: {topic}")
                st.download_button(
                    label="📄 Download Report as PDF",
                    data=bytes(pdf_bytes),
                    file_name=f"{topic.replace(' ', '_')}_Report.pdf",
                    mime="application/pdf",
                    type="primary"
                )
            except Exception as e:
                st.warning(f"Could not generate PDF: {e}")

        with tab2:
            st.markdown("### AI Critic Evaluation")
            st.info("The critic agent analyzed the drafted report and provided the following feedback to ensure quality:")
            st.markdown(results.get("feedback", "*No feedback generated.*"))

        with tab3:
            st.markdown("### Reference URLs")
            urls = results.get("urls", [])
            if urls:
                for idx, url in enumerate(urls):
                    st.markdown(f"{idx + 1}. [{url}]({url})")
            else:
                st.write("No specific URLs were retained.")

        with tab4:
            st.markdown("### Raw Scraped Content")
            with st.expander("Expand to see all raw text scraped from the sources", expanded=False):
                st.text(results.get("scrape_content", "*No scrape content available.*"))