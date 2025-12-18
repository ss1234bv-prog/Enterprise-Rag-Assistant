"""Enterprise RAG Assistant"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Futuristic Light CSS styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Main container */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
    }
    
    .status-ready {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    /* Source cards */
    .source-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-left: 4px solid #0ea5e9;
        border: 1px solid #bae6fd;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .source-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.02) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .source-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.2);
        border-color: #7dd3fc;
    }
    
    .source-card-title {
        font-weight: 700;
        color: #0369a1;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .source-card-meta {
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.6;
    }
    
    .source-card-content {
        background: #f0f9ff;
        padding: 0.75rem;
        border-radius: 8px;
        margin-top: 0.75rem;
        font-size: 0.85rem;
        color: #334155;
        border-left: 3px solid #7dd3fc;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 2px solid #e0f2fe;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem;
    }
    
    /* Compact sidebar elements */
    [data-testid="stSidebar"] .stFileUploader {
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stButton {
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .section-header {
        color: #0369a1 !important;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] label {
        color: #334155 !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button:disabled {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
        color: #94a3b8 !important;
        box-shadow: none;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] .stMarkdown {
        color: #64748b !important;
    }
    
    [data-testid="stSidebar"] small {
        color: #94a3b8 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #e0f2fe !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0369a1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #bae6fd;
    }
    
    /* Progress container */
    .progress-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.1);
        border: 1px solid #e0f2fe;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);
    }
    
    .metric-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0369a1 !important;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Fix main content height */
    .main .block-container {
        max-height: calc(100vh - 4rem);
        overflow-y: auto;
    }
    
    /* Enterprise Chat Interface */
    .stChatMessage {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        color: #334155;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background: #f8fafc;
        border-left: 4px solid #0ea5e9;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant-message"] {
        background: #ffffff;
        border-left: 4px solid #22c55e;
    }
    
    /* Query input section */
    .query-section {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1);
        border: 1px solid #e0f2fe;
        margin-top: 2rem;
    }
    
    .query-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #0369a1;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    /* Welcome screen */
    .welcome-container {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        border: none;
        border-radius: 20px;
        padding: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.3);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Enterprise RAG Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent Document Analysis powered by OpenAI GPT-4o, ChromaDB, and LangChain</div>', unsafe_allow_html=True)

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("**Configuration Required:** OpenAI API key not found. Please add your API key to the `.env` file.")
    st.code("OPENAI_API_KEY=your-api-key-here", language="bash")
    st.stop()

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Sidebar
with st.sidebar:
    # Document Management at the top
    st.markdown('<div class="section-header">Document Management</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True
    )
    
    process_btn = st.button(
        "Process Documents",
        type="primary",
        use_container_width=True,
        disabled=not uploaded_files
    )
    
    st.markdown("---")
    
    # Database controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset DB", use_container_width=True, help="Clear all indexed documents"):
            import shutil
            if os.path.exists("./chroma_db"):
                shutil.rmtree("./chroma_db")
            st.session_state.rag_pipeline = None
            st.session_state.processing_complete = False
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("Clear Chat", use_container_width=True, help="Clear conversation history"):
            st.session_state.chat_history = []
            st.rerun()
    
    if process_btn and uploaded_files:
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Import components
            status_text.text("Loading components...")
            progress_bar.progress(5)
            from src.ingestion import IngestionPipeline
            from src.vectorstore import VectorIndexer
            
            # Step 2: Save files
            status_text.text(f"Saving {len(uploaded_files)} file(s)...")
            progress_bar.progress(15)
            upload_dir = "./data/documents"
            os.makedirs(upload_dir, exist_ok=True)
            file_paths = []
            
            for f in uploaded_files:
                try:
                    path = os.path.join(upload_dir, f.name)
                    with open(path, "wb") as out:
                        out.write(f.getbuffer())
                    file_paths.append(path)
                except Exception as file_error:
                    st.error(f"Error saving file '{f.name}': {str(file_error)}")
                    raise
            
            # Step 3: Load and chunk documents
            status_text.text("Processing documents...")
            progress_bar.progress(30)
            ingestion = IngestionPipeline(chunk_size=1000, chunk_overlap=200)
            chunks = ingestion.process_documents(file_paths)
            
            # Step 4: Initialize indexer
            status_text.text(f"Preparing vector store ({len(chunks)} chunks)...")
            progress_bar.progress(40)
            indexer = VectorIndexer(
                api_key=api_key,
                embedding_model="text-embedding-3-small",
                persist_directory="./chroma_db",
                collection_name="enterprise_documents"
            )
            
            # Step 5: Generate embeddings
            status_text.text(f"Generating embeddings ({len(chunks)} chunks)...")
            progress_bar.progress(50)
            try:
                indexer.index_documents(chunks)
            except Exception as embed_error:
                if "expecting embedding with dimension" in str(embed_error):
                    # Dimension mismatch - clear and retry
                    status_text.text("Clearing old database due to dimension mismatch...")
                    import shutil
                    if os.path.exists("./chroma_db"):
                        shutil.rmtree("./chroma_db")
                    os.makedirs("./chroma_db", exist_ok=True)
                    # Recreate indexer and retry
                    indexer = VectorIndexer(
                        api_key=api_key,
                        embedding_model="text-embedding-3-small",
                        persist_directory="./chroma_db",
                        collection_name="enterprise_documents"
                    )
                    status_text.text(f"Retrying embeddings ({len(chunks)} chunks)...")
                    indexer.index_documents(chunks)
                else:
                    raise
            
            # Step 6: Initialize RAG pipeline
            status_text.text("Initializing pipeline...")
            progress_bar.progress(90)
            from src.rag_pipeline import RAGPipeline
            st.session_state.rag_pipeline = RAGPipeline(api_key=api_key)
            st.session_state.rag_pipeline.load_existing_index()
            
            # Complete
            progress_bar.progress(100)
            status_text.text("Processing complete")
            st.session_state.processing_complete = True
            
            st.success(f"Processed {len(uploaded_files)} document(s) into {len(chunks)} chunks")
            progress_bar.empty()
            status_text.empty()
            st.rerun()
            
        except Exception as e:
            st.error(f"Processing Error: {str(e)}")
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
    
    st.divider()
    
    # System Information
    st.markdown('<div class="section-header">System Information</div>', unsafe_allow_html=True)
    
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Model</div>
            <div class="metric-value">GPT-4o</div>
        </div>
        """, unsafe_allow_html=True)
    with info_col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Embeddings</div>
            <div class="metric-value">Ada-3</div>
        </div>
        """, unsafe_allow_html=True)

# Main content area
if st.session_state.rag_pipeline is None:
    # Welcome state
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="welcome-container">
            <h3 style="margin-bottom: 0.5rem; font-size: 1.5rem;">Quick Start</h3>
            <p style="font-size: 0.95rem; opacity: 0.95; line-height: 1.5; margin: 0;">
                1. Upload documents via sidebar<br>
                2. Click "Process Documents"<br>
                3. Ask questions in the chat
            </p>
        </div>
        """, unsafe_allow_html=True)
        
