import markdown2
import pdfkit
import os
import argparse
from typing import Optional

class MarkdownToPDFConverter:
    def __init__(self, css_path: Optional[str] = None):
        """
        Initialize the converter with optional CSS styling.
        
        Args:
            css_path (str, optional): Path to custom CSS file for styling
        """
        self.css_path = css_path
        self.options = {
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '15mm',
            'encoding': 'UTF-8',
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'dpi': '200'
        }

    def convert_file(self, input_path: str, output_path: str) -> None:
        """
        Convert a Markdown file to PDF.
        
        Args:
            input_path (str): Path to input Markdown file
            output_path (str): Path where the PDF will be saved
        
        Raises:
            FileNotFoundError: If input file doesn't exist
            RuntimeError: If conversion fails
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        try:
            # Read and convert markdown to HTML
            with open(input_path, 'r', encoding='utf-8') as md_file:
                markdown_content = md_file.read()
            
            html_content = markdown2.markdown(
                markdown_content,
                extras=['tables', 'code-friendly', 'fenced-code-blocks']
            )

            # Add CSS if provided
            if self.css_path:
                with open(self.css_path, 'r', encoding='utf-8') as css_file:
                    css_content = css_file.read()
                html_content = f"""
                <html>
                    <head>
                        <style>{css_content}</style>
                    </head>
                    <body>{html_content}</body>
                </html>
                """

            # Convert HTML to PDF
            pdfkit.from_string(html_content, output_path, options=self.options)
            print(f"Successfully converted {input_path} to {output_path}")

        except Exception as e:
            raise RuntimeError(f"Conversion failed: {str(e)}")

def main():
    # Define default paths
    default_input_path = r'C:\Users\bhask\OneDrive\Documents\Experiments\ResumeTracker\MDfile\resume.md'
    default_output_path = r'C:\Users\bhask\OneDrive\Documents\Experiments\ResumeTracker\PDFResume\Bhaskar_Kumar_CV.pdf'
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert Markdown files to PDF')
    parser.add_argument('--input', help='Input Markdown file path', default=default_input_path)
    parser.add_argument('--output', help='Output PDF file path', default=default_output_path)
    parser.add_argument('--css', help='Path to custom CSS file', default=None)
    
    args = parser.parse_args()
    
    # Create converter and process file
    converter = MarkdownToPDFConverter(css_path=args.css)
    converter.convert_file(input_path=args.input, output_path=args.output)

if __name__ == '__main__':
    main()