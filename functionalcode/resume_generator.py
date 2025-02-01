import sys

import os
# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from typing import Optional
import PyPDF2
from llmcalls.orresponse import OpenRouterClient 
from mdtopdf import MarkdownToPDFConverter

class ResumeGenerator:
    def __init__(self, pdf_path: str, output_md_path: str, output_pdf_path: str):
        """
        Initialize the resume generator.
        
        Args:
            pdf_path (str): Path to the existing resume PDF
            output_md_path (str): Path where the markdown file will be saved
            output_pdf_path (str): Path where the final PDF will be saved
        """
        self.pdf_path = pdf_path
        self.output_md_path = output_md_path
        self.output_pdf_path = output_pdf_path
        self.client = OpenRouterClient()

    def generate_prompt(self, jd: str, resume_text: str) -> str:
        """Generate the complete prompt for OpenRouter."""
        return f"""You are an expert professional resume writer. 
        Create an optimized resume based on this job description and the candidate's current resume.
        
        Job Description:
        {jd}

        Current Resume:
        {resume_text}

        Please create an ATS-optimized resume that achieves a 90%+ compatibility score by:

        1. Analyzing the job description to:
        - Extract critical keywords, skills, and requirements
        - Identify primary and secondary job responsibilities
        - Note specific technical tools, methodologies, and industry terms
        - Map required years of experience and qualifications

        2. Transforming the resume content to:
        - Mirror exact phrases and keywords from the job description
        - Convert all bullets into the format: [Action Verb] + [Achievement] + [Result/Impact] + [Metrics]
        - Incorporate relevant keywords naturally within achievement statements
        - Include both spelled-out terms and acronyms (e.g., "Artificial Intelligence (AI)")
        - Use industry-standard job titles that align with the target role

        3. Implementing ATS-friendly formatting:
        - Use clean, standard section headers
        - Avoid tables, columns, graphics, or special characters
        - Utilize simple bullet points (• or -)
        - Maintain consistent date formats (MM/YYYY)
        - Use standard fonts (Arial, Calibri, Times New Roman) and sizes (10-12 pt)

        4. Verification Process:
        - Cross-reference against job description for keyword coverage
        - Ensure every required skill/qualification is addressed
        - Verify metrics and achievements align with role priorities
        - Run through ATS simulation tool to confirm 90%+ match
        - Adjust content based on ATS feedback until target score is reached

        Note: Retain all original contact information, education details, and verifiable achievements. Focus on reorganizing and rephrasing content to maximize ATS compatibility while maintaining authenticity.
        
        Please provide the optimized resume in markdown format with clear sections and bullet points. Keep the content concise, relevant, and achievement-oriented.
        
        Only provide markdown formatted text. Do not include any other content or formatting or comments."""

    def extract_text_from_pdf(self) -> str:
        """Extract text content from the PDF file."""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    def create_resume(self, jd: str) -> bool:
        """
        Create an optimized resume based on the job description.
        
        Args:
            jd (str): The job description to optimize the resume for
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Extract text from existing resume
            resume_text = self.extract_text_from_pdf()
            
            # Generate the complete prompt
            prompt = self.generate_prompt(jd, resume_text)
            
            # Get optimized resume from OpenRouter
            markdown_content = self.client.generate_text(prompt)
            
            if not markdown_content:
                raise RuntimeError("Failed to generate resume content")
            
            # Save markdown content
            with open(self.output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Convert to PDF
            converter = MarkdownToPDFConverter()
            converter.convert_file(self.output_md_path, self.output_pdf_path)
            
            return True
            
        except Exception as e:
            print(f"Error in create_resume: {str(e)}")
            return False

def main():
    # Define paths
    pdf_path = r"C:\Users\bhask\OneDrive\Documents\Experiments\ResumeTracker\Basicresume\Bhaskar_Kumar_CV.pdf"
    output_md_path = r"C:\Users\bhask\OneDrive\Documents\Experiments\ResumeTracker\MDfile\resume.md"
    output_pdf_path = r"C:\Users\bhask\OneDrive\Documents\Experiments\ResumeTracker\PDFResume\Bhaskar_Kumar_CV.pdf"
    
    # Get job description from user
    print("Please enter the job description:")
    jd = input()
    
    # Create and run resume generator
    generator = ResumeGenerator(pdf_path, output_md_path, output_pdf_path)
    generator.create_resume(jd)

if __name__ == "__main__":
    main()