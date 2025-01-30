import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

class OpenRouterClient:
    def __init__(self):
        """Initialize the OpenRouter client."""
        load_dotenv()
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        
    def generate_text(self, prompt: str) -> Optional[str]:
        """
        Generate text using OpenRouter API.
        
        Args:
            prompt (str): The prompt to send to the model
            
        Returns:
            Optional[str]: Generated text or None if generation fails
        """
        try:
            completion = self.client.chat.completions.create(
                model="anthropic/claude-3.5-sonnet",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
                temperature=0
            )
            
            if completion.choices and completion.choices[0].message.content:
                return completion.choices[0].message.content
            return None
            
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return None