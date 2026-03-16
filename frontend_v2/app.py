"""
Streamlit Frontend for Endee AI Knowledge Assistant
Interactive web interface for semantic search and Q&A.
"""

import streamlit as st
import requests
import json
import time
from typing import Optional, List
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# Configuration
# ============================================================================

API_URL = os.getenv("API_URL", "http://localhost:8000")
DEFAULT_MODEL = "gpt-3.5-turbo"

# Streamlit page configuration
st.set_page_config(
    page_title="Endee AI Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
        font-weight: 500;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .answer-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-left: 4px solid #0084ff;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #f0f7ff;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# Session State Initialization
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_status" not in st.session_state:
    st.session_state.system_status = None

if "last_query_result" not in st.session_state:
    st.session_state.last_query_result = None

# ============================================================================
# Helper Functions
# ============================================================================

def check_system_health() -> dict:
    """Check if backend is healthy."""
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return {
        "status": "unhealthy",
        "endee_connected": False,
        "timestamp": datetime.now().isoformat()
    }


def get_collection_stats() -> dict:
    """Get collection statistics."""
    try:
        response = requests.get(
            f"{API_URL}/stats",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return {"collection_stats": {}}


def query_rag_pipeline(query: str, top_k: int = 5) -> Optional[dict]:
    """Send query to RAG pipeline.
    
    Args:
        query: User query
        top_k: Number of results to retrieve
        
    Returns:
        Response from RAG pipeline or None if error
    """
    try:
        payload = {
            "query": query,
            "top_k": top_k,
            "retrieve_only": False,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            f"{API_URL}/query",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error communicating with backend: {str(e)}")
        return None


def retrieve_only(query: str, top_k: int = 5) -> Optional[dict]:
    """Retrieve documents without generating answer.
    
    Args:
        query: User query
        top_k: Number of results
        
    Returns:
        Retrieved documents or None
    """
    try:
        response = requests.post(
            f"{API_URL}/query/retrieve",
            params={"query": query, "top_k": top_k},
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return None


# ============================================================================
# Header
# ============================================================================

st.title("🧠 Endee AI Knowledge Assistant")
st.markdown("Powered by Endee Vector Database & OpenAI GPT")

# ============================================================================
# Sidebar
# ============================================================================

with st.sidebar:
    st.header("⚙️ Settings")
    
    # System Status
    with st.expander("📊 System Status", expanded=True):
        if st.button("Refresh Status"):
            st.session_state.system_status = check_system_health()
        
        if st.session_state.system_status is None:
            st.session_state.system_status = check_system_health()
        
        status = st.session_state.system_status
        
        col1, col2 = st.columns(2)
        with col1:
            if status["status"] == "healthy":
                st.success("Backend Online")
            else:
                st.warning("Backend Offline")
        
        with col2:
            if status["endee_connected"]:
                st.success("Endee Connected")
            else:
                st.error("Endee Offline")
        
        # Collection Stats
        stats = get_collection_stats()
        if "collection_stats" in stats:
            st.metric("Vectors in DB", stats["collection_stats"].get("count", 0))
    
    # Query Settings
    st.subheader("🔍 Query Settings")
    
    top_k = st.slider(
        "Number of results to retrieve",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )
    
    temperature = st.slider(
        "Answer temperature (creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    max_tokens = st.slider(
        "Max response length",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100
    )
    
    # Document Upload
    st.subheader("📤 Upload Documents")
    
    uploaded_file = st.file_uploader(
        "Upload a document (TXT, PDF, MD)",
        type=["txt", "pdf", "md"]
    )
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.read())}
                    response = requests.post(
                        f"{API_URL}/documents/upload",
                        files=files,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✓ Document processed: {result['chunks_created']} chunks created")
                    else:
                        st.error("Failed to process document")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============================================================================
# Main Content - Tabs
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat",
    "🔍 Semantic Search",
    "📊 Analytics",
    "ℹ️ About"
])

# ============================================================================
# Tab 1: Chat Interface
# ============================================================================

with tab1:
    st.header("Ask a Question")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base and generating answer..."):
                result = query_rag_pipeline(user_input, top_k=top_k)
                
                if result and result.get("success"):
                    # Display answer
                    answer = result.get("answer", "No answer generated")
                    st.markdown(answer)
                    
                    st.session_state.last_query_result = result
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    # Display sources
                    with st.expander("📚 Sources Used"):
                        sources = result.get("sources", [])
                        if sources:
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"{i}. {source}")
                        else:
                            st.info("No specific sources retrieved")
                    
                    # Display metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Retrieval Time",
                            f"{result.get('retrieval_time', 0):.2f}s"
                        )
                    with col2:
                        st.metric(
                            "Generation Time",
                            f"{result.get('generation_time', 0):.2f}s"
                        )
                    
                    # Display context chunks
                    with st.expander("🔗 Retrieved Chunks"):
                        chunks = result.get("context_chunks", [])
                        if chunks:
                            for i, chunk in enumerate(chunks, 1):
                                st.markdown(f"**Chunk {i}** (Score: {chunk['score']:.3f})")
                                st.markdown(chunk["text"][:500] + "..." if len(chunk["text"]) > 500 else chunk["text"])
                                st.divider()
                        else:
                            st.info("No chunks retrieved")
                
                elif result:
                    st.error(result.get("answer", "Unknown error"))
                else:
                    st.error("Failed to get response from backend")

