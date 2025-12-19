"""
Since PaddleOCR-VL API already returns Markdown,
this is just for additional processing if needed
"""

class MarkdownConverter:
    """Process markdown from PaddleOCR-VL API"""
    
    def convert_from_json(self, json_path):
        """Load markdown from JSON"""
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return self.convert_content(content)
    
    def convert_content(self, content):
        """Extract markdown from extracted content"""
        markdown_lines = []
        
        if isinstance(content, list):
            for page in content:
                # API already provides markdown
                if 'markdown' in page:
                    markdown_lines.append(page['markdown'])
                elif 'text' in page:
                    markdown_lines.append(page['text'])
        
        return "\n\n---\n\n".join(markdown_lines)
    
    def add_metadata(self, markdown_content, title="", author="", date=""):
        """Add YAML front matter"""
        metadata = ["---"]
        if title:
            metadata.append(f"title: {title}")
        if author:
            metadata.append(f"author: {author}")
        if date:
            metadata.append(f"date: {date}")
        metadata.append("---\n")
        
        return "\n".join(metadata) + markdown_content