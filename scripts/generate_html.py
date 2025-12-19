"""
Generate HTML using Direct ERNIE API from Baidu
Bypasses SDK limitations for better model access
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class ERNIEHTMLGenerator:
    """
    Uses Direct ERNIE API from Baidu (same as PaddleOCR)
    No SDK limitations, full model access
    """
    
    def __init__(self, access_token=None):
        # Use provided token or get from env
        self.access_token = access_token or os.getenv("BAIDU_ACCESS_TOKEN", "")
        self.available = bool(self.access_token)
        
        # ERNIE API endpoints - choose your model
        # Check available models at: https://aistudio.baidu.com/
        self.api_url = os.getenv("ERNIE_API_URL", "")
        
        if self.available and not self.api_url:
            # Default endpoint (you can customize)
            self.api_url = "https://aistudio-app.baidu.com/api/v1/ernie"
            print("⚠ Using default ERNIE API endpoint. Set ERNIE_API_URL for custom endpoint.")
        
        if self.available:
            print("✓ ERNIE Direct API initialized with common access token")
    
    def generate_html(self, markdown_content, page_title="Generated Page"):
        """
        Use ERNIE Direct API to convert markdown to styled HTML
        """
        
        if not self.available:
            print("⚠ ERNIE API not available, using fallback HTML generation")
            return self._fallback_html(markdown_content, page_title)
        
        print("🤖 Calling ERNIE Direct API to generate HTML...")
        
        prompt = f"""You are an expert web designer. Convert the following markdown content into a beautiful, professional, responsive HTML page.

Requirements:
1. Create a complete, self-contained HTML5 document
2. Include modern CSS with flexbox/grid layouts
3. Use semantic HTML tags (article, section, header, footer, nav)
4. Make it mobile-responsive with media queries
5. Use a professional color scheme (blues, grays, whites)
6. Include proper typography and spacing
7. Preserve ALL content from the markdown
8. Add subtle design elements (gradients, shadows, borders)
9. Ensure accessibility (WCAG standards)
10. Return ONLY the complete HTML code, no explanations

Markdown to convert:
---
{markdown_content}
---

Generate the complete, production-ready HTML page now:"""
        
        try:
            # Prepare request headers with common token
            headers = {
                "Authorization": f"token {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare payload
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "top_p": 0.9,
                "penalty_score": 1.0
            }
            
            print(f"📡 Calling ERNIE API endpoint...")
            
            # Call ERNIE API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract response based on API format
                if 'result' in result:
                    html_content = result['result'].get('response', '')
                elif 'choices' in result:
                    html_content = result['choices'][0].get('message', {}).get('content', '')
                else:
                    html_content = str(result)
                
                # Clean HTML
                html_content = html_content.replace("```html", "").replace("```", "").strip()
                
                if html_content and html_content.startswith("<!DOCTYPE"):
                    print("✓ HTML generated successfully with ERNIE Direct API!")
                    return html_content
                else:
                    print("⚠ ERNIE returned unexpected format, using fallback")
                    return self._fallback_html(markdown_content, page_title)
            else:
                error_msg = response.json().get('errorMsg', response.text)
                print(f"⚠ ERNIE API error: {response.status_code} - {error_msg}")
                return self._fallback_html(markdown_content, page_title)
        
        except Exception as e:
            print(f"⚠ ERNIE API generation failed: {e}, using fallback")
            return self._fallback_html(markdown_content, page_title)
    
    def _fallback_html(self, markdown_content, page_title):
        """Generate fallback HTML without ERNIE"""
        print("Using fallback HTML generation...")
        html_lines = self._markdown_to_html(markdown_content)
        html_body = "\n".join(html_lines)
        return self._wrap_with_styling(html_body, page_title)
    
    def _markdown_to_html(self, markdown_content):
        """Convert markdown to HTML"""
        lines = markdown_content.split('\n')
        html_lines = []
        in_list = False
        
        for line in lines:
            line = line.rstrip()
            
            if not line:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                continue
            
            if line.startswith("# "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h1>{line[2:].strip()}</h1>")
            elif line.startswith("## "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h2>{line[3:].strip()}</h2>")
            elif line.startswith("### "):
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h3>{line[4:].strip()}</h3>")
            elif line.startswith("- "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"<li>{line[2:].strip()}</li>")
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<p>{line}</p>")
        
        if in_list:
            html_lines.append("</ul>")
        
        return html_lines
    
    def _wrap_with_styling(self, html_body, page_title):
        """Wrap with professional styling"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        main {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            opacity: 0.95;
            font-size: 1.1em;
        }}
        
        article {{
            padding: 60px 40px;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 2em;
            margin: 1.5em 0 0.5em 0;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}
        
        h1:first-child {{
            margin-top: 0;
        }}
        
        h2 {{
            color: #764ba2;
            font-size: 1.5em;
            margin: 1.3em 0 0.5em 0;
        }}
        
        h3 {{
            color: #667eea;
            font-size: 1.2em;
            margin: 1em 0 0.5em 0;
        }}
        
        p {{
            margin: 1em 0;
            text-align: justify;
        }}
        
        ul, ol {{
            margin: 1em 0 1em 2em;
        }}
        
        li {{
            margin: 0.5em 0;
        }}
        
        ul li {{
            list-style: none;
            position: relative;
            padding-left: 20px;
        }}
        
        ul li:before {{
            content: "▸";
            color: #667eea;
            position: absolute;
            left: 0;
            font-weight: bold;
        }}
        
        footer {{
            background: #f8f9fa;
            padding: 40px;
            text-align: center;
            border-top: 1px solid #e0e0e0;
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            main {{ border-radius: 0; }}
            header {{ padding: 40px 20px; }}
            header h1 {{ font-size: 1.8em; }}
            article {{ padding: 30px 20px; }}
            h1 {{ font-size: 1.3em; }}
        }}
    </style>
</head>
<body>
    <main>
        <header>
            <h1>📄 {page_title}</h1>
            <p>Generated using PaddleOCR-VL & ERNIE</p>
        </header>
        <article>
            {html_body}
        </article>
        <footer>
            <p>✨ Created with PaddleOCR-VL (Baidu) & ERNIE</p>
            <p style="margin-top: 0.5em; font-size: 0.9em;">Powered by advanced AI from Baidu's PaddlePaddle ecosystem</p>
        </footer>
    </main>
</body>
</html>"""