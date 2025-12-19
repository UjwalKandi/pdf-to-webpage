"""
PDF to Webpage Converter - Streamlit App (Production Ready)
Powered by PaddleOCR-VL API & ERNIE 4.5 Bot SDK from Baidu
Direct API Integration with Single Common Access Token
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
    page_title="PDF to Webpage",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==================== THEME ====================

def apply_theme():
    """Apply light theme"""
    bg = "#ffffff"
    bg_sec = "#f6f8fb"
    text = "#1a1a1a"
    text_sec = "#666666"
    accent = "#0066cc"
    
    st.markdown(f"""
    <style>
    html, body {{ height: 100%; margin: 0; padding: 0; }}
    [data-testid="stAppViewContainer"] {{ display: flex; flex-direction: column; }}
    [data-testid="stMainBlockContainer"] {{ flex: 1; background: {bg}; }}
    body {{ background: {bg}; color: {text}; }}
    .stButton > button {{ background: {accent}; color: white; border: none; border-radius: 6px; font-weight: 600; }}
    .stButton > button:hover {{ opacity: 0.9; }}
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{ color: {accent}; border-bottom: 2px solid {accent}; }}
    .success-box {{ background: rgba(40, 167, 69, 0.1); border: 1px solid #28a745; padding: 12px; border-radius: 6px; margin: 10px 0; }}
    .error-box {{ background: rgba(220, 53, 69, 0.1); border: 1px solid #dc3545; padding: 12px; border-radius: 6px; margin: 10px 0; }}
    .info-box {{ background: rgba(0, 102, 204, 0.1); border: 1px solid {accent}; padding: 12px; border-radius: 6px; margin: 10px 0; }}
    .subtitle {{ color: {text_sec}; font-size: 0.95em; margin: 0.5em 0 0 0; }}
    .subtitle-small {{ color: {text_sec}; font-size: 0.85em; margin-top: 0.3em; }}
    h1, h2, h3 {{ color: {text}; }}
    .footer-spacer {{ min-height: 100px; }}
    .footer-container {{ 
        text-align: center; 
        color: gray; 
        font-size: 0.85em; 
        padding: 2rem 1rem; 
        margin-top: auto; 
        border-top: 1px solid #e0e0e0;
    }}
    .tech-badge {{
        display: inline-block;
        background: {bg_sec};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.9em;
        margin: 2px;
        border: 1px solid {accent};
        color: {accent};
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

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
    st.markdown(f'<div class="success-box">✓ {msg}</div>', unsafe_allow_html=True)

def show_error(msg):
    st.markdown(f'<div class="error-box">✗ {msg}</div>', unsafe_allow_html=True)

def show_info(msg):
    st.markdown(f'<div class="info-box">ℹ {msg}</div>', unsafe_allow_html=True)

def safe_extract(pdf_path):
    """Safe PDF extraction with PaddleOCR-VL API"""
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
    """Safe HTML generation with ERNIE"""
    try:
        generator = ERNIEHTMLGenerator(access_token)
        html = generator.generate_html(markdown, title)
        return html, None
    except Exception as e:
        return None, str(e)

# ==================== HEADER ====================

st.markdown("""
    <div>
        <h1 style='margin: 0;'>📄 PDF to Webpage</h1>
        <p class='subtitle'>
            Powered by <strong>PaddleOCR-VL API</strong> (Advanced Document Analysis) & 
            <strong>ERNIE 4.5 Bot SDK</strong> (Intelligent HTML Generation) from Baidu
        </p>
        <p class='subtitle-small'>
            🔵 PaddleOCR-VL for vision-language document understanding | 🤖 ERNIE for creative content generation
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ==================== TABS ====================

tab1, tab2, tab3 = st.tabs(["📥 Convert", "👀 Preview", "❓ Help"])

# ==================== TAB 1: CONVERT ====================

with tab1:
    st.markdown("### Step 1: Upload PDF")
    st.markdown("*Powered by PaddleOCR-VL API for advanced document understanding*")
    
    uploaded_file = st.file_uploader("Choose PDF", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        
        pdf_path = Path("temp_uploads") / uploaded_file.name
        pdf_path.parent.mkdir(exist_ok=True)
        
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        show_success(f"{uploaded_file.name} ({uploaded_file.size / (1024*1024):.2f} MB)")
        
        st.divider()
        
        # Step 2: Extract with PaddleOCR-VL API
        st.markdown("### Step 2: Extract with PaddleOCR-VL API")
        st.markdown("*Advanced vision-language model for accurate text and layout extraction*")
        
        with st.expander("🔑 Configuration Setup", expanded=False):
            st.markdown("""
                Get API credentials from [Baidu AI Studio](https://aistudio.baidu.com):
                
                **Step 1: Get Common Access Token**
                1. Go to https://aistudio.baidu.com
                2. Click your **profile icon** (top right)
                3. Select **Personal Center** → **Access Token**
                4. Copy your **common access token**
                
                **Step 2: Get API Endpoints**
                1. Visit https://aistudio.baidu.com/paddleocr/task
                2. Find your API endpoints:
                   - **Layout Parsing (PaddleOCR-VL):** Used for document parsing
                   - **OCR (PP-OCRv5):** Used for text recognition
                
                **Step 3: Configure `.env` File**
                Create/Update `.env` in your project root:
                ```
                BAIDU_ACCESS_TOKEN=<your_common_access_token>
                PADDLEOCR_VL_API_URL=https://pd93m801a53ai521.aistudio-app.com/layout-parsing
                PPOCR_V5_API_URL=https://mc8ajcu7f6nbc9he.aistudio-app.com/ocr
                ```
                
                **Features of Common Token:**
                ✓ Works for all Baidu APIs
                ✓ PaddleOCR-VL API access
                ✓ PP-OCRv5 API access
                ✓ ERNIE Bot SDK access
                ✓ Free Tier: 1M tokens/year + 3000 pages/day
                
                **Learn More:** [Baidu AI Studio Documentation](https://aistudio.baidu.com)
            """)
        
        if st.button("🔍 Extract Text & Layout", key="btn_extract", use_container_width=True):
            with st.spinner("🔍 PaddleOCR-VL API is extracting text and layout..."):
                try:
                    from scripts.extract_pdf import PaddleOCRExtractor
                    extractor = PaddleOCRExtractor()
                    
                    if not extractor.available:
                        show_error("PaddleOCR-VL API not configured. Check your .env file.")
                    else:
                        extracted = extractor.extract_from_pdf(str(pdf_path))
                        st.session_state.extracted = extracted
                        st.session_state.step = max(st.session_state.step, 1)
                        
                        pages = len(extracted)
                        chars = sum(p.get('char_count', 0) for p in extracted)
                        show_success(f"✓ PaddleOCR-VL extracted {pages} pages ({chars:,} characters)")
                        st.rerun()
                
                except Exception as e:
                    show_error(f"Extraction failed: {str(e)}")
        
        # Step 3: Markdown
        if st.session_state.extracted:
            st.markdown("### Step 3: Convert to Markdown")
            st.markdown("*Structure and format the extracted content*")
            
            if st.button("📝 Convert", key="btn_convert", use_container_width=True):
                with st.spinner("Converting..."):
                    markdown, error = safe_convert(st.session_state.extracted)
                    
                    if error:
                        show_error(f"Conversion failed: {error}")
                    else:
                        converter = MarkdownConverter()
                        markdown = converter.add_metadata(
                            markdown,
                            title=uploaded_file.name.replace('.pdf', ''),
                            author="PDF to Webpage",
                            date=datetime.now().strftime("%Y-%m-%d")
                        )
                        st.session_state.markdown_content = markdown
                        st.session_state.step = max(st.session_state.step, 2)
                        show_success("✓ Markdown conversion complete")
                        st.rerun()
        
        # Step 4: HTML with ERNIE
        if st.session_state.markdown_content:
            st.markdown("### Step 4: Generate HTML with ERNIE 4.5 Bot SDK")
            st.markdown("*AI-powered HTML generation for beautiful webpages*")
            
            with st.expander("🔑 ERNIE Bot SDK Configuration (Optional)", expanded=False):
                st.markdown("""
                    Get free access from [Baidu AI Studio](https://aistudio.baidu.com):
                    
                    **Using Common Access Token**
                    
                    1. Go to https://aistudio.baidu.com
                    2. Click your **profile icon** (top right)
                    3. Select **Personal Center** → **Access Token**
                    4. Copy your **common access token**
                    5. Add to `.env`:
                    ```
                    BAIDU_ACCESS_TOKEN=<your_common_access_token>
                    ```
                    6. Restart the app
                    
                    **About ERNIE Bot SDK:**
                    - Official Baidu SDK for ERNIE models
                    - Install: `pip install --upgrade erniebot`
                    - Uses single common access token
                    - Free Tier: 1M tokens/year for all ERNIE models
                    - Available Models: ernie-3.5, ernie-4.5, etc.
                    - Smart content generation for custom styling
                    
                    **Without Common Token:**
                    - Uses professional fallback HTML styling
                    - No AI-powered customization
                    - Still produces beautiful, responsive pages
                    
                    **Learn More:** 
                    - [ERNIE Bot SDK GitHub](https://github.com/baidubce/bce-qianfan-sdk)
                    - [Baidu AI Studio](https://aistudio.baidu.com)
                """)
                
                if os.getenv("BAIDU_ACCESS_TOKEN"):
                    st.info("✓ Common access token configured - will use official ERNIE Bot SDK for HTML generation")
                else:
                    st.info("ℹ Common access token not configured - will use professional fallback HTML styling")
            
            page_title = st.text_input(
                "Page Title",
                value=uploaded_file.name.replace('.pdf', ''),
                label_visibility="collapsed",
                key="page_title_input"
            )
            
            if st.button("🎨 Generate HTML", key="btn_generate", use_container_width=True):
                with st.spinner("🤖 Generating HTML with ERNIE 4.5 Bot SDK..."):
                    # Use common token for all APIs
                    access_token = os.getenv("BAIDU_ACCESS_TOKEN", "")
                    html, error = safe_generate_html(st.session_state.markdown_content, page_title, access_token)
                    
                    if error:
                        show_error(f"HTML generation failed: {error}")
                    else:
                        st.session_state.html_content = html
                        st.session_state.step = max(st.session_state.step, 3)
                        
                        if access_token:
                            show_success("✓ HTML generated with ERNIE 4.5 Bot SDK! Check Preview tab")
                        else:
                            show_success("✓ HTML generated with professional fallback styling! Check Preview tab")
                        st.rerun()
        
        # Step 5: Download
        if st.session_state.html_content:
            st.divider()
            st.markdown("### Step 5: Download & Deploy")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📥 Download HTML",
                    st.session_state.html_content,
                    "index.html",
                    "text/html",
                    use_container_width=True
                )
            
            with col2:
                st.download_button(
                    "📝 Download Markdown",
                    st.session_state.markdown_content,
                    "content.md",
                    "text/markdown",
                    use_container_width=True
                )
            
            with col3:
                st.download_button(
                    "📦 Download JSON",
                    json.dumps(st.session_state.extracted, ensure_ascii=False, indent=2),
                    "data.json",
                    "application/json",
                    use_container_width=True
                )

# ==================== TAB 2: PREVIEW ====================

with tab2:
    if st.session_state.html_content or st.session_state.uploaded_file:
        left_col, right_col = st.columns(2)
        
        with left_col:
            st.markdown("### 📄 Uploaded PDF")
            
            if st.session_state.uploaded_file:
                st.markdown(f"**{st.session_state.uploaded_file.name}**")
                st.markdown(f"Size: {st.session_state.uploaded_file.size / (1024*1024):.2f} MB")
            
            # EXTRACTION STATS
            st.markdown("#### Extraction Stats (PaddleOCR-VL)")
            if st.session_state.extracted:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Pages", len(st.session_state.extracted))
                with col_b:
                    total_chars = sum(p.get('char_count', 0) for p in st.session_state.extracted)
                    st.metric("Characters", f"{total_chars:,}")
                
                total_lines = sum(p.get('line_count', 0) for p in st.session_state.extracted)
                st.metric("Lines", total_lines)
                
                with st.expander("View Details"):
                    for idx, page in enumerate(st.session_state.extracted, 1):
                        chars = page.get('char_count', 0)
                        lines = page.get('line_count', 0)
                        error = page.get('error', None)
                        if error:
                            st.write(f"**Page {idx}:** {lines} lines, {chars} chars - Error: {error}")
                        else:
                            st.write(f"**Page {idx}:** {lines} lines, {chars} chars")
            else:
                show_info("Extract PDF to see stats")
            
            # MARKDOWN STATS
            st.markdown("#### Markdown Stats")
            if st.session_state.markdown_content:
                lines = st.session_state.markdown_content.split('\n')
                headings = len([l for l in lines if l.startswith('#')])
                lists = len([l for l in lines if l.startswith('-')])
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Lines", len(lines))
                with col_b:
                    st.metric("Headings", headings)
                
                st.metric("Lists", lists)
            else:
                show_info("Convert to Markdown to see stats")
        
        with right_col:
            st.markdown("### 🌐 Generated Webpage")
            
            if st.session_state.html_content:
                st.components.v1.html(st.session_state.html_content, height=600, scrolling=True)
            else:
                show_info("Generate HTML to see preview")
    else:
        show_info("Upload a PDF in the Convert tab to see preview")

# ==================== TAB 3: HELP ====================

with tab3:
    st.markdown("### 📚 About This Tool")
    
    with st.expander("🛠️ Baidu Technology Stack", expanded=True):
        st.markdown("""
        #### Core Technologies
        
        **🔵 PaddleOCR-VL API (Vision-Language Model)**
        - Advanced optical character recognition from Baidu
        - Vision-language understanding for document layout
        - Direct API integration with Baidu AI Studio endpoints
        - Extracts text, tables, formulas, and charts automatically
        - Returns Markdown + JSON directly from API
        - Supports 109 languages worldwide
        - State-of-the-art (SOTA) performance on document analysis benchmarks
        - Free tier: 3000 pages/day per model
        
        **Models Used by PaddleOCR-VL:**
        - **NaViT-style Dynamic Resolution Visual Encoder** - Processes high-resolution images dynamically
        - **ERNIE-4.5-0.3B Language Model** - Lightweight yet powerful language understanding component
        - **PP-LCNet** - Document classification and layout detection
        - **UVDoc** - Layout analysis and understanding
        - **PP-OCRv5** - Advanced text detection and recognition
        
        **Key Features:**
        - Compact yet powerful architecture
        - State-of-the-art performance in document analysis
        - Multilingual support (109 languages)
        - Low resource consumption
        - Handles complex document elements (tables, formulas, charts)
        - Supports 5 text types: Simplified Chinese, Pinyin, Traditional Chinese, English, Japanese
        - Direct API endpoints from Baidu AI Studio
        - Single common access token for all APIs
        
        **🤖 ERNIE 4.5 Bot SDK (Enhanced Representation through Knowledge Integration)**
        - Large language model from Baidu
        - Official Python SDK (`erniebot` package)
        - Fine-tuned for both Chinese and English
        - Excellent for creative content generation and design
        - Powers intelligent HTML generation with custom styling
        - Official authentication via access tokens
        - Free tier: 1M tokens/year for all ERNIE models
        - Single token works for all ERNIE models
        - Install: `pip install --upgrade erniebot`
        - Available models: ernie-3.5, ernie-4.5, etc.
        
        **📊 Markdown** - Clean, structured formatting
        - Converts extracted text to readable Markdown format
        - Automatic heading and list detection
        - Easy to edit and version control
        - YAML front matter support for metadata
        
        **🎨 Streamlit** - Modern web app framework
        - Beautiful, responsive user interface
        - Real-time preview capabilities
        - Easy deployment and sharing
        - Session state management for seamless workflow
        
        **🌐 HTML5 + CSS** - Professional webpages
        - Responsive design (mobile & desktop)
        - Clean, semantic HTML structure
        - Modern CSS with professional styling
        - Gradient backgrounds and subtle animations
        
        #### Why These Technologies?
        - **PaddleOCR-VL API**: Baidu's official state-of-the-art document understanding service
        - **ERNIE 4.5 Bot SDK**: Advanced AI with official Python SDK
        - **Direct API Integration**: Simple, reliable, and scalable approach
        - **Official SDKs**: No workarounds, following Baidu best practices
        - **Single Token**: All APIs use one common access token for simplicity
        - **Seamless Integration**: Perfect combination for end-to-end document processing
        """)
    
    with st.expander("🚀 Getting Started", expanded=False):
        st.markdown("""
        #### Prerequisites
        - Python 3.8 or higher
        - Free Baidu AI Studio account (no credit card required)
        - Basic command line/terminal knowledge
        
        #### Step 1: Register at Baidu AI Studio
        
        1. Go to [Baidu AI Studio](https://aistudio.baidu.com)
        2. Sign up with GitHub, Google, or email
        3. Complete basic profile setup
        4. You get **free resources** upon registration
        
        #### Step 2: Get Common Access Token
        
        1. Log in to Baidu AI Studio
        2. Click your **profile icon** (top right corner)
        3. Select **Personal Center**
        4. Click **Access Token** section
        5. Copy your **common access token** (works for all APIs)
        
        #### Step 3: Get API Endpoints
        
        1. Visit [PaddleOCR Task Page](https://aistudio.baidu.com/paddleocr/task)
        2. You'll see your personal API endpoints:
           - **Layout Parsing (PaddleOCR-VL):** For document parsing with Markdown output
           - **OCR (PP-OCRv5):** For text recognition (optional fallback)
        3. Copy the endpoint URLs
        
        #### Step 4: Create `.env` File
        
        In your project root, create a file named `.env`:
        ```
        BAIDU_ACCESS_TOKEN=<paste_your_common_access_token_here>
        PADDLEOCR_VL_API_URL=https://pd93m801a53ai521.aistudio-app.com/layout-parsing
        PPOCR_V5_API_URL=https://mc8ajcu7f6nbc9he.aistudio-app.com/ocr
        ```
        
        #### Step 5: Install Dependencies
        
        ```bash
        # Upgrade pip
        pip install --upgrade pip
        
        # Install all requirements
        pip install -r requirements.txt
        
        # Install ERNIE Bot SDK
        pip install --upgrade erniebot
        ```
        
        #### Step 6: Run the Application
        
        ```bash
        streamlit run app.py
        ```
        
        Your app will open at `http://localhost:8501`
        
        #### Step 7: Use the Application
        
        1. **Upload** a text-based PDF (ideally with clear, readable text)
        2. **Extract** text using PaddleOCR-VL API (powered by common token)
        3. **Convert** to Markdown format
        4. **Generate** HTML with ERNIE 4.5 Bot SDK (also uses common token)
        5. **Download** HTML, Markdown, or JSON
        6. **Deploy** to GitHub Pages or any web hosting
        
        #### Processing Time Expectations
        - Extraction: Depends on PDF size (typically 10-60 seconds)
        - Markdown conversion: Less than 1 second
        - HTML generation: 5-15 seconds (with ERNIE Bot SDK)
        - TOTAL: Usually 30-90 seconds per PDF
        
        #### Deploy to GitHub Pages (Free Hosting)
        
        1. Create new repository: `username.github.io`
        2. Download the HTML file from the app
        3. Upload `index.html` to repository root
        4. Go to Settings → Pages
        5. Select main branch as source
        6. Your site is live at `https://username.github.io` 🎉
        
        #### Free API Limits & Quotas
        - **PaddleOCR-VL:** 3000 pages/day per model
        - **ERNIE Bot:** 1M tokens/year for all ERNIE models
        - **GitHub Pages:** Unlimited free hosting
        
        #### Troubleshooting
        
        **Issue: "API not configured"**
        - Check your `.env` file exists in project root
        - Verify `BAIDU_ACCESS_TOKEN` is correct
        - Restart the Streamlit app
        
        **Issue: "Invalid token"**
        - Go to Baidu AI Studio > Personal Center > Access Token
        - Regenerate a new token if needed
        - Update `.env` with new token
        - Restart the app
        
        **Issue: "Exceeded daily limit"**
        - You've hit the 3000 pages/day limit for PaddleOCR
        - Wait until next day, or request higher quota from Baidu
        
        **Issue: Slow extraction**
        - Large PDFs take longer (normal)
        - Complex layouts take more processing time
        - Try with a smaller PDF first to test
        """)
    
    with st.expander("❓ FAQ", expanded=False):
        st.markdown("""
        **Q: What is a "common access token"?**
        A: A single authentication credential from Baidu AI Studio that works for all their APIs - PaddleOCR, ERNIE, and more. One token = access to everything.
        
        **Q: Do I need ALL three APIs configured?**
        A: No. You only need:
        - PaddleOCR-VL API (required) - for document extraction
        - ERNIE Bot SDK (optional) - for AI-powered HTML styling
        - PP-OCRv5 (optional) - as fallback if PaddleOCR fails
        
        **Q: What if I don't have an ERNIE API key?**
        A: The app will still work! It uses a professional fallback HTML template. You just won't get AI-powered custom styling.
        
        **Q: How accurate is PaddleOCR-VL?**
        A: Very accurate for text-based PDFs. It's state-of-the-art on public benchmarks. Scanned PDFs (image-heavy) may have varying accuracy.
        
        **Q: What PDF formats work?**
        A: Best with text-based PDFs. Scanned PDFs (images) are supported but may need better quality for accuracy.
        
        **Q: Can I process 5000 pages per day?**
        A: No, free tier limit is 3000 pages/day. After that, you need to request higher quota from Baidu.
        
        **Q: Can I use this commercially?**
        A: Check Baidu's Terms of Service. Both PaddleOCR and ERNIE have commercial licenses available.
        
        **Q: What languages does it support?**
        A: PaddleOCR-VL supports 109 languages: Chinese, English, Japanese, Arabic, Hindi, Korean, Russian, Thai, French, German, Spanish, and many more.
        
        **Q: Can it extract tables and charts?**
        A: Yes! PaddleOCR-VL can recognize and extract tables, mathematical formulas, and charts automatically.
        
        **Q: Why use APIs instead of downloading local models?**
        A: APIs are simpler, always use latest models, require no GPU, no storage space, and handle everything server-side.
        
        **Q: What if my PDF has handwriting?**
        A: PaddleOCR-VL is trained on handwritten text too! It should work well with readable handwriting.
        
        **Q: How do I increase API limits?**
        A: Contact Baidu AI Studio support or fill out a quota request form on their platform.
        
        **Q: Can I integrate this into my own app?**
        A: Yes! The code is modular and uses standard APIs. You can adapt it to your needs.
        """)
    
    with st.expander("🔗 Resources & Documentation", expanded=False):
        st.markdown("""
        #### Official Baidu Resources
        - [Baidu AI Studio Home](https://aistudio.baidu.com) - Main platform
        - [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR) - Official repo
        - [PaddleOCR-VL API Task](https://aistudio.baidu.com/paddleocr/task) - API access
        - [ERNIE Models Hub](https://huggingface.co/collections/baidu/ernie-45) - All ERNIE models
        - [PaddlePaddle Framework](https://www.paddlepaddle.org.cn/) - Deep learning framework
        - [ERNIE Bot SDK GitHub](https://github.com/baidubce/bce-qianfan-sdk) - SDK repo
        
        #### Getting Help
        - [Baidu AI Studio Forum](https://aistudio.baidu.com/forum) - Community support
        - [PaddleOCR Issues](https://github.com/PaddlePaddle/PaddleOCR/issues) - Bug reports
        - [Baidu Open Platform](https://open.baidu.com/) - API documentation
        
        #### Learning Resources
        - [Markdown Guide](https://www.markdownguide.org/) - Markdown basics
        - [Streamlit Documentation](https://docs.streamlit.io/) - Streamlit reference
        - [GitHub Pages Guide](https://pages.github.com/) - Free web hosting
        - [HTML Basics](https://developer.mozilla.org/en-US/docs/Web/HTML) - HTML reference
        - [CSS Guide](https://developer.mozilla.org/en-US/docs/Web/CSS) - CSS reference
        
        #### Related Tools & Tutorials
        - [Doc2Page Tutorial](https://huggingface.co/spaces/PaddlePaddle/doc2page) - Interactive demo
        - [ERNIE Bot SDK Examples](https://github.com/baidubce/bce-qianfan-sdk/tree/main/examples) - Code examples
        - [PaddleOCR Getting Started](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/README_en.md) - Setup guide
        """)
    
    with st.expander("📋 Project Information", expanded=False):
        st.markdown("""
        #### About This Project
        
        **Project Name:** PDF to Webpage Converter
        
        **Objective:** Build a Web Page with PaddleOCR & ERNIE
        
        **Hackathon Challenge:**
        - ✓ Use PaddleOCR-VL to extract text and layout from PDFs
        - ✓ Convert content into structured Markdown
        - ✓ Use ERNIE model to generate beautiful web pages
        - ✓ Deploy on GitHub Pages (or any web host)
        
        **Technologies Used:**
        - **PaddleOCR-VL API** - Advanced document analysis
        - **ERNIE 4.5 Bot SDK** - Intelligent HTML generation
        - **Streamlit** - Web application framework
        - **Markdown** - Content structure format
        - **HTML5 + CSS** - Responsive webpage styling
        - **Python** - Core programming language
        
        **Features Implemented:**
        - ✓ Multi-page PDF support
        - ✓ Automatic layout and structure detection
        - ✓ AI-powered HTML generation
        - ✓ Professional, responsive webpage design
        - ✓ GitHub Pages deployment ready
        - ✓ Real-time preview in browser
        - ✓ Multiple download formats (HTML, Markdown, JSON)
        - ✓ Error handling and recovery
        - ✓ Single common token for all APIs
        
        **Architecture:**
        - Direct API integration with Baidu AI Studio
        - No local GPU or model downloads required
        - Stateful session management for seamless workflow
        - Error recovery with fallback options
        - Clean, modular code structure
        
        **System Requirements:**
        - Python 3.8+
        - Internet connection (for API calls)
        - Modern web browser
        - ~50MB free disk space
        
        **License:** Open Source (MIT)
        
        **Repository:** [GitHub - PDF to Webpage](https://github.com/yourusername/pdf-to-webpage)
        
        **Version:** 1.0.0
        
        **Last Updated:** 2024
        """)

# ==================== SPACER ====================

st.markdown('<div class="footer-spacer"></div>', unsafe_allow_html=True)

# ==================== FOOTER ====================

st.markdown("""
    <div class="footer-container">
        <p>Made with ❤️ using <strong>Streamlit</strong> • Powered by <strong>PaddleOCR-VL API</strong> & <strong>ERNIE 4.5 Bot SDK</strong> (Baidu)</p>
        <p style="margin: 0.8em 0 0 0; font-size: 0.9em;">
            <span class="tech-badge">🔵 PaddleOCR-VL API</span>
            <span class="tech-badge">🤖 ERNIE 4.5 Bot SDK</span>
            <span class="tech-badge">📊 Markdown</span>
            <span class="tech-badge">🎨 Streamlit</span>
            <span class="tech-badge">🌐 HTML5</span>
        </p>
        <p style="margin: 0.8em 0 0 0; font-size: 0.85em;">
            <strong>Technology Stack:</strong><br>
            🔵 <strong>PaddleOCR-VL API:</strong> Vision-language model for document understanding (NaViT Visual Encoder + ERNIE-4.5-0.3B)<br>
            🤖 <strong>ERNIE 4.5 Bot SDK:</strong> Official SDK for intelligent content generation<br>
            📦 <strong>PaddlePaddle:</strong> Baidu's deep learning framework<br>
            🔐 <strong>Single Common Token:</strong> Universal authentication for all Baidu APIs
        </p>
        <p style="margin: 1em 0 0 0; font-size: 0.8em;">📄 PDF to Webpage Converter | Baidu PaddlePaddle Ecosystem | Open Source</p>
    </div>
""", unsafe_allow_html=True)