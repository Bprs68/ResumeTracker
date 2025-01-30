import streamlit as st
import os
import tempfile
from resume_generator import ResumeGenerator
import time

def wait_for_file(file_path, timeout=10):
    """Wait for file to exist and be readable"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'rb') as f:
                    f.read(1)  # Try to read 1 byte
                return True
            except:
                pass
        time.sleep(0.1)
    return False

def cleanup_temp_files(file_paths):
    """Helper function to safely clean up temporary files"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                for _ in range(3):
                    try:
                        os.unlink(file_path)
                        break
                    except:
                        time.sleep(0.1)
        except Exception as e:
            st.warning(f"Warning: Could not delete temporary file {file_path}: {str(e)}")

def main():
    st.set_page_config(page_title="Resume Generator", page_icon="📄")
    
    st.title("Resume Generator 📄")
    st.write("Paste the job description to generate an optimized resume.")
    
    # Job description input
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Enter the job description..."
    )
    
    # Paths configuration
    input_pdf_path = r"C:\Users\bhask\OneDrive\Documents\Experiments\ResumeTracker\Basicresume\Bhaskar_Kumar_CV.pdf"
    
    if job_description:
        if st.button("Generate Optimized Resume", type="primary"):
            with st.spinner("Generating your optimized resume..."):
                # Create temporary directory for our files
                temp_dir = tempfile.mkdtemp()
                timestamp = str(int(time.time()))
                tmp_md_path = os.path.join(temp_dir, f'resume_md_{timestamp}.md')
                tmp_generated_pdf_path = os.path.join(temp_dir, f'resume_pdf_{timestamp}.pdf')
                
                try:
                    # Initialize resume generator with temporary paths
                    generator = ResumeGenerator(
                        pdf_path=input_pdf_path,
                        output_md_path=tmp_md_path,
                        output_pdf_path=tmp_generated_pdf_path
                    )
                    
                    # Generate the resume
                    if not generator.create_resume(job_description):
                        raise Exception("Failed to generate resume")
                    
                    # Wait for PDF file to be ready
                    if not wait_for_file(tmp_generated_pdf_path):
                        raise TimeoutError("Timeout waiting for PDF file to be generated")
                    
                    # Read the generated PDF for download
                    with open(tmp_generated_pdf_path, "rb") as file:
                        pdf_bytes = file.read()
                    
                    if pdf_bytes:  # Make sure we actually got the PDF content
                        st.success("Resume generated successfully!")
                        st.download_button(
                            label="Download Optimized Resume",
                            data=pdf_bytes,
                            file_name="optimized_resume.pdf",
                            mime="application/pdf"
                        )
                        
                        # Display markdown preview if available
                        try:
                            with open(tmp_md_path, 'r', encoding='utf-8') as f:
                                markdown_content = f.read()
                            with st.expander("Preview Generated Resume"):
                                st.markdown(markdown_content)
                        except Exception as e:
                            st.warning("Could not load preview, but PDF is available for download.")
                    else:
                        st.error("Generated PDF appears to be empty. Please try again.")
                
                except TimeoutError as e:
                    st.error("Timeout error: Failed to generate resume. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Please try again or check your input.")
                
                finally:
                    # Clean up temporary files
                    cleanup_temp_files([tmp_md_path, tmp_generated_pdf_path])
                    try:
                        os.rmdir(temp_dir)  # Remove temp directory if empty
                    except:
                        pass

    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Paste the job description in the text area above
    2. Click "Generate Optimized Resume"
    3. Wait for the generation process to complete
    4. Download your optimized resume
    
    Note: The generator will use your base resume to create an optimized version for the specific job description.
    """)

if __name__ == "__main__":
    main()