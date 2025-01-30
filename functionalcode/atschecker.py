import streamlit as st
import PyPDF2
import os
from llmcalls.geminiresponse import setup_gemini, generate_text

class ATSChecker:
    def __init__(self):
        setup_gemini()

    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    def generate_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """Generate prompt for ATS analysis"""
        return f"""As an ATS (Applicant Tracking System) expert, analyze the compatibility between this resume and job description.

Job Description:
{job_description}

Resume:
{resume_text}

Please provide a detailed analysis in the following format:

1. Compatibility Score (0-100):
- Calculate a score based on keyword matching, skills alignment, and overall relevance
- Explain the score breakdown

2. Key Findings:
- List the most important matching keywords found
- Identify critical job requirements that are present in the resume
- Point out any missing key requirements

3. Skills Analysis:
- Required skills present in resume
- Required skills missing from resume
- Additional relevant skills found

4. Optimization Suggestions:
- Specific recommendations for improving ATS compatibility
- Keywords to add or emphasize
- Format improvements if needed

Please provide the analysis in markdown format with clear sections and bullet points.
Keep explanations concise but informative.
"""

    def analyze_resume(self, resume_text: str, job_description: str) -> str:
        """Analyze resume against job description"""
        try:
            prompt = self.generate_analysis_prompt(resume_text, job_description)
            analysis = generate_text(prompt)
            return analysis
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {str(e)}")

def main():
    st.set_page_config(page_title="ATS Resume Checker", page_icon="📝")
    
    st.title("ATS Resume Compatibility Checker 📝")
    st.write("Upload your resume and paste the job description to check ATS compatibility")
    
    # Initialize ATS Checker
    checker = ATSChecker()
    
    # File uploader for resume
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=['pdf'])
    
    # Job description input
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Enter the job description..."
    )
    
    if uploaded_file is not None and job_description:
        if st.button("Check ATS Compatibility", type="primary"):
            with st.spinner("Analyzing your resume..."):
                try:
                    # Extract text from resume
                    resume_text = checker.extract_text_from_pdf(uploaded_file)
                    
                    # Get analysis
                    analysis = checker.analyze_resume(resume_text, job_description)
                    
                    # Display results
                    st.success("Analysis complete!")
                    st.markdown(analysis)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Upload your resume in PDF format
    2. Paste the complete job description
    3. Click "Check ATS Compatibility"
    4. Review the analysis and recommendations
    
    ### Tips:
    - Use a clean, properly formatted PDF resume
    - Include the complete job description for best results
    - Pay attention to the missing keywords and skills
    - Follow the optimization suggestions to improve your score
    """)

if __name__ == "__main__":
    main()