else:
    # Enterprise-grade chat interface
    st.markdown("---")
    
    # Display chat history - Professional format
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                with st.chat_message("user"):
                    st.write(msg['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(msg['content'])
                    
                    if 'sources' in msg and msg['sources']:
                        with st.expander(f"View {len(msg['sources'])} Source Citation(s)", expanded=False):
                            for idx, src in enumerate(msg['sources'], 1):
                                chunk_preview = src.get('content', '')[:250] + '...' if len(src.get('content', '')) > 250 else src.get('content', '')
                                st.markdown(f"""
                                <div class="source-card">
                                    <div class="source-card-title">Source {idx}: {src.get('source', 'Unknown')}</div>
                                    <div class="source-card-meta">
                                        <strong>Page:</strong> {src.get('page', 'N/A')} | 
                                        <strong>Chunk ID:</strong> {src.get('chunk_id', 'N/A')} | 
                                        <strong>Relevance:</strong> {src.get('relevance', 0):.1%}
                                    </div>
                                    <div class="source-card-content">
                                        {chunk_preview}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
    
    else:
        st.info("Start a conversation by asking a question below.")
    
    # Query input
    if question := st.chat_input("Ask a question about your documents..."):
        # User message
        st.session_state.chat_history.append({'role': 'user', 'content': question})
        with st.chat_message("user"):
            st.write(question)
        
        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag_pipeline.query(question)
                    st.write(response.answer)
                    
                    sources_data = []
                    if response.sources:
                        with st.expander(f"View {len(response.sources)} Source Citation(s)", expanded=True):
                            for idx, src in enumerate(response.sources, 1):
                                relevance = src.relevance if src.relevance else 0.0
                                chunk_id = getattr(src, 'chunk_id', 'N/A')
                                content = getattr(src, 'content', '')
                                chunk_preview = content[:250] + '...' if len(content) > 250 else content
                                
                                sources_data.append({
                                    'source': src.source,
                                    'page': src.page,
                                    'chunk_id': chunk_id,
                                    'relevance': relevance,
                                    'content': content
                                })
                                st.markdown(f"""
                                <div class="source-card">
                                    <div class="source-card-title">Source {idx}: {src.source}</div>
                                    <div class="source-card-meta">
                                        <strong>Page:</strong> {src.page} | 
                                        <strong>Chunk ID:</strong> {chunk_id} | 
                                        <strong>Relevance:</strong> {relevance:.1%}
                                    </div>
                                    <div class="source-card-content">
                                        {chunk_preview}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response.answer,
                        'sources': sources_data
                    })
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
