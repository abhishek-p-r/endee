"""Client for Google Gemini AI."""
from typing import Optional
import google.generativeai as genai
from backend.config import settings
from backend.logging_config import get_logger

logger = get_logger("gemini_client")


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: str = None):
        """Initialize the Gemini client.
        
        Args:
            api_key: The Gemini API key.
        """
        self.api_key = api_key or settings.gemini_api_key
        if not self.api_key:
            logger.warning("No Gemini API key provided")
            self.model = None
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini client initialized")
    
    def generate(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """Generate text using Gemini.
        
        Args:
            prompt: The prompt for generation.
            temperature: Temperature for generation (0-1).
            
        Returns:
            Generated text or None if generation fails.
        """
        try:
            if not self.model:
                logger.error("Gemini model not initialized")
                return None
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": 1024,
                }
            )
            
            logger.info("Successfully generated response with Gemini")
            return response.text
        except Exception as e:
            logger.error(f"Error generating with Gemini: {str(e)}")
            return None


# Global Gemini client instance
_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """Get or create the Gemini client singleton."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
