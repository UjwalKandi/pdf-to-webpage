"""
DocWeb - Streamlit App (Minimalist Edition)
Clean, simple interface with proper contrast
"""

import streamlit as st
import os
from pathlib import Path
from scripts.markdown_convert import MarkdownConverter
from scripts.generate_html import ERNIEHTMLGenerator
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================

st.set_page_config(
    page_title="DocWeb",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== CLEAN WHITE THEME ====================

st.markdown("""
    <style>
    /* White background throughout */
    body {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #f8f8f8 !important;
    }
    
    /* Text - Dark Grey/Black */
    p, span, div, li, a {
        color: #1a1a1a !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        color: #1a1a1a !important;
    }
    
    /* Clean button styling - Professional Blue */
    .stButton > button {
        background-color: #4a90e2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px;
        padding: 0.7rem 1.4rem;
        font-weight: 600;
        width: 100%;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #3a7bc8 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffffff !important;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffffff !important;
        color: #4a90e2 !important;
        border-bottom: 2px solid #4a90e2 !important;
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        background-color: #f8f8f8 !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    [data-testid="stExpanderDetails"] {
        background-color: #f8f8f8 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricContainer"] {
        background-color: #f8f8f8 !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* File uploader - Remove all borders and outlines */
    [data-testid="stFileUploader"] {
        background-color: #e8e8e8 !important;
        border: none !important;
        padding: 2rem !important;
        border-radius: 8px;
    }
    
    /* Remove dotted outline from file uploader container */
    [data-testid="stFileUploader"] > div {
        border: none !important;
        outline: none !important;
    }
    
    /* Remove focus outline */
    [data-testid="stFileUploader"]:focus-within {
        outline: none !important;
        border: none !important;
    }
    
    /* File uploader text - dark */
    [data-testid="stFileUploader"] [data-testid="stText"] {
        color: #333333 !important;
    }
    
    [data-testid="stFileUploader"] p {
        color: #333333 !important;
    }
    
    [data-testid="stFileUploader"] span {
        color: #333333 !important;
    }
    
    /* Browse files button - dark text */
    [data-testid="stFileUploader"] button {
        color: #ffffff !important;
        background-color: #4a90e2 !important;
        border: none !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background-color: #3a7bc8 !important;
    }
    
    /* File uploader SVG icon - dark */
    [data-testid="stFileUploader"] svg {
        color: #333333 !important;
        stroke: #333333 !important;
        fill: #333333 !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
    }
    
    .stSelectbox > div > div > select {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #1a1a1a !important;
    }
    
    /* Success/Info/Error boxes */
    .success-message {
        background-color: #e8f5e9 !important;
        border-left: 4px solid #28a745 !important;
        padding: 1rem;
        border-radius: 4px;
        color: #1a1a1a !important;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #ffebee !important;
        border-left: 4px solid #dc3545 !important;
        padding: 1rem;
        border-radius: 4px;
        color: #1a1a1a !important;
        margin: 1rem 0;
    }
    
    .info-message {
        background-color: #e3f2fd !important;
        border-left: 4px solid #4a90e2 !important;
        padding: 1rem;
        border-radius: 4px;
        color: #1a1a1a !important;
        margin: 1rem 0;
    }
    
    /* Code blocks */
    [data-testid="stCode"] {
        background-color: #f8f8f8 !important;
        color: #1a1a1a !important;
    }
    
    /* Code block text color */
    [data-testid="stCode"] code {
        color: #1a1a1a !important;
    }
    
    /* Divider */
    hr {
        border-color: #e0e0e0 !important;
        margin: 1.5rem 0;
    }
    
    /* Download button - Professional Blue */
    .stDownloadButton > button {
        background-color: #4a90e2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .stDownloadButton > button:hover {
        background-color: #3a7bc8 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Spinner text */
    [data-testid="stSpinner"] {
        color: #4a90e2 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'extracted' not in st.session_state:
    st.session_state.extracted = None
if 'markdown_content' not in st.session_state:
    st.session_state.markdown_content = None
if 'html_content' not in st.session_state:
    st.session_state.html_content = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# ==================== HELPER FUNCTIONS ====================

def show_success(msg):
    st.markdown(f'<div class="success-message">✓ {msg}</div>', unsafe_allow_html=True)

def show_error(msg):
    st.markdown(f'<div class="error-message">✗ {msg}</div>', unsafe_allow_html=True)

def show_info(msg):
    st.markdown(f'<div class="info-message">ℹ {msg}</div>', unsafe_allow_html=True)

def safe_extract(pdf_path):
    """Safe PDF extraction"""
    try:
        from scripts.extract_pdf import PaddleOCRExtractor
        extractor = PaddleOCRExtractor()
        
        if not extractor.available:
            return None, "PaddleOCR-VL API not configured. Check your .env file."
        
        extracted = extractor.extract_from_pdf(pdf_path)
        return extracted, None
    except Exception as e:
        return None, str(e)

def safe_convert(content):
    """Safe markdown conversion"""
    try:
        converter = MarkdownConverter()
        markdown = converter.convert_content(content)
        return markdown, None
    except Exception as e:
        return None, str(e)

def safe_generate_html(markdown, title, access_token):
    """Safe HTML generation"""
    try:
        generator = ERNIEHTMLGenerator(access_token)
        html = generator.generate_html(markdown, title)
        return html, None
    except Exception as e:
        return None, str(e)

# ==================== MAIN HEADER ====================

st.markdown("""
    <div style="padding: 2rem 0; text-align: center; border-bottom: 1px solid #e0e0e0; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: #1a1a1a; font-size: 2.2em;">📄 DocWeb</h1>
        <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1rem;">Transform PDFs into responsive webpages with Baidu AI (PaddleOCR-VL & ERNIE)</p>
    </div>
""", unsafe_allow_html=True)

# ==================== TABS ====================

tab1, tab2, tab3 = st.tabs(["Convert", "Preview", "Help"])

# ==================== TAB 1: CONVERT ====================

with tab1:
    # Upload Section
    st.markdown("### 1. Upload PDF")
    uploaded_file = st.file_uploader(
        "Select a PDF file",
        type=["pdf"],
        label_visibility="collapsed",
        help="Choose a text-based PDF (max 100MB)"
    )
    
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        show_success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.2f} MB)")
        
        pdf_path = Path("temp_uploads") / uploaded_file.name
        pdf_path.parent.mkdir(exist_ok=True)
        
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract Section
        st.markdown("### 2. Extract Text")
        
        if st.button("🔍 Extract", key="btn_extract", use_container_width=True):
            with st.spinner("Extracting text from PDF..."):
                extracted, error = safe_extract(str(pdf_path))
                
                if error:
                    show_error(f"Extraction failed: {error}")
                else:
                    st.session_state.extracted = extracted
                    st.session_state.step = max(st.session_state.step, 1)
                    
                    pages = len(extracted)
                    chars = sum(p.get('char_count', 0) for p in extracted)
                    show_success(f"Extracted {pages} page(s) • {chars:,} characters")
                    st.rerun()
        
        # Convert Section
        if st.session_state.extracted:
            st.markdown("### 3. Convert to Markdown")
            
            if st.button("📝 Convert", key="btn_convert", use_container_width=True):
                with st.spinner("Converting to Markdown..."):
                    markdown, error = safe_convert(st.session_state.extracted)
                    
                    if error:
                        show_error(f"Conversion failed: {error}")
                    else:
                        converter = MarkdownConverter()
                        markdown = converter.add_metadata(
                            markdown,
                            title=uploaded_file.name.replace('.pdf', ''),
                            author="DocWeb",
                            date=datetime.now().strftime("%Y-%m-%d")
                        )
                        st.session_state.markdown_content = markdown
                        st.session_state.step = max(st.session_state.step, 2)
                        show_success("Markdown conversion complete")
                        st.rerun()
        
        # Generate Section
        if st.session_state.markdown_content:
            st.markdown("### 4. Generate HTML")
            
            col1, col2 = st.columns(2)
            with col1:
                page_title = st.text_input(
                    "Page Title",
                    value=uploaded_file.name.replace('.pdf', ''),
                    label_visibility="collapsed"
                )
            with col2:
                use_api = st.checkbox(
                    "Use ERNIE API",
                    value=bool(os.getenv("BAIDU_ACCESS_TOKEN")),
                    help="Enable AI-powered styling (requires API token)"
                )
            
            if st.button("🎨 Generate HTML", key="btn_generate", use_container_width=True):
                with st.spinner("Generating HTML..."):
                    access_token = os.getenv("BAIDU_ACCESS_TOKEN", "") if use_api else ""
                    html, error = safe_generate_html(
                        st.session_state.markdown_content,
                        page_title,
                        access_token
                    )
                    
                    if error:
                        show_error(f"Generation failed: {error}")
                    else:
                        st.session_state.html_content = html
                        st.session_state.step = max(st.session_state.step, 3)
                        show_success("HTML generated successfully")
                        st.rerun()
        
        # Download Section
        if st.session_state.html_content:
            st.markdown("### 5. Download")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📥 HTML",
                    st.session_state.html_content,
                    "index.html",
                    "text/html",
                    use_container_width=True
                )
            
            with col2:
                st.download_button(
                    "📝 Markdown",
                    st.session_state.markdown_content,
                    "content.md",
                    "text/markdown",
                    use_container_width=True
                )
            
            with col3:
                st.download_button(
                    "📦 JSON",
                    json.dumps(st.session_state.extracted, ensure_ascii=False, indent=2),
                    "data.json",
                    "application/json",
                    use_container_width=True
                )

# ==================== TAB 2: PREVIEW ====================

with tab2:
    if st.session_state.html_content or st.session_state.uploaded_file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Input PDF")
            
            if st.session_state.uploaded_file:
                st.write(f"**{st.session_state.uploaded_file.name}**")
                st.write(f"Size: {st.session_state.uploaded_file.size / (1024*1024):.2f} MB")
            
            if st.session_state.extracted:
                st.markdown("#### Extraction Stats")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Pages", len(st.session_state.extracted))
                with col_b:
                    total_chars = sum(p.get('char_count', 0) for p in st.session_state.extracted)
                    st.metric("Characters", f"{total_chars:,}")
        
        with col2:
            st.markdown("### Generated Webpage")
            
            if st.session_state.html_content:
                st.components.v1.html(st.session_state.html_content, height=500, scrolling=True)
            else:
                show_info("Generate HTML in the Convert tab to preview")
    else:
        show_info("Upload a PDF and complete conversion to see preview")

# ==================== TAB 3: HELP ====================

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Getting Started")
        st.markdown("""
        1. **Upload** a text-based PDF
        2. **Extract** text with PaddleOCR-VL
        3. **Convert** to Markdown format
        4. **Generate** HTML webpage
        5. **Download** and deploy
        """)
        
        st.markdown("### Configure API")
        st.markdown("""
        1. Register at [Baidu AI Studio](https://aistudio.baidu.com)
        2. Get common access token
        3. Add to `.env` file:
        """)
        st.markdown('<div style="background-color: #f8f8f8; padding: 1rem; border-radius: 4px; margin: 0.5rem 0;"><code style="color: #ffffff;">BAIDU_ACCESS_TOKEN=your_token</code></div>', unsafe_allow_html=True)
        st.markdown("4. Restart app")
    
    with col2:
        st.markdown("### Technology Stack")
        st.markdown("""
        - **PaddleOCR-VL**: Document OCR
        - **ERNIE 4.5**: HTML generation
        - **Streamlit**: Web interface
        - **Markdown**: Content structure
        - **HTML5**: Responsive design
        """)
        
        st.markdown("### Deploy to GitHub Pages")
        st.markdown("""
        1. Download HTML file
        2. Create GitHub repo
        3. Upload `index.html`
        4. Enable Pages in settings
        5. Share your URL
        """)
    
    with st.expander("📚 Full Documentation"):
        st.markdown("""
        ### Supported Features
        - Multi-page PDF extraction
        - Automatic structure detection
        - AI-powered styling
        - Mobile-responsive output
        - Multiple export formats
        
        ### Best Practices
        - Use well-scanned PDFs
        - Clear document structure helps
        - Readable fonts work best
        - Avoid image-only PDFs
        
        ### Troubleshooting
        - **Slow extraction**: Large PDFs take longer
        - **Poor text quality**: Try higher resolution scan
        - **API errors**: Verify token and quota
        
        ### Resources
        - [GitHub Repository](https://github.com/UjwalKandi/pdf-to-webpage)
        - [PaddleOCR Docs](https://github.com/PaddlePaddle/PaddleOCR)
        - [Baidu AI Studio](https://aistudio.baidu.com)
        """)

# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666; font-size: 0.9rem;">
        <p style="margin: 0;">Made with ❤️ • <strong>PaddleOCR-VL</strong> • <strong>ERNIE 4.5</strong> • <strong>Streamlit</strong></p>
        <p style="margin: 0.5rem 0 0 0;"><a href="https://github.com/UjwalKandi/pdf-to-webpage" style="color: #0066cc; text-decoration: none;">View on GitHub</a></p>
    </div>
""", unsafe_allow_html=True)
