import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


# """Initialize the Gemini API with your API key."""

api_key = os.environ.get("GEMINI_API_KEY") or "YOUR_ACTUAL_API_KEY"
genai.configure(api_key=api_key)
    
def generate_text(prompt):
    """Generates text using the Gemini API."""
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generate the response
        response = model.generate_content(prompt)
        
        # Check if the response was successful
        if response.text:
            return response.text
        else:
            print(f"No text generated. Response: {response}")
            return None
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":

    
    # Get user input and generate response
    user_prompt = input("Enter your prompt: ")
    generated_response = generate_text(user_prompt)
    
    if generated_response:
        print("\nGenerated Response:\n", generated_response)
    else:
        print("Failed to generate a response.")