# ============================================================================
# Tab 2: Semantic Search
# ============================================================================

with tab2:
    st.header("🔍 Semantic Search")
    st.write("Search for documents without generating an answer")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input("Search query:")
    
    with col2:
        search_top_k = st.number_input("Top K", min_value=1, max_value=20, value=5)
    
    if st.button("Search"):
        with st.spinner("Searching..."):
            result = retrieve_only(search_query, top_k=search_top_k)
            
            if result:
                st.success(f"Found {result['count']} results")
                
                for i, chunk in enumerate(result["results"], 1):
                    with st.container(border=True):
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"**Result {i}**")
                            st.markdown(chunk["text"][:300] + "...")
                        
                        with col2:
                            st.metric("Score", f"{chunk['score']:.3f}")
                        
                        st.caption(f"Source: {chunk['source']}")

# ============================================================================
# Tab 3: Analytics
# ============================================================================

with tab3:
    st.header("📊 Analytics & Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    stats = get_collection_stats()
    if "collection_stats" in stats:
        with col1:
            st.metric(
                "Total Vectors",
                stats["collection_stats"].get("count", 0)
            )
        
        with col2:
            st.metric(
                "Collection Size",
                stats["collection_stats"].get("memory_used_mb", 0)
            )
        
        with col3:
            st.metric(
                "Last Updated",
                stats["collection_stats"].get("last_updated", "Never")
            )
    
    st.subheader("Query Statistics")
    
    if st.session_state.last_query_result:
        result = st.session_state.last_query_result
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Chunks Retrieved", len(result.get("context_chunks", [])))
        
        with col2:
            st.metric("Retrieval Time", f"{result.get('retrieval_time', 0):.3f}s")
        
        with col3:
            st.metric("Generation Time", f"{result.get('generation_time', 0):.3f}s")
        
        with col4:
            total_time = result.get('retrieval_time', 0) + result.get('generation_time', 0)
            st.metric("Total Time", f"{total_time:.3f}s")
    
    else:
        st.info("No query results yet. Try asking a question in the Chat tab.")

# ============================================================================
# Tab 4: About
# ============================================================================

with tab4:
    st.header("ℹ️ About Endee AI Knowledge Assistant")
    
    st.markdown("""
    ### What is this?
    
    This is an intelligent knowledge assistant powered by:
    
    - **Endee Vector Database**: Fast semantic search using vectors
    - **OpenAI Embeddings**: High-quality text embeddings
    - **GPT Models**: Advanced language understanding and generation
    
    ### How it works
    
    1. **Document Upload**: Upload your documents (PDF, TXT, Markdown)
    2. **Processing**: Documents are automatically chunked and embedded
    3. **Storage**: Embeddings are stored in Endee vector database
    4. **Retrieval**: When you ask a question, it searches for similar content
    5. **Generation**: GPT generates an answer based on retrieved context
    
    ### System Architecture
    
    ```
    User Query
         ↓
    OpenAI Embeddings
         ↓
    Endee Vector Search
         ↓
    Retrieved Context
         ↓
    GPT Answer Generation
         ↓
    Response to User
    ```
    
    ### Features
    
    - ✅ Semantic search over documents
    - ✅ AI-powered Q&A with RAG
    - ✅ Support for multiple document formats
    - ✅ Real-time streaming responses
    - ✅ Document source attribution
    - ✅ Performance metrics
    - ✅ System health monitoring
    
    ### Configuration
    
    **Backend URL**: `{API_URL}`
    
    ### For More Information
    
    Visit [https://github.com/endee-io/endee](https://github.com/endee-io/endee)
    """.format(API_URL=API_URL))

# ============================================================================
# Footer
# ============================================================================

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🧠 Endee Vector Database")

with footer_col2:
    st.caption("🤖 OpenAI GPT-3.5 Turbo")

with footer_col3:
    if st.session_state.system_status and st.session_state.system_status["status"] == "healthy":
        st.caption("✓ System Online")
    else:
        st.caption("✗ System Offline")

if __name__ == "__main__":
    pass
