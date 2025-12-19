"""
Extract text and layout from PDF using Baidu PaddleOCR APIs
Direct API integration with provided endpoints
Uses common access token for all APIs
"""
import base64
import requests
import json
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class PaddleOCRExtractor:
    """
    Uses PaddleOCR-VL API directly from Baidu AI Studio
    Endpoint: /layout-parsing (Document parsing with Markdown + JSON)
    """
    
    def __init__(self):
        self.api_url = os.getenv("PADDLEOCR_VL_API_URL", "")
        self.token = os.getenv("BAIDU_ACCESS_TOKEN", "")
        self.available = bool(self.api_url and self.token)
        
        if not self.available:
            print("⚠ PaddleOCR-VL API not configured")
            print("Add to .env:")
            print("  BAIDU_ACCESS_TOKEN=<your_access_token>")
            print("  PADDLEOCR_VL_API_URL=<your_url>")
    
    def extract_from_pdf(self, pdf_path):
        """
        Extract text and layout from PDF using PaddleOCR-VL API
        Returns markdown and structured data
        """
        if not self.available:
            raise Exception(
                "PaddleOCR-VL API not configured. "
                "Get token from https://aistudio.baidu.com (Personal Center > Access Token)"
            )
        
        print(f"📄 Reading PDF: {pdf_path}")
        
        # Read and encode PDF
        with open(pdf_path, "rb") as file:
            file_bytes = file.read()
            file_data = base64.b64encode(file_bytes).decode("ascii")
        
        print(f"📤 Uploading to PaddleOCR-VL API...")
        
        # Prepare request with common access token
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "file": file_data,
            "fileType": 0,  # 0 for PDF, 1 for image
            "useDocOrientationClassify": True,
            "useDocUnwarping": True,
            "useChartRecognition": True,
        }
        
        try:
            print("🔄 Processing with PaddleOCR-VL...")
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=300  # 5 minute timeout
            )
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_data = response.json()
                error_msg = error_data.get("errorMsg", "Unknown error")
                raise Exception(f"API Error ({response.status_code}): {error_msg}")
            
            result = response.json()["result"]
            
            # Extract layout parsing results
            layout_results = result.get("layoutParsingResults", [])
            
            if not layout_results:
                raise Exception("No results from API")
            
            print(f"📊 API returned {len(layout_results)} page(s)")
            
            # Convert API results to our format
            extracted_content = []
            
            for page_num, page_result in enumerate(layout_results, 1):
                print(f"🔍 Processing page {page_num}...")
                
                try:
                    # Get markdown from API
                    markdown_obj = page_result.get("markdown", {})
                    markdown_text = markdown_obj.get("text", "")
                    
                    # Count lines and chars
                    lines = [l.strip() for l in markdown_text.split('\n') if l.strip()]
                    char_count = len(markdown_text)
                    
                    page_content = {
                        "page_number": page_num,
                        "text": markdown_text,
                        "lines": lines,
                        "char_count": char_count,
                        "line_count": len(lines),
                        "markdown": markdown_text,
                    }
                    
                    # Check for images in markdown
                    images = markdown_obj.get("images", {})
                    if images:
                        print(f"   Found {len(images)} images in markdown")
                        page_content["markdown_images"] = len(images)
                    
                    extracted_content.append(page_content)
                    print(f"✓ Page {page_num}: {len(lines)} lines, {char_count} chars")
                
                except Exception as e:
                    print(f"⚠ Error processing page {page_num}: {e}")
                    extracted_content.append({
                        "page_number": page_num,
                        "text": "",
                        "lines": [],
                        "char_count": 0,
                        "line_count": 0,
                        "error": str(e)
                    })
            
            return extracted_content
        
        except requests.exceptions.Timeout:
            raise Exception("API request timeout. Try again or use a smaller PDF.")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error. Check your internet connection.")
        except Exception as e:
            raise Exception(f"API extraction failed: {str(e)}")
    
    def save_extracted_content(self, content, output_path):
        """Save extracted content as JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"✓ Saved to {output_path}")
        except Exception as e:
            print(f"✗ Failed to save: {e}")


class PPOCRv5Extractor:
    """
    Uses PP-OCRv5 API directly from Baidu AI Studio
    Endpoint: /ocr (Text recognition only)
    Optional fallback if PaddleOCR-VL fails
    """
    
    def __init__(self):
        self.api_url = os.getenv("PPOCR_V5_API_URL", "")
        self.token = os.getenv("BAIDU_ACCESS_TOKEN", "")
        self.available = bool(self.api_url and self.token)
    
    def extract_from_pdf(self, pdf_path):
        """
        Extract text from PDF using PP-OCRv5 API
        Returns OCR results (fallback option)
        """
        if not self.available:
            return None
        
        print(f"📄 Reading PDF with PP-OCRv5...")
        
        # Read and encode PDF
        with open(pdf_path, "rb") as file:
            file_bytes = file.read()
            file_data = base64.b64encode(file_bytes).decode("ascii")
        
        # Prepare request with common access token
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "file": file_data,
            "fileType": 0,  # 0 for PDF
            "useDocOrientationClassify": False,
            "useDocUnwarping": False,
            "useTextlineOrientation": False,
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=300
            )
            
            if response.status_code != 200:
                return None
            
            result = response.json()["result"]
            return result.get("ocrResults", [])
        
        except:
            